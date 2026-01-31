# Python 코딩 규칙 (42개 규칙)

> **버전**: 2026.01
> **적용 대상**: Python 3.10+
> **목표**: 타입 안전하고 유지보수 가능한 코드

---

## 우선순위 요약

| 우선순위 | 카테고리 | 규칙 수 | 핵심 효과 |
|---------|---------|--------|----------|
| 🔴 CRITICAL | TYPE | 6 | 타입 안전성 확보 |
| 🔴 CRITICAL | ERROR | 5 | 안정적 에러 처리 |
| 🟠 HIGH | ASYNC | 5 | 비동기 최적화 |
| 🟠 HIGH | CLASS | 5 | 클래스 설계 |
| 🟡 MEDIUM | FUNC | 6 | 함수 설계 |
| 🟡 MEDIUM | IMPORT | 5 | import 정리 |
| 🟢 LOW | PERF | 5 | 성능 최적화 |
| 🟢 LOW | TEST | 5 | 테스트 패턴 |

---

## 🔴 CRITICAL: TYPE (타입 힌트)

### TYPE-001: 모든 함수에 타입 힌트

```python
# ❌ BAD
def process(data):
    return data.upper()

# ✅ GOOD
def process(data: str) -> str:
    return data.upper()
```

### TYPE-002: 현대 문법 사용 (3.10+)

```python
# ❌ BAD (3.9 이전)
from typing import List, Dict, Optional
def fn(items: List[int]) -> Optional[str]:
    pass

# ✅ GOOD (3.10+)
def fn(items: list[int]) -> str | None:
    pass
```

### TYPE-003: TypeVar로 제네릭

```python
from typing import TypeVar

T = TypeVar('T')

def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

### TYPE-004: Protocol로 덕 타이핑

```python
from typing import Protocol

class Readable(Protocol):
    def read(self) -> bytes: ...

def process(source: Readable) -> str:
    return source.read().decode()
```

### TYPE-005: TypedDict로 딕셔너리 타입

```python
from typing import TypedDict

class UserDict(TypedDict):
    id: int
    name: str
    email: str | None

def get_user() -> UserDict:
    return {"id": 1, "name": "test", "email": None}
```

### TYPE-006: Any 사용 금지

```python
# ❌ BAD
def process(data: Any) -> Any:
    pass

# ✅ GOOD
def process(data: dict[str, int]) -> list[str]:
    pass
```

---

## 🔴 CRITICAL: ERROR (에러 처리)

### ERROR-001: 구체적 예외 처리

```python
# ❌ BAD
try:
    risky()
except:  # bare except
    pass

# ❌ BAD
except Exception:  # 너무 넓음
    pass

# ✅ GOOD
except ValueError as e:
    logger.error(f"값 오류: {e}")
    raise
```

### ERROR-002: 예외 체이닝

```python
# ❌ BAD
except ValueError:
    raise RuntimeError("처리 실패")  # 원인 손실

# ✅ GOOD
except ValueError as e:
    raise RuntimeError("처리 실패") from e
```

### ERROR-003: 커스텀 예외 계층

```python
class AppError(Exception):
    """기본 예외"""
    pass

class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} not found: {id}")
```

### ERROR-004: 컨텍스트 매니저

```python
from contextlib import contextmanager

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

### ERROR-005: 에러 로깅

```python
import logging

logger = logging.getLogger(__name__)

try:
    process()
except ValueError as e:
    logger.exception("처리 실패")  # 스택 트레이스 포함
    raise
```

---

## 🟠 HIGH: ASYNC (비동기)

### ASYNC-001: 병렬 실행 (TaskGroup)

```python
# ❌ BAD: 순차 실행
user = await fetch_user()
posts = await fetch_posts()

# ✅ GOOD: 병렬 실행 (3.11+)
async with asyncio.TaskGroup() as tg:
    user_task = tg.create_task(fetch_user())
    posts_task = tg.create_task(fetch_posts())

user = user_task.result()
posts = posts_task.result()
```

### ASYNC-002: 동시성 제한

```python
async def fetch_all(urls: list[str], limit: int = 10):
    semaphore = asyncio.Semaphore(limit)

    async def fetch_one(url: str):
        async with semaphore:
            return await fetch(url)

    return await asyncio.gather(*[fetch_one(url) for url in urls])
```

### ASYNC-003: 타임아웃

```python
async def fetch_with_timeout(url: str):
    async with asyncio.timeout(30):
        return await fetch(url)
```

### ASYNC-004: 블로킹 호출 금지

```python
# ❌ BAD
async def bad():
    time.sleep(1)  # 블로킹!

# ✅ GOOD
async def good():
    await asyncio.sleep(1)
```

### ASYNC-005: 비동기 제너레이터

```python
async def stream_data() -> AsyncIterator[bytes]:
    async for chunk in source:
        yield process(chunk)
```

---

## 🟠 HIGH: CLASS (클래스 설계)

### CLASS-001: dataclass 사용

```python
# ❌ BAD
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# ✅ GOOD
@dataclass
class Point:
    x: float
    y: float
```

### CLASS-002: 불변 dataclass

```python
@dataclass(frozen=True, slots=True)
class Config:
    name: str
    value: int
```

### CLASS-003: Pydantic for 유효성 검사

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)

    model_config = {"frozen": True}
