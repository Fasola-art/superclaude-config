#!/usr/bin/env python3
"""
백테스팅 엔진
과거 데이터를 사용하여 트레이딩 전략의 성과를 시뮬레이션

기능:
- 전략 성과 시뮬레이션
- 포트폴리오 관리
- 성과 지표 계산 (승률, 수익률, 샤프 비율, 최대 낙폭 등)
- 거래 내역 기록
"""

from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
import json
import math
from pathlib import Path
import sys

# 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from indicators.technical_indicators import OHLCV


class OrderType(Enum):
    """주문 타입"""
    MARKET = 'market'       # 시장가
    LIMIT = 'limit'         # 지정가
    STOP = 'stop'           # 스탑
    STOP_LIMIT = 'stop_limit'


class OrderSide(Enum):
    """주문 방향"""
    BUY = 'buy'
    SELL = 'sell'


@dataclass
class Order:
    """주문 정보"""
    id: str
    timestamp: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None          # 지정가 주문 시
    stop_price: Optional[float] = None     # 스탑 주문 시
    filled_price: Optional[float] = None   # 체결 가격
    filled_quantity: float = 0             # 체결 수량
    status: str = 'pending'                # pending, filled, cancelled, rejected


@dataclass
class Trade:
    """거래 기록"""
    id: str
    timestamp: str
    symbol: str
    side: str
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    pnl: float = 0                         # 손익
    pnl_percent: float = 0                 # 손익률
    holding_period: int = 0                # 보유 기간 (캔들 수)
    exit_reason: str = ''                  # 청산 이유


@dataclass
class BacktestResult:
    """백테스트 결과"""
    # 기본 정보
    strategy_name: str
    symbol: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float

    # 거래 통계
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float

    # 수익 통계
    total_return: float               # 총 수익률 (%)
    annualized_return: float          # 연간 수익률 (%)
    profit_factor: float              # 이익/손실 비율
    avg_trade_return: float           # 평균 거래 수익률

    # 리스크 통계
    max_drawdown: float               # 최대 낙폭 (%)
    sharpe_ratio: float               # 샤프 비율
    sortino_ratio: float              # 소르티노 비율
    calmar_ratio: float               # 칼마 비율

    # 추가 통계
    avg_holding_period: float         # 평균 보유 기간
    best_trade: float                 # 최고 수익 거래
    worst_trade: float                # 최저 수익 거래
    consecutive_wins: int             # 연속 승리
    consecutive_losses: int           # 연속 패배

    # 상세 데이터
    trades: List[Dict] = field(default_factory=list)
    equity_curve: List[float] = field(default_factory=list)


