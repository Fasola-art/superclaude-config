#!/usr/bin/env python3
"""
모멘텀 전략
가격의 모멘텀(추세의 강도)을 기반으로 매매 시그널 생성

주요 지표:
- RSI (상대강도지수)
- MACD (이동평균수렴확산지수)
- 이동평균 크로스오버
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import sys
from pathlib import Path

# 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from strategies.base_strategy import (
    BaseStrategy, TradeSignal, SignalType, PositionSide
)


@dataclass
class MomentumConfig:
    """모멘텀 전략 설정"""
    rsi_period: int = 14                    # RSI 기간
    rsi_oversold: float = 30.0              # 과매도 기준
    rsi_overbought: float = 70.0            # 과매수 기준
    macd_fast: int = 12                     # MACD 빠른 이동평균
    macd_slow: int = 26                     # MACD 느린 이동평균
    macd_signal: int = 9                    # MACD 시그널
    sma_short: int = 20                     # 단기 이동평균
    sma_long: int = 50                      # 장기 이동평균
    min_confidence: float = 0.5             # 최소 신뢰도
    use_rsi: bool = True                    # RSI 사용 여부
    use_macd: bool = True                   # MACD 사용 여부
    use_ma_cross: bool = True               # 이동평균 크로스 사용 여부


class MomentumStrategy(BaseStrategy):
    """
    모멘텀 기반 트레이딩 전략

    전략 로직:
    1. RSI가 과매도 영역에서 상승하면 매수 시그널
    2. RSI가 과매수 영역에서 하락하면 매도 시그널
    3. MACD 골든크로스 → 매수, 데드크로스 → 매도
    4. 단기 MA가 장기 MA를 상향 돌파 → 매수
    5. 단기 MA가 장기 MA를 하향 돌파 → 매도
    """

    def __init__(self, config: Dict = None):
        """
        초기화

        Args:
            config: 전략 설정 딕셔너리
        """
        super().__init__(name='momentum', config=config)

        # 설정 로드
        cfg = config or {}
        self.momentum_config = MomentumConfig(
            rsi_period=cfg.get('rsi_period', 14),
            rsi_oversold=cfg.get('rsi_oversold', 30.0),
            rsi_overbought=cfg.get('rsi_overbought', 70.0),
            macd_fast=cfg.get('macd_fast', 12),
            macd_slow=cfg.get('macd_slow', 26),
            macd_signal=cfg.get('macd_signal', 9),
            sma_short=cfg.get('sma_short', 20),
            sma_long=cfg.get('sma_long', 50),
            min_confidence=cfg.get('min_confidence', 0.5),
            use_rsi=cfg.get('use_rsi', True),
            use_macd=cfg.get('use_macd', True),
            use_ma_cross=cfg.get('use_ma_cross', True)
        )

        # 이전 값 저장 (크로스오버 감지용)
        self._prev_macd: Optional[float] = None
        self._prev_signal: Optional[float] = None
        self._prev_sma_short: Optional[float] = None
        self._prev_sma_long: Optional[float] = None

    def generate_signal(self, data: Dict) -> TradeSignal:
        """
        모멘텀 시그널 생성

        Args:
            data: {
                'symbol': str,
                'close': float,
                'rsi': float (optional),
                'macd': float (optional),
                'macd_signal': float (optional),
                'sma_short': float (optional),
                'sma_long': float (optional),
                'prices': List[float] (optional, for calculation)
            }

        Returns:
            TradeSignal 객체
        """
        symbol = data.get('symbol', 'UNKNOWN')
        price = data.get('close', data.get('price', 0))
        timestamp = data.get('timestamp', datetime.now().isoformat())

        # 지표 값 추출 또는 계산
        indicators = {}
        buy_signals = 0
        sell_signals = 0
        reasons = []

        # ===== RSI 분석 =====
        if self.momentum_config.use_rsi:
            rsi = data.get('rsi')
            if rsi is not None:
                indicators['rsi'] = rsi

                if rsi < self.momentum_config.rsi_oversold:
                    buy_signals += 2
                    reasons.append(f'RSI 과매도({rsi:.1f})')
                elif rsi > self.momentum_config.rsi_overbought:
                    sell_signals += 2
                    reasons.append(f'RSI 과매수({rsi:.1f})')

        # ===== MACD 분석 =====
        if self.momentum_config.use_macd:
            macd = data.get('macd')
            macd_signal = data.get('macd_signal')

            if macd is not None and macd_signal is not None:
                indicators['macd'] = macd
                indicators['macd_signal'] = macd_signal

                # 골든크로스 / 데드크로스 감지
                if self._prev_macd is not None and self._prev_signal is not None:
                    # 골든크로스: MACD가 시그널 라인을 상향 돌파
                    if self._prev_macd <= self._prev_signal and macd > macd_signal:
                        buy_signals += 2
                        reasons.append('MACD 골든크로스')
                    # 데드크로스: MACD가 시그널 라인을 하향 돌파
                    elif self._prev_macd >= self._prev_signal and macd < macd_signal:
                        sell_signals += 2
                        reasons.append('MACD 데드크로스')

                # 현재 위치
                if macd > macd_signal:
                    buy_signals += 1
                else:
                    sell_signals += 1

                self._prev_macd = macd
                self._prev_signal = macd_signal

        # ===== 이동평균 크로스오버 =====
        if self.momentum_config.use_ma_cross:
            sma_short = data.get('sma_short')
            sma_long = data.get('sma_long')

            if sma_short is not None and sma_long is not None:
                indicators['sma_short'] = sma_short
                indicators['sma_long'] = sma_long

                # 크로스오버 감지
                if self._prev_sma_short is not None and self._prev_sma_long is not None:
                    # 골든크로스
                    if self._prev_sma_short <= self._prev_sma_long and sma_short > sma_long:
                        buy_signals += 2
                        reasons.append('MA 골든크로스')
                    # 데드크로스
                    elif self._prev_sma_short >= self._prev_sma_long and sma_short < sma_long:
                        sell_signals += 2
                        reasons.append('MA 데드크로스')

                # 현재 위치
                if sma_short > sma_long:
                    buy_signals += 1
                    reasons.append('단기MA > 장기MA')
                else:
                    sell_signals += 1
                    reasons.append('단기MA < 장기MA')

                self._prev_sma_short = sma_short
                self._prev_sma_long = sma_long

        # ===== 시그널 결정 =====
        total_signals = buy_signals + sell_signals

        if total_signals == 0:
            signal_type = SignalType.HOLD
            side = PositionSide.NONE
            confidence = 0.0
            reason = '시그널 없음'
        elif buy_signals > sell_signals and buy_signals >= 3:
            signal_type = SignalType.BUY
            side = PositionSide.LONG
            confidence = min(buy_signals / total_signals, 0.95)
            reason = ' / '.join(reasons) if reasons else '매수 조건 충족'
        elif sell_signals > buy_signals and sell_signals >= 3:
            signal_type = SignalType.SELL
            side = PositionSide.SHORT
            confidence = min(sell_signals / total_signals, 0.95)
            reason = ' / '.join(reasons) if reasons else '매도 조건 충족'
        else:
            signal_type = SignalType.HOLD
            side = PositionSide.NONE
            confidence = 0.5
            reason = '혼조세: ' + ' / '.join(reasons) if reasons else '관망'

        # 손절/익절 계산
        stop_loss = None
        target_price = None

        if signal_type == SignalType.BUY:
            stop_loss = price * 0.97      # 3% 손절
            target_price = price * 1.06   # 6% 익절
        elif signal_type == SignalType.SELL:
            stop_loss = price * 1.03      # 3% 손절
            target_price = price * 0.94   # 6% 익절

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
        self._prev_macd = None
        self._prev_signal = None
        self._prev_sma_short = None
        self._prev_sma_long = None
        self.signals_history.clear()


# 테스트 코드
if __name__ == '__main__':
    strategy = MomentumStrategy({
        'rsi_period': 14,
        'use_rsi': True,
        'use_macd': True,
        'use_ma_cross': True
    })

    # 테스트 데이터 (매수 시그널 예상)
    test_data = {
        'symbol': 'BTC/USD',
        'close': 50000,
        'rsi': 25,  # 과매도
        'macd': 100,
        'macd_signal': 50,  # MACD > Signal
        'sma_short': 49500,
        'sma_long': 49000,  # 골든크로스
        'timestamp': datetime.now().isoformat()
    }

    signal = strategy.generate_signal(test_data)

    print("=== 모멘텀 전략 테스트 ===")
    print(f"시그널: {signal.signal_type.value}")
    print(f"방향: {signal.side.value}")
    print(f"신뢰도: {signal.confidence * 100:.1f}%")
    print(f"이유: {signal.reason}")
    print(f"손절가: {signal.stop_loss}")
    print(f"목표가: {signal.target_price}")