```

### CLASS-004: Protocol로 인터페이스

```python
class Repository(Protocol):
    def get(self, id: int) -> Model | None: ...
    def save(self, model: Model) -> None: ...
```

### CLASS-005: 가변 기본값 금지

```python
# ❌ BAD
def fn(items: list = []):  # 공유됨!
    items.append(1)

# ✅ GOOD
def fn(items: list | None = None):
    if items is None:
        items = []
    items.append(1)
```

---

## 🟡 MEDIUM: FUNC (함수 설계)

### FUNC-001: 단일 책임

```python
# ❌ BAD: 너무 많은 책임
def process_user(data):
    validate(data)
    transform(data)
    save(data)
    send_email(data)

# ✅ GOOD: 분리
def validate_user(data): ...
def transform_user(data): ...
def save_user(data): ...
```

### FUNC-002: 명확한 매개변수

```python
# ❌ BAD
def create(n, e, a, c, co, p):
    pass

# ✅ GOOD
@dataclass
class UserData:
    name: str
    email: str
    age: int

def create_user(data: UserData) -> User:
    pass
```

### FUNC-003: 데코레이터 활용

```python
from functools import cache, wraps

@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### FUNC-004: 제너레이터 사용

```python
def read_large_file(path: str) -> Iterator[str]:
    with open(path) as f:
        for line in f:
            yield line.strip()
```

### FUNC-005: 조기 반환

```python
# ❌ BAD
def process(data):
    if data:
        if data.valid:
            return do_something(data)
        else:
            return None
    else:
        return None

# ✅ GOOD
def process(data):
    if not data:
        return None
    if not data.valid:
        return None
    return do_something(data)
```

### FUNC-006: 순수 함수 선호

```python
# ❌ BAD: 부작용
def add_item(items: list, item):
    items.append(item)  # 원본 수정

# ✅ GOOD: 순수 함수
def add_item(items: list, item) -> list:
    return [*items, item]
```

---

## 🟡 MEDIUM: IMPORT (import 규칙)

### IMPORT-001: 절대 import 우선

```python
# ✅ GOOD
from mypackage.utils import helper

# ⚠️ 조건부
from .utils import helper  # 패키지 내부만
```

### IMPORT-002: import 순서

```python
# 1. 표준 라이브러리
import os
import sys
from pathlib import Path

# 2. 서드파티
import httpx
from pydantic import BaseModel

# 3. 로컬
from mypackage import utils
from mypackage.models import User
```

### IMPORT-003: 명시적 import

```python
# ❌ BAD
from os import *

# ✅ GOOD
from os import path, environ
```

### IMPORT-004: type-only import

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from heavy_module import HeavyClass

def fn(obj: "HeavyClass") -> None:
    pass
```

### IMPORT-005: lazy import

```python
def process():
    import heavy_module  # 필요할 때만 로드
    return heavy_module.do_something()
```

---

## 🟢 LOW: PERF (성능)

### PERF-001: 리스트 컴프리헨션

```python
# ❌ BAD
result = []
for x in items:
    if x > 0:
        result.append(x * 2)

# ✅ GOOD
result = [x * 2 for x in items if x > 0]
```

### PERF-002: 제너레이터 표현식

```python
# 메모리 효율적
total = sum(x * 2 for x in large_list)
```

### PERF-003: 문자열 빌더

```python
# ❌ BAD
result = ""
for s in strings:
    result += s

# ✅ GOOD
result = "".join(strings)
```

### PERF-004: 딕셔너리 get

```python
# ❌ BAD
if key in d:
    value = d[key]
else:
    value = default

# ✅ GOOD
value = d.get(key, default)
```

### PERF-005: slots 사용

```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
```

---

## 🟢 LOW: TEST (테스트)

### TEST-001: pytest 사용

```python
def test_add():
    assert add(1, 2) == 3
```

### TEST-002: fixture 활용

```python
@pytest.fixture
def sample_user() -> User:
    return User(id=1, name="test")

def test_greeting(sample_user: User):
    assert sample_user.greeting() == "Hello, test!"
```

### TEST-003: parametrize

```python
@pytest.mark.parametrize("input,expected", [
    ("1", 1),
    ("42", 42),
    ("-1", -1),
])
def test_parse_int(input: str, expected: int):
    assert parse_int(input) == expected
```

### TEST-004: 예외 테스트

```python
def test_invalid_input():
    with pytest.raises(ValueError, match="변환할 수 없습니다"):
        parse_int("invalid")
```

### TEST-005: mock 사용

```python
from unittest.mock import patch

def test_fetch_calls_api():
    with patch("module.requests.get") as mock:
        mock.return_value.json.return_value = {"id": 1}
        result = fetch_user(1)
        mock.assert_called_once()
```

---

## 📊 체크리스트

### 새 프로젝트 시작 시
- [ ] pyproject.toml 설정
- [ ] mypy strict 모드
- [ ] ruff 설정
- [ ] pytest 설정

### 코드 리뷰 시
- [ ] 타입 힌트 완전성
- [ ] 예외 처리 적절성
- [ ] 비동기 병렬화
- [ ] 테스트 커버리지

---

**META**
- Version: 2026.01
- Last Updated: 2026-01-30
