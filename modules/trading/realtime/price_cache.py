#!/usr/bin/env python3
"""
가격 캐시 관리
TTL 기반 가격 데이터 캐싱 및 조회
"""

import threading
from datetime import datetime
from typing import Dict, Optional, List
import logging

from .cache_types import CachedPrice, CacheStats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PriceCache:
    """
    가격 캐시

    사용법:
        cache = PriceCache(default_ttl=30)
        cache.set('AAPL', 185.50, source='yahoo')
        price = cache.get('AAPL')
    """

    def __init__(self, default_ttl: int = 60, max_size: int = 1000):
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._cache: Dict[str, CachedPrice] = {}
        self._lock = threading.RLock()
        self._stats = CacheStats()

    def set(self, symbol: str, price: float, source: str = 'unknown',
            ttl: Optional[int] = None) -> None:
        """가격 설정"""
        with self._lock:
            if len(self._cache) >= self.max_size:
                self._evict_oldest()
            self._cache[symbol.upper()] = CachedPrice(
                symbol=symbol.upper(), price=price, source=source,
                updated_at=datetime.now(), ttl_seconds=ttl or self.default_ttl
            )
            self._stats.updates += 1

    def get(self, symbol: str, default: Optional[float] = None) -> Optional[float]:
        """가격 조회"""
        with self._lock:
            cached = self._cache.get(symbol.upper())
            if cached and cached.is_valid:
                self._stats.hits += 1
                return cached.price
            self._stats.misses += 1
            return default

    def get_with_info(self, symbol: str) -> Optional[CachedPrice]:
        """캐시 정보와 함께 조회"""
        with self._lock:
            cached = self._cache.get(symbol.upper())
            if cached and cached.is_valid:
                self._stats.hits += 1
                return cached
            self._stats.misses += 1
            return None

    def get_many(self, symbols: List[str]) -> Dict[str, float]:
        """다중 심볼 조회"""
        return {s.upper(): p for s in symbols if (p := self.get(s)) is not None}

    def invalidate(self, symbol: str) -> bool:
        """캐시 무효화"""
        with self._lock:
            if symbol.upper() in self._cache:
                del self._cache[symbol.upper()]
                return True
            return False

    def clear(self) -> int:
        """전체 캐시 클리어"""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count

    def cleanup_expired(self) -> int:
        """만료된 항목 정리"""
        with self._lock:
            expired = [k for k, v in self._cache.items() if not v.is_valid]
            for key in expired:
                del self._cache[key]
                self._stats.evictions += 1
            return len(expired)

    def _evict_oldest(self):
        """가장 오래된 항목 제거"""
        if not self._cache:
            return
        oldest = min(self._cache.keys(), key=lambda k: self._cache[k].updated_at)
        del self._cache[oldest]
        self._stats.evictions += 1

    @property
    def size(self) -> int:
        return len(self._cache)

    @property
    def stats(self) -> Dict:
        total = self._stats.hits + self._stats.misses
        hit_rate = (self._stats.hits / total * 100) if total > 0 else 0
        return {
            'size': self.size, 'hits': self._stats.hits,
            'misses': self._stats.misses, 'hit_rate': f"{hit_rate:.1f}%",
            'updates': self._stats.updates, 'evictions': self._stats.evictions
        }

    def list_all(self) -> List[Dict]:
        """전체 캐시 목록"""
        with self._lock:
            return [{
                'symbol': v.symbol, 'price': v.price, 'source': v.source,
                'age_seconds': round(v.age_seconds, 1), 'valid': v.is_valid
            } for v in self._cache.values()]


# 글로벌 인스턴스
_global_cache: Optional[PriceCache] = None


def get_global_cache() -> PriceCache:
    """글로벌 캐시 인스턴스"""
    global _global_cache
    if _global_cache is None:
        _global_cache = PriceCache()
    return _global_cache
