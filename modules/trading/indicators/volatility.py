#!/usr/bin/env python3
"""변동성 지표"""

from typing import List, Tuple
import math
from .types import OHLCV
from .moving_averages import sma, ema


def atr(candles: List[OHLCV], period: int = 14) -> List[float]:
    """
    Average True Range (평균 실제 범위)

    Args:
        candles: OHLCV 데이터 리스트
        period: 기간 (기본 14)

    Returns:
        ATR 값 리스트
    """
    if len(candles) < 2:
        return []

    # True Range 계산
    tr_values = []
    for i in range(1, len(candles)):
        high_low = candles[i].high - candles[i].low
        high_close = abs(candles[i].high - candles[i - 1].close)
        low_close = abs(candles[i].low - candles[i - 1].close)
        tr_values.append(max(high_low, high_close, low_close))

    if len(tr_values) < period:
        return []

    # ATR = TR의 지수 이동평균
    atr_values = [sum(tr_values[:period]) / period]
    for tr in tr_values[period:]:
        atr_values.append((atr_values[-1] * (period - 1) + tr) / period)

    return [round(v, 4) for v in atr_values]


def bollinger_bands(
    prices: List[float],
    period: int = 20,
    std_dev: float = 2.0
) -> Tuple[List[float], List[float], List[float]]:
    """
    볼린저 밴드

    Args:
        prices: 가격 리스트
        period: 기간 (기본 20)
        std_dev: 표준편차 배수 (기본 2.0)

    Returns:
        (상단밴드, 중간밴드(SMA), 하단밴드)
    """
    if len(prices) < period:
        return [], [], []

    middle = sma(prices, period)
    upper = []
    lower = []

    for i in range(len(middle)):
        window = prices[i:i + period]
        std = math.sqrt(sum((x - middle[i]) ** 2 for x in window) / period)
        upper.append(round(middle[i] + std_dev * std, 4))
        lower.append(round(middle[i] - std_dev * std, 4))

    return upper, middle, lower


def keltner_channel(
    candles: List[OHLCV],
    ema_period: int = 20,
    atr_period: int = 10,
    atr_multiplier: float = 2.0
) -> Tuple[List[float], List[float], List[float]]:
    """
    켈트너 채널

    Args:
        candles: OHLCV 데이터 리스트
        ema_period: EMA 기간
        atr_period: ATR 기간
        atr_multiplier: ATR 배수

    Returns:
        (상단밴드, 중간밴드(EMA), 하단밴드)
    """
    closes = [c.close for c in candles]

    if len(closes) < max(ema_period, atr_period):
        return [], [], []

    middle = ema(closes, ema_period)
    atr_values = atr(candles, atr_period)

    # 길이 맞추기
    min_len = min(len(middle), len(atr_values))
    middle = middle[-min_len:]
    atr_values = atr_values[-min_len:]

    upper = [round(m + a * atr_multiplier, 4) for m, a in zip(middle, atr_values)]
    lower = [round(m - a * atr_multiplier, 4) for m, a in zip(middle, atr_values)]

    return upper, middle, lower
