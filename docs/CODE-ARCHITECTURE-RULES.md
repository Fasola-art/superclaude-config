# Code Architecture Rules (필수)

> 코드 아키텍처 설계 시 필수 준수 규칙

---

## UI/Hook 분리

| 원칙 | 설명 |
|------|------|
| 컴포넌트 역할 | UI 렌더링만 담당 |
| 상태 관리 | Custom Hook으로 분리 |
| API 호출 | Custom Hook으로 분리 |
| Hook 파일명 | `use-[기능명].ts` |

### 예시

```typescript
// ❌ 나쁜 예: 컴포넌트에 로직 혼재
function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/user').then(res => res.json()).then(setUser);
  }, []);

  return <div>{user?.name}</div>;
}

// ✅ 좋은 예: Hook으로 분리
function UserProfile() {
  const { user, loading } = useUser();
  return <div>{user?.name}</div>;
}

// hooks/use-user.ts
function useUser() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/user').then(res => res.json()).then(setUser);
  }, []);

  return { user, loading };
}
```

---

## 공통 기능 추출

| 원칙 | 설명 |
|------|------|
| 반복 패턴 | 2회 이상 반복 → 공통 컴포넌트로 추출 |
| Props 통합 | 유사한 Props → BaseProps 타입으로 통합 |
| 관련 컴포넌트 | Compound Component 패턴 적용 |

### Compound Component 예시

```typescript
// ✅ Compound Component 패턴
<Card>
  <Card.Header>제목</Card.Header>
  <Card.Body>내용</Card.Body>
  <Card.Footer>푸터</Card.Footer>
</Card>
```

---

## SSOT (Single Source of Truth)

| 원칙 | 설명 |
|------|------|
| 데이터 출처 | 모든 데이터/상태는 단일 출처만 가져야 함 |
| 파생 값 | 파생 가능한 값은 상태로 저장하지 말고 계산 |
| 검증 로직 | 중복 검증 로직 → 단일 함수로 통합 |
| 상수/설정 | 중복 상수/설정 → 단일 파일에서 관리 |

### 예시

```typescript
// ❌ 나쁜 예: 파생 값을 상태로 저장
const [items, setItems] = useState([]);
const [total, setTotal] = useState(0); // 파생 값

// ✅ 좋은 예: 계산으로 파생
const [items, setItems] = useState([]);
const total = useMemo(() => items.reduce((sum, i) => sum + i.price, 0), [items]);
```

---

## Database Normalization Rules (필수)

### 정규화 3단계 적용 원칙

| 정규형 | 규칙 | 체크 항목 |
|--------|------|----------|
| 1NF | 원자값 | 컬럼에 배열/중첩 객체 대신 별도 테이블 |
| 2NF | 완전 함수 종속 | 복합키 사용 시 모든 컬럼이 전체 키에 종속 |
| 3NF | 이행 종속 제거 | 비키 컬럼 간 종속성 없음 |

### 예시

```sql
-- ❌ 나쁜 예: 1NF 위반 (배열 저장)
CREATE TABLE orders (
  id INT,
  items TEXT  -- 'item1,item2,item3' 형태로 저장
);

-- ✅ 좋은 예: 별도 테이블
CREATE TABLE orders (
  id INT PRIMARY KEY
);

CREATE TABLE order_items (
  id INT PRIMARY KEY,
  order_id INT REFERENCES orders(id),
  item_name TEXT
);
```

---

## 체크리스트

### 컴포넌트 작성 시
- [ ] 상태 관리 로직이 Hook으로 분리되었는가?
- [ ] API 호출이 Hook으로 분리되었는가?
- [ ] 2회 이상 반복되는 패턴이 공통 컴포넌트로 추출되었는가?

### 데이터 설계 시
- [ ] 모든 상태가 단일 출처를 가지는가?
- [ ] 파생 가능한 값이 상태로 저장되지 않았는가?
- [ ] 데이터베이스가 3NF를 준수하는가?
