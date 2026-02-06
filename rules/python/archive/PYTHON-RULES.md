# Python Coding Rules (42 Rules)

> **Version**: 2026.01
> **Target**: Python 3.10+
> **Goal**: Type-safe and maintainable code

---

## Priority Summary

| Priority | Category | Rules | Key Effect             |
|----------|----------|-------|------------------------|
| CRITICAL | TYPE     | 6     | Type safety            |
| CRITICAL | ERROR    | 5     | Robust error handling  |
| HIGH     | ASYNC    | 5     | Async optimization     |
| HIGH     | CLASS    | 5     | Class design           |
| MEDIUM   | FUNC     | 6     | Function design        |
| MEDIUM   | IMPORT   | 5     | Import organization    |
| LOW      | PERF     | 5     | Performance optimization |
| LOW      | TEST     | 5     | Test patterns          |

---

## CRITICAL: TYPE (Type Hints)

### TYPE-001: Type Hints on All Functions

```python
# BAD
def process(data):
    return data.upper()

# GOOD
def process(data: str) -> str:
    return data.upper()
```

### TYPE-002: Use Modern Syntax (3.10+)

```python
# BAD (pre-3.9)
from typing import List, Dict, Optional
def fn(items: List[int]) -> Optional[str]:
    pass

# GOOD (3.10+)
def fn(items: list[int]) -> str | None:
    pass
```

### TYPE-003: TypeVar for Generics

```python
from typing import TypeVar

T = TypeVar('T')

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

### TYPE-004: Protocol for Duck Typing

```python
from typing import Protocol

class Readable(Protocol):
    def read(self) -> bytes: ...

def process(source: Readable) -> str:
    return source.read().decode()
```

### TYPE-005: TypedDict for Dictionary Types

```python
from typing import TypedDict

class UserDict(TypedDict):
    id: int
    name: str
    email: str | None

def get_user() -> UserDict:
    return {"id": 1, "name": "test", "email": None}
```

### TYPE-006: Never Use Any

```python
# BAD
def process(data: Any) -> Any:
    pass

# GOOD
def process(data: dict[str, int]) -> list[str]:
    pass
```

---

## CRITICAL: ERROR (Error Handling)

### ERROR-001: Catch Specific Exceptions

```python
# BAD
try:
    risky()
except:  # bare except
    pass

# BAD
except Exception:  # Too broad
    pass

# GOOD
except ValueError as e:
    logger.error(f"Value error: {e}")
    raise
```

### ERROR-002: Exception Chaining

```python
# BAD
except ValueError:
    raise RuntimeError("Processing failed")  # Original cause lost

# GOOD
except ValueError as e:
    raise RuntimeError("Processing failed") from e
```

### ERROR-003: Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base exception"""
    pass

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} not found: {id}")
```

### ERROR-004: Context Managers

```python
from contextlib import contextmanager

@contextmanager
def transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

### ERROR-005: Error Logging

```python
import logging

logger = logging.getLogger(__name__)

try:
    process()
except ValueError as e:
    logger.exception("Processing failed")  # Includes stack trace
    raise
```

---

## HIGH: ASYNC (Async)

### ASYNC-001: Parallel Execution (TaskGroup)

```python
# BAD: Sequential execution
user = await fetch_user()
posts = await fetch_posts()

# GOOD: Parallel execution (3.11+)
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
# BAD
async def bad():
    time.sleep(1)  # Blocking!

# GOOD
async def good():
    await asyncio.sleep(1)
```

### ASYNC-005: Async Generators

```python
async def stream_data() -> AsyncIterator[bytes]:
    async for chunk in source:
        yield process(chunk)
```

---

## HIGH: CLASS (Class Design)

### CLASS-001: Use dataclass

```python
# BAD
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# GOOD
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

### CLASS-005: No Mutable Default Arguments

```python
# BAD
def fn(items: list = []):  # Shared!
    items.append(1)

# GOOD
def fn(items: list | None = None):
    if items is None:
        items = []
    items.append(1)
```

---

## MEDIUM: FUNC (Function Design)

### FUNC-001: Single Responsibility

