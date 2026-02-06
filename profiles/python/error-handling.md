# Error Handling Rules

## Patterns

| Pattern | When to Use |
|---------|-------------|
| Specific exception | Expected errors |
| Custom exception | Domain errors |
| Context manager | Resource management |

## Good Patterns

```python
# Specific exception
def parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Cannot convert '{value}'") from e

# Custom exception hierarchy
class AppError(Exception): pass

class UserNotFoundError(AppError):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

class ValidationError(AppError):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"{field}: {message}")

# Context manager
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
```

## Anti-patterns

```python
# BAD: Bare except
try:
    risky()
except:  # Catches KeyboardInterrupt too!
    pass

# BAD: Ignore exception
try:
    risky()
except Exception:
    pass

# BAD: No exception chaining
except ValueError:
    raise RuntimeError("Failed")  # Original cause lost

# GOOD: Chain exceptions
except ValueError as e:
    raise RuntimeError("Failed") from e
```
