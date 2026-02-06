# Type Hint Rules

## Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| Basic types | Simple values | `int`, `str`, `bool` |
| Collections | Lists, dicts | `list[int]`, `dict[str, int]` |
| Optional | None possible | `str \| None` (3.10+) |
| Union | Multiple types | `int \| str` |
| TypeVar | Generics | `T = TypeVar('T')` |
| Protocol | Duck typing | `class Readable(Protocol):` |

## Good Patterns

```python
from typing import TypeVar, Protocol
from collections.abc import Callable

# Basic type hints
def greet(name: str, age: int) -> str:
    return f"Hello, {name}! You are {age}."

# Optional (3.10+)
def find_user(user_id: int) -> User | None:
    return users.get(user_id)

# Generics
T = TypeVar('T')
def first(items: list[T]) -> T | None:
    return items[0] if items else None

# Protocol (duck typing)
class Readable(Protocol):
    def read(self) -> bytes: ...

def process(source: Readable) -> str:
    return source.read().decode()

# Callable
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)
```

## Anti-patterns

```python
# BAD: Any overuse
def process(data: Any) -> Any: ...

# BAD: No type hints
def calculate(x, y): return x + y

# BAD: Old syntax (pre-3.9)
from typing import List, Optional
def fn(items: List[int]) -> Optional[str]: ...

# GOOD: Modern (3.10+)
def fn(items: list[int]) -> str | None: ...
```
