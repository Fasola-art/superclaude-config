# TDD 가이드 (테스트 주도 개발)

> **버전**: 2026.01
> **대상**: TypeScript, Python, Go
> **목표**: 테스트 먼저, 코드 나중에

---

## ⚡ 빠른 시작 (3단계 TDD)

| 단계 | 행동 | 결과 |
|------|------|------|
| 1 | 🔴 Red | 예상 동작을 정의하는 실패하는 테스트 작성 |
| 2 | 🟢 Green | 테스트를 통과하는 최소한의 코드 작성 |
| 3 | 🔵 Refactor | 테스트 통과 유지하며 코드 정리 |

**황금 규칙**: 실패하는 테스트 없이 프로덕션 코드를 작성하지 마세요.

---

## 우선순위 요약

| 우선순위 | 카테고리 | 규칙 수 | 핵심 효과 |
|----------|----------|---------|-----------|
| CRITICAL | CYCLE | 4 | TDD 사이클 준수 |
| CRITICAL | TEST-FIRST | 3 | 테스트 우선 원칙 |
| HIGH | STRUCTURE | 4 | 테스트 구조화 |
| HIGH | COVERAGE | 3 | 커버리지 전략 |
| HIGH | MOCK | 4 | Mock을 통한 테스트 격리 |
| MEDIUM | LANG | 9 | 언어별 패턴 |
| LOW | PERF | 3 | 테스트 성능 |

---

## CRITICAL: CYCLE (TDD 사이클)

### CYCLE-001: 먼저 실패하는 테스트

**항상 실패하는 테스트로 시작하세요.**

```typescript
// 1단계: 실패하는 테스트 작성
describe('Calculator', () => {
  it('두 숫자를 더해야 한다', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});

// 이 시점: Calculator 클래스가 없음 → 테스트 실패 ✓
```

### CYCLE-002: 최소한의 Green

**테스트를 통과하는 가장 간단한 코드를 작성하세요.**

```typescript
// 2단계: 최소 구현
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}

// 테스트 통과 → 리팩토링으로 이동
```

**안티패턴**: 과도한 설계를 하지 마세요. 필요한 만큼만 작성하세요.

### CYCLE-003: 안전한 리팩토링

**테스트가 통과하는 상태를 유지하며 코드 품질을 개선하세요.**

```typescript
// 3단계: 리팩토링 (필요시)
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }

  // 같은 TDD 사이클로 더 많은 연산 추가
  subtract(a: number, b: number): number {
    return a - b;
  }
}

// 각 리팩토링 후 테스트 실행 → 모두 통과 ✓
```

### CYCLE-004: 작은 단계

**작은 증분 단계를 밟으세요.**

```typescript
// BAD: 코드 작성 전에 큰 테스트 스위트 작성
describe('UserService', () => {
  it('should create user');
  it('should update user');
  it('should delete user');
  // ... 20개 이상의 테스트
});

// GOOD: 한 번에 하나의 테스트
describe('UserService', () => {
  it('유효한 이메일로 사용자를 생성해야 한다', () => {
    // Red → Green → Refactor
  });
  // 그 다음 테스트 추가
});
```

---

## CRITICAL: TEST-FIRST (테스트 우선 원칙)

### FIRST-001: 구현 전에 동작 정의

```typescript
// 예상 동작으로 시작
describe('EmailValidator', () => {
  it('유효한 이메일 형식을 허용해야 한다', () => {
    const validator = new EmailValidator();
    expect(validator.isValid('user@example.com')).toBe(true);
  });

  it('@가 없는 이메일을 거부해야 한다', () => {
    const validator = new EmailValidator();
    expect(validator.isValid('userexample.com')).toBe(false);
  });
});
```

### FIRST-002: 엣지 케이스 조기 테스트

```typescript
describe('divide', () => {
  it('두 숫자를 나눠야 한다', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('0으로 나눌 때 에러를 던져야 한다', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  it('음수를 처리해야 한다', () => {
    expect(divide(-10, 2)).toBe(-5);
  });
});
```

