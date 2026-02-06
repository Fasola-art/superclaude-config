#!/usr/bin/env python3
"""추세 지표"""

from typing import List, Dict
from .types import OHLCV
from .moving_averages import ema


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
