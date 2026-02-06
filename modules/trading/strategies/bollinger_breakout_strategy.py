#!/usr/bin/env python3
"""
볼린저 밴드 돌파 전략
가격이 볼린저 밴드 상단/하단을 돌파할 때 매매 시그널 생성

주요 로직:
- 가격이 하단밴드 아래로 내려갔다가 다시 진입 시 매수
- 가격이 상단밴드 위로 올라갔다가 다시 진입 시 매도
"""

from typing import Dict, Optional
from datetime import datetime

from strategies.base_strategy import (
    BaseStrategy, TradeSignal, SignalType, PositionSide
)
from strategies.bollinger_utils import (
    BollingerConfig, get_position, check_volume,
    check_volatility, calculate_targets, create_hold_signal
)


class BollingerBreakoutStrategy(BaseStrategy):
    """볼린저 밴드 돌파 전략"""

    def __init__(self, config: Dict = None):
        super().__init__(name='bollinger_breakout', config=config)
        cfg = config or {}
        self.bb_config = BollingerConfig(
            period=cfg.get('period', 20),
            std_dev=cfg.get('std_dev', 2.0),
            min_confidence=cfg.get('min_confidence', 0.5),
            use_volume_confirmation=cfg.get('use_volume_confirmation', True),
            volume_threshold=cfg.get('volume_threshold', 1.2)
        )
        self._prev_price: Optional[float] = None
        self._prev_bb_upper: Optional[float] = None
        self._prev_bb_lower: Optional[float] = None
        self._prev_position: Optional[str] = None

    def generate_signal(self, data: Dict) -> TradeSignal:
        """볼린저 밴드 돌파 시그널 생성"""
        symbol = data.get('symbol', 'UNKNOWN')
        price = data.get('close', data.get('price', 0))
        timestamp = data.get('timestamp', datetime.now().isoformat())

        bb_upper = data.get('bb_upper')
        bb_middle = data.get('bb_middle')
        bb_lower = data.get('bb_lower')

        if None in (bb_upper, bb_middle, bb_lower):
            return create_hold_signal(timestamp, symbol, price, '볼린저 밴드 데이터 부족')

        indicators = {
            'bb_upper': bb_upper, 'bb_middle': bb_middle,
            'bb_lower': bb_lower, 'price': price
        }

        current_position = get_position(price, bb_upper, bb_lower)
        signal_type, side, confidence, reason = self._analyze_breakout(
            price, bb_upper, bb_middle, bb_lower, current_position
        )

        if self.bb_config.use_volume_confirmation and signal_type != SignalType.HOLD:
            confidence, reason = check_volume(
                data, confidence, reason, indicators, self.bb_config.volume_threshold
            )

        confidence, reason = check_volatility(
            bb_upper, bb_lower, bb_middle, confidence, reason, indicators
        )

        stop_loss, target_price = calculate_targets(signal_type, price, bb_upper, bb_lower)

        self._prev_price = price
        self._prev_bb_upper = bb_upper
        self._prev_bb_lower = bb_lower
        self._prev_position = current_position

        return TradeSignal(
            timestamp=timestamp, symbol=symbol, signal_type=signal_type,
            side=side, price=price, target_price=target_price,
            stop_loss=stop_loss, confidence=round(confidence, 3),
            reason=reason, indicators=indicators
        )

    def _analyze_breakout(
        self, price: float, upper: float, middle: float, lower: float, current_pos: str
    ) -> tuple:
        """돌파 패턴 분석"""
        if not self._prev_position or not self._prev_price:
            return SignalType.HOLD, PositionSide.NONE, 0.5, f'현재 위치: {current_pos}'

        # 하단밴드 돌파 후 복귀 → 매수
        if self._prev_position == 'below_lower' and current_pos == 'inside' and price > lower:
            confidence = 0.7
            reason = '하단밴드 돌파 후 복귀 (과매도 반등)'
            if price > middle:
                confidence += 0.1
                reason += ' / 중간선 상승 돌파'
            return SignalType.BUY, PositionSide.LONG, confidence, reason

        # 상단밴드 돌파 후 복귀 → 매도
        if self._prev_position == 'above_upper' and current_pos == 'inside' and price < upper:
            confidence = 0.7
            reason = '상단밴드 돌파 후 복귀 (과매수 조정)'
            if price < middle:
                confidence += 0.1
                reason += ' / 중간선 하향 돌파'
            return SignalType.SELL, PositionSide.SHORT, confidence, reason

        return SignalType.HOLD, PositionSide.NONE, 0.5, f'현재 위치: {current_pos}'

    def reset(self):
        """전략 상태 초기화"""
        self._prev_price = None
        self._prev_bb_upper = None
        self._prev_bb_lower = None
        self._prev_position = None
        self.signals_history.clear()
