# 🚀 雙核心 AI 戰情室：全自動加密貨幣市場監控系統
**Automated Crypto Market Monitor & AI Commentary System**

## 💡 專案簡介 (Project Overview)
本專案為一個端到端 (End-to-End) 的全自動化商業情報管線。透過串接多個外部 API，系統能自動獲取主流加密貨幣市場即時報價，進行時間序列的均線分析，並將繁雜的數據轉化為高階視覺化圖表與 AI 驅動的市場點評，最終推播至企業通訊軟體，實現 24/7 的無人化數據監控。

## 🛠️ 技術棧 (Tech Stack)
* **資料工程 (ETL):** `Python`, `requests`, `Pandas` (Data Cleaning, Concat, Time Series)
* **數據分析與視覺化:** `Matplotlib`, `Seaborn` (Moving Average, Subplots)
* **AI 賦能 (GenAI):** `Google Gemini API` (Data-driven Prompt Engineering)
* **雲端部署與自動化:** `GitHub Actions` (CI/CD, Serverless Cron Jobs)
* **警報推播:** `Discord Webhook` (JSON Payload, Binary Image Upload)

## ⚙️ 核心系統架構 (Architecture)
1. **Extract:** 透過 CoinGecko API 獲取 BTC 與 ETH 過去 7 日的歷史連續報價。
2. **Transform:** 使用 Pandas 進行 Unix 時間戳轉換，並計算 24 小時移動平均線 (MA24) 進行降噪。
3. **Visualize:** 利用 Seaborn 雙子圖引擎，渲染出具備高度商業可讀性的對比趨勢圖。
4. **AI Insight:** 將即時現價與均線落點作為參數注入 Prompt，調用 Gemini 模型生成高管級市場點評。
5. **Load & Alert:** 透過 HTTP POST 夾帶二進位圖片檔與 JSON 報告，精準投遞至 Discord 戰情室。

## 🛡️ 系統強健度設計 (Robustness)
* **資安合規:** 嚴格遵守資安規範，將所有 Webhook URL 與 API Keys 抽離程式碼，統一由 GitHub Secrets 以環境變數 (Environment Variables) 注入。
* **容錯機制:** 實作 HTTP Status Code 檢測與 `try-except` 防呆機制。即使 AI 服務端點異常 (如 404/500 錯誤)，核心的圖表渲染與推播產線依然能獨立運作並回報錯誤，確保監控不中斷。

---
*Powered by Python & Gemini AI | Developed with 💻*# crypto-bot