class Portfolio:
    """포트폴리오 관리"""

    def __init__(self, initial_capital: float, commission: float = 0.001):
        """
        초기화

        Args:
            initial_capital: 초기 자본금
            commission: 수수료율 (기본 0.1%)
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.commission = commission

        self.positions: Dict[str, Dict] = {}  # {symbol: {quantity, avg_price}}
        self.orders: List[Order] = []
        self.trades: List[Trade] = []
        self.equity_history: List[Dict] = []

        self._order_counter = 0
        self._trade_counter = 0

    def get_equity(self, current_prices: Dict[str, float]) -> float:
        """
        현재 총 자산 계산

        Args:
            current_prices: {symbol: price}

        Returns:
            총 자산 가치
        """
        position_value = sum(
            pos['quantity'] * current_prices.get(symbol, pos['avg_price'])
            for symbol, pos in self.positions.items()
        )
        return self.cash + position_value

    def place_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        order_type: OrderType = OrderType.MARKET,
        price: Optional[float] = None,
        stop_price: Optional[float] = None,
        timestamp: str = None
    ) -> Order:
        """
        주문 생성

        Args:
            symbol: 심볼
            side: 매수/매도
            quantity: 수량
            order_type: 주문 타입
            price: 지정가 가격
            stop_price: 스탑 가격
            timestamp: 주문 시각

        Returns:
            Order 객체
        """
        self._order_counter += 1
        order = Order(
            id=f"order_{self._order_counter}",
            timestamp=timestamp or datetime.now().isoformat(),
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )
        self.orders.append(order)
        return order

    def execute_order(self, order: Order, execution_price: float) -> bool:
        """
        주문 체결

        Args:
            order: 주문 객체
            execution_price: 체결 가격

        Returns:
            체결 성공 여부
        """
        total_cost = execution_price * order.quantity
        commission_cost = total_cost * self.commission

        if order.side == OrderSide.BUY:
            # 매수
            required = total_cost + commission_cost
            if self.cash < required:
                order.status = 'rejected'
                return False

            self.cash -= required

            if order.symbol in self.positions:
                # 기존 포지션에 추가
                pos = self.positions[order.symbol]
                total_qty = pos['quantity'] + order.quantity
                pos['avg_price'] = (
                    pos['avg_price'] * pos['quantity'] + execution_price * order.quantity
                ) / total_qty
                pos['quantity'] = total_qty
            else:
                # 새 포지션
                self.positions[order.symbol] = {
                    'quantity': order.quantity,
                    'avg_price': execution_price,
                    'entry_time': order.timestamp
                }

        else:  # SELL
            if order.symbol not in self.positions:
                order.status = 'rejected'
                return False

            pos = self.positions[order.symbol]
            if pos['quantity'] < order.quantity:
                order.status = 'rejected'
                return False

            # 거래 기록 생성
            self._trade_counter += 1
            pnl = (execution_price - pos['avg_price']) * order.quantity - commission_cost
            pnl_percent = (execution_price - pos['avg_price']) / pos['avg_price'] * 100

            trade = Trade(
                id=f"trade_{self._trade_counter}",
                timestamp=order.timestamp,
                symbol=order.symbol,
                side='sell',
                entry_price=pos['avg_price'],
                exit_price=execution_price,
                quantity=order.quantity,
                pnl=round(pnl, 2),
                pnl_percent=round(pnl_percent, 2)
            )
            self.trades.append(trade)

            self.cash += total_cost - commission_cost

            # 포지션 업데이트
            pos['quantity'] -= order.quantity
            if pos['quantity'] <= 0:
                del self.positions[order.symbol]

        order.filled_price = execution_price
        order.filled_quantity = order.quantity
        order.status = 'filled'
        return True

    def record_equity(self, timestamp: str, prices: Dict[str, float]):
        """자산 기록"""
        equity = self.get_equity(prices)
        self.equity_history.append({
            'timestamp': timestamp,
            'equity': equity,
            'cash': self.cash,
            'positions_value': equity - self.cash
        })


class BacktestEngine:
    """백테스팅 엔진"""

    def __init__(
        self,
        initial_capital: float = 10000,
        commission: float = 0.001,
        slippage: float = 0.001
    ):
        """
        초기화

        Args:
            initial_capital: 초기 자본금
            commission: 수수료율
            slippage: 슬리피지율
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.portfolio: Optional[Portfolio] = None

    def run(
        self,
        candles: List[OHLCV],
        strategy_func: Callable[[Dict, Dict], Optional[Dict]],
        symbol: str = 'UNKNOWN'
    ) -> BacktestResult:
        """
        백테스트 실행

        Args:
            candles: OHLCV 데이터 리스트
            strategy_func: 전략 함수 (data, state) -> signal or None
            symbol: 심볼

        Returns:
            BacktestResult 객체
        """
        if len(candles) < 50:
            raise ValueError("최소 50개 이상의 캔들이 필요합니다.")

        self.portfolio = Portfolio(self.initial_capital, self.commission)
        strategy_state = {}

        for i in range(50, len(candles)):
            candle = candles[i]
            history = candles[:i + 1]

            # 현재 가격으로 자산 기록
            current_prices = {symbol: candle.close}
            self.portfolio.record_equity(candle.timestamp, current_prices)

            # 전략 데이터 준비
            data = {
                'symbol': symbol,
                'timestamp': candle.timestamp,
                'open': candle.open,
                'high': candle.high,
                'low': candle.low,
                'close': candle.close,
                'volume': candle.volume,
                'history': history
            }

            # 전략 실행
            signal = strategy_func(data, strategy_state)

            if signal:
                self._process_signal(signal, symbol, candle)

        # 잔여 포지션 청산
        if symbol in self.portfolio.positions:
            last_price = candles[-1].close
            pos = self.portfolio.positions[symbol]
            order = self.portfolio.place_order(
                symbol=symbol,
                side=OrderSide.SELL,
                quantity=pos['quantity'],
                timestamp=candles[-1].timestamp
            )
            self.portfolio.execute_order(order, last_price)

        # 결과 계산
        return self._calculate_result(symbol, candles)

    def _process_signal(self, signal: Dict, symbol: str, candle: OHLCV):
        """시그널 처리"""
        signal_type = signal.get('type', 'hold')
        confidence = signal.get('confidence', 0.5)

        # 신뢰도가 낮으면 무시
        if confidence < 0.3:
            return

        # 슬리피지 적용
        execution_price = candle.close * (1 + self.slippage)

        if signal_type == 'buy':
            # 이미 포지션이 있으면 무시
            if symbol in self.portfolio.positions:
                return

            # 포지션 크기 결정 (자본의 95%)
            available = self.portfolio.cash * 0.95
            quantity = available / execution_price

            if quantity > 0:
                order = self.portfolio.place_order(
                    symbol=symbol,
                    side=OrderSide.BUY,
                    quantity=quantity,
                    timestamp=candle.timestamp
                )
                self.portfolio.execute_order(order, execution_price)

        elif signal_type == 'sell':
            if symbol not in self.portfolio.positions:
                return

            pos = self.portfolio.positions[symbol]
            execution_price = candle.close * (1 - self.slippage)

            order = self.portfolio.place_order(
                symbol=symbol,
                side=OrderSide.SELL,
                quantity=pos['quantity'],
                timestamp=candle.timestamp
            )
            self.portfolio.execute_order(order, execution_price)

    def _calculate_result(self, symbol: str, candles: List[OHLCV]) -> BacktestResult:
        """결과 계산"""
        trades = self.portfolio.trades
        equity_curve = [e['equity'] for e in self.portfolio.equity_history]

        if not equity_curve:
            equity_curve = [self.initial_capital]

        # 기본 통계
        final_capital = equity_curve[-1]
        total_trades = len(trades)
        winning_trades = sum(1 for t in trades if t.pnl > 0)
        losing_trades = sum(1 for t in trades if t.pnl <= 0)
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        # 수익 통계
        total_return = (final_capital - self.initial_capital) / self.initial_capital * 100
        trading_days = len(equity_curve)
        annualized_return = total_return * (252 / trading_days) if trading_days > 0 else 0

        gross_profit = sum(t.pnl for t in trades if t.pnl > 0)
        gross_loss = abs(sum(t.pnl for t in trades if t.pnl < 0))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        avg_trade_return = (sum(t.pnl_percent for t in trades) / total_trades) if total_trades > 0 else 0

        # 리스크 통계
        max_drawdown = self._calculate_max_drawdown(equity_curve)
        sharpe_ratio = self._calculate_sharpe(equity_curve)
        sortino_ratio = self._calculate_sortino(equity_curve)
        calmar_ratio = annualized_return / max_drawdown if max_drawdown > 0 else 0

        # 추가 통계
        best_trade = max((t.pnl_percent for t in trades), default=0)
        worst_trade = min((t.pnl_percent for t in trades), default=0)
        cons_wins, cons_losses = self._calculate_consecutive(trades)

        return BacktestResult(
            strategy_name='custom',
            symbol=symbol,
            start_date=candles[0].timestamp if candles else '',
            end_date=candles[-1].timestamp if candles else '',
            initial_capital=self.initial_capital,
            final_capital=round(final_capital, 2),
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=round(win_rate, 2),
            total_return=round(total_return, 2),
            annualized_return=round(annualized_return, 2),
            profit_factor=round(profit_factor, 2),
            avg_trade_return=round(avg_trade_return, 2),
            max_drawdown=round(max_drawdown, 2),
            sharpe_ratio=round(sharpe_ratio, 2),
            sortino_ratio=round(sortino_ratio, 2),
            calmar_ratio=round(calmar_ratio, 2),
            avg_holding_period=0,
            best_trade=round(best_trade, 2),
            worst_trade=round(worst_trade, 2),
            consecutive_wins=cons_wins,
            consecutive_losses=cons_losses,
            trades=[asdict(t) for t in trades[-50:]],  # 최근 50개만
            equity_curve=equity_curve[-100:]  # 최근 100개만
        )

    def _calculate_max_drawdown(self, equity_curve: List[float]) -> float:
        """최대 낙폭 계산"""
        peak = equity_curve[0]
        max_dd = 0

        for value in equity_curve:
            if value > peak:
                peak = value
            dd = (peak - value) / peak * 100
            if dd > max_dd:
                max_dd = dd

        return max_dd

    def _calculate_sharpe(self, equity_curve: List[float], risk_free: float = 0.02) -> float:
        """샤프 비율 계산"""
        if len(equity_curve) < 2:
            return 0

        returns = []
        for i in range(1, len(equity_curve)):
            r = (equity_curve[i] - equity_curve[i - 1]) / equity_curve[i - 1]
            returns.append(r)

        if not returns:
            return 0

        avg_return = sum(returns) / len(returns)
        std_return = math.sqrt(sum((r - avg_return) ** 2 for r in returns) / len(returns))

        if std_return == 0:
            return 0

        return (avg_return - risk_free / 252) / std_return * math.sqrt(252)

    def _calculate_sortino(self, equity_curve: List[float], risk_free: float = 0.02) -> float:
        """소르티노 비율 계산 (하방 변동성만 고려)"""
        if len(equity_curve) < 2:
            return 0

        returns = []
        for i in range(1, len(equity_curve)):
            r = (equity_curve[i] - equity_curve[i - 1]) / equity_curve[i - 1]
            returns.append(r)

        if not returns:
            return 0

        avg_return = sum(returns) / len(returns)

        # 하방 변동성만 계산
        downside_returns = [min(0, r - risk_free / 252) for r in returns]
        downside_deviation = math.sqrt(
            sum(r ** 2 for r in downside_returns) / len(downside_returns)
        )

        if downside_deviation == 0:
            return 0

        return (avg_return - risk_free / 252) / downside_deviation * math.sqrt(252)

    def _calculate_consecutive(self, trades: List[Trade]) -> tuple:
        """연속 승패 계산"""
        if not trades:
            return 0, 0

        max_wins = 0
        max_losses = 0
        current_wins = 0
        current_losses = 0

        for trade in trades:
            if trade.pnl > 0:
                current_wins += 1
                current_losses = 0
                max_wins = max(max_wins, current_wins)
            else:
                current_losses += 1
                current_wins = 0
                max_losses = max(max_losses, current_losses)

        return max_wins, max_losses


