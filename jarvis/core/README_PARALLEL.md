# Parallel Processing Module

asyncio 및 ThreadPoolExecutor 기반 병렬 처리

## API

### run_parallel(tasks)
비동기 태스크 병렬 실행

```python
tasks = [lambda: fetch(url) for url in urls]
results = await run_parallel(tasks)
```

### run_with_timeout(task, timeout)
타임아웃과 함께 실행

```python
result = await run_with_timeout(slow_task, timeout=5)
```

### TaskPool
작업 풀 관리

```python
with TaskPool(max_workers=4) as pool:
    results = pool.map(process_item, items)
```

### parallel_sync(tasks, max_workers)
동기 함수 병렬 실행

```python
tasks = [lambda: compute(i) for i in range(10)]
results = parallel_sync(tasks, max_workers=4)
```

## 테스트

```bash
python3 tests/test_parallel.py
```
