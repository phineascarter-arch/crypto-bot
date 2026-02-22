import os
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import google.generativeai as genai  # 召喚 AI 模組

# 🔐 讀取兩把金鑰
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not WEBHOOK_URL or not GEMINI_API_KEY:
    print("❌ 致命錯誤：找不到 Webhook 或 Gemini API Key！請檢查 Secrets。")
    exit(1)

# 🧠 初始化 AI 大腦
genai.configure(api_key=GEMINI_API_KEY)
# 使用最新的輕量級模型，速度快且免費額度高
model = genai.GenerativeModel('gemini-1.5-flash')

coins = ['bitcoin', 'ethereum']
df_list = [] 
latest_data = {} # 用來收集要餵給 AI 的最新情報

print("📡 啟動多執行緒 API 產線...")
for coin in coins:
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=7"
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    
    if res.status_code == 200:
        data = res.json()
        temp_df = pd.DataFrame(data['prices'], columns=['Time', 'Price_USD'])
        temp_df['Time'] = pd.to_datetime(temp_df['Time'], unit='ms')
        temp_df['Coin_Name'] = coin.upper()
        temp_df['MA24_Price'] = temp_df['Price_USD'].rolling(window=24).mean()
        df_list.append(temp_df)
        
        # 🎯 抓取最後一筆 (最新) 的價格與均線，存入情報庫
        latest_price = temp_df['Price_USD'].iloc[-1]
        latest_ma24 = temp_df['MA24_Price'].iloc[-1]
        latest_data[coin.upper()] = {"price": latest_price, "ma24": latest_ma24}

df = pd.concat(df_list)

print("🎨 啟動 Seaborn 雙子圖渲染引擎...")
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
sns.set_theme(style="darkgrid")

btc_df = df[df['Coin_Name'] == 'BITCOIN']
sns.lineplot(ax=axes[0], data=btc_df, x='Time', y='Price_USD', color='orange', alpha=0.5, label='Actual Price')
sns.lineplot(ax=axes[0], data=btc_df, x='Time', y='MA24_Price', color='red', linewidth=2, label='MA24')
axes[0].set_title('BITCOIN (BTC) 7-Day Trend', fontsize=14, fontweight='bold')
axes[0].legend(loc='upper left')

eth_df = df[df['Coin_Name'] == 'ETHEREUM']
sns.lineplot(ax=axes[1], data=eth_df, x='Time', y='Price_USD', color='blue', alpha=0.5, label='Actual Price')
sns.lineplot(ax=axes[1], data=eth_df, x='Time', y='MA24_Price', color='purple', linewidth=2, label='MA24')
axes[1].set_title('ETHEREUM (ETH) 7-Day Trend', fontsize=14, fontweight='bold')
axes[1].legend(loc='upper left')

plt.xticks(rotation=45)
plt.tight_layout()
image_filename = "crypto_ai_duel.png"
plt.savefig(image_filename)
plt.close()

print("🤖 啟動 Gemini AI 分析師，正在撰寫戰情報告...")
# 高管的 Prompt Engineering (提示詞工程)：把數據塞進咒語裡
prompt = f"""
你是一位華爾街資深的加密貨幣交易員，說話精準、一針見血，不說廢話。
請根據以下我用程式算出來的最新數據，寫一段 100 字以內的「高管戰情點評」。
重點分析現價與 MA24 均線的關係，判斷短期是偏多還是偏空。

【即時市場數據】
比特幣 (BTC): 目前現價 ${latest_data['BITCOIN']['price']:,.0f}, 24小時均線 ${latest_data['BITCOIN']['ma24']:,.0f}
以太幣 (ETH): 目前現價 ${latest_data['ETHEREUM']['price']:,.0f}, 24小時均線 ${latest_data['ETHEREUM']['ma24']:,.0f}
"""

# 呼叫 AI 產生內容
try:
    ai_response = model.generate_content(prompt)
    ai_commentary = ai_response.text
except Exception as e:
    ai_commentary = f"⚠️ AI 系統忙線中，無法生成報告。錯誤訊息: {e}"

print("🚀 呼叫 Discord 物流車，夾帶 AI 報告與圖表發射...")
payload = {
    "content": f"🚨 **雙雄戰情匯報 (Powered by Gemini AI)** 🚨\n\n{ai_commentary}"
}

with open(image_filename, "rb") as img_file:
    requests.post(WEBHOOK_URL, data=payload, files={"file": (image_filename, img_file, "image/png")})
    print("✅ 全自動 AI 戰情室部署完畢！")
