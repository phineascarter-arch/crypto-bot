import os
import requests

# 🔐 從保險箱拿同一把 Discord 鑰匙
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

if not WEBHOOK_URL:
    print("❌ 找不到 Webhook 網址！")
    exit(1)

print("📡 啟動輕量級 API：獲取 BTC 與 ETH 即時報價...")
# 這次我們用 CoinGecko 的 simple/price 端點，速度極快，專門用來抓當下價格
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

try:
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        btc_price = data['bitcoin']['usd']
        eth_price = data['ethereum']['usd']
        
        print(f"✅ 抓取成功：BTC ${btc_price}, ETH ${eth_price}")
        
        # 📦 包裝輕量級文字包裹
        payload = {
            "content": f"⏱️ **整點市場快報** ⏱️\n\n🔸 **比特幣 (BTC):** `${btc_price:,.0f} USD`\n🔹 **以太幣 (ETH):** `${eth_price:,.0f} USD`\n\n*(此為系統每小時自動推播)*"
        }
        
        # 🚀 發射至 Discord
        requests.post(WEBHOOK_URL, json=payload)
        print("✅ 整點快報投遞成功！")
        
    else:
        print(f"⚠️ API 異常，狀態碼：{response.status_code}")
        
except Exception as e:
    print(f"❌ 執行發生錯誤：{e}")
