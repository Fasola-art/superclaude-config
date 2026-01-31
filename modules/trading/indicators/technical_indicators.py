#!/usr/bin/env python3
"""
기술적 지표 라이브러리
트레이딩에서 사용되는 주요 기술적 지표 계산 함수들

지원 지표:
- 이동평균 (SMA, EMA, WMA)
- 모멘텀 지표 (RSI, MACD, Stochastic)
- 변동성 지표 (ATR, Bollinger Bands)
- 추세 지표 (ADX, Parabolic SAR)
- 거래량 지표 (OBV, VWAP)
"""

from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
import math


@dataclass
class OHLCV:
    """캔들스틱 데이터"""
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


# ============ 이동평균 지표 ============

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


# ============ 모멘텀 지표 ============

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


# ============ 변동성 지표 ============

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


# ============ 추세 지표 ============

def adx(candles: List[OHLCV], period: int = 14) -> Dict[str, List[float]]:
    """
    Average Directional Index (평균방향지수)

    Args:
        candles: OHLCV 데이터 리스트
        period: 기간 (기본 14)

    Returns:
        {'adx': [...], '+di': [...], '-di': [...]}
    """
    if len(candles) < period + 1:
        return {'adx': [], '+di': [], '-di': []}

    # +DM, -DM 계산
    plus_dm = []
    minus_dm = []
    tr_list = []

    for i in range(1, len(candles)):
        high_diff = candles[i].high - candles[i - 1].high
        low_diff = candles[i - 1].low - candles[i].low

        if high_diff > low_diff and high_diff > 0:
            plus_dm.append(high_diff)
        else:
            plus_dm.append(0)

        if low_diff > high_diff and low_diff > 0:
            minus_dm.append(low_diff)
        else:
            minus_dm.append(0)

        # True Range
        hl = candles[i].high - candles[i].low
        hc = abs(candles[i].high - candles[i - 1].close)
        lc = abs(candles[i].low - candles[i - 1].close)
        tr_list.append(max(hl, hc, lc))

    # 평활화
    def smooth(values: List[float], period: int) -> List[float]:
        result = [sum(values[:period])]
        for v in values[period:]:
            result.append(result[-1] - (result[-1] / period) + v)
        return result

    smooth_plus_dm = smooth(plus_dm, period)
    smooth_minus_dm = smooth(minus_dm, period)
    smooth_tr = smooth(tr_list, period)

    # +DI, -DI 계산
    plus_di = []
    minus_di = []
    dx_list = []

    for i in range(len(smooth_tr)):
        if smooth_tr[i] == 0:
            plus_di.append(0)
            minus_di.append(0)
        else:
            pdi = (smooth_plus_dm[i] / smooth_tr[i]) * 100
            mdi = (smooth_minus_dm[i] / smooth_tr[i]) * 100
            plus_di.append(round(pdi, 2))
            minus_di.append(round(mdi, 2))

            # DX
            di_sum = pdi + mdi
            if di_sum == 0:
                dx_list.append(0)
            else:
                dx_list.append(abs(pdi - mdi) / di_sum * 100)

    # ADX = DX의 EMA
    adx_values = ema(dx_list, period) if len(dx_list) >= period else []

    return {
        'adx': [round(v, 2) for v in adx_values],
        '+di': plus_di,
        '-di': minus_di
    }


# ============ 거래량 지표 ============

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


# ============ 유틸리티 함수 ============

def calculate_all_indicators(
    candles: List[OHLCV],
    config: Dict = None
) -> Dict[str, any]:
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


# 테스트
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

    closes = [c.close for c in test_candles]

    print("=== 기술적 지표 계산 테스트 ===\n")

    # SMA
    sma20 = sma(closes, 20)
    print(f"SMA(20) 최근 5개: {sma20[-5:]}")

    # RSI
    rsi_values = rsi(closes, 14)
    print(f"RSI(14) 최근값: {rsi_values[-1] if rsi_values else 'N/A'}")

    # MACD
    macd_line, signal_line, histogram = macd(closes)
    print(f"MACD 최근값: {macd_line[-1] if macd_line else 'N/A'}")

    # ATR
    atr_values = atr(test_candles, 14)
    print(f"ATR(14) 최근값: {atr_values[-1] if atr_values else 'N/A'}")

    # Bollinger Bands
    bb_upper, bb_middle, bb_lower = bollinger_bands(closes)
    print(f"BB 상단/중간/하단: {bb_upper[-1]:.2f} / {bb_middle[-1]:.2f} / {bb_lower[-1]:.2f}")
