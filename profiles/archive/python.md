# Python Language Profile

> **Version**: 1.0.0
> **Target**: Python 3.10+
> **Auto-detect**: Presence of `pyproject.toml`, `requirements.txt`, `setup.py`

---

## Goal

**Primary Outcome**: Generate type-safe and maintainable Python code

**Success Criteria**:
- [ ] Type hints on all functions
- [ ] `mypy --strict` passes
- [ ] Zero `ruff` lint warnings
- [ ] Test coverage 80%+

**Failure Cases**:
- `Any` type overuse → Replace with concrete types
- Bare `except:` → Specify concrete exceptions

---

## Quick Reference

### Required Rules

| Rule | Description | Example |
|------|-------------|---------|
| **Type hints** | All function signatures | `def fn(x: int) -> str:` |
| **f-string** | String formatting | `f"Hello, {name}"` |
| **pathlib** | Path handling | `Path("file.txt")` |
| **dataclass** | Data classes | `@dataclass` |

### Recommended Tools

| Tool | Purpose | Config File |
|------|---------|-------------|
| `ruff` | Lint + Format | `pyproject.toml` |
| `mypy` | Type check | `pyproject.toml` |
| `pytest` | Testing | `pytest.ini` |
| `uv` | Package management | `pyproject.toml` |

---

## Section 1: Type Hint Rules

### Type Hint Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Basic types | Simple values | `int`, `str`, `bool`, `float` |
| Collections | Lists, dicts | `list[int]`, `dict[str, int]` |
| Optional | None possible | `str \| None` (3.10+) |
| Union | Multiple types | `int \| str` |
| TypeVar | Generics | `T = TypeVar('T')` |
| Protocol | Duck typing | `class Readable(Protocol):` |

### Type Hint Patterns

```python
from typing import TypeVar, Protocol
from collections.abc import Callable, Iterable

# GOOD: Basic type hints
def greet(name: str, age: int) -> str:
    return f"Hello, {name}! You are {age}."

# GOOD: Optional (3.10+ syntax)
def find_user(user_id: int) -> User | None:
    return users.get(user_id)

# GOOD: Generics
T = TypeVar('T')

def first(items: list[T]) -> T | None:
    return items[0] if items else None

# GOOD: Protocol (duck typing)
class Readable(Protocol):
    def read(self) -> bytes: ...

def process(source: Readable) -> str:
    return source.read().decode()

# GOOD: Callable
def apply(
    func: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    return func(a, b)
```

### Type Hint Anti-patterns

```python
# BAD: Any overuse
def process(data: Any) -> Any:
    return data

# BAD: No type hints
def calculate(x, y):
    return x + y

# BAD: Old syntax (pre-3.9)
from typing import List, Dict, Optional
def fn(items: List[int]) -> Optional[str]:
    ...

# GOOD: Modern syntax (3.10+)
def fn(items: list[int]) -> str | None:
    ...
```

### Exception Handling

| Situation | Solution |
|-----------|----------|
| External library has no types | `# type: ignore[import]` + create stub |
| Complex type | Use `TypeAlias` |
| Runtime type check needed | `isinstance()` or `pydantic` |

---

## Section 2: Error Handling Rules

### Error Handling Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Specific exception | Expected errors | `except ValueError:` |
| Custom exception | Domain errors | `class UserNotFound(Exception)` |
| Context manager | Resource management | `with open(...) as f:` |
| Result pattern | Functional errors | `returns` library |

### Error Handling Patterns

```python
# GOOD: Specific exception handling
def parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Cannot convert '{value}' to integer") from e

# GOOD: Custom exception hierarchy
class AppError(Exception):
    """Base application exception"""
    pass

class UserNotFoundError(AppError):
    """User not found"""
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"User ID {user_id} not found")

class ValidationError(AppError):
    """Validation failed"""
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"{field}: {message}")

# GOOD: Context manager
from contextlib import contextmanager

@contextmanager
def database_transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# Usage
with database_transaction() as conn:
    conn.execute("INSERT INTO ...")
```

### Error Handling Anti-patterns

```python
# BAD: Bare except
try:
    risky_operation()
except:  # Catches everything (including KeyboardInterrupt)
    pass

# BAD: Ignore exception
try:
    risky_operation()
except Exception:
    pass  # Do nothing

# BAD: Too broad exception
try:
    value = data["key"]
except Exception as e:  # Should only catch KeyError
    handle_error(e)

# BAD: No exception chaining
try:
    process(data)
except ValueError:
    raise RuntimeError("Processing failed")  # Original cause lost
```

---

## Section 3: Class Design Rules

### Class Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `@dataclass` | Data containers | Config, DTO |
| `NamedTuple` | Immutable data | Coordinates, results |
| `Pydantic` | Validation | API input/output |
| `Protocol` | Interface | Duck typing |

### Class Patterns

```python
from dataclasses import dataclass, field
from typing import Self

# GOOD: dataclass
@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: Self) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# GOOD: dataclass with defaults
@dataclass
class Config:
    name: str
    debug: bool = False
    max_retries: int = 3
    tags: list[str] = field(default_factory=list)

# GOOD: Pydantic for validation
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)

    model_config = {"frozen": True}

# GOOD: Protocol
from typing import Protocol

class Repository(Protocol):
    def get(self, id: int) -> Model | None: ...
    def save(self, model: Model) -> None: ...
    def delete(self, id: int) -> bool: ...
```

### Class Anti-patterns

```python
# BAD: Manual __init__, __eq__, __repr__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# GOOD: Use dataclass
@dataclass
class Point:
    x: float
    y: float

# BAD: Mutable default value
class Config:
    def __init__(self, items: list = []):  # All instances share this
        self.items = items
```

---

## Section 4: Function Design Rules

