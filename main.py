import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("🔐 步驟零：系統啟動，正在從 GitHub 保險箱讀取機密金鑰...")
# 這裡不會寫出真實網址，而是去 GitHub Secrets 尋找名為 DISCORD_WEBHOOK 的密碼
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

# 防呆機制：如果保險箱沒鎖好或名字打錯，程式直接停止，避免後續報錯
if not WEBHOOK_URL:
    print("❌ 致命錯誤：找不到 Webhook 網址！請檢查 GitHub Secrets 是否正確設定了 'DISCORD_WEBHOOK'。")
    exit(1)

print("📡 步驟一：啟動 API 抓取 7 日歷史報價...")
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)

# 🛡️ 安全氣囊：確認 CoinGecko 有沒有給我們正確的資料
if response.status_code == 200:
    data = response.json()
    
    # 🧹 步驟二：Pandas 數據清洗與轉換
    df = pd.DataFrame(data['prices'], columns=['Time', 'Price_USD'])
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')

    print("🎨 步驟三：Seaborn 繪製高階商業趨勢圖...")
    plt.figure(figsize=(10, 5))
    sns.set_theme(style="darkgrid")
    sns.lineplot(data=df, x='Time', y='Price_USD', color='orange', linewidth=2)
    
    # 圖表裝飾與國際化 (使用英文避免 Linux 雲端主機出現亂碼)
    plt.title('Bitcoin 7-Day Trend (Cloud Automated Report)', fontsize=16, fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 💾 將畫布存成實體圖片檔，然後關閉畫布釋放記憶體
    image_filename = "btc_trend.png"
    plt.savefig(image_filename)
    plt.close() 

    print("🚀 步驟四：呼叫 Discord 專線物流車，準備投遞報告...")
    
    # 包裝文字訊息
    payload = {
        "content": "🚨 **雲端戰情匯報** 🚨\n老闆早安！這是雲端無人機自動為您生成的市場趨勢圖，請查收！"
    }

    # 以二進位模式 ('rb') 打開剛剛畫好的圖片，準備上傳
    with open(image_filename, "rb") as img_file:
        files = {"file": (image_filename, img_file, "image/png")}
        
        # 發射！使用保險箱裡拿出來的 WEBHOOK_URL 發送請求
        discord_res = requests.post(WEBHOOK_URL, data=payload, files=files)

    # 確認 Discord 是否成功接收
    if discord_res.status_code in [200, 204]:
        print("✅ 雲端任務圓滿達成！請檢查您的 Discord 戰情室！")
    else:
        print(f"⚠️ Discord 發送失敗，狀態碼：{discord_res.status_code} | 錯誤訊息：{discord_res.text}")

else:
    print(f"❌ 產線中斷！CoinGecko 拒絕提供資料。狀態碼：{response.status_code}")
    print("💡 高管提示：可能是 API 呼叫頻率過高 (429)，雲端機器人將在下次排程重試。")
