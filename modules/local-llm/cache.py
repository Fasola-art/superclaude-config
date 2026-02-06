"""추론 결과 캐싱 시스템."""
import hashlib
import json
import time
from pathlib import Path
from typing import Any

# 상대/절대 import 호환
try:
    from .constants import MODULE_DIR
except ImportError:
    from constants import MODULE_DIR

CACHE_DIR = MODULE_DIR / ".cache"
CACHE_TTL_HOURS = 24

class InferenceCache:
    """LRU 기반 추론 결과 캐시."""

    def __init__(self, max_size: int = 1000):
        self._cache: dict[str, tuple[Any, float]] = {}
        self._max_size = max_size
        CACHE_DIR.mkdir(exist_ok=True)

    def _hash_key(self, prompt: str, model: str, params: dict) -> str:
        """프롬프트와 파라미터로 캐시 키 생성."""
        content = json.dumps({"prompt": prompt, "model": model, **params}, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get(self, prompt: str, model: str, params: dict) -> str | None:
        """캐시에서 결과 조회."""
        key = self._hash_key(prompt, model, params)
        if key in self._cache:
            result, timestamp = self._cache[key]
            if time.time() - timestamp < CACHE_TTL_HOURS * 3600:
                return result
            del self._cache[key]
        return None

    def set(self, prompt: str, model: str, params: dict, result: str):
        """결과를 캐시에 저장."""
        if len(self._cache) >= self._max_size:
            self._evict_oldest()
        key = self._hash_key(prompt, model, params)
        self._cache[key] = (result, time.time())

    def _evict_oldest(self):
        """가장 오래된 항목 제거."""
        if self._cache:
            oldest = min(self._cache.items(), key=lambda x: x[1][1])
            del self._cache[oldest[0]]

    def clear(self):
        """캐시 전체 삭제."""
        self._cache.clear()

    @property
    def size(self) -> int:
        return len(self._cache)
