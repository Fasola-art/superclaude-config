#!/usr/bin/env python3
"""
Realtime Analysis Module
SuperClaude v2.0.9 실시간 분석 모듈

기능:
- 데이터 스트림 처리
- 실시간 분석
- 대시보드 데이터 생성
- WebSocket 연결 관리
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import deque
import time

MODULE_DIR = Path.home() / '.claude' / 'modules' / 'realtime-analysis'
CONFIG_FILE = MODULE_DIR / 'config.json'
STREAMS_DIR = MODULE_DIR / 'streams'
PROCESSORS_DIR = MODULE_DIR / 'processors'
DASHBOARDS_DIR = MODULE_DIR / 'dashboards'


class StreamStatus(Enum):
    IDLE = 'idle'
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'
    ERROR = 'error'


class DataType(Enum):
    PRICE = 'price'
    VOLUME = 'volume'
    ORDER = 'order'
    TRADE = 'trade'
    NEWS = 'news'
    METRIC = 'metric'


@dataclass
class DataPoint:
    """데이터 포인트"""
    timestamp: str
    type: DataType
    symbol: str
    value: float
    metadata: Dict = field(default_factory=dict)


@dataclass
class StreamConfig:
    """스트림 설정"""
    id: str
    name: str
    source: str
    symbols: List[str]
    dataTypes: List[DataType]
    interval: int  # milliseconds
    enabled: bool


@dataclass
class AnalysisResult:
    """분석 결과"""
    timestamp: str
    symbol: str
    analysisType: str
    value: float
    trend: str
    confidence: float
    alerts: List[str]


def load_config() -> Dict:
    """설정 로드"""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {
        'streams': [],
        'processors': {
            'movingAverage': {'windows': [5, 10, 20]},
            'volatility': {'period': 20},
            'anomaly': {'threshold': 2.0}
        },
        'dashboard': {
            'updateInterval': 1000,
            'maxDataPoints': 1000
        },
        'websocket': {
            'reconnectDelay': 5000,
            'maxReconnectAttempts': 10,
            'pingInterval': 30000
        }
    }


def ensure_dirs():
    """디렉토리 생성"""
    for dir_path in [STREAMS_DIR, PROCESSORS_DIR, DASHBOARDS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)


# ============ 데이터 버퍼 ============

class DataBuffer:
    """시계열 데이터 버퍼"""

    def __init__(self, max_size: int = 10000):
        self.max_size = max_size
        self.data: Dict[str, deque] = {}

    def add(self, symbol: str, point: DataPoint):
        """데이터 추가"""
        if symbol not in self.data:
            self.data[symbol] = deque(maxlen=self.max_size)
        self.data[symbol].append(point)

    def get(self, symbol: str, count: int = None) -> List[DataPoint]:
        """데이터 조회"""
        if symbol not in self.data:
            return []

        data = list(self.data[symbol])
        if count:
            return data[-count:]
        return data

    def get_values(self, symbol: str, count: int = None) -> List[float]:
        """값만 조회"""
        points = self.get(symbol, count)
        return [p.value for p in points]

    def clear(self, symbol: str = None):
        """버퍼 초기화"""
        if symbol:
            if symbol in self.data:
                self.data[symbol].clear()
        else:
            self.data.clear()


# ============ 스트림 프로세서 ============

class StreamProcessor:
    """스트림 데이터 프로세서"""

    def __init__(self):
        self.config = load_config()
        self.buffer = DataBuffer()
        self.callbacks: List[Callable] = []

    def add_callback(self, callback: Callable):
        """콜백 추가"""
        self.callbacks.append(callback)

    def process(self, data: Dict) -> DataPoint:
        """데이터 처리"""
        point = DataPoint(
            timestamp=data.get('timestamp', datetime.now().isoformat()),
            type=DataType(data.get('type', 'price')),
            symbol=data.get('symbol', 'UNKNOWN'),
            value=float(data.get('value', 0)),
            metadata=data.get('metadata', {})
        )

        # 버퍼에 추가
        self.buffer.add(point.symbol, point)

        # 콜백 실행
        for callback in self.callbacks:
            try:
                callback(point)
            except Exception:
                pass

        return point

    def batch_process(self, data_list: List[Dict]) -> List[DataPoint]:
        """배치 처리"""
        return [self.process(d) for d in data_list]


# ============ 실시간 분석 엔진 ============

class RealtimeAnalyzer:
    """실시간 분석 엔진"""

    def __init__(self, processor: StreamProcessor):
        self.processor = processor
        self.config = load_config()

    def moving_average(self, symbol: str, window: int) -> Optional[float]:
        """이동평균 계산"""
        values = self.processor.buffer.get_values(symbol, window)
        if len(values) < window:
            return None
        return round(sum(values) / len(values), 4)

    def volatility(self, symbol: str, period: int = 20) -> Optional[float]:
        """변동성 계산 (표준편차)"""
        values = self.processor.buffer.get_values(symbol, period)
        if len(values) < period:
            return None

        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return round(variance ** 0.5, 4)

    def detect_anomaly(self, symbol: str, threshold: float = 2.0) -> bool:
        """이상치 감지"""
        values = self.processor.buffer.get_values(symbol, 100)
        if len(values) < 20:
            return False

        mean = sum(values[:-1]) / (len(values) - 1)
        std = (sum((v - mean) ** 2 for v in values[:-1]) / (len(values) - 1)) ** 0.5

        if std == 0:
            return False

        current = values[-1]
        z_score = abs(current - mean) / std
        return z_score > threshold

    def detect_trend(self, symbol: str, period: int = 10) -> str:
        """추세 감지"""
        values = self.processor.buffer.get_values(symbol, period)
        if len(values) < period:
            return 'unknown'

        # 선형 회귀 기울기
        n = len(values)
        sum_x = sum(range(n))
        sum_y = sum(values)
        sum_xy = sum(i * v for i, v in enumerate(values))
        sum_x2 = sum(i ** 2 for i in range(n))

        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)

        if slope > 0.01:
            return 'up'
        elif slope < -0.01:
            return 'down'
        else:
            return 'sideways'

    def analyze(self, symbol: str) -> AnalysisResult:
        """종합 분석"""
        alerts = []

        # 이동평균
        ma5 = self.moving_average(symbol, 5)
        ma20 = self.moving_average(symbol, 20)

        # 변동성
        vol = self.volatility(symbol, 20)
        if vol and vol > 0.05:  # 5% 이상 변동성
            alerts.append(f'높은 변동성: {vol * 100:.1f}%')

        # 이상치
        if self.detect_anomaly(symbol):
            alerts.append('가격 이상치 감지')

        # 추세
        trend = self.detect_trend(symbol)

        # 현재 가격
        values = self.processor.buffer.get_values(symbol, 1)
        current = values[-1] if values else 0

        # 신뢰도 계산
        data_count = len(self.processor.buffer.get(symbol))
        confidence = min(data_count / 100, 1.0)

        return AnalysisResult(
            timestamp=datetime.now().isoformat(),
            symbol=symbol,
            analysisType='realtime',
            value=current,
            trend=trend,
            confidence=round(confidence, 2),
            alerts=alerts
        )


# ============ 대시보드 데이터 생성 ============

class DashboardGenerator:
    """대시보드 데이터 생성기"""

    def __init__(self, processor: StreamProcessor, analyzer: RealtimeAnalyzer):
        self.processor = processor
        self.analyzer = analyzer
        self.config = load_config()

    def generate_summary(self, symbols: List[str]) -> Dict:
        """요약 데이터 생성"""
        summaries = {}

        for symbol in symbols:
            analysis = self.analyzer.analyze(symbol)
            values = self.processor.buffer.get_values(symbol, 100)

            if values:
                summaries[symbol] = {
                    'current': values[-1],
                    'high': max(values),
                    'low': min(values),
                    'change': round((values[-1] - values[0]) / values[0] * 100, 2) if values[0] > 0 else 0,
                    'trend': analysis.trend,
                    'alerts': analysis.alerts,
                    'dataPoints': len(values)
                }

        return {
            'timestamp': datetime.now().isoformat(),
            'symbols': summaries,
            'totalAlerts': sum(len(s.get('alerts', [])) for s in summaries.values())
        }

    def generate_chart_data(self, symbol: str, period: int = 100) -> Dict:
        """차트 데이터 생성"""
        points = self.processor.buffer.get(symbol, period)

        return {
            'symbol': symbol,
            'period': period,
            'data': [
                {
                    'timestamp': p.timestamp,
                    'value': p.value
                }
                for p in points
            ],
            'indicators': {
                'ma5': self.analyzer.moving_average(symbol, 5),
                'ma20': self.analyzer.moving_average(symbol, 20),
                'volatility': self.analyzer.volatility(symbol)
            }
        }

    def save_snapshot(self, symbols: List[str]):
        """스냅샷 저장"""
        ensure_dirs()
        snapshot = self.generate_summary(symbols)

        filename = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = DASHBOARDS_DIR / filename

        filepath.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False))
        return filename


# ============ WebSocket 매니저 ============

class WebSocketManager:
    """WebSocket 연결 관리자"""

    def __init__(self):
        self.config = load_config()
        self.connections: Dict[str, Any] = {}
        self.status: Dict[str, StreamStatus] = {}
        self.reconnect_attempts: Dict[str, int] = {}

    async def connect(self, stream_id: str, url: str, on_message: Callable):
        """WebSocket 연결"""
        self.status[stream_id] = StreamStatus.CONNECTING
        self.reconnect_attempts[stream_id] = 0

        try:
            # 실제 WebSocket 연결 (aiohttp 또는 websockets 라이브러리 필요)
            # 여기서는 시뮬레이션
            self.status[stream_id] = StreamStatus.CONNECTED
            self.connections[stream_id] = {
                'url': url,
                'connected_at': datetime.now().isoformat(),
                'message_handler': on_message
            }

            return True

        except Exception as e:
            self.status[stream_id] = StreamStatus.ERROR
            return False

    async def disconnect(self, stream_id: str):
        """연결 해제"""
        if stream_id in self.connections:
            # 실제 연결 해제 로직
            del self.connections[stream_id]
        self.status[stream_id] = StreamStatus.DISCONNECTED

    async def reconnect(self, stream_id: str):
        """재연결"""
        max_attempts = self.config['websocket'].get('maxReconnectAttempts', 10)

        if self.reconnect_attempts.get(stream_id, 0) >= max_attempts:
            self.status[stream_id] = StreamStatus.ERROR
            return False

        self.reconnect_attempts[stream_id] = self.reconnect_attempts.get(stream_id, 0) + 1

        delay = self.config['websocket'].get('reconnectDelay', 5000) / 1000
        await asyncio.sleep(delay)

        if stream_id in self.connections:
            return await self.connect(
                stream_id,
                self.connections[stream_id]['url'],
                self.connections[stream_id]['message_handler']
            )
        return False

    def get_status(self) -> Dict:
        """전체 상태 조회"""
        return {
            'timestamp': datetime.now().isoformat(),
            'connections': {
                stream_id: {
                    'status': self.status.get(stream_id, StreamStatus.IDLE).value,
                    'reconnectAttempts': self.reconnect_attempts.get(stream_id, 0)
                }
                for stream_id in set(list(self.connections.keys()) + list(self.status.keys()))
            }
        }


# ============ 메인 API ============

# 글로벌 인스턴스
_processor = None
_analyzer = None
_dashboard = None


def get_instances():
    """인스턴스 가져오기"""
    global _processor, _analyzer, _dashboard

    if _processor is None:
        _processor = StreamProcessor()
        _analyzer = RealtimeAnalyzer(_processor)
        _dashboard = DashboardGenerator(_processor, _analyzer)

    return _processor, _analyzer, _dashboard


def process_data(data: List[Dict]) -> List[Dict]:
    """데이터 처리 API"""
    processor, _, _ = get_instances()
    points = processor.batch_process(data)
    return [asdict(p) for p in points]


def get_analysis(symbol: str) -> Dict:
    """분석 결과 API"""
    _, analyzer, _ = get_instances()
    result = analyzer.analyze(symbol)
    return asdict(result)


def get_dashboard(symbols: List[str]) -> Dict:
    """대시보드 데이터 API"""
    _, _, dashboard = get_instances()
    return dashboard.generate_summary(symbols)


def get_chart(symbol: str, period: int = 100) -> Dict:
    """차트 데이터 API"""
    _, _, dashboard = get_instances()
    return dashboard.generate_chart_data(symbol, period)


if __name__ == '__main__':
    import random

    # 테스트 데이터 생성 및 처리
    processor, analyzer, dashboard = get_instances()

    symbols = ['BTC/USD', 'ETH/USD', 'AAPL']
    base_prices = {'BTC/USD': 50000, 'ETH/USD': 3000, 'AAPL': 180}

    print("=== 실시간 데이터 시뮬레이션 ===\n")

    for i in range(100):
        for symbol in symbols:
            # 가격 변동 시뮬레이션
            change = random.uniform(-0.02, 0.02)
            base_prices[symbol] *= (1 + change)

            data = {
                'timestamp': datetime.now().isoformat(),
                'type': 'price',
                'symbol': symbol,
                'value': base_prices[symbol]
            }
            processor.process(data)

    # 분석 결과 출력
    print("=== 분석 결과 ===\n")
    for symbol in symbols:
        analysis = get_analysis(symbol)
        print(f"[{symbol}]")
        print(f"  현재가: {analysis['value']:.2f}")
        print(f"  추세: {analysis['trend']}")
        print(f"  신뢰도: {analysis['confidence'] * 100:.0f}%")
        if analysis['alerts']:
            print(f"  알림: {', '.join(analysis['alerts'])}")
        print()

    # 대시보드 요약
    print("=== 대시보드 요약 ===\n")
    summary = get_dashboard(symbols)
    print(f"총 알림: {summary['totalAlerts']}개")
    for symbol, data in summary['symbols'].items():
        print(f"  {symbol}: {data['change']:+.2f}% ({data['trend']})")
