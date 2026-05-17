import yfinance as yf
import pandas as pd
import requests
from ta.momentum import RSIIndicator

#Discord Webhook URL
WEBHOOK_URL = "ここにWebhook URL"

#監視銘柄
stocks = [
    "IONQ",
    "RGTI",
    "NVDA",
    "7011.T",   # 三菱重工
    "9984.T"    # ソフトバンクG
]

def send_discord(message):
    payload = {
        "content": message
    }

    requests.post(WEBHOOK_URL, json=payload)

for stock in stocks:
    try:
        # 3ヶ月分取得
        df = yf.download(stock, period="3mo", progress=False)

        if len(df) < 30:
            continue

        # RSI計算
        rsi = RSIIndicator(close=df["Close"]).rsi()

        latest_rsi = float(rsi.iloc[-1])

        # 出来高平均
        avg_volume = df["Volume"].tail(20).mean()
        latest_volume = df["Volume"].iloc[-1]

        volume_ratio = latest_volume / avg_volume

        # 移動平均線
        ma5 = df["Close"].tail(5).mean()
        ma25 = df["Close"].tail(25).mean()

        # 条件
        if (
            volume_ratio >= 2
            and ma5 > ma25
            and 40 <= latest_rsi <= 70
        ):

            message = f"""
📈 買い候補

銘柄: {stock}

RSI: {latest_rsi:.1f}
出来高倍率: {volume_ratio:.2f}
5日線 > 25日線
"""

            send_discord(message)

            print(f"{stock} 通知送信")

    except Exception as e:
        print(f"{stock} エラー: {e}")