# 테스트
if __name__ == '__main__':
    from datetime import timedelta
    import random

    # 테스트 데이터 생성
    test_candles = []
    base_price = 100

    for i in range(200):
        change = random.uniform(-2, 2)
        open_p = base_price
        close_p = base_price + change
        high_p = max(open_p, close_p) + random.uniform(0, 1)
        low_p = min(open_p, close_p) - random.uniform(0, 1)
        volume = random.uniform(1000, 10000)

        test_candles.append(OHLCV(
            timestamp=(datetime.now() - timedelta(hours=200 - i)).isoformat(),
            open=open_p,
            high=high_p,
            low=low_p,
            close=close_p,
            volume=volume
        ))
        base_price = close_p

    # 간단한 테스트 전략
    def simple_strategy(data: Dict, state: Dict) -> Optional[Dict]:
        """단순 RSI 전략"""
        history = data['history']
        closes = [c.close for c in history]

        if len(closes) < 20:
            return None

        # 간단한 모멘텀 계산
        ma5 = sum(closes[-5:]) / 5
        ma20 = sum(closes[-20:]) / 20

        if ma5 > ma20 and not state.get('in_position'):
            state['in_position'] = True
            return {'type': 'buy', 'confidence': 0.7}
        elif ma5 < ma20 and state.get('in_position'):
            state['in_position'] = False
            return {'type': 'sell', 'confidence': 0.7}

        return None

    # 백테스트 실행
    engine = BacktestEngine(initial_capital=10000)
    result = engine.run(test_candles, simple_strategy, 'TEST/USD')

    print("=== 백테스트 결과 ===\n")
    print(f"초기 자본: ${result.initial_capital:,.2f}")
    print(f"최종 자본: ${result.final_capital:,.2f}")
    print(f"총 수익률: {result.total_return:.2f}%")
    print(f"연간 수익률: {result.annualized_return:.2f}%")
    print(f"총 거래: {result.total_trades}회")
    print(f"승률: {result.win_rate:.1f}%")
    print(f"최대 낙폭: {result.max_drawdown:.2f}%")
    print(f"샤프 비율: {result.sharpe_ratio:.2f}")
    print(f"이익인자: {result.profit_factor:.2f}")
