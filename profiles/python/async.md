# Async Programming Rules

## Patterns

| Pattern | When to Use |
|---------|-------------|
| `asyncio.TaskGroup` | Parallel execution (3.11+) |
| `asyncio.Semaphore` | Limit concurrency |
| `asyncio.timeout` | Set timeouts |

## Parallel Execution

```python
# GOOD: Parallel with TaskGroup (3.11+)
async with asyncio.TaskGroup() as tg:
    user_task = tg.create_task(fetch_user())
    posts_task = tg.create_task(fetch_posts())

user = user_task.result()
posts = posts_task.result()
```

## Concurrency Control

```python
async def fetch_all(urls: list[str], limit: int = 10):
    semaphore = asyncio.Semaphore(limit)

    async def fetch_one(url: str):
        async with semaphore:
            return await fetch(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])
```

## Timeouts

```python
async def fetch_with_timeout(url: str):
    async with asyncio.timeout(30):
        return await fetch(url)
```

## Anti-patterns

```python
# BAD: Blocking in async
async def bad():
    time.sleep(1)  # Blocks event loop!

# GOOD: Non-blocking
async def good():
    await asyncio.sleep(1)
```

## Async Generator

```python
async def stream_data() -> AsyncIterator[bytes]:
    async for chunk in source:
        yield process(chunk)
```
