# Python High Priority Rules (ASYNC + CLASS)

## ASYNC: Async Patterns

### ASYNC-001: Parallel Execution (TaskGroup)
```python
# BAD: Sequential
user = await fetch_user()
posts = await fetch_posts()

# GOOD: Parallel (3.11+)
async with asyncio.TaskGroup() as tg:
    user_task = tg.create_task(fetch_user())
    posts_task = tg.create_task(fetch_posts())
user = user_task.result()
posts = posts_task.result()
```

### ASYNC-002: Limit Concurrency
```python
async def fetch_all(urls: list[str], limit: int = 10):
    semaphore = asyncio.Semaphore(limit)
    async def fetch_one(url: str):
        async with semaphore:
            return await fetch(url)
    return await asyncio.gather(*[fetch_one(url) for url in urls])
```

### ASYNC-003: Timeouts
```python
async def fetch_with_timeout(url: str):
    async with asyncio.timeout(30):
        return await fetch(url)
```

### ASYNC-004: Never Block
```python
# BAD: time.sleep(1)
# GOOD: await asyncio.sleep(1)
```

### ASYNC-005: Async Generators
```python
async def stream_data() -> AsyncIterator[bytes]:
    async for chunk in source:
        yield process(chunk)
```

---

## CLASS: Class Design

### CLASS-001: Use dataclass
```python
@dataclass
class Point:
    x: float
    y: float
```

### CLASS-002: Immutable dataclass
```python
@dataclass(frozen=True, slots=True)
class Config:
    name: str
    value: int
```

### CLASS-003: Pydantic for Validation
```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)
    model_config = {"frozen": True}
```

### CLASS-004: Protocol for Interfaces
```python
class Repository(Protocol):
    def get(self, id: int) -> Model | None: ...
    def save(self, model: Model) -> None: ...
```

### CLASS-005: No Mutable Defaults
```python
# BAD: def fn(items: list = []):
# GOOD
def fn(items: list | None = None):
    if items is None:
        items = []
```
