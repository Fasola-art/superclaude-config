#!/usr/bin/env python3
"""
기본 전략 클래스
모든 트레이딩 전략의 기반이 되는 추상 클래스

사용법:
    class MyStrategy(BaseStrategy):
        def generate_signal(self, data):
            # 전략 로직 구현
            return signal
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
from pathlib import Path


class SignalType(Enum):
    """시그널 타입"""
    BUY = 'buy'          # 매수 시그널
    SELL = 'sell'        # 매도 시그널
    HOLD = 'hold'        # 관망
    CLOSE = 'close'      # 포지션 청산


class PositionSide(Enum):
    """포지션 방향"""
    LONG = 'long'        # 롱 포지션
    SHORT = 'short'      # 숏 포지션
    NONE = 'none'        # 포지션 없음


@dataclass
class TradeSignal:
    """트레이딩 시그널 데이터"""
    timestamp: str                          # 시그널 발생 시간
    symbol: str                             # 심볼
    signal_type: SignalType                 # 시그널 타입
    side: PositionSide                      # 포지션 방향
    price: float                            # 현재 가격
    target_price: Optional[float] = None    # 목표가
    stop_loss: Optional[float] = None       # 손절가
    confidence: float = 0.5                 # 신뢰도 (0.0 ~ 1.0)
    reason: str = ''                        # 시그널 발생 이유
    indicators: Dict[str, float] = field(default_factory=dict)  # 지표 값들
    metadata: Dict[str, Any] = field(default_factory=dict)      # 추가 메타데이터


@dataclass
class Position:
    """현재 포지션 정보"""
    symbol: str                             # 심볼
    side: PositionSide                      # 방향
    entry_price: float                      # 진입 가격
    quantity: float                         # 수량
    entry_time: str                         # 진입 시간
    unrealized_pnl: float = 0.0            # 미실현 손익
    stop_loss: Optional[float] = None       # 손절가
    take_profit: Optional[float] = None     # 익절가


class BaseStrategy(ABC):
    """
    기본 전략 추상 클래스

    모든 전략은 이 클래스를 상속받아 구현해야 합니다.
    """

    def __init__(self, name: str, config: Dict = None):
        """
        초기화

        Args:
            name: 전략 이름
            config: 전략 설정
        """
        self.name = name
        self.config = config or {}
        self.position: Optional[Position] = None
        self.signals_history: List[TradeSignal] = []
        self.trades_history: List[Dict] = []

    @abstractmethod
    def generate_signal(self, data: Dict) -> TradeSignal:
        """
        시그널 생성 (추상 메서드)

        Args:
            data: OHLCV 데이터 및 기타 정보

        Returns:
            TradeSignal 객체
        """
        pass

    def on_tick(self, tick_data: Dict) -> Optional[TradeSignal]:
        """
        틱 데이터 수신 시 호출

        Args:
            tick_data: 틱 데이터 (price, volume, timestamp 등)

        Returns:
            시그널이 발생하면 TradeSignal, 없으면 None
        """
        signal = self.generate_signal(tick_data)

        if signal.signal_type != SignalType.HOLD:
            self.signals_history.append(signal)

        return signal

    def on_candle_close(self, candle: Dict) -> Optional[TradeSignal]:
        """
        캔들 마감 시 호출

        Args:
            candle: 완성된 캔들 데이터 (open, high, low, close, volume)

        Returns:
            시그널이 발생하면 TradeSignal, 없으면 None
        """
        return self.on_tick(candle)

    def update_position(self, position: Optional[Position]):
        """
        포지션 업데이트

        Args:
            position: 새 포지션 정보
        """
        self.position = position

    def calculate_position_size(
        self,
        capital: float,
        price: float,
        risk_percent: float = 0.02
    ) -> float:
        """
        포지션 크기 계산

        Args:
            capital: 총 자본금
            price: 현재 가격
            risk_percent: 리스크 비율 (기본 2%)

        Returns:
            적정 포지션 크기
        """
        risk_amount = capital * risk_percent
        return risk_amount / price

    def validate_signal(self, signal: TradeSignal) -> bool:
        """
        시그널 유효성 검증

        Args:
            signal: 검증할 시그널

        Returns:
            유효하면 True
        """
        # 기본 검증
        if signal.confidence < self.config.get('min_confidence', 0.3):
            return False

        # 포지션이 있는 경우 반대 방향 시그널만 허용
        if self.position and self.position.side != PositionSide.NONE:
            if signal.signal_type == SignalType.BUY and self.position.side == PositionSide.LONG:
                return False
            if signal.signal_type == SignalType.SELL and self.position.side == PositionSide.SHORT:
                return False

        return True

    def to_dict(self) -> Dict:
        """전략 정보를 딕셔너리로 변환"""
        return {
            'name': self.name,
            'config': self.config,
            'has_position': self.position is not None,
            'signals_count': len(self.signals_history),
            'trades_count': len(self.trades_history)
        }

    def save_state(self, filepath: Path):
        """
        전략 상태 저장

        Args:
            filepath: 저장할 파일 경로
        """
        state = {
            'name': self.name,
            'config': self.config,
            'saved_at': datetime.now().isoformat(),
            'signals_count': len(self.signals_history),
            'trades_count': len(self.trades_history)
        }
        filepath.write_text(json.dumps(state, indent=2, ensure_ascii=False))

    def __str__(self) -> str:
        return f"Strategy({self.name})"

    def __repr__(self) -> str:
        return f"Strategy(name={self.name}, config={self.config})"
