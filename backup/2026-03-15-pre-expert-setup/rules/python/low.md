# Python Low Priority Rules (PERF + TEST)

## PERF: Performance

### PERF-001: List Comprehension
```python
# BAD
result = []
for x in items:
    if x > 0: result.append(x * 2)

# GOOD
result = [x * 2 for x in items if x > 0]
```

### PERF-002: Generator Expression
```python
total = sum(x * 2 for x in large_list)
```

### PERF-003: String Joining
```python
# BAD: result += s in loop
# GOOD
result = "".join(strings)
```

### PERF-004: Dictionary get()
```python
# BAD: if key in d: value = d[key]
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

## TEST: Testing with pytest

### TEST-001: Use pytest
```python
def test_add():
    assert add(1, 2) == 3
```

### TEST-002: Fixtures
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
    ("1", 1), ("42", 42), ("-1", -1),
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

### Setup
- [ ] pyproject.toml
- [ ] mypy strict mode
- [ ] ruff
- [ ] pytest

### Review
- [ ] Type hints complete
- [ ] Exceptions handled
- [ ] Async parallelized
- [ ] Tests coverage