### FIRST-003: 테스트를 문서로 사용

```typescript
describe('ShoppingCart', () => {
  describe('아이템 추가 시', () => {
    it('아이템 수가 증가해야 한다', () => { /* ... */ });
    it('총 가격이 업데이트되어야 한다', () => { /* ... */ });
    it('중복 아이템을 허용해야 한다', () => { /* ... */ });
  });

  describe('아이템 제거 시', () => {
    it('아이템 수가 감소해야 한다', () => { /* ... */ });
    it('음수 수량을 허용하지 않아야 한다', () => { /* ... */ });
  });
});
```

---

## HIGH: STRUCTURE (테스트 구조)

### STRUCT-001: Arrange-Act-Assert (AAA)

```typescript
it('주문에 할인을 적용해야 한다', () => {
  // Arrange: 테스트 데이터 설정
  const order = new Order();
  order.addItem({ name: 'Widget', price: 100 });
  const discount = new PercentDiscount(10);

  // Act: 동작 실행
  order.applyDiscount(discount);

  // Assert: 결과 검증
  expect(order.total).toBe(90);
});
```

### STRUCT-002: 테스트당 하나의 논리적 검증

```typescript
// BAD: 여러 관련 없는 검증
it('주문을 처리해야 한다', () => {
  expect(order.isValid).toBe(true);
  expect(order.total).toBe(100);
  expect(order.items.length).toBe(3);
  expect(user.orders.length).toBe(1);
});

// GOOD: 테스트당 하나의 논리적 개념
it('주문을 검증해야 한다', () => {
  expect(order.isValid).toBe(true);
});

it('아이템에서 총액을 계산해야 한다', () => {
  expect(order.total).toBe(100);
});
```

### STRUCT-003: 설명적인 테스트 이름

```typescript
// BAD: 모호한 이름
it('should work');
it('test user');
it('handles error');

// GOOD: 동작 설명
it('사용자를 찾지 못하면 빈 배열을 반환해야 한다');
it('이메일이 유효하지 않으면 ValidationError를 던져야 한다');
it('네트워크 실패 시 3번 재시도해야 한다');
```

### STRUCT-004: 테스트 격리

```typescript
// BAD: 테스트가 서로 의존
let user: User;

it('사용자를 생성해야 한다', () => {
  user = createUser({ name: 'Alice' });
  expect(user.id).toBeDefined();
});

it('사용자를 업데이트해야 한다', () => {
  user.name = 'Bob';  // 이전 테스트에 의존!
  expect(user.name).toBe('Bob');
});

// GOOD: 독립적인 테스트
describe('User', () => {
  let user: User;

  beforeEach(() => {
    user = createUser({ name: 'Alice' });
  });

  it('이름을 업데이트해야 한다', () => {
    user.name = 'Bob';
    expect(user.name).toBe('Bob');
  });
});
```

---

## HIGH: MOCK (Mocking & 테스트 더블)

### MOCK-001: 외부 의존성에 Mock 사용

**단위 테스트를 데이터베이스, API, 파일 시스템에서 격리하세요.**

```typescript
// TypeScript - 외부 API Mocking
import { vi } from 'vitest';
import { fetchUserData } from './api';

vi.mock('./api', () => ({
  fetchUserData: vi.fn(),
}));

it('사용자 데이터를 처리해야 한다', async () => {
  vi.mocked(fetchUserData).mockResolvedValue({
    id: '1',
    name: 'Alice',
  });

  const result = await processUser('1');
  expect(result.greeting).toBe('Hello, Alice!');
});
```

### MOCK-002: Stub vs Mock vs Spy