```python
# BAD: Too many responsibilities
def process_user(data):
    validate(data)
    transform(data)
    save(data)
    send_email(data)

# GOOD: Separated
def validate_user(data): ...
def transform_user(data): ...
def save_user(data): ...
```

### FUNC-002: Clear Parameters

```python
# BAD
def create(n, e, a, c, co, p):
    pass

# GOOD
@dataclass
class UserData:
    name: str
    email: str
    age: int

def create_user(data: UserData) -> User:
    pass
```

### FUNC-003: Use Decorators

```python
from functools import cache, wraps

@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### FUNC-004: Use Generators

```python
def read_large_file(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()
```

### FUNC-005: Early Return

```python
# BAD
def process(data):
    if data:
        if data.valid:
            return do_something(data)
        else:
            return None
    else:
        return None

# GOOD
def process(data):
    if not data:
        return None
    if not data.valid:
        return None
    return do_something(data)
```

### FUNC-006: Prefer Pure Functions

```python
# BAD: Side effects
def add_item(items: list, item):
    items.append(item)  # Mutates original

# GOOD: Pure function
def add_item(items: list, item) -> list:
    return [*items, item]
```

---

## MEDIUM: IMPORT (Import Rules)

### IMPORT-001: Prefer Absolute Imports

```python
# GOOD
from mypackage.utils import helper

# Conditional
from .utils import helper  # Only within package
```

### IMPORT-002: Import Order

```python
# 1. Standard library
import os
import sys
from pathlib import Path

# 2. Third-party
import httpx
from pydantic import BaseModel

# 3. Local
from mypackage import utils
from mypackage.models import User
```

### IMPORT-003: Explicit Imports

```python
# BAD
from os import *

# GOOD
from os import path, environ
```

### IMPORT-004: Type-Only Imports

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from heavy_module import HeavyClass

def fn(obj: "HeavyClass") -> None:
    pass
```

### IMPORT-005: Lazy Import

```python
def process():
    import heavy_module  # Load only when needed
    return heavy_module.do_something()
```

---

## LOW: PERF (Performance)

### PERF-001: List Comprehension

```python
# BAD
result = []
for x in items:
    if x > 0:
        result.append(x * 2)

# GOOD
result = [x * 2 for x in items if x > 0]
```

### PERF-002: Generator Expression

```python
# Memory efficient
total = sum(x * 2 for x in large_list)
```

### PERF-003: String Joining

```python
# BAD
result = ""
for s in strings:
    result += s

# GOOD
result = "".join(strings)
```

### PERF-004: Dictionary get()

```python
# BAD
if key in d:
    value = d[key]
else:
    value = default

# GOOD
value = d.get(key, default)
```

### PERF-005: Use slots

```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
```

---

## LOW: TEST (Testing)

### TEST-001: Use pytest

```python
def test_add():
    assert add(1, 2) == 3
```

### TEST-002: Use Fixtures

```python
@pytest.fixture
def sample_user() -> User:
    return User(id=1, name="test")

def test_greeting(sample_user: User):
    assert sample_user.greeting() == "Hello, test!"
```

### TEST-003: Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    ("1", 1),
    ("42", 42),
    ("-1", -1),
])
def test_parse_int(input: str, expected: int):
    assert parse_int(input) == expected
```

### TEST-004: Test Exceptions

```python
def test_invalid_input():
    with pytest.raises(ValueError, match="cannot convert"):
        parse_int("invalid")
```

### TEST-005: Use Mocks

```python
from unittest.mock import patch

def test_fetch_calls_api():
    with patch("module.requests.get") as mock:
        mock.return_value.json.return_value = {"id": 1}
        result = fetch_user(1)
        mock.assert_called_once()
```

---

## Checklist

### New Project Setup
- [ ] Configure pyproject.toml
- [ ] Enable mypy strict mode
- [ ] Configure ruff
- [ ] Configure pytest

### Code Review
- [ ] Type hint completeness
- [ ] Exception handling appropriateness
- [ ] Async parallelization
- [ ] Test coverage

---

**META**
- Version: 2026.01
- Last Updated: 2026-01-30
