# Python Medium Priority Rules (FUNC + IMPORT)

## FUNC: Function Design

### FUNC-001: Single Responsibility
```python
# BAD: Too many responsibilities
def process_user(data):
    validate(data); transform(data); save(data); send_email(data)

# GOOD: Separated
def validate_user(data): ...
def transform_user(data): ...
def save_user(data): ...
```

### FUNC-002: Clear Parameters
```python
# BAD: def create(n, e, a, c, co, p):
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
from functools import cache

@cache
def fibonacci(n: int) -> int:
    if n < 2: return n
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
def process(data):
    if not data: return None
    if not data.valid: return None
    return do_something(data)
```

### FUNC-006: Pure Functions
```python
# BAD: items.append(item)  # Mutates
# GOOD
def add_item(items: list, item) -> list:
    return [*items, item]
```

---

## IMPORT: Import Rules

### IMPORT-001: Absolute Imports
```python
from mypackage.utils import helper
```

### IMPORT-002: Import Order
```python
# 1. Standard library
import os, sys
from pathlib import Path

# 2. Third-party
import httpx
from pydantic import BaseModel

# 3. Local
from mypackage import utils
```

### IMPORT-003: Explicit Imports
```python
# BAD: from os import *
# GOOD
from os import path, environ
```

### IMPORT-004: Type-Only Imports
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from heavy_module import HeavyClass

def fn(obj: "HeavyClass") -> None: pass
```

### IMPORT-005: Lazy Import
```python
def process():
    import heavy_module  # Load only when needed
    return heavy_module.do_something()
```
