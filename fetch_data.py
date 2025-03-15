from app import fetch_btc_data

def job():
    print("Fetching BTC wallet data...")
    try:
        success = fetch_btc_data()
        if success:
            print("Data fetched and saved successfully")
        else:
            print("Failed to fetch data")
    except Exception as e:
        print(f"Error during data fetch: {e}")

# 立即執行一次
try:
    job()
except Exception as e:
    print(f"Error in initial job execution: {e}")





