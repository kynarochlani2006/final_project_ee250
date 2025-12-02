import yfinance as yf
import numpy as np
import socket
import json
import time
from collections import deque

SERVER_IP = "YOUR_CLOUD_SERVER_IP"
SERVER_PORT = 5001
STOCK = "TSLA"
WINDOW = 20
SPIKE_THRESHOLD = 2.0

prices = deque(maxlen=WINDOW)

def get_price():
    try:
        ticker = yf.Ticker(STOCK)
        return float(ticker.fast_info['last_price'])
    except:
        return None

def compute_volatility():
    if len(prices) < 2:
        return 0.0
    return float(np.std(list(prices)))

def run_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    print("Connected to cloud server.")

    while True:
        price = get_price()
        if price is None:
            time.sleep(1)
            continue

        prices.append(price)

        vol = compute_volatility()
        spike = vol > SPIKE_THRESHOLD

        payload = {
            "stock": STOCK,
            "price": price,
            "volatility": vol,
            "spike": spike,
            "timestamp": time.time(),
        }

        sock.send((json.dumps(payload) + "\n").encode())
        print("Sent:", payload)
        time.sleep(1)

run_client()
