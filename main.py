import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
if not WEBHOOK_URL:
    print("❌ 致命錯誤：找不到 Webhook 網址！請檢查 GitHub Secrets。")
    exit(1)

print("📡 步驟一：啟動 API 抓取 7 日歷史報價...")
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data['prices'], columns=['Time', 'Price_USD'])
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')

    # 🧠 戰略二核心：Pandas 滾動運算 (Moving Average)
    print("🧠 步驟二：啟動高階分析，計算 24 小時移動平均線 (MA24)...")
    # 因為數據是每小時一筆，滾動 24 筆就等於「過去 24 小時的平均成本」
    df['MA24_Price'] = df['Price_USD'].rolling(window=24).mean()

    print("🎨 步驟三：Seaborn 雙軌繪圖產線...")
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="darkgrid")
    
    # 畫第一條線：真實價格 (波動大，橘色，稍微透明一點)
    sns.lineplot(data=df, x='Time', y='Price_USD', color='orange', alpha=0.5, linewidth=1.5, label='Actual Price')
    
    # 畫第二條線：24小時移動平均線 (平滑趨勢，紅色，粗實線)
    sns.lineplot(data=df, x='Time', y='MA24_Price', color='red', linewidth=2.5, label='24H Moving Average (MA24)')

    plt.title('Bitcoin 7-Day Trend with MA24 Analysis', fontsize=16, fontweight='bold')
    plt.xlabel('Date & Time', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.xticks(rotation=45)
    
    # 加上圖例，老闆才看得懂哪條線是什麼 (loc='upper left' 代表放在左上角)
    plt.legend(loc='upper left') 
    plt.tight_layout()

    image_filename = "btc_ma_trend.png"
    plt.savefig(image_filename)
    plt.close() 

    print("🚀 步驟四：呼叫 Discord 物流車...")
    payload = {
        "content": "🚨 **雲端高階戰情匯報** 🚨\n老闆早安！\n系統已自動為您加入 **24小時移動平均線(MA24)**。\n當橘線(現價)跌破紅線(均線)時，請留意短期的下行風險！"
    }

    with open(image_filename, "rb") as img_file:
        files = {"file": (image_filename, img_file, "image/png")}
        discord_res = requests.post(WEBHOOK_URL, data=payload, files=files)

    if discord_res.status_code in [200, 204]:
        print("✅ 雲端分析任務圓滿達成！")
    else:
        print(f"⚠️ Discord 發送失敗，狀態碼：{discord_res.status_code}")
else:
    print(f"❌ 產線中斷！狀態碼：{response.status_code}")
