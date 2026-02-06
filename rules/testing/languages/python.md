# Python Testing (pytest)

## Fixtures

```python
import pytest

@pytest.fixture
def user():
    return User(name="Alice", email="alice@example.com")

@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()

def test_user_creation(user):
    assert user.name == "Alice"
```

## Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
])
def test_uppercase(input: str, expected: str):
    assert input.upper() == expected
```

## Exception Testing

```python
def test_division_by_zero():
    with pytest.raises(ValueError, match="cannot divide by zero"):
        divide(10, 0)
```

## Mocking

```python
from unittest.mock import patch

def test_fetch_calls_api():
    with patch("module.requests.get") as mock:
        mock.return_value.json.return_value = {"id": 1}
        result = fetch_user(1)
        mock.assert_called_once()
```

---

## Commands

```bash
pytest                # Run all
pytest -v --tb=short  # Verbose
pytest --cov=src      # Coverage
pytest -n auto        # Parallel (xdist)
```
