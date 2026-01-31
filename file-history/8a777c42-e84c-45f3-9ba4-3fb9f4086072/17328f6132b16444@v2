# Python 규칙 퀵 레퍼런스

## 🔴 CRITICAL (반드시 적용)

### 타입 힌트
```python
# ✅ 현대 문법 (3.10+)
def fn(items: list[int]) -> str | None:
    pass
```

### 예외 처리
```python
# ✅ 구체적 예외 + 체이닝
except ValueError as e:
    raise RuntimeError("처리 실패") from e
```

### 가변 기본값 금지
```python
# ❌ def fn(items: list = []):
# ✅ def fn(items: list | None = None):
```

---

## 🟠 HIGH (강력 권장)

### 비동기 병렬 실행
```python
async with asyncio.TaskGroup() as tg:
    task1 = tg.create_task(fetch1())
    task2 = tg.create_task(fetch2())
```

### dataclass 사용
```python
@dataclass(frozen=True, slots=True)
class Config:
    name: str
    value: int
```

### 커스텀 예외
```python
class AppError(Exception): pass
class ValidationError(AppError): pass
```

---

## 🟡 MEDIUM (권장)

### import 순서
```python
# 1. 표준 라이브러리
# 2. 서드파티
# 3. 로컬
```

### 리스트 컴프리헨션
```python
result = [x * 2 for x in items if x > 0]
```

### 문자열 결합
```python
result = "".join(strings)
```

---

## 🟢 LOW (선택)

### slots
```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
```

### 제너레이터
```python
total = sum(x for x in large_list)
```

---

## 검사 명령어

```bash
# 타입 체크
mypy --strict .

# 린트
ruff check .

# 포맷
ruff format .

# 테스트
pytest -v --cov
```
