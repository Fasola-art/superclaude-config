# Python 언어 프로필

> **버전**: 1.0.0
> **적용 대상**: Python 3.10+
> **자동 감지**: `pyproject.toml`, `requirements.txt`, `setup.py` 존재 시

---

## 🎯 목표

**Primary Outcome**: 타입 안전하고 유지보수 가능한 Python 코드 생성

**Success Criteria**:
- [ ] 모든 함수에 타입 힌트 적용
- [ ] `mypy --strict` 통과
- [ ] `ruff` 린트 경고 0개
- [ ] 테스트 커버리지 80% 이상

**Failure Cases**:
- 🔴 `Any` 타입 남용 → 구체적 타입으로 교체
- 🔴 bare `except:` → 구체적 예외 지정

---

## 🚀 빠른 참조

### 필수 규칙

| 규칙 | 설명 | 예시 |
|------|------|------|
| **타입 힌트** | 모든 함수 시그니처 | `def fn(x: int) -> str:` |
| **f-string** | 문자열 포맷팅 | `f"Hello, {name}"` |
| **pathlib** | 경로 처리 | `Path("file.txt")` |
| **dataclass** | 데이터 클래스 | `@dataclass` |

### 권장 도구

| 도구 | 용도 | 설정 파일 |
|------|------|----------|
| `ruff` | 린트 + 포맷 | `pyproject.toml` |
| `mypy` | 타입 체크 | `pyproject.toml` |
| `pytest` | 테스트 | `pytest.ini` |
| `uv` | 패키지 관리 | `pyproject.toml` |

---

## 📋 섹션 1: 타입 힌트 규칙

### 📊 타입 힌트 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| 기본 타입 | 단순 값 | `int`, `str`, `bool`, `float` |
| 컬렉션 | 리스트, 딕셔너리 | `list[int]`, `dict[str, int]` |
| Optional | None 가능 | `str \| None` (3.10+) |
| Union | 여러 타입 | `int \| str` |
| TypeVar | 제네릭 | `T = TypeVar('T')` |
| Protocol | 덕 타이핑 | `class Readable(Protocol):` |

### ✅ 타입 힌트 패턴

```python
from typing import TypeVar, Protocol
from collections.abc import Callable, Iterable

# ✅ GOOD: 기본 타입 힌트
def greet(name: str, age: int) -> str:
    return f"Hello, {name}! You are {age}."

# ✅ GOOD: Optional (3.10+ 문법)
def find_user(user_id: int) -> User | None:
    return users.get(user_id)

# ✅ GOOD: 제네릭
T = TypeVar('T')

def first(items: list[T]) -> T | None:
    return items[0] if items else None

# ✅ GOOD: Protocol (덕 타이핑)
class Readable(Protocol):
    def read(self) -> bytes: ...

def process(source: Readable) -> str:
    return source.read().decode()

# ✅ GOOD: Callable
def apply(
    func: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    return func(a, b)
```

### ❌ 타입 힌트 안티패턴

```python
# ❌ BAD: Any 남용
def process(data: Any) -> Any:
    return data

# ❌ BAD: 타입 힌트 없음
def calculate(x, y):
    return x + y

# ❌ BAD: 오래된 문법 (3.9 이전)
from typing import List, Dict, Optional
def fn(items: List[int]) -> Optional[str]:
    ...

# ✅ GOOD: 현대 문법 (3.10+)
def fn(items: list[int]) -> str | None:
    ...
```

### ⚠️ 예외 처리

| 상황 | 대응 방법 |
|------|----------|
| 외부 라이브러리 타입 없음 | `# type: ignore[import]` + stub 생성 |
| 복잡한 타입 | `TypeAlias` 사용 |
| 런타임 타입 체크 필요 | `isinstance()` 또는 `pydantic` |

---

## 📋 섹션 2: 에러 처리 규칙

### 📊 에러 처리 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| 구체적 예외 | 예상 가능한 에러 | `except ValueError:` |
| 커스텀 예외 | 도메인 에러 | `class UserNotFound(Exception)` |
| 컨텍스트 매니저 | 리소스 관리 | `with open(...) as f:` |
| Result 패턴 | 함수형 에러 | `returns` 라이브러리 |

### ✅ 에러 처리 패턴

