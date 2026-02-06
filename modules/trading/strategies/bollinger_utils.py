#!/usr/bin/env python3
"""볼린저 밴드 전략 유틸리티 함수"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass

from strategies.base_strategy import TradeSignal, SignalType, PositionSide


@dataclass
class BollingerConfig:
    """볼린저 밴드 전략 설정"""
    period: int = 20
    std_dev: float = 2.0
    min_confidence: float = 0.5
    use_volume_confirmation: bool = True
    volume_threshold: float = 1.2


def get_position(price: float, upper: float, lower: float) -> str:
    """가격 위치 판단"""
    if price > upper:
        return 'above_upper'
    elif price < lower:
        return 'below_lower'
    return 'inside'


def check_volume(
    data: Dict, confidence: float, reason: str,
    indicators: Dict, threshold: float
) -> Tuple[float, str]:
    """거래량 확인"""
    volume = data.get('volume')
    avg_volume = data.get('avg_volume')

    if volume and avg_volume:
        indicators['volume'] = volume
        indicators['avg_volume'] = avg_volume
        volume_ratio = volume / avg_volume

        if volume_ratio >= threshold:
            confidence = min(confidence + 0.1, 0.95)
            reason += f' / 거래량 증가 ({volume_ratio:.1f}x)'
        else:
            confidence -= 0.1
            reason += ' / 거래량 부족'

    return confidence, reason


def check_volatility(
    upper: float, lower: float, middle: float,
    confidence: float, reason: str, indicators: Dict
) -> Tuple[float, str]:
    """변동성 확인"""
    band_width = (upper - lower) / middle
    indicators['band_width'] = round(band_width, 4)

    if band_width < 0.05:
        confidence *= 0.8
        reason += ' / 낮은 변동성'

    return confidence, reason


def calculate_targets(
    signal_type: SignalType, price: float, upper: float, lower: float
) -> Tuple[Optional[float], Optional[float]]:
    """손절가/목표가 계산"""
    if signal_type == SignalType.BUY:
        return lower * 0.99, upper
    elif signal_type == SignalType.SELL:
        return upper * 1.01, lower
    return None, None


def create_hold_signal(
    timestamp: str, symbol: str, price: float, reason: str
) -> TradeSignal:
    """HOLD 시그널 생성"""
    return TradeSignal(
        timestamp=timestamp,
        symbol=symbol,
        signal_type=SignalType.HOLD,
        side=PositionSide.NONE,
        price=price,
        confidence=0.0,
        reason=reason,
        indicators={}
    )
