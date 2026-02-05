#!/usr/bin/env python3
"""
가격 캐시 타입 정의
"""

from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class CachedPrice:
    """캐시된 가격 정보"""
    symbol: str
    price: float
    source: str              # 'yahoo', 'binance', 'manual'
    updated_at: datetime
    ttl_seconds: int = 60    # 유효 시간

    @property
    def is_valid(self) -> bool:
        """유효성 검사"""
        return datetime.now() < self.updated_at + timedelta(seconds=self.ttl_seconds)

    @property
    def age_seconds(self) -> float:
        """경과 시간 (초)"""
        return (datetime.now() - self.updated_at).total_seconds()


@dataclass
class CacheStats:
    """캐시 통계"""
    hits: int = 0
    misses: int = 0
    updates: int = 0
    evictions: int = 0