```python
# ✅ GOOD: 구체적 예외 처리
def parse_int(value: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"'{value}'를 정수로 변환할 수 없습니다") from e

# ✅ GOOD: 커스텀 예외 계층
class AppError(Exception):
    """애플리케이션 기본 예외"""
    pass

class UserNotFoundError(AppError):
    """사용자를 찾을 수 없음"""
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"사용자 ID {user_id}를 찾을 수 없습니다")

class ValidationError(AppError):
    """유효성 검사 실패"""
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"{field}: {message}")

# ✅ GOOD: 컨텍스트 매니저
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

# 사용
with database_transaction() as conn:
    conn.execute("INSERT INTO ...")
```

### ❌ 에러 처리 안티패턴

```python
# ❌ BAD: bare except
try:
    risky_operation()
except:  # 모든 예외 (KeyboardInterrupt 포함)
    pass

# ❌ BAD: 예외 무시
try:
    risky_operation()
except Exception:
    pass  # 아무것도 안함

# ❌ BAD: 너무 넓은 예외
try:
    value = data["key"]
except Exception as e:  # KeyError만 잡아야 함
    handle_error(e)

# ❌ BAD: 예외 체이닝 없음
try:
    process(data)
except ValueError:
    raise RuntimeError("처리 실패")  # 원인 정보 손실
```

---

## 📋 섹션 3: 클래스 설계 규칙

### 📊 클래스 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| `@dataclass` | 데이터 컨테이너 | 설정, DTO |
| `NamedTuple` | 불변 데이터 | 좌표, 결과 |
| `Pydantic` | 유효성 검사 | API 입출력 |
| `Protocol` | 인터페이스 | 덕 타이핑 |

### ✅ 클래스 패턴

```python
from dataclasses import dataclass, field
from typing import Self

# ✅ GOOD: dataclass
@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: Self) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# ✅ GOOD: dataclass with defaults
@dataclass
class Config:
    name: str
    debug: bool = False
    max_retries: int = 3
    tags: list[str] = field(default_factory=list)

# ✅ GOOD: Pydantic for validation
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)

    model_config = {"frozen": True}

# ✅ GOOD: Protocol
from typing import Protocol

class Repository(Protocol):
    def get(self, id: int) -> Model | None: ...
    def save(self, model: Model) -> None: ...
    def delete(self, id: int) -> bool: ...
```

### ❌ 클래스 안티패턴

```python
# ❌ BAD: 수동 __init__, __eq__, __repr__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

# ✅ GOOD: dataclass 사용
@dataclass
class Point:
    x: float
    y: float

# ❌ BAD: 가변 기본값
class Config:
    def __init__(self, items: list = []):  # 모든 인스턴스가 공유
        self.items = items
```

---

## 📋 섹션 4: 함수 설계 규칙

### 📊 함수 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| 순수 함수 | 상태 없음 | `def add(a, b): return a + b` |
| 제너레이터 | 지연 평가 | `yield item` |
| 데코레이터 | 횡단 관심사 | `@cache`, `@retry` |
| 클로저 | 상태 캡처 | `def outer(): def inner(): ...` |

### ✅ 함수 패턴

```python
from functools import cache, wraps
from collections.abc import Iterator
from typing import ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

# ✅ GOOD: 캐시 데코레이터
@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# ✅ GOOD: 제너레이터
def read_large_file(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()

# ✅ GOOD: 타입 안전한 데코레이터
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

### ❌ 함수 안티패턴

```python
# ❌ BAD: 가변 기본 인자
def append_to(item, target: list = []):
    target.append(item)
    return target

# ✅ GOOD: None 기본값
def append_to(item, target: list | None = None):
    if target is None:
        target = []
    target.append(item)
    return target

# ❌ BAD: 너무 많은 인자
def create_user(name, email, age, city, country, phone, ...):
    ...

# ✅ GOOD: dataclass 또는 TypedDict
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

## 📋 섹션 5: 비동기 프로그래밍 규칙

### 📊 비동기 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| `asyncio` | I/O 바운드 | 네트워크, 파일 |
| `aiohttp` | HTTP 클라이언트 | API 호출 |
| `asyncpg` | PostgreSQL | 비동기 DB |
| `TaskGroup` | 병렬 실행 | 3.11+ |

### ✅ 비동기 패턴

