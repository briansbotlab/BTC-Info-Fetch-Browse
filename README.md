# BTC 錢包分佈追蹤系統

這個專案是一個自動化系統，用於追蹤和分析比特幣（BTC）錢包的資金分佈情況。通過定期從 BitInfoCharts 網站抓取數據，系統可以幫助使用者了解不同規模的 BTC 持有者分佈變化。

## 功能特點

### 數據收集
- 自動從 BitInfoCharts 抓取 BTC 錢包分佈數據
- 按照以下範圍對錢包進行分組：
  - 0.001-1 BTC
  - 1-10 BTC
  - 10-100 BTC
  - 100+ BTC
- 每天自動更新數據

### 數據展示
- 直觀的網頁界面
- 互動式圖表顯示歷史趨勢
- 詳細的數據表格，包含：
  - 每個分組的當前 BTC 總量
  - 與前一天相比的變化量
  - 正負變化的顏色標示（綠色表示增加，紅色表示減少）

## 技術棧

- **後端**：
  - Python 3.x
  - Flask (Web 框架)
  - SQLAlchemy (ORM)
  - SQLite (數據庫)
  - BeautifulSoup4 (網頁解析)

- **前端**：
  - HTML5
  - Bootstrap 5
  - Chart.js (圖表展示)

## 安裝步驟

1. 克隆專案：
```bash
git clone [repository-url]
cd [project-directory]
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 運行應用：

啟動 Web 服務器：
```bash
python app.py
```

在另一個終端中啟動數據抓取服務：
```bash
python fetch_data.py
```

4. 訪問網頁界面：
打開瀏覽器訪問 http://localhost:5000

## 數據更新機制

- 系統會在每天午夜 12 點自動抓取新數據
- 每次抓取的數據都會保存到本地數據庫
- 可以通過運行 `fetch_data.py` 手動觸發數據更新

## 數據分析價值

這個系統可以幫助使用者：
- 追蹤大額持有者（鯨魚）的持倉變化
- 觀察小額持有者的累積趨勢
- 分析市場資金流向
- 評估財富分配的變化

## 注意事項

- 數據來源於 BitInfoCharts，可能存在延遲
- 系統需要穩定的網絡連接
- 建議定期備份數據庫文件
- 請遵守數據源的使用條款和規定

## 貢獻指南

歡迎提交 Pull Requests 來改進這個專案。以下是一些可能的改進方向：
- 添加更多的數據源
- 優化數據抓取效率
- 增加更多的分析功能
- 改進用戶界面

## 授權協議

本專案採用 MIT 授權協議。詳見 [LICENSE](LICENSE) 文件。 