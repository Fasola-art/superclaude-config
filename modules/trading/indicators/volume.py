#!/usr/bin/env python3
"""거래량 지표"""

from typing import List
from .types import OHLCV


def obv(candles: List[OHLCV]) -> List[float]:
    """
    On-Balance Volume (누적 거래량)

    Args:
        candles: OHLCV 데이터 리스트

    Returns:
        OBV 값 리스트
    """
    if len(candles) < 2:
        return []

    obv_values = [candles[0].volume]

    for i in range(1, len(candles)):
        if candles[i].close > candles[i - 1].close:
            obv_values.append(obv_values[-1] + candles[i].volume)
        elif candles[i].close < candles[i - 1].close:
            obv_values.append(obv_values[-1] - candles[i].volume)
        else:
            obv_values.append(obv_values[-1])

    return obv_values


def vwap(candles: List[OHLCV]) -> List[float]:
    """
    Volume Weighted Average Price (거래량 가중 평균 가격)

    Args:
        candles: OHLCV 데이터 리스트

    Returns:
        VWAP 값 리스트
    """
    if not candles:
        return []

    vwap_values = []
    cumulative_tp_volume = 0
    cumulative_volume = 0

    for candle in candles:
        # Typical Price = (High + Low + Close) / 3
        typical_price = (candle.high + candle.low + candle.close) / 3
        tp_volume = typical_price * candle.volume

        cumulative_tp_volume += tp_volume
        cumulative_volume += candle.volume

        if cumulative_volume > 0:
            vwap_values.append(round(cumulative_tp_volume / cumulative_volume, 4))
        else:
            vwap_values.append(0)

    return vwap_values
