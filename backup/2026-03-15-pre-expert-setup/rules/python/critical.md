# Python Critical Rules (TYPE + ERROR)

## TYPE: Type Hints

### TYPE-001: All Functions Typed
```python
# GOOD
def process(data: str) -> str:
    return data.upper()
```

### TYPE-002: Modern Syntax (3.10+)
```python
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

### TYPE-005: TypedDict for Dicts
```python
from typing import TypedDict

class UserDict(TypedDict):
    id: int
    name: str
    email: str | None
```

### TYPE-006: Never Use Any
```python
# BAD: def process(data: Any) -> Any
# GOOD: def process(data: dict[str, int]) -> list[str]
```

---

## ERROR: Exception Handling

### ERROR-001: Catch Specific
```python
# BAD: except: or except Exception:
# GOOD
except ValueError as e:
    logger.error(f"Value error: {e}")
    raise
```

### ERROR-002: Exception Chaining
```python
except ValueError as e:
    raise RuntimeError("Processing failed") from e
```

### ERROR-003: Custom Exceptions
```python
class AppError(Exception): pass
class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"{field}: {message}")
```

### ERROR-004: Context Managers
```python
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

### ERROR-005: Logging
```python
logger = logging.getLogger(__name__)
try:
    process()
except ValueError as e:
    logger.exception("Processing failed")  # Includes stack trace
    raise
```
