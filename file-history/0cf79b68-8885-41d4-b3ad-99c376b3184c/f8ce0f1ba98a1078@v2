#!/usr/bin/env python3
"""
Trading Module
SuperClaude v2.0.9 트레이딩 모듈

기능:
- 기술적 지표 계산
- 백테스팅
- 알림 시스템
- 전략 관리
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import math

MODULE_DIR = Path.home() / '.claude' / 'modules' / 'trading'
CONFIG_FILE = MODULE_DIR / 'config.json'
STRATEGIES_DIR = MODULE_DIR / 'strategies'
INDICATORS_DIR = MODULE_DIR / 'indicators'
BACKTESTING_DIR = MODULE_DIR / 'backtesting'
ALERTS_DIR = MODULE_DIR / 'alerts'


class TrendDirection(Enum):
    UP = 'up'
    DOWN = 'down'
    SIDEWAYS = 'sideways'


class SignalType(Enum):
    BUY = 'buy'
    SELL = 'sell'
    HOLD = 'hold'


@dataclass
class OHLCV:
    """캔들스틱 데이터"""
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class TradingSignal:
    """트레이딩 시그널"""
    timestamp: str
    symbol: str
    signal_type: SignalType
    price: float
    confidence: float
    strategy: str
    indicators: Dict[str, float]
    reason: str


def load_config() -> Dict:
    """설정 로드"""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {
        'defaultTimeframe': '1h',
        'indicators': {
            'sma': {'periods': [20, 50, 200]},
            'ema': {'periods': [12, 26]},
            'rsi': {'period': 14},
            'macd': {'fast': 12, 'slow': 26, 'signal': 9},
            'bb': {'period': 20, 'std': 2}
        },
        'alerts': {
            'enabled': True,
            'priceThreshold': 0.05,
            'volumeThreshold': 2.0
        }
    }


# ============ 기술적 지표 계산 ============

class Indicators:
    """기술적 지표 계산기"""

    @staticmethod
    def sma(prices: List[float], period: int) -> List[float]:
        """단순 이동평균"""
        if len(prices) < period:
            return []

        result = []
        for i in range(period - 1, len(prices)):
            avg = sum(prices[i - period + 1:i + 1]) / period
            result.append(round(avg, 4))
        return result

    @staticmethod
    def ema(prices: List[float], period: int) -> List[float]:
        """지수 이동평균"""
        if len(prices) < period:
            return []

        multiplier = 2 / (period + 1)
        ema_values = [sum(prices[:period]) / period]

        for price in prices[period:]:
            ema_values.append(
                (price - ema_values[-1]) * multiplier + ema_values[-1]
            )
        return [round(v, 4) for v in ema_values]

    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> List[float]:
        """상대강도지수"""
        if len(prices) < period + 1:
            return []

        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]
            gains.append(max(0, change))
            losses.append(abs(min(0, change)))

        rsi_values = []
        avg_gain = sum(gains[:period]) / period
        avg_loss = sum(losses[:period]) / period

        for i in range(period, len(gains)):
            if avg_loss == 0:
                rsi_values.append(100)
            else:
                rs = avg_gain / avg_loss
                rsi_values.append(round(100 - (100 / (1 + rs)), 2))

            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        return rsi_values

    @staticmethod
    def macd(
        prices: List[float],
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Tuple[List[float], List[float], List[float]]:
        """MACD"""
        if len(prices) < slow:
            return [], [], []

        fast_ema = Indicators.ema(prices, fast)
        slow_ema = Indicators.ema(prices, slow)

        # MACD 라인
        macd_line = []
        offset = slow - fast
        for i in range(len(slow_ema)):
            macd_line.append(round(fast_ema[i + offset] - slow_ema[i], 4))

        # 시그널 라인
        signal_line = Indicators.ema(macd_line, signal)

        # 히스토그램
        histogram = []
        offset = len(macd_line) - len(signal_line)
        for i in range(len(signal_line)):
            histogram.append(round(macd_line[i + offset] - signal_line[i], 4))

        return macd_line, signal_line, histogram

    @staticmethod
    def bollinger_bands(
        prices: List[float],
        period: int = 20,
        std_dev: float = 2.0
    ) -> Tuple[List[float], List[float], List[float]]:
        """볼린저 밴드"""
        if len(prices) < period:
            return [], [], []

        middle = Indicators.sma(prices, period)
        upper = []
        lower = []

        for i in range(len(middle)):
            start_idx = i
            window = prices[start_idx:start_idx + period]
            std = math.sqrt(sum((x - middle[i]) ** 2 for x in window) / period)

            upper.append(round(middle[i] + std_dev * std, 4))
            lower.append(round(middle[i] - std_dev * std, 4))

        return upper, middle, lower

    @staticmethod
    def atr(candles: List[OHLCV], period: int = 14) -> List[float]:
        """Average True Range"""
        if len(candles) < period:
            return []

        tr_values = []
        for i in range(1, len(candles)):
            high_low = candles[i].high - candles[i].low
            high_close = abs(candles[i].high - candles[i - 1].close)
            low_close = abs(candles[i].low - candles[i - 1].close)
            tr_values.append(max(high_low, high_close, low_close))

        # ATR 계산 (EMA 방식)
        atr_values = [sum(tr_values[:period]) / period]
        for tr in tr_values[period:]:
            atr_values.append((atr_values[-1] * (period - 1) + tr) / period)

        return [round(v, 4) for v in atr_values]


# ============ 전략 엔진 ============

class StrategyEngine:
    """전략 실행 엔진"""

    def __init__(self):
        self.config = load_config()
        self.indicators = Indicators()

    def analyze(self, symbol: str, candles: List[OHLCV]) -> TradingSignal:
        """시장 분석 및 시그널 생성"""
        if len(candles) < 50:
            return TradingSignal(
                timestamp=datetime.now().isoformat(),
                symbol=symbol,
                signal_type=SignalType.HOLD,
                price=candles[-1].close if candles else 0,
                confidence=0,
                strategy='insufficient_data',
                indicators={},
                reason='데이터 부족'
            )

        prices = [c.close for c in candles]
        current_price = prices[-1]

        # 지표 계산
        sma20 = self.indicators.sma(prices, 20)
        sma50 = self.indicators.sma(prices, 50)
        rsi = self.indicators.rsi(prices, 14)
        macd_line, signal_line, histogram = self.indicators.macd(prices)
        upper_bb, middle_bb, lower_bb = self.indicators.bollinger_bands(prices)

        # 최근 값들
        indicators = {
            'sma20': sma20[-1] if sma20 else 0,
            'sma50': sma50[-1] if sma50 else 0,
            'rsi': rsi[-1] if rsi else 50,
            'macd': macd_line[-1] if macd_line else 0,
            'macd_signal': signal_line[-1] if signal_line else 0,
            'bb_upper': upper_bb[-1] if upper_bb else 0,
            'bb_lower': lower_bb[-1] if lower_bb else 0
        }

        # 시그널 판단
        signal_type, confidence, reason = self._generate_signal(
            current_price, indicators
        )

        return TradingSignal(
            timestamp=datetime.now().isoformat(),
            symbol=symbol,
            signal_type=signal_type,
            price=current_price,
            confidence=confidence,
            strategy='multi_indicator',
            indicators=indicators,
            reason=reason
        )

    def _generate_signal(
        self,
        price: float,
        indicators: Dict[str, float]
    ) -> Tuple[SignalType, float, str]:
        """시그널 생성 로직"""
        buy_signals = 0
        sell_signals = 0
        reasons = []

        # 골든 크로스 / 데드 크로스
        if indicators['sma20'] > indicators['sma50']:
            buy_signals += 1
            reasons.append('SMA 골든크로스')
        elif indicators['sma20'] < indicators['sma50']:
            sell_signals += 1
            reasons.append('SMA 데드크로스')

        # RSI
        if indicators['rsi'] < 30:
            buy_signals += 2
            reasons.append('RSI 과매도')
        elif indicators['rsi'] > 70:
            sell_signals += 2
            reasons.append('RSI 과매수')

        # MACD
        if indicators['macd'] > indicators['macd_signal']:
            buy_signals += 1
            reasons.append('MACD 상향')
        elif indicators['macd'] < indicators['macd_signal']:
            sell_signals += 1
            reasons.append('MACD 하향')

        # 볼린저 밴드
        if price < indicators['bb_lower']:
            buy_signals += 1
            reasons.append('BB 하단 이탈')
        elif price > indicators['bb_upper']:
            sell_signals += 1
            reasons.append('BB 상단 이탈')

        # 최종 판단
        total = buy_signals + sell_signals
        if buy_signals > sell_signals and buy_signals >= 2:
            confidence = min(buy_signals / total * 100, 95) if total > 0 else 50
            return SignalType.BUY, round(confidence, 1), ' / '.join(reasons)
        elif sell_signals > buy_signals and sell_signals >= 2:
            confidence = min(sell_signals / total * 100, 95) if total > 0 else 50
            return SignalType.SELL, round(confidence, 1), ' / '.join(reasons)
        else:
            return SignalType.HOLD, 50, '혼조세' if reasons else '시그널 없음'


# ============ 백테스팅 ============

@dataclass
class BacktestResult:
    """백테스트 결과"""
    symbol: str
    strategy: str
    period: str
    totalTrades: int
    winRate: float
    profitFactor: float
    totalReturn: float
    maxDrawdown: float
    sharpeRatio: float
    trades: List[Dict]


class Backtester:
    """백테스팅 엔진"""

    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital
        self.engine = StrategyEngine()

    def run(
        self,
        symbol: str,
        candles: List[OHLCV],
        strategy_name: str = 'multi_indicator'
    ) -> BacktestResult:
        """백테스트 실행"""
        capital = self.initial_capital
        position = 0
        entry_price = 0
        trades = []
        equity_curve = [capital]

        for i in range(50, len(candles)):
            window = candles[:i + 1]
            signal = self.engine.analyze(symbol, window)
            current_price = candles[i].close

            # 매수 시그널 (포지션 없을 때)
            if signal.signal_type == SignalType.BUY and position == 0:
                position = capital / current_price
                entry_price = current_price
                trades.append({
                    'type': 'BUY',
                    'price': current_price,
                    'timestamp': candles[i].timestamp,
                    'confidence': signal.confidence
                })

            # 매도 시그널 (포지션 있을 때)
            elif signal.signal_type == SignalType.SELL and position > 0:
                capital = position * current_price
                pnl = (current_price - entry_price) / entry_price * 100
                trades.append({
                    'type': 'SELL',
                    'price': current_price,
                    'timestamp': candles[i].timestamp,
                    'pnl': round(pnl, 2)
                })
                position = 0

            equity_curve.append(capital + (position * current_price if position > 0 else 0))

        # 결과 계산
        win_trades = [t for t in trades if t.get('type') == 'SELL' and t.get('pnl', 0) > 0]
        loss_trades = [t for t in trades if t.get('type') == 'SELL' and t.get('pnl', 0) <= 0]

        total_trades = len([t for t in trades if t.get('type') == 'SELL'])
        win_rate = len(win_trades) / total_trades * 100 if total_trades > 0 else 0

        gross_profit = sum(t.get('pnl', 0) for t in win_trades)
        gross_loss = abs(sum(t.get('pnl', 0) for t in loss_trades))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        total_return = (equity_curve[-1] - self.initial_capital) / self.initial_capital * 100
        max_drawdown = self._calculate_max_drawdown(equity_curve)
        sharpe_ratio = self._calculate_sharpe(equity_curve)

        return BacktestResult(
            symbol=symbol,
            strategy=strategy_name,
            period=f"{candles[0].timestamp} ~ {candles[-1].timestamp}",
            totalTrades=total_trades,
            winRate=round(win_rate, 2),
            profitFactor=round(profit_factor, 2),
            totalReturn=round(total_return, 2),
            maxDrawdown=round(max_drawdown, 2),
            sharpeRatio=round(sharpe_ratio, 2),
            trades=trades[-20:]  # 최근 20개만
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

        avg_return = sum(returns) / len(returns)
        std_return = math.sqrt(sum((r - avg_return) ** 2 for r in returns) / len(returns))

        if std_return == 0:
            return 0

        return (avg_return - risk_free / 252) / std_return * math.sqrt(252)


# ============ 알림 시스템 ============

class AlertManager:
    """알림 관리자"""

    def __init__(self):
        self.config = load_config()
        self.alerts_file = ALERTS_DIR / 'active_alerts.json'
        ALERTS_DIR.mkdir(parents=True, exist_ok=True)

    def load_alerts(self) -> List[Dict]:
        """알림 목록 로드"""
        if self.alerts_file.exists():
            return json.loads(self.alerts_file.read_text())
        return []

    def save_alerts(self, alerts: List[Dict]):
        """알림 목록 저장"""
        self.alerts_file.write_text(json.dumps(alerts, indent=2, ensure_ascii=False))

    def add_alert(
        self,
        symbol: str,
        condition: str,
        target_price: float,
        note: str = ''
    ) -> Dict:
        """알림 추가"""
        alerts = self.load_alerts()

        alert = {
            'id': f"alert_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'symbol': symbol,
            'condition': condition,
            'targetPrice': target_price,
            'note': note,
            'created': datetime.now().isoformat(),
            'triggered': False
        }

        alerts.append(alert)
        self.save_alerts(alerts)
        return alert

    def check_alerts(self, symbol: str, current_price: float) -> List[Dict]:
        """알림 체크"""
        alerts = self.load_alerts()
        triggered = []

        for alert in alerts:
            if alert['symbol'] != symbol or alert['triggered']:
                continue

            condition = alert['condition']
            target = alert['targetPrice']

            should_trigger = False
            if condition == 'above' and current_price >= target:
                should_trigger = True
            elif condition == 'below' and current_price <= target:
                should_trigger = True
            elif condition == 'cross':
                # 교차 조건 (별도 로직 필요)
                pass

            if should_trigger:
                alert['triggered'] = True
                alert['triggeredAt'] = datetime.now().isoformat()
                alert['triggeredPrice'] = current_price
                triggered.append(alert)

        self.save_alerts(alerts)
        return triggered


# ============ 메인 API ============

def analyze_market(symbol: str, candles: List[Dict]) -> Dict:
    """시장 분석 API"""
    ohlcv_candles = [
        OHLCV(
            timestamp=c['timestamp'],
            open=c['open'],
            high=c['high'],
            low=c['low'],
            close=c['close'],
            volume=c['volume']
        )
        for c in candles
    ]

    engine = StrategyEngine()
    signal = engine.analyze(symbol, ohlcv_candles)
    return asdict(signal)


def run_backtest(symbol: str, candles: List[Dict], capital: float = 10000) -> Dict:
    """백테스트 API"""
    ohlcv_candles = [
        OHLCV(
            timestamp=c['timestamp'],
            open=c['open'],
            high=c['high'],
            low=c['low'],
            close=c['close'],
            volume=c['volume']
        )
        for c in candles
    ]

    backtester = Backtester(initial_capital=capital)
    result = backtester.run(symbol, ohlcv_candles)
    return asdict(result)


if __name__ == '__main__':
    # 테스트 데이터로 분석
    import random

    # 더미 데이터 생성
    base_price = 100
    test_candles = []
    for i in range(200):
        change = random.uniform(-2, 2)
        open_p = base_price
        close_p = base_price + change
        high_p = max(open_p, close_p) + random.uniform(0, 1)
        low_p = min(open_p, close_p) - random.uniform(0, 1)
        volume = random.uniform(1000, 10000)

        test_candles.append({
            'timestamp': (datetime.now() - timedelta(hours=200 - i)).isoformat(),
            'open': open_p,
            'high': high_p,
            'low': low_p,
            'close': close_p,
            'volume': volume
        })
        base_price = close_p

    # 분석 실행
    signal = analyze_market('TEST/USD', test_candles)
    print("=== 시장 분석 결과 ===")
    print(json.dumps(signal, indent=2, ensure_ascii=False))

    # 백테스트 실행
    result = run_backtest('TEST/USD', test_candles)
    print("\n=== 백테스트 결과 ===")
    print(json.dumps({k: v for k, v in result.items() if k != 'trades'}, indent=2, ensure_ascii=False))
