from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests
from datetime import datetime, timedelta
import pandas as pd
import sqlite3
import json
from bs4 import BeautifulSoup
import time
import re
import os

app = Flask(__name__)

# Database setup
Base = declarative_base()

def get_db_engine():
    # 確保數據庫目錄存在
    db_path = 'btc_wallets.db'
    
    # 創建數據庫引擎
    engine = create_engine(f'sqlite:///{db_path}', 
                         connect_args={'check_same_thread': False, 'timeout': 30})
    return engine

engine = get_db_engine()
Session = sessionmaker(bind=engine)

class WalletStats(Base):
    __tablename__ = 'wallet_stats'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    group_0001_to_1 = Column(Float)
    group_1_to_10 = Column(Float)
    group_10_to_100 = Column(Float)
    group_100_plus = Column(Float)

# 創建數據庫表
try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Error creating database: {e}")

def fetch_btc_data():
    url = "https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        time.sleep(2)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        stats = {
            'group_0001_to_1': 0.0,
            'group_1_to_10': 0.0,
            'group_10_to_100': 0.0,
            'group_100_plus': 0.0
        }
        
        tables = soup.find_all('table')
        for table in tables:
            if 'Bitcoin distribution' in table.get_text():
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        range_text = cols[0].text.strip()
                        btc_text = cols[3].text.strip()
                        
                        try:
                            btc_amount = float(btc_text.split(' BTC')[0].replace(',', '').strip())
                            
                            if '[0.001 - 0.01)' in range_text:
                                stats['group_0001_to_1'] += btc_amount
                            elif '[0.01 - 0.1)' in range_text:
                                stats['group_0001_to_1'] += btc_amount
                            elif '[0.1 - 1)' in range_text:
                                stats['group_0001_to_1'] += btc_amount
                            elif '[1 - 10)' in range_text:
                                stats['group_1_to_10'] += btc_amount
                            elif '[10 - 100)' in range_text:
                                stats['group_10_to_100'] += btc_amount
                            elif '[100 - 1,000)' in range_text:
                                stats['group_100_plus'] += btc_amount
                            elif '[1,000 - 10,000)' in range_text:
                                stats['group_100_plus'] += btc_amount
                            elif '[10,000 - 100,000)' in range_text:
                                stats['group_100_plus'] += btc_amount
                            elif '[100,000 - 1,000,000)' in range_text:
                                stats['group_100_plus'] += btc_amount
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing BTC amount from {btc_text}: {e}")
                            continue
        
        session = Session()
        try:
            new_stat = WalletStats(
                date=datetime.now().date(),
                group_0001_to_1=stats['group_0001_to_1'],
                group_1_to_10=stats['group_1_to_10'],
                group_10_to_100=stats['group_10_to_100'],
                group_100_plus=stats['group_100_plus']
            )
            session.add(new_stat)
            session.commit()
            print(f"Successfully fetched and stored data: {stats}")
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    session = Session()
    try:
        stats = session.query(WalletStats).order_by(WalletStats.date).all()
        result = []
        
        for i, stat in enumerate(stats):
            data = {
                'date': stat.date.strftime('%Y-%m-%d'),
                'amounts': {
                    'group_0001_to_1': float(stat.group_0001_to_1),
                    'group_1_to_10': float(stat.group_1_to_10),
                    'group_10_to_100': float(stat.group_10_to_100),
                    'group_100_plus': float(stat.group_100_plus)
                },
                'changes': {
                    'group_0001_to_1': 0.0,
                    'group_1_to_10': 0.0,
                    'group_10_to_100': 0.0,
                    'group_100_plus': 0.0
                }
            }
            
            if i > 0:
                prev_stat = stats[i-1]
                data['changes'] = {
                    'group_0001_to_1': float(stat.group_0001_to_1 - prev_stat.group_0001_to_1),
                    'group_1_to_10': float(stat.group_1_to_10 - prev_stat.group_1_to_10),
                    'group_10_to_100': float(stat.group_10_to_100 - prev_stat.group_10_to_100),
                    'group_100_plus': float(stat.group_100_plus - prev_stat.group_100_plus)
                }
            
            result.append(data)
            
        return jsonify(result)
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True) 