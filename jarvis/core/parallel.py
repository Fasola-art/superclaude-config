#!/usr/bin/env python3
"""병렬 처리 유틸리티"""

import asyncio
from typing import List, Callable, Any, Optional, TypeVar
from concurrent.futures import ThreadPoolExecutor, as_completed

T = TypeVar('T')


async def run_parallel(tasks: List[Callable[[], T]]) -> List[T]:
    """비동기 태스크 병렬 실행"""
    return await asyncio.gather(*[asyncio.create_task(asyncio.to_thread(task)) for task in tasks])


async def run_with_timeout(task: Callable[[], T], timeout: int) -> Optional[T]:
    """타임아웃과 함께 태스크 실행"""
    try:
        return await asyncio.wait_for(asyncio.to_thread(task), timeout=timeout)
    except asyncio.TimeoutError:
        print(f"Task timeout after {timeout}s")
        return None


class TaskPool:
    """작업 풀 관리"""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, fn: Callable, *args, **kwargs) -> Any:
        """작업 제출"""
        return self.executor.submit(fn, *args, **kwargs)

    def map(self, fn: Callable, items: List[Any]) -> List[Any]:
        """여러 항목에 함수 매핑"""
        futures = [self.submit(fn, item) for item in items]
        return [f.result() for f in as_completed(futures)]

    def shutdown(self, wait: bool = True):
        """풀 종료"""
        self.executor.shutdown(wait=wait)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()


async def parallel_async(coroutines: List) -> List[Any]:
    """코루틴 병렬 실행"""
    return await asyncio.gather(*coroutines)


def parallel_sync(tasks: List[Callable], max_workers: int = 4) -> List[Any]:
    """동기 함수 병렬 실행"""
    with TaskPool(max_workers=max_workers) as pool:
        return pool.map(lambda t: t(), tasks)
