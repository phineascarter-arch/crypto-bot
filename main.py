import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
if not WEBHOOK_URL:
    print("❌ 致命錯誤：找不到 Webhook 網址！")
    exit(1)

coins = ['bitcoin', 'ethereum']
df_list = [] 

print("📡 啟動多執行緒 API 產線...")
for coin in coins:
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=7"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    
    if res.status_code == 200:
        data = res.json()
        temp_df = pd.DataFrame(data['prices'], columns=['Time', 'Price_USD'])
        temp_df['Time'] = pd.to_datetime(temp_df['Time'], unit='ms')
        
        temp_df['Coin_Name'] = coin.upper()
        # 🧠 這裡就是計算 MA24 的引擎！
        temp_df['MA24_Price'] = temp_df['Price_USD'].rolling(window=24).mean()
        
        df_list.append(temp_df)

df = pd.concat(df_list)

print("🎨 啟動 Seaborn 雙子圖渲染引擎...")
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
sns.set_theme(style="darkgrid")

# --- 樓上：比特幣 ---
btc_df = df[df['Coin_Name'] == 'BITCOIN']
sns.lineplot(ax=axes[0], data=btc_df, x='Time', y='Price_USD', color='orange', alpha=0.5, label='Actual Price')
sns.lineplot(ax=axes[0], data=btc_df, x='Time', y='MA24_Price', color='red', linewidth=2, label='MA24 (Trend)')
axes[0].set_title('BITCOIN (BTC) 7-Day Trend', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Price (USD)')
axes[0].legend(loc='upper left') # 🎯 關鍵修復：把比特幣的圖例顯示在左上角

# --- 樓下：以太幣 ---
eth_df = df[df['Coin_Name'] == 'ETHEREUM']
sns.lineplot(ax=axes[1], data=eth_df, x='Time', y='Price_USD', color='blue', alpha=0.5, label='Actual Price')
sns.lineplot(ax=axes[1], data=eth_df, x='Time', y='MA24_Price', color='purple', linewidth=2, label='MA24 (Trend)')
axes[1].set_title('ETHEREUM (ETH) 7-Day Trend', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Price (USD)')
axes[1].set_xlabel('Date & Time')
axes[1].legend(loc='upper left') # 🎯 關鍵修復：把以太幣的圖例也顯示出來

plt.xticks(rotation=45)
plt.tight_layout()

image_filename = "crypto_duel.png"
plt.savefig(image_filename)
plt.close()

print("🚀 呼叫 Discord 物流車...")
payload = {
    "content": "🚨 **雙雄戰情匯報 (含 MA24 趨勢分析)** 🚨\n老闆早安！圖表已加上明確的圖例標示，紅線與紫線即為24小時均線！"
}

with open(image_filename, "rb") as img_file:
    requests.post(WEBHOOK_URL, data=payload, files={"file": (image_filename, img_file, "image/png")})
