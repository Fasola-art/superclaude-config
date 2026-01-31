#!/usr/bin/env python3
"""
평균회귀 전략
가격이 평균에서 벗어났을 때 다시 평균으로 회귀할 것을 예상하는 전략

주요 지표:
- 볼린저 밴드 (가격이 밴드 밖으로 이탈 시 회귀 예상)
- Z-Score (표준편차 기반 이탈 측정)
- RSI (극단적 과매수/과매도 시 반전 예상)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import math
import sys
from pathlib import Path

# 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from strategies.base_strategy import (
    BaseStrategy, TradeSignal, SignalType, PositionSide
)


@dataclass
class MeanReversionConfig:
    """평균회귀 전략 설정"""
    bb_period: int = 20                     # 볼린저 밴드 기간
    bb_std: float = 2.0                     # 볼린저 밴드 표준편차 배수
    z_score_period: int = 20                # Z-Score 계산 기간
    z_score_threshold: float = 2.0          # Z-Score 임계값
    rsi_period: int = 14                    # RSI 기간
    rsi_extreme_low: float = 20.0           # 극단적 과매도
    rsi_extreme_high: float = 80.0          # 극단적 과매수
    min_confidence: float = 0.5             # 최소 신뢰도
    use_bollinger: bool = True              # 볼린저 밴드 사용
    use_z_score: bool = True                # Z-Score 사용
    use_rsi: bool = True                    # RSI 사용


class MeanReversionStrategy(BaseStrategy):
    """
    평균회귀 기반 트레이딩 전략

    전략 로직:
    1. 가격이 볼린저 밴드 하단 이탈 → 매수 (상단 이탈 → 매도)
    2. Z-Score가 -2 이하 → 매수, +2 이상 → 매도
    3. RSI가 20 이하 → 매수, 80 이상 → 매도
    4. 목표가는 중심선(평균)으로 설정
    """

    def __init__(self, config: Dict = None):
        """
        초기화

        Args:
            config: 전략 설정 딕셔너리
        """
        super().__init__(name='mean_reversion', config=config)

        # 설정 로드
        cfg = config or {}
        self.mr_config = MeanReversionConfig(
            bb_period=cfg.get('bb_period', 20),
            bb_std=cfg.get('bb_std', 2.0),
            z_score_period=cfg.get('z_score_period', 20),
            z_score_threshold=cfg.get('z_score_threshold', 2.0),
            rsi_period=cfg.get('rsi_period', 14),
            rsi_extreme_low=cfg.get('rsi_extreme_low', 20.0),
            rsi_extreme_high=cfg.get('rsi_extreme_high', 80.0),
            min_confidence=cfg.get('min_confidence', 0.5),
            use_bollinger=cfg.get('use_bollinger', True),
            use_z_score=cfg.get('use_z_score', True),
            use_rsi=cfg.get('use_rsi', True)
        )

        # 가격 히스토리 (자체 계산용)
        self._price_history: List[float] = []

    def _calculate_z_score(self, prices: List[float]) -> Optional[float]:
        """
        Z-Score 계산

        Args:
            prices: 가격 리스트

        Returns:
            Z-Score 값
        """
        if len(prices) < 2:
            return None

        mean = sum(prices) / len(prices)
        variance = sum((p - mean) ** 2 for p in prices) / len(prices)
        std = math.sqrt(variance)

        if std == 0:
            return 0

        return (prices[-1] - mean) / std

    def _calculate_bollinger(
        self,
        prices: List[float],
        period: int,
        std_dev: float
    ) -> Optional[Dict[str, float]]:
        """
        볼린저 밴드 계산

        Args:
            prices: 가격 리스트
            period: 기간
            std_dev: 표준편차 배수

        Returns:
            {'upper': float, 'middle': float, 'lower': float}
        """
        if len(prices) < period:
            return None

        recent = prices[-period:]
        middle = sum(recent) / period
        variance = sum((p - middle) ** 2 for p in recent) / period
        std = math.sqrt(variance)

        return {
            'upper': middle + std_dev * std,
            'middle': middle,
            'lower': middle - std_dev * std,
            'std': std
        }

    def generate_signal(self, data: Dict) -> TradeSignal:
        """
        평균회귀 시그널 생성

        Args:
            data: {
                'symbol': str,
                'close': float,
                'bb_upper': float (optional),
                'bb_middle': float (optional),
                'bb_lower': float (optional),
                'z_score': float (optional),
                'rsi': float (optional),
                'prices': List[float] (optional, for calculation)
            }

        Returns:
            TradeSignal 객체
        """
        symbol = data.get('symbol', 'UNKNOWN')
        price = data.get('close', data.get('price', 0))
        timestamp = data.get('timestamp', datetime.now().isoformat())

        # 가격 히스토리 업데이트
        self._price_history.append(price)
        if len(self._price_history) > 100:
            self._price_history = self._price_history[-100:]

        # 지표 값 수집
        indicators = {}
        buy_signals = 0
        sell_signals = 0
        reasons = []
        mean_price = price  # 기본값

        # ===== 볼린저 밴드 분석 =====
        if self.mr_config.use_bollinger:
            bb_upper = data.get('bb_upper')
            bb_middle = data.get('bb_middle')
            bb_lower = data.get('bb_lower')

            # 제공되지 않으면 자체 계산
            if bb_upper is None and len(self._price_history) >= self.mr_config.bb_period:
                bb = self._calculate_bollinger(
                    self._price_history,
                    self.mr_config.bb_period,
                    self.mr_config.bb_std
                )
                if bb:
                    bb_upper = bb['upper']
                    bb_middle = bb['middle']
                    bb_lower = bb['lower']

            if bb_upper is not None and bb_lower is not None:
                indicators['bb_upper'] = bb_upper
                indicators['bb_middle'] = bb_middle
                indicators['bb_lower'] = bb_lower
                mean_price = bb_middle

                # 밴드 위치 백분율 계산 (0% = 하단, 100% = 상단)
                bb_range = bb_upper - bb_lower
                if bb_range > 0:
                    bb_position = (price - bb_lower) / bb_range * 100
                    indicators['bb_position'] = round(bb_position, 1)

                    if price < bb_lower:
                        buy_signals += 3
                        reasons.append(f'BB 하단 이탈 ({bb_position:.0f}%)')
                    elif price > bb_upper:
                        sell_signals += 3
                        reasons.append(f'BB 상단 이탈 ({bb_position:.0f}%)')
                    elif bb_position < 20:
                        buy_signals += 1
                        reasons.append(f'BB 하단 근접 ({bb_position:.0f}%)')
                    elif bb_position > 80:
                        sell_signals += 1
                        reasons.append(f'BB 상단 근접 ({bb_position:.0f}%)')

        # ===== Z-Score 분석 =====
        if self.mr_config.use_z_score:
            z_score = data.get('z_score')

            # 제공되지 않으면 자체 계산
            if z_score is None and len(self._price_history) >= self.mr_config.z_score_period:
                z_score = self._calculate_z_score(
                    self._price_history[-self.mr_config.z_score_period:]
                )

            if z_score is not None:
                indicators['z_score'] = round(z_score, 3)
                threshold = self.mr_config.z_score_threshold

                if z_score < -threshold:
                    buy_signals += 2
                    reasons.append(f'Z-Score 하향이탈 ({z_score:.2f})')
                elif z_score > threshold:
                    sell_signals += 2
                    reasons.append(f'Z-Score 상향이탈 ({z_score:.2f})')

        # ===== RSI 분석 (극단값만) =====
        if self.mr_config.use_rsi:
            rsi = data.get('rsi')

            if rsi is not None:
                indicators['rsi'] = rsi

                if rsi < self.mr_config.rsi_extreme_low:
                    buy_signals += 2
                    reasons.append(f'RSI 극단적 과매도 ({rsi:.1f})')
                elif rsi > self.mr_config.rsi_extreme_high:
                    sell_signals += 2
                    reasons.append(f'RSI 극단적 과매수 ({rsi:.1f})')

        # ===== 시그널 결정 =====
        total_signals = buy_signals + sell_signals

        if total_signals == 0:
            signal_type = SignalType.HOLD
            side = PositionSide.NONE
            confidence = 0.0
            reason = '평균 근처 - 관망'
        elif buy_signals > sell_signals and buy_signals >= 2:
            signal_type = SignalType.BUY
            side = PositionSide.LONG
            confidence = min(buy_signals / max(total_signals, 1), 0.95)
            reason = ' / '.join(reasons) if reasons else '평균 이하 이탈'
        elif sell_signals > buy_signals and sell_signals >= 2:
            signal_type = SignalType.SELL
            side = PositionSide.SHORT
            confidence = min(sell_signals / max(total_signals, 1), 0.95)
            reason = ' / '.join(reasons) if reasons else '평균 이상 이탈'
        else:
            signal_type = SignalType.HOLD
            side = PositionSide.NONE
            confidence = 0.3
            reason = '혼조세: ' + ' / '.join(reasons) if reasons else '관망'

        # 손절/익절 계산 (평균회귀 전략은 평균으로의 회귀를 목표)
        stop_loss = None
        target_price = mean_price  # 목표는 중심선

        if signal_type == SignalType.BUY:
            stop_loss = price * 0.95      # 5% 손절 (평균회귀 실패 시)
        elif signal_type == SignalType.SELL:
            stop_loss = price * 1.05      # 5% 손절

        return TradeSignal(
            timestamp=timestamp,
            symbol=symbol,
            signal_type=signal_type,
            side=side,
            price=price,
            target_price=target_price,
            stop_loss=stop_loss,
            confidence=round(confidence, 3),
            reason=reason,
            indicators=indicators
        )

    def reset(self):
        """전략 상태 초기화"""
        self._price_history.clear()
        self.signals_history.clear()


# 테스트 코드
if __name__ == '__main__':
    strategy = MeanReversionStrategy({
        'bb_period': 20,
        'bb_std': 2.0,
        'z_score_threshold': 2.0
    })

    # 가격 데이터 시뮬레이션 (하락 후 반등 예상)
    import random

    # 먼저 히스토리 생성
    base = 100
    for i in range(30):
        base += random.uniform(-1, 1)
        strategy.generate_signal({
            'symbol': 'TEST/USD',
            'close': base,
            'timestamp': datetime.now().isoformat()
        })

    # 급락 시나리오 (매수 시그널 예상)
    test_data = {
        'symbol': 'TEST/USD',
        'close': 90,  # 급락
        'rsi': 15,    # 극단적 과매도
        'timestamp': datetime.now().isoformat()
    }

    signal = strategy.generate_signal(test_data)

    print("=== 평균회귀 전략 테스트 ===")
    print(f"시그널: {signal.signal_type.value}")
    print(f"방향: {signal.side.value}")
    print(f"신뢰도: {signal.confidence * 100:.1f}%")
    print(f"이유: {signal.reason}")
    print(f"손절가: {signal.stop_loss}")
    print(f"목표가: {signal.target_price}")
    print(f"지표: {signal.indicators}")
