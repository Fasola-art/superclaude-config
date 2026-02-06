#!/usr/bin/env python3
"""지표 유틸리티 함수"""

from typing import List, Dict, Any
from .types import OHLCV
from .moving_averages import sma, ema
from .momentum import rsi, macd
from .volatility import atr, bollinger_bands
from .volume import obv, vwap


def calculate_all_indicators(
    candles: List[OHLCV],
    config: Dict = None
) -> Dict[str, Any]:
    """
    모든 지표 한 번에 계산

    Args:
        candles: OHLCV 데이터 리스트
        config: 지표 설정

    Returns:
        모든 지표 값을 담은 딕셔너리
    """
    cfg = config or {}
    closes = [c.close for c in candles]

    result = {}

    # 이동평균
    result['sma20'] = sma(closes, cfg.get('sma_period', 20))
    result['sma50'] = sma(closes, 50)
    result['ema12'] = ema(closes, 12)
    result['ema26'] = ema(closes, 26)

    # 모멘텀
    result['rsi'] = rsi(closes, cfg.get('rsi_period', 14))
    macd_line, signal_line, histogram = macd(closes)
    result['macd'] = macd_line
    result['macd_signal'] = signal_line
    result['macd_histogram'] = histogram

    # 변동성
    result['atr'] = atr(candles, cfg.get('atr_period', 14))
    bb_upper, bb_middle, bb_lower = bollinger_bands(closes)
    result['bb_upper'] = bb_upper
    result['bb_middle'] = bb_middle
    result['bb_lower'] = bb_lower

    # 거래량
    result['obv'] = obv(candles)
    result['vwap'] = vwap(candles)

    return result


if __name__ == '__main__':
    from datetime import datetime, timedelta
    import random

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
