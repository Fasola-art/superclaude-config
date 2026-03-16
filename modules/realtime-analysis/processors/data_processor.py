#!/usr/bin/env python3
"""
실시간 데이터 프로세서
스트림 데이터 처리 및 분석

기능:
- 데이터 집계 (OHLCV 생성)
- 실시간 지표 계산
- 이상치 감지
- 알림 트리거
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from collections import deque
import math
import threading


MODULE_DIR = Path(__file__).parent.parent


@dataclass
class OHLCV:
    """캔들스틱 데이터"""
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    trades: int = 0


@dataclass
class TickData:
    """틱 데이터"""
    timestamp: str
    symbol: str
    price: float
    volume: float
    side: Optional[str] = None


@dataclass
class AggregatedData:
    """집계된 데이터"""
    symbol: str
    timeframe: str               # 1m, 5m, 15m, 1h 등
    current_candle: OHLCV
    completed_candles: List[OHLCV]
    tick_count: int
    total_volume: float


class TickBuffer:
    """틱 데이터 버퍼"""

    def __init__(self, max_size: int = 10000):
        """초기화"""
        self.max_size = max_size
        self.data: Dict[str, deque] = {}  # symbol -> ticks
        self._lock = threading.Lock()

    def add(self, tick: TickData):
        """틱 추가"""
        with self._lock:
            if tick.symbol not in self.data:
                self.data[tick.symbol] = deque(maxlen=self.max_size)
            self.data[tick.symbol].append(tick)

    def get(self, symbol: str, count: int = None) -> List[TickData]:
        """틱 조회"""
        with self._lock:
            if symbol not in self.data:
                return []
            ticks = list(self.data[symbol])
            return ticks[-count:] if count else ticks

    def get_prices(self, symbol: str, count: int = None) -> List[float]:
        """가격만 조회"""
        ticks = self.get(symbol, count)
        return [t.price for t in ticks]

    def clear(self, symbol: str = None):
        """버퍼 초기화"""
        with self._lock:
            if symbol:
                if symbol in self.data:
                    self.data[symbol].clear()
            else:
                self.data.clear()


class CandleAggregator:
    """캔들 집계기"""

    TIMEFRAME_SECONDS = {
        '1m': 60,
        '5m': 300,
        '15m': 900,
        '30m': 1800,
        '1h': 3600,
        '4h': 14400,
        '1d': 86400
    }

    def __init__(self, timeframe: str = '1m', max_candles: int = 1000):
        """
        초기화

        Args:
            timeframe: 타임프레임
            max_candles: 최대 캔들 수
        """
        self.timeframe = timeframe
        self.interval = self.TIMEFRAME_SECONDS.get(timeframe, 60)
        self.max_candles = max_candles

        self.candles: Dict[str, deque] = {}           # symbol -> candles
        self.current: Dict[str, OHLCV] = {}           # symbol -> current candle
        self.candle_start: Dict[str, datetime] = {}   # symbol -> candle start time
        self._lock = threading.Lock()

    def _get_candle_start(self, timestamp: datetime) -> datetime:
        """캔들 시작 시간 계산"""
        ts = timestamp.timestamp()
        aligned = int(ts // self.interval) * self.interval
        return datetime.fromtimestamp(aligned)

    def add_tick(self, symbol: str, price: float, volume: float, timestamp: datetime = None) -> Optional[OHLCV]:
        """
        틱 추가

        Args:
            symbol: 심볼
            price: 가격
            volume: 거래량
            timestamp: 시간

        Returns:
            완성된 캔들이 있으면 반환
        """
        if timestamp is None:
            timestamp = datetime.now()

        candle_start = self._get_candle_start(timestamp)
        completed = None

        with self._lock:
            if symbol not in self.candles:
                self.candles[symbol] = deque(maxlen=self.max_candles)

            # 새 캔들 시작
            if symbol not in self.current or self.candle_start.get(symbol) != candle_start:
                # 기존 캔들 완성
                if symbol in self.current:
                    completed = self.current[symbol]
                    self.candles[symbol].append(completed)

                # 새 캔들 생성
                self.current[symbol] = OHLCV(
                    timestamp=candle_start.isoformat(),
                    open=price,
                    high=price,
                    low=price,
                    close=price,
                    volume=volume,
                    trades=1
                )
                self.candle_start[symbol] = candle_start

            else:
                # 기존 캔들 업데이트
                candle = self.current[symbol]
                candle.high = max(candle.high, price)
                candle.low = min(candle.low, price)
                candle.close = price
                candle.volume += volume
                candle.trades += 1

        return completed

    def get_candles(self, symbol: str, count: int = None) -> List[OHLCV]:
        """캔들 조회"""
        with self._lock:
            if symbol not in self.candles:
                return []
            candles = list(self.candles[symbol])
            return candles[-count:] if count else candles

    def get_current(self, symbol: str) -> Optional[OHLCV]:
        """현재 캔들 조회"""
        with self._lock:
            return self.current.get(symbol)


class RealtimeIndicators:
    """실시간 지표 계산기"""

    @staticmethod
    def sma(prices: List[float], period: int) -> Optional[float]:
        """단순 이동평균"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period

    @staticmethod
    def ema(prices: List[float], period: int, prev_ema: float = None) -> Optional[float]:
        """지수 이동평균"""
        if len(prices) < 1:
            return None

        if prev_ema is None:
            if len(prices) < period:
                return None
            return sum(prices[:period]) / period

        multiplier = 2 / (period + 1)
        return (prices[-1] - prev_ema) * multiplier + prev_ema

    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> Optional[float]:
        """상대강도지수"""
        if len(prices) < period + 1:
            return None

        gains = []
        losses = []

        for i in range(len(prices) - period, len(prices)):
            change = prices[i] - prices[i - 1]
            gains.append(max(0, change))
            losses.append(abs(min(0, change)))

        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def volatility(prices: List[float], period: int = 20) -> Optional[float]:
        """변동성 (표준편차)"""
        if len(prices) < period:
            return None

        recent = prices[-period:]
        mean = sum(recent) / period
        variance = sum((p - mean) ** 2 for p in recent) / period
        return math.sqrt(variance)

    @staticmethod
    def momentum(prices: List[float], period: int = 10) -> Optional[float]:
        """모멘텀"""
        if len(prices) < period + 1:
            return None
        return prices[-1] - prices[-period - 1]

    @staticmethod
    def vwap(prices: List[float], volumes: List[float]) -> Optional[float]:
        """거래량 가중 평균 가격"""
        if not prices or not volumes or len(prices) != len(volumes):
            return None

        total_volume = sum(volumes)
        if total_volume == 0:
            return None

        return sum(p * v for p, v in zip(prices, volumes)) / total_volume