```python
import asyncio
from collections.abc import AsyncIterator

# ✅ GOOD: 병렬 실행 (3.11+)
async def fetch_all(urls: list[str]) -> list[Response]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(url)) for url in urls]
    return [t.result() for t in tasks]

# ✅ GOOD: 세마포어로 동시성 제한
async def fetch_with_limit(urls: list[str], limit: int = 10) -> list[Response]:
    semaphore = asyncio.Semaphore(limit)

    async def fetch_one(url: str) -> Response:
        async with semaphore:
            return await fetch(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])

# ✅ GOOD: 비동기 제너레이터
async def stream_data(source: AsyncReader) -> AsyncIterator[bytes]:
    async for chunk in source:
        yield process(chunk)

# ✅ GOOD: 타임아웃
async def fetch_with_timeout(url: str, timeout: float = 30.0) -> Response:
    async with asyncio.timeout(timeout):
        return await fetch(url)
```

### ❌ 비동기 안티패턴

```python
# ❌ BAD: 블로킹 호출
async def bad_example():
    time.sleep(1)  # 블로킹!
    # await asyncio.sleep(1) 사용

# ❌ BAD: 순차 실행
async def fetch_all(urls):
    results = []
    for url in urls:
        results.append(await fetch(url))  # 병렬 가능
    return results

# ❌ BAD: run_until_complete 중첩
asyncio.get_event_loop().run_until_complete(coro())  # deprecated
# asyncio.run(coro()) 사용
```

---

## 📋 섹션 6: 테스트 규칙

### 📊 테스트 전략

| 테스트 유형 | 도구 | 커버리지 목표 |
|------------|------|--------------|
| 단위 테스트 | pytest | 80% |
| 통합 테스트 | pytest | 핵심 경로 100% |
| 타입 테스트 | mypy | 공개 API 100% |
| Property 테스트 | hypothesis | 엣지 케이스 |

### ✅ 테스트 패턴

```python
import pytest
from unittest.mock import Mock, patch

# ✅ GOOD: 명확한 테스트명
def test_parse_valid_json_returns_config():
    json_str = '{"name": "test"}'
    result = parse_config(json_str)
    assert result.name == "test"

# ✅ GOOD: fixture 사용
@pytest.fixture
def sample_user() -> User:
    return User(id=1, name="Test", email="test@example.com")

def test_user_greeting(sample_user: User):
    assert sample_user.greeting() == "Hello, Test!"

# ✅ GOOD: parametrize
@pytest.mark.parametrize("input,expected", [
    ("1", 1),
    ("42", 42),
    ("-1", -1),
])
def test_parse_int(input: str, expected: int):
    assert parse_int(input) == expected

# ✅ GOOD: 예외 테스트
def test_parse_invalid_raises_error():
    with pytest.raises(ValueError, match="변환할 수 없습니다"):
        parse_int("not a number")

# ✅ GOOD: mock 사용
def test_fetch_user_calls_api():
    with patch("module.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"id": 1}
        result = fetch_user(1)
        mock_get.assert_called_once_with("/api/users/1")
```

---

## 📋 섹션 7: 프로젝트 구조 규칙

### 📊 권장 구조

```
project/
├── pyproject.toml          # 프로젝트 설정 (필수)
├── README.md
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── py.typed         # PEP 561 마커
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
│   ├── conftest.py         # 공유 fixture
│   ├── unit/
│   └── integration/
└── scripts/
    └── dev.py
```

### ✅ pyproject.toml 설정

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

## ✅ 자가 진단 체크리스트

### 🔴 Critical (반드시 완료)
- [ ] 모든 함수에 타입 힌트 적용
- [ ] `mypy --strict` 통과
- [ ] bare `except:` 사용 0개
- [ ] 가변 기본 인자 사용 0개

### 🟡 Important (80% 이상)
- [ ] `ruff` 경고 0개
- [ ] 테스트 커버리지 80%+
- [ ] docstring 작성 (공개 API)
- [ ] `@dataclass` 활용

### 🟢 Nice-to-have
- [ ] Property-based 테스트
- [ ] 비동기 코드 최적화
- [ ] 벤치마크 작성

**합격 기준**: Critical 100% + Important 80% 이상

---

## 📚 참조

| 문서 | 링크 |
|------|------|
| Python 공식 | https://docs.python.org/3/ |
| PEP 8 | https://peps.python.org/pep-0008/ |
| Mypy | https://mypy.readthedocs.io/ |
| Ruff | https://docs.astral.sh/ruff/ |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Auto-detect: `pyproject.toml`, `requirements.txt`, `setup.py`
