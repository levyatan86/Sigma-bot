# Enhanced Basic Python Chart Scanner (without ccxt)
# Simulates BTC/USDT data for breakout and volume spike detection

import time
import pandas as pd
import random
from datetime import datetime, timedelta

# Simulate OHLCV data
def generate_mock_ohlcv(symbol='BTC/USDT', timeframe='1m', limit=100):
    now = datetime.utcnow()
    data = []
    base_price = 30000
    for i in range(limit):
        timestamp = now - timedelta(minutes=(limit - i))
        open_ = base_price + random.uniform(-20, 20)
        high = open_ + random.uniform(0, 10)
        low = open_ - random.uniform(0, 10)
        close = random.uniform(low, high)
        volume = random.uniform(10, 1000)
        data.append([timestamp, open_, high, low, close, volume])
        base_price = close  # follow last close to keep structure more realistic
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

# Detect breakout: current close > previous high
def detect_breakout(df):
    recent = df.iloc[-1]
    prev = df.iloc[-2]
    breakout = recent['close'] > prev['high']
    print(f"🔎 Checking breakout: Close={recent['close']:.2f}, Prev High={prev['high']:.2f} → {'Yes' if breakout else 'No'}")
    return breakout

# Detect volume spike: current volume > 2x average of last N-1
def detect_volume_spike(df):
    recent_vol = df.iloc[-1]['volume']
    avg_vol = df.iloc[:-1]['volume'].mean()
    spike = recent_vol > 2 * avg_vol
    print(f"🔎 Checking volume spike: Volume={recent_vol:.2f}, Avg={avg_vol:.2f} → {'Yes' if spike else 'No'}")
    return spike

# Main loop
def run_scanner():
    print("🔍 Starting Enhanced Chart Scanner with Mock Data...\n")
    while True:
        df = generate_mock_ohlcv()
        if detect_breakout(df):
            print("🚨 Breakout detected on BTC/USDT!")
        if detect_volume_spike(df):
            print("📈 Volume spike detected on BTC/USDT!")
        print("—" * 40)
        time.sleep(5)

if __name__ == '__main__':
    run_scanner()
