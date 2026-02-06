"""캐시 시스템 테스트."""
import sys
sys.path.insert(0, str(__file__).replace("/tests/test_cache.py", ""))

import pytest
from cache import InferenceCache

class TestInferenceCache:
    """InferenceCache 테스트."""

    def test_set_and_get(self):
        """캐시 저장 및 조회."""
        cache = InferenceCache(max_size=10)
        cache.set("prompt1", "model1", {"temp": 0.7}, "result1")
        result = cache.get("prompt1", "model1", {"temp": 0.7})
        assert result == "result1"

    def test_cache_miss(self):
        """캐시 미스."""
        cache = InferenceCache(max_size=10)
        result = cache.get("nonexistent", "model", {})
        assert result is None

    def test_different_params_different_cache(self):
        """다른 파라미터는 다른 캐시."""
        cache = InferenceCache(max_size=10)
        cache.set("prompt", "model", {"temp": 0.5}, "result_a")
        cache.set("prompt", "model", {"temp": 0.7}, "result_b")

        assert cache.get("prompt", "model", {"temp": 0.5}) == "result_a"
        assert cache.get("prompt", "model", {"temp": 0.7}) == "result_b"

    def test_eviction(self):
        """캐시 사이즈 초과 시 eviction."""
        cache = InferenceCache(max_size=2)
        cache.set("p1", "m", {}, "r1")
        cache.set("p2", "m", {}, "r2")
        cache.set("p3", "m", {}, "r3")

        assert cache.size == 2
        # 가장 오래된 항목이 제거됨
        assert cache.get("p1", "m", {}) is None

    def test_clear(self):
        """캐시 전체 삭제."""
        cache = InferenceCache(max_size=10)
        cache.set("p1", "m", {}, "r1")
        cache.set("p2", "m", {}, "r2")
        cache.clear()
        assert cache.size == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
