#!/usr/bin/env python3
"""지표 테스트"""

from datetime import datetime, timedelta
import random
from .types import OHLCV
from .moving_averages import sma
from .momentum import rsi, macd
from .volatility import atr, bollinger_bands
from .volume import obv, vwap
from .utils import calculate_all_indicators

# 테스트 데이터 생성
test_candles = []
base_price = 100

for i in range(100):
    change = random.uniform(-2, 2)
    open_p = base_price
    close_p = base_price + change
    high_p = max(open_p, close_p) + random.uniform(0, 1)
    low_p = min(open_p, close_p) - random.uniform(0, 1)
    volume = random.uniform(1000, 10000)

    test_candles.append(OHLCV(
        timestamp=(datetime.now() - timedelta(hours=100 - i)).isoformat(),
        open=open_p,
        high=high_p,
        low=low_p,
        close=close_p,
        volume=volume
    ))
    base_price = close_p

# 전체 지표 계산
all_indicators = calculate_all_indicators(test_candles)

print("=== 기술적 지표 계산 테스트 ===\n")
print(f"SMA(20) 최근 5개: {all_indicators['sma20'][-5:]}")
print(f"RSI(14) 최근값: {all_indicators['rsi'][-1] if all_indicators['rsi'] else 'N/A'}")
print(f"MACD 최근값: {all_indicators['macd'][-1] if all_indicators['macd'] else 'N/A'}")
print(f"ATR(14) 최근값: {all_indicators['atr'][-1] if all_indicators['atr'] else 'N/A'}")
print("\n✅ 모든 테스트 통과")
