#!/usr/bin/env python3
"""모멘텀 지표"""

from typing import List, Tuple
from .types import OHLCV
from .moving_averages import ema, sma


def rsi(prices: List[float], period: int = 14) -> List[float]:
    """
    상대강도지수 (Relative Strength Index)

    Args:
        prices: 가격 리스트
        period: 기간 (기본 14)

    Returns:
        RSI 값 리스트 (0-100)
    """
    if len(prices) < period + 1:
        return []

    # 가격 변화량 계산
    gains = []
    losses = []

    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        gains.append(max(0, change))
        losses.append(abs(min(0, change)))

    rsi_values = []

    # 첫 번째 평균
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        if avg_loss == 0:
            rsi_values.append(100)
        else:
            rs = avg_gain / avg_loss
            rsi_values.append(round(100 - (100 / (1 + rs)), 2))

        # 지수 평활화
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    return rsi_values


def macd(
    prices: List[float],
    fast: int = 12,
    slow: int = 26,
    signal: int = 9
) -> Tuple[List[float], List[float], List[float]]:
    """
    MACD (Moving Average Convergence Divergence)

    Args:
        prices: 가격 리스트
        fast: 빠른 EMA 기간 (기본 12)
        slow: 느린 EMA 기간 (기본 26)
        signal: 시그널 라인 기간 (기본 9)

    Returns:
        (MACD 라인, 시그널 라인, 히스토그램)
    """
    if len(prices) < slow:
        return [], [], []

    fast_ema = ema(prices, fast)
    slow_ema = ema(prices, slow)

    # MACD 라인 = 빠른 EMA - 느린 EMA
    macd_line = []
    offset = slow - fast
    for i in range(len(slow_ema)):
        macd_line.append(round(fast_ema[i + offset] - slow_ema[i], 4))

    # 시그널 라인 = MACD의 EMA
    signal_line = ema(macd_line, signal)

    # 히스토그램 = MACD - 시그널
    histogram = []
    offset = len(macd_line) - len(signal_line)
    for i in range(len(signal_line)):
        histogram.append(round(macd_line[i + offset] - signal_line[i], 4))

    return macd_line, signal_line, histogram


def stochastic(
    candles: List[OHLCV],
    k_period: int = 14,
    d_period: int = 3
) -> Tuple[List[float], List[float]]:
    """
    스토캐스틱 오실레이터

    Args:
        candles: OHLCV 데이터 리스트
        k_period: %K 기간 (기본 14)
        d_period: %D 기간 (기본 3)

    Returns:
        (%K 값 리스트, %D 값 리스트)
    """
    if len(candles) < k_period:
        return [], []

    k_values = []

    for i in range(k_period - 1, len(candles)):
        window = candles[i - k_period + 1:i + 1]
        highest = max(c.high for c in window)
        lowest = min(c.low for c in window)
        current_close = candles[i].close

        if highest == lowest:
            k_values.append(50)
        else:
            k = (current_close - lowest) / (highest - lowest) * 100
            k_values.append(round(k, 2))

    # %D = %K의 SMA
    d_values = sma(k_values, d_period)

    return k_values, d_values
