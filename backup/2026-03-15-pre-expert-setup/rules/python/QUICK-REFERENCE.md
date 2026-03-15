# Python Rules Quick Reference

## CRITICAL (Must Apply)

### Type Hints
```python
# Modern syntax (3.10+)
def fn(items: list[int]) -> str | None:
    pass
```

### Exception Handling
```python
# Specific exception + chaining
except ValueError as e:
    raise RuntimeError("Processing failed") from e
```

### No Mutable Default Arguments
```python
# BAD: def fn(items: list = []):
# GOOD: def fn(items: list | None = None):
```

---

## HIGH (Strongly Recommended)

### Async Parallel Execution
```python
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch1())
    task2 = tg.create_task(fetch2())
```

### Use dataclass
```python
@dataclass(frozen=True, slots=True)
class Config:
    name: str
    value: int
```

### Custom Exceptions
```python
class AppError(Exception): pass
class ValidationError(AppError): pass
```

---

## MEDIUM (Recommended)

### Import Order
```python
# 1. Standard library
# 2. Third-party
# 3. Local
```

### List Comprehension
```python
result = [x * 2 for x in items if x > 0]
```

### String Joining
```python
result = "".join(strings)
```

---

## LOW (Optional)

### slots
```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
```

### Generator
```python
total = sum(x for x in large_list)
```

---

## Validation Commands

```bash
# Type check
mypy --strict .

# Lint
ruff check .

# Format
ruff format .

# Test
pytest -v --cov
```
