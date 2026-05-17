import yfinance as yf
import pandas as pd
import requests
from ta.momentum import RSIIndicator

WEBHOOK_URL = "https://discord.com/api/webhooks/1505542989559369838/p3aooJAVUYy-ZqZ7UDf8T-2grl4UveEGFdc6wFNCTzzUo_DolUDJnAhPhPAaRtgdZRYl"

stocks = [
    "IONQ",
    "RGTI",
    "NVDA",
    "7011.T",
    "9984.T"
]

def send_discord(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print(f"Discord送信エラー: {e}")

candidates = []

for stock in stocks:
    try:
        df = yf.download(stock, period="3mo", auto_adjust=True, progress=False)

        if df is None or len(df) < 30:
            continue

        close = df["Close"].astype(float).squeeze()
        volume = df["Volume"].astype(float).squeeze()

        rsi = RSIIndicator(close=close).rsi()
        latest_rsi = float(rsi.iloc[-1])

        avg_volume = volume.tail(20).mean()
        latest_volume = volume.iloc[-1]
        volume_ratio = latest_volume / avg_volume if avg_volume != 0 else 0

        ma5 = close.tail(5).mean()
        ma25 = close.tail(25).mean()

        if (
            volume_ratio >= 2
            and ma5 > ma25
            and 40 <= latest_rsi <= 70
        ):
            candidates.append(
                f"{stock} | RSI:{latest_rsi:.1f} | Vol:{volume_ratio:.2f}"
            )

    except Exception as e:
        print(f"{stock} エラー: {e}")

# ★ここが重要：必ず送信
if len(candidates) > 0:
    message = "📈 買い候補\n\n" + "\n".join(candidates)
else:
    message = "📉 条件一致なし"

send_discord(message)

print("送信完了")