class AnomalyDetector:
    """이상치 감지기"""

    def __init__(self, z_threshold: float = 3.0, lookback: int = 100):
        """
        초기화

        Args:
            z_threshold: Z-Score 임계값
            lookback: 참조 기간
        """
        self.z_threshold = z_threshold
        self.lookback = lookback

    def detect(self, prices: List[float]) -> Dict:
        """
        이상치 감지

        Args:
            prices: 가격 리스트

        Returns:
            감지 결과
        """
        if len(prices) < self.lookback:
            return {'detected': False, 'reason': '데이터 부족'}

        reference = prices[-self.lookback:-1]
        current = prices[-1]

        mean = sum(reference) / len(reference)
        variance = sum((p - mean) ** 2 for p in reference) / len(reference)
        std = math.sqrt(variance)

        if std == 0:
            return {'detected': False, 'z_score': 0}

        z_score = abs(current - mean) / std

        return {
            'detected': z_score > self.z_threshold,
            'z_score': round(z_score, 2),
            'current': current,
            'mean': round(mean, 4),
            'std': round(std, 4),
            'deviation': round((current - mean) / mean * 100, 2)
        }


class DataProcessor:
    """통합 데이터 프로세서"""

    def __init__(self, timeframe: str = '1m'):
        """초기화"""
        self.tick_buffer = TickBuffer()
        self.aggregator = CandleAggregator(timeframe)
        self.indicators = RealtimeIndicators()
        self.anomaly_detector = AnomalyDetector()

        self.ema_cache: Dict[str, Dict[int, float]] = {}  # symbol -> {period: ema}
        self.callbacks: List[Callable] = []

    def add_callback(self, callback: Callable):
        """콜백 추가"""
        self.callbacks.append(callback)

    def _dispatch_event(self, event_type: str, data: Dict):
        """이벤트 전달"""
        event = {
            'type': event_type,
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception:
                pass

    def process_tick(self, symbol: str, price: float, volume: float = 0) -> Dict:
        """
        틱 데이터 처리

        Args:
            symbol: 심볼
            price: 가격
            volume: 거래량

        Returns:
            처리 결과
        """
        timestamp = datetime.now()

        # 틱 버퍼에 추가
        tick = TickData(
            timestamp=timestamp.isoformat(),
            symbol=symbol,
            price=price,
            volume=volume
        )
        self.tick_buffer.add(tick)

        # 캔들 집계
        completed_candle = self.aggregator.add_tick(symbol, price, volume, timestamp)
        if completed_candle:
            self._dispatch_event('candle_completed', {
                'symbol': symbol,
                'candle': completed_candle.__dict__
            })

        # 지표 계산
        prices = self.tick_buffer.get_prices(symbol, 200)
        indicators = self._calculate_indicators(symbol, prices)

        # 이상치 감지
        anomaly = self.anomaly_detector.detect(prices)
        if anomaly['detected']:
            self._dispatch_event('anomaly_detected', {
                'symbol': symbol,
                'anomaly': anomaly
            })

        return {
            'symbol': symbol,
            'price': price,
            'volume': volume,
            'timestamp': timestamp.isoformat(),
            'indicators': indicators,
            'anomaly': anomaly,
            'current_candle': self.aggregator.get_current(symbol).__dict__ if self.aggregator.get_current(symbol) else None
        }

    def _calculate_indicators(self, symbol: str, prices: List[float]) -> Dict:
        """지표 계산"""
        if not prices:
            return {}

        # EMA 캐시 초기화
        if symbol not in self.ema_cache:
            self.ema_cache[symbol] = {}

        indicators = {}

        # SMA
        indicators['sma_20'] = self.indicators.sma(prices, 20)
        indicators['sma_50'] = self.indicators.sma(prices, 50)

        # EMA (캐시 사용)
        for period in [12, 26]:
            prev_ema = self.ema_cache[symbol].get(period)
            new_ema = self.indicators.ema(prices, period, prev_ema)
            if new_ema:
                self.ema_cache[symbol][period] = new_ema
                indicators[f'ema_{period}'] = round(new_ema, 4)

        # RSI
        rsi = self.indicators.rsi(prices, 14)
        if rsi:
            indicators['rsi_14'] = round(rsi, 2)

        # 변동성
        vol = self.indicators.volatility(prices, 20)
        if vol:
            indicators['volatility_20'] = round(vol, 4)

        # 모멘텀
        mom = self.indicators.momentum(prices, 10)
        if mom:
            indicators['momentum_10'] = round(mom, 4)

        return indicators

    def get_summary(self, symbol: str) -> Dict:
        """요약 정보 조회"""
        prices = self.tick_buffer.get_prices(symbol, 1000)
        candles = self.aggregator.get_candles(symbol, 100)
        current = self.aggregator.get_current(symbol)

        if not prices:
            return {'symbol': symbol, 'status': 'no_data'}

        return {
            'symbol': symbol,
            'current_price': prices[-1],
            'price_change': round(prices[-1] - prices[0], 4) if len(prices) > 1 else 0,
            'price_change_percent': round((prices[-1] - prices[0]) / prices[0] * 100, 2) if len(prices) > 1 and prices[0] > 0 else 0,
            'high': max(prices),
            'low': min(prices),
            'tick_count': len(prices),
            'candle_count': len(candles),
            'current_candle': current.__dict__ if current else None,
            'indicators': self._calculate_indicators(symbol, prices),
            'last_update': datetime.now().isoformat()
        }


# 테스트
if __name__ == '__main__':
    import random

    processor = DataProcessor(timeframe='1m')

    # 이벤트 콜백
    def on_event(event):
        print(f"[이벤트] {event['type']}: {event['data'].get('symbol', 'N/A')}")

    processor.add_callback(on_event)

    print("=== 데이터 프로세서 테스트 ===\n")

    # 시뮬레이션
    symbol = 'BTC/USDT'
    base_price = 50000

    print("틱 데이터 시뮬레이션 (100개)...")
    for i in range(100):
        # 가격 변동
        change = random.uniform(-50, 50)
        price = base_price + change
        volume = random.uniform(0.1, 10)

        result = processor.process_tick(symbol, price, volume)
        base_price = price

    # 요약 조회
    summary = processor.get_summary(symbol)

    print(f"\n=== {symbol} 요약 ===")
    print(f"현재 가격: ${summary['current_price']:,.2f}")
    print(f"변동률: {summary['price_change_percent']:.2f}%")
    print(f"고가: ${summary['high']:,.2f}")
    print(f"저가: ${summary['low']:,.2f}")
    print(f"틱 수: {summary['tick_count']}")

    print(f"\n지표:")
    for key, value in summary['indicators'].items():
        if value is not None:
            print(f"  {key}: {value}")
