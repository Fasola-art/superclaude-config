# Class Design Rules

## Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `@dataclass` | Data containers | Config, DTO |
| `NamedTuple` | Immutable data | Coordinates |
| `Pydantic` | Validation | API input/output |
| `Protocol` | Interface | Duck typing |

## dataclass

```python
from dataclasses import dataclass, field
from typing import Self

# Frozen + slots for performance
@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: Self) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# With defaults
@dataclass
class Config:
    name: str
    debug: bool = False
    items: list[str] = field(default_factory=list)
```

## Pydantic

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)

    model_config = {"frozen": True}
```

## Protocol

```python
from typing import Protocol

class Repository(Protocol):
    def get(self, id: int) -> Model | None: ...
    def save(self, model: Model) -> None: ...

# Any class with get/save methods satisfies Repository
```

## Anti-patterns

```python
# BAD: Mutable default argument
def fn(items: list = []):  # Shared across calls!
    items.append(1)

# GOOD
def fn(items: list | None = None):
    if items is None:
        items = []
```