### Function Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Pure function | No state | `def add(a, b): return a + b` |
| Generator | Lazy evaluation | `yield item` |
| Decorator | Cross-cutting concerns | `@cache`, `@retry` |
| Closure | State capture | `def outer(): def inner(): ...` |

### Function Patterns

```python
from functools import cache, wraps
from collections.abc import Iterator
from typing import ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

# GOOD: Cache decorator
@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# GOOD: Generator
def read_large_file(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()

# GOOD: Type-safe decorator
def retry(times: int = 3) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
            raise RuntimeError("Unreachable")
        return wrapper
    return decorator

@retry(times=3)
def fetch_data() -> dict:
    ...
```

### Function Anti-patterns

```python
# BAD: Mutable default argument
def append_to(item, target: list = []):
    target.append(item)
    return target

# GOOD: None default
def append_to(item, target: list | None = None):
    if target is None:
        target = []
    target.append(item)
    return target

# BAD: Too many arguments
def create_user(name, email, age, city, country, phone, ...):
    ...

# GOOD: dataclass or TypedDict
@dataclass
class UserData:
    name: str
    email: str
    age: int
    ...

def create_user(data: UserData) -> User:
    ...
```

---

## Section 5: Async Programming Rules

### Async Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `asyncio` | I/O bound | Network, files |
| `aiohttp` | HTTP client | API calls |
| `asyncpg` | PostgreSQL | Async DB |
| `TaskGroup` | Parallel execution | 3.11+ |

### Async Patterns

```python
import asyncio
from collections.abc import AsyncIterator

# GOOD: Parallel execution (3.11+)
async def fetch_all(urls: list[str]) -> list[Response]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(url)) for url in urls]
    return [t.result() for t in tasks]

# GOOD: Concurrency limit with semaphore
async def fetch_with_limit(urls: list[str], limit: int = 10) -> list[Response]:
    semaphore = asyncio.Semaphore(limit)

    async def fetch_one(url: str) -> Response:
        async with semaphore:
            return await fetch(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])

# GOOD: Async generator
async def stream_data(source: AsyncReader) -> AsyncIterator[bytes]:
    async for chunk in source:
        yield process(chunk)

# GOOD: Timeout
async def fetch_with_timeout(url: str, timeout: float = 30.0) -> Response:
    async with asyncio.timeout(timeout):
        return await fetch(url)
```

### Async Anti-patterns

```python
# BAD: Blocking call
async def bad_example():
    time.sleep(1)  # Blocking!
    # Use await asyncio.sleep(1)

# BAD: Sequential execution
async def fetch_all(urls):
    results = []
    for url in urls:
        results.append(await fetch(url))  # Can parallelize
    return results

# BAD: Nested run_until_complete
asyncio.get_event_loop().run_until_complete(coro())  # deprecated
# Use asyncio.run(coro())
```

---

## Section 6: Testing Rules

### Test Strategy

| Test Type | Tool | Coverage Target |
|-----------|------|-----------------|
| Unit test | pytest | 80% |
| Integration test | pytest | 100% critical paths |
| Type test | mypy | 100% public API |
| Property test | hypothesis | Edge cases |

### Test Patterns

```python
import pytest
from unittest.mock import Mock, patch

# GOOD: Clear test name
def test_parse_valid_json_returns_config():
    json_str = '{"name": "test"}'
    result = parse_config(json_str)
    assert result.name == "test"

# GOOD: Fixture usage
@pytest.fixture
def sample_user() -> User:
    return User(id=1, name="Test", email="test@example.com")

def test_user_greeting(sample_user: User):
    assert sample_user.greeting() == "Hello, Test!"

# GOOD: Parametrize
@pytest.mark.parametrize("input,expected", [
    ("1", 1),
    ("42", 42),
    ("-1", -1),
])
def test_parse_int(input: str, expected: int):
    assert parse_int(input) == expected

# GOOD: Exception test
def test_parse_invalid_raises_error():
    with pytest.raises(ValueError, match="Cannot convert"):
        parse_int("not a number")

# GOOD: Mock usage
def test_fetch_user_calls_api():
    with patch("module.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"id": 1}
        result = fetch_user(1)
        mock_get.assert_called_once_with("/api/users/1")
```

---

## Section 7: Project Structure Rules

### Recommended Structure

```
project/
├── pyproject.toml          # Project config (required)
├── README.md
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── py.typed         # PEP 561 marker
│       ├── core/
│       │   ├── __init__.py
│       │   └── models.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── user.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Shared fixtures
│   ├── unit/
│   └── integration/
└── scripts/
    └── dev.py
```

### pyproject.toml Configuration

```toml
[project]
name = "mypackage"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "mypy", "ruff"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "C4", "SIM"]

[tool.mypy]
strict = true
python_version = "3.10"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"
```

---

## Self-Diagnosis Checklist

### Critical (Must Complete)
- [ ] Type hints on all functions
- [ ] `mypy --strict` passes
- [ ] Zero bare `except:` usage
- [ ] Zero mutable default arguments

### Important (80%+)
- [ ] Zero `ruff` warnings
- [ ] Test coverage 80%+
- [ ] Docstrings written (public API)
- [ ] Using `@dataclass`

### Nice-to-have
- [ ] Property-based tests
- [ ] Async code optimization
- [ ] Written benchmarks

**Pass Criteria**: Critical 100% + Important 80%+

---

## References

| Document | Link |
|----------|------|
| Python Official | https://docs.python.org/3/ |
| PEP 8 | https://peps.python.org/pep-0008/ |
| Mypy | https://mypy.readthedocs.io/ |
| Ruff | https://docs.astral.sh/ruff/ |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Auto-detect: `pyproject.toml`, `requirements.txt`, `setup.py`
