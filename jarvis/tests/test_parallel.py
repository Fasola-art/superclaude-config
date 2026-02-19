#!/usr/bin/env python3
"""병렬 처리 테스트"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import time
import pytest
from jarvis.core.parallel import run_parallel, run_with_timeout, TaskPool, parallel_sync


def slow_task(n: int) -> int:
    """지연 태스크"""
    time.sleep(0.1)
    return n * 2


def test_task_pool():
    """TaskPool 테스트"""
    with TaskPool(max_workers=4) as pool:
        items = list(range(10))
        results = pool.map(slow_task, items)
        expected = sorted([i * 2 for i in items])
        assert sorted(results) == expected
    print("✅ TaskPool test passed")


@pytest.mark.asyncio
async def test_run_parallel():
    """병렬 실행 테스트"""
    tasks = [lambda: slow_task(i) for i in range(5)]
    results = await run_parallel(tasks)
    assert len(results) == 5
    print("✅ run_parallel test passed")


@pytest.mark.asyncio
async def test_timeout():
    """타임아웃 테스트"""
    def long_task():
        time.sleep(2)
        return "done"

    result = await run_with_timeout(long_task, timeout=1)
    assert result is None  # 타임아웃 발생
    print("✅ timeout test passed")


def test_parallel_sync():
    """동기 병렬 실행 테스트"""
    tasks = [lambda: slow_task(i) for i in range(5)]
    results = parallel_sync(tasks, max_workers=4)
    assert len(results) == 5
    print("✅ parallel_sync test passed")


if __name__ == "__main__":
    test_task_pool()
    test_parallel_sync()

    asyncio.run(test_run_parallel())
    asyncio.run(test_timeout())

    print("\n🎉 All parallel tests passed!")
