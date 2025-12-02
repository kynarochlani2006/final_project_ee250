import yfinance as yf
import numpy as np
import time
import requests
from collections import deque

# --------------------------
# CONFIG
# --------------------------
RENDER_URL = "https://final-project-ee250.onrender.com/ingest"
STOCK = "TSLA"
WINDOW = 20
SPIKE_THRESHOLD = 2.0

prices = deque(maxlen=WINDOW)

# --------------------------
def get_price():
    try:
        ticker = yf.Ticker(STOCK)
        return float(ticker.fast_info['last_price'])
    except Exception as e:
        print("Error fetching price:", e)
        return None

# --------------------------
def compute_volatility():
    if len(prices) < 2:
        return 0.0
    arr = np.array(prices)
    return float(np.std(arr))

# --------------------------
def run():
    print("Sending data to Render:", RENDER_URL)

    while True:
        price = get_price()
        if price is None:
            time.sleep(1)
            continue

        prices.append(price)
        volatility = compute_volatility()
        spike = volatility > SPIKE_THRESHOLD

        payload = {
            "stock": STOCK,
            "price": price,
            "volatility": volatility,
            "spike": spike,
            "timestamp": time.time()
        }

        try:
            r = requests.post(RENDER_URL, json=payload, timeout=5)
            print("Sent:", payload, "Status:", r.status_code)
        except Exception as e:
            print("Error posting:", e)

        time.sleep(1)

run()