```typescript
// Stub: 미리 정해진 데이터 반환
const stubRepo = {
  findById: () => ({ id: '1', name: 'Test' }),
};

// Mock: 상호작용 검증
const mockRepo = {
  save: vi.fn(),
};
service.createUser(data);
expect(mockRepo.save).toHaveBeenCalledWith(
  expect.objectContaining({ name: 'Alice' })
);

// Spy: 실제 구현을 감싸서 호출 추적
const spy = vi.spyOn(realRepo, 'findById');
await service.getUser('1');
expect(spy).toHaveBeenCalledWith('1');
```

### MOCK-003: 과도한 Mocking 피하기

```typescript
// BAD: 모든 것을 Mocking
it('숫자를 더해야 한다', () => {
  const mockAdd = vi.fn().mockReturnValue(5);
  expect(mockAdd(2, 3)).toBe(5);  // Mock을 테스트, 코드가 아님!
});

// GOOD: 외부 의존성만 Mock
it('처리된 데이터를 저장해야 한다', async () => {
  const mockDb = { save: vi.fn().mockResolvedValue({ id: '1' }) };
  const service = new DataService(mockDb);

  const result = await service.processAndSave({ value: 42 });

  expect(result.processed).toBe(true);  // 실제 로직 테스트
  expect(mockDb.save).toHaveBeenCalled();  // 부수 효과 검증
});
```

### MOCK-004: 테스트 간 Mock 리셋

```typescript
describe('UserService', () => {
  const mockRepo = { findById: vi.fn() };

  beforeEach(() => {
    vi.clearAllMocks();  // 호출 기록 리셋
  });

  afterEach(() => {
    vi.resetAllMocks();  // 구현 리셋
  });

  it('테스트 1', () => { /* ... */ });
  it('테스트 2', () => { /* ... */ });
});
```

---

## MEDIUM: LANG (언어별 패턴)

### TypeScript (Jest/Vitest)

```typescript
// 타입 안전 Mock
import { vi, type Mock } from 'vitest';

interface UserRepository {
  findById(id: string): Promise<User | null>;
}

const mockRepo: UserRepository = {
  findById: vi.fn(),
};

it('ID로 사용자를 찾아야 한다', async () => {
  vi.mocked(mockRepo.findById).mockResolvedValue({ id: '1', name: 'Alice' });

  const user = await service.getUser('1');
  expect(user?.name).toBe('Alice');
});
```

### Python (pytest)

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

def test_user_creation(user: User) -> None:
    assert user.name == "Alice"

@pytest.mark.parametrize("input_val,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
])
def test_uppercase(input_val: str, expected: str) -> None:
    assert input_val.upper() == expected
```

### Go (testing)

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"양수", 2, 3, 5},
        {"음수", -2, -3, -5},
        {"영", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("got %d, want %d", result, tt.expected)
            }
        })
    }
}
```

---

## 체크리스트

### 각 TDD 사이클 전
- [ ] 요구사항을 명확히 이해
- [ ] 예상 동작을 설명하는 테스트 이름 작성
- [ ] 올바른 이유로 테스트 실패 (문법 오류가 아님)

### 구현 후
- [ ] 모든 테스트 통과
- [ ] 코드 리팩토링 완료
- [ ] 중복 로직 없음
- [ ] 테스트 커버리지 목표 달성

### 코드 리뷰
- [ ] 코드 전에 테스트 작성됨
- [ ] 테스트가 문서로 읽힘
- [ ] 엣지 케이스 커버됨
- [ ] 테스트 간 의존성 없음

---

## 명령어

```bash
# TypeScript/JavaScript
npm test              # 모든 테스트 실행
npm test -- --watch   # 감시 모드
npm test -- --coverage

# Python
pytest                # 모든 테스트 실행
pytest -v --tb=short  # 상세, 짧은 traceback
pytest --cov=src      # 커버리지 포함

# Go
go test ./...         # 모든 테스트 실행
go test -v ./...      # 상세
go test -cover ./...  # 커버리지 포함
go test -race ./...   # 레이스 감지
```

---

**META**
- 버전: 2026.01
- 최종 수정: 2026-02-01
- 카테고리: 테스트 방법론
