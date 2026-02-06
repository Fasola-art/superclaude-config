#!/usr/bin/env python3
"""이동평균 지표"""

from typing import List


def sma(prices: List[float], period: int) -> List[float]:
    """
    단순 이동평균 (Simple Moving Average)

    Args:
        prices: 가격 리스트
        period: 기간

    Returns:
        SMA 값 리스트
    """
    if len(prices) < period:
        return []

    result = []
    for i in range(period - 1, len(prices)):
        avg = sum(prices[i - period + 1:i + 1]) / period
        result.append(round(avg, 4))
    return result


def ema(prices: List[float], period: int) -> List[float]:
    """
    지수 이동평균 (Exponential Moving Average)

    Args:
        prices: 가격 리스트
        period: 기간

    Returns:
        EMA 값 리스트
    """
    if len(prices) < period:
        return []

    multiplier = 2 / (period + 1)
    ema_values = [sum(prices[:period]) / period]  # 첫 값은 SMA

    for price in prices[period:]:
        ema_values.append(
            (price - ema_values[-1]) * multiplier + ema_values[-1]
        )
    return [round(v, 4) for v in ema_values]


def wma(prices: List[float], period: int) -> List[float]:
    """
    가중 이동평균 (Weighted Moving Average)

    Args:
        prices: 가격 리스트
        period: 기간

    Returns:
        WMA 값 리스트
    """
    if len(prices) < period:
        return []

    weights = list(range(1, period + 1))
    weight_sum = sum(weights)

    result = []
    for i in range(period - 1, len(prices)):
        window = prices[i - period + 1:i + 1]
        weighted_avg = sum(p * w for p, w in zip(window, weights)) / weight_sum
        result.append(round(weighted_avg, 4))
    return result
