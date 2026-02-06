# Testing Rules (pytest)

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

## Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
])
def test_uppercase(input: str, expected: str):
    assert input.upper() == expected
```

## Test Exceptions

```python
def test_invalid_input():
    with pytest.raises(ValueError, match="cannot convert"):
        parse_int("invalid")
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

## Commands

```bash
pytest                # Run all
pytest -v --tb=short  # Verbose
pytest --cov=src      # Coverage
pytest -n auto        # Parallel (xdist)
```
