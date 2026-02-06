#!/usr/bin/env python3
"""다이버전스 감지"""

from typing import List, Tuple, Dict
from .momentum import rsi


def rsi_divergence(
    prices: List[float],
    rsi_period: int = 14,
    lookback: int = 5
) -> Dict[str, List[int]]:
    """
    RSI 다이버전스 감지

    Args:
        prices: 가격 리스트
        rsi_period: RSI 계산 기간 (기본 14)
        lookback: 고점/저점 탐색 범위 (기본 5)

    Returns:
        {
            'bullish': [인덱스 리스트],  # 강세 다이버전스 발생 지점
            'bearish': [인덱스 리스트],  # 약세 다이버전스 발생 지점
            'hidden_bullish': [인덱스 리스트],  # 숨은 강세 다이버전스
            'hidden_bearish': [인덱스 리스트]   # 숨은 약세 다이버전스
        }
    """
    if len(prices) < rsi_period + lookback * 2:
        return {
            'bullish': [],
            'bearish': [],
            'hidden_bullish': [],
            'hidden_bearish': []
        }

    rsi_values = rsi(prices, rsi_period)
    if not rsi_values:
        return {
            'bullish': [],
            'bearish': [],
            'hidden_bullish': [],
            'hidden_bearish': []
        }

    # 가격과 RSI의 고점/저점 찾기
    def find_peaks_troughs(
        data: List[float],
        lookback_range: int
    ) -> Tuple[List[int], List[int]]:
        """피크(고점)와 트로프(저점) 인덱스 찾기"""
        peaks = []
        troughs = []

        for i in range(lookback_range, len(data) - lookback_range):
            window = data[i - lookback_range:i + lookback_range + 1]
            if data[i] == max(window):
                peaks.append(i)
            elif data[i] == min(window):
                troughs.append(i)

        return peaks, troughs

    # 가격 데이터 길이 맞추기 (RSI는 period만큼 짧음)
    price_offset = len(prices) - len(rsi_values)
    aligned_prices = prices[price_offset:]

    price_peaks, price_troughs = find_peaks_troughs(aligned_prices, lookback)
    rsi_peaks, rsi_troughs = find_peaks_troughs(rsi_values, lookback)

    bullish_div = []
    bearish_div = []
    hidden_bullish_div = []
    hidden_bearish_div = []

    # 강세 다이버전스: 가격 저점은 낮아지는데 RSI 저점은 높아짐
    for i in range(1, len(price_troughs)):
        curr_idx = price_troughs[i]
        prev_idx = price_troughs[i - 1]

        if curr_idx in rsi_troughs and prev_idx in rsi_troughs:
            if (aligned_prices[curr_idx] < aligned_prices[prev_idx] and
                rsi_values[curr_idx] > rsi_values[prev_idx]):
                bullish_div.append(curr_idx + price_offset)

    # 약세 다이버전스: 가격 고점은 높아지는데 RSI 고점은 낮아짐
    for i in range(1, len(price_peaks)):
        curr_idx = price_peaks[i]
        prev_idx = price_peaks[i - 1]

        if curr_idx in rsi_peaks and prev_idx in rsi_peaks:
            if (aligned_prices[curr_idx] > aligned_prices[prev_idx] and
                rsi_values[curr_idx] < rsi_values[prev_idx]):
                bearish_div.append(curr_idx + price_offset)

    # 숨은 강세 다이버전스: 가격 저점은 높아지는데 RSI 저점은 낮아짐
    for i in range(1, len(price_troughs)):
        curr_idx = price_troughs[i]
        prev_idx = price_troughs[i - 1]

        if curr_idx in rsi_troughs and prev_idx in rsi_troughs:
            if (aligned_prices[curr_idx] > aligned_prices[prev_idx] and
                rsi_values[curr_idx] < rsi_values[prev_idx]):
                hidden_bullish_div.append(curr_idx + price_offset)

    # 숨은 약세 다이버전스: 가격 고점은 낮아지는데 RSI 고점은 높아짐
    for i in range(1, len(price_peaks)):
        curr_idx = price_peaks[i]
        prev_idx = price_peaks[i - 1]

        if curr_idx in rsi_peaks and prev_idx in rsi_peaks:
            if (aligned_prices[curr_idx] < aligned_prices[prev_idx] and
                rsi_values[curr_idx] > rsi_values[prev_idx]):
                hidden_bearish_div.append(curr_idx + price_offset)

    return {
        'bullish': bullish_div,
        'bearish': bearish_div,
        'hidden_bullish': hidden_bullish_div,
        'hidden_bearish': hidden_bearish_div
    }
