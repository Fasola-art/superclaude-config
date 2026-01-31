# React 에러 패턴

> **카테고리**: react
> **갱신일**: 2026-01-30

---

## 🔴 Critical 에러

### Hydration Mismatch

**메시지**: `Text content does not match server-rendered HTML`

**원인**: 서버/클라이언트 렌더링 불일치

**해결책**:
```typescript
// ❌ 원인: 클라이언트 전용 값
function Component() {
  return <div>{new Date().toLocaleString()}</div>;  // 서버/클라이언트 다름
}

// ✅ 해결 1: useEffect
function Component() {
  const [time, setTime] = useState<string>();
  useEffect(() => {
    setTime(new Date().toLocaleString());
  }, []);
  return <div>{time}</div>;
}

// ✅ 해결 2: suppressHydrationWarning
<time suppressHydrationWarning>
  {new Date().toLocaleString()}
</time>

// ✅ 해결 3: dynamic import (ssr: false)
const ClientOnly = dynamic(() => import('./ClientComponent'), {
  ssr: false
});
```

**예방**: 서버/클라이언트 분기 명확히

---

### Invalid Hook Call

**메시지**: `Hooks can only be called inside of the body of a function component`

**원인**: Hook 규칙 위반

**해결책**:
```typescript
// ❌ 원인 1: 조건문 안에서 Hook
if (condition) {
  const [state, setState] = useState();  // 에러
}

// ✅ 해결: 최상위에서 호출
const [state, setState] = useState();
if (condition) {
  // state 사용
}

// ❌ 원인 2: 일반 함수에서 Hook
function helper() {
  const [state, setState] = useState();  // 에러
}

// ✅ 해결: 커스텀 훅으로 변경 (use 접두사)
function useHelper() {
  const [state, setState] = useState();
  return state;
}
```

**예방**: ESLint `react-hooks/rules-of-hooks` 활성화

---

### Too Many Re-renders

**메시지**: `Too many re-renders. React limits the number of renders`

**원인**: 렌더링 중 setState 호출

**해결책**:
```typescript
// ❌ 원인: 렌더링 중 상태 변경
function Component() {
  const [count, setCount] = useState(0);
  setCount(count + 1);  // 무한 루프
  return <div>{count}</div>;
}

// ✅ 해결 1: useEffect 사용
useEffect(() => {
  setCount(c => c + 1);
}, [dependency]);

// ✅ 해결 2: 이벤트 핸들러로 이동
<button onClick={() => setCount(c => c + 1)}>Increment</button>

// ❌ 원인 2: 인라인 함수가 상태 변경
<Child onChange={setData(newData)} />  // 즉시 실행됨

// ✅ 해결: 화살표 함수로 래핑
<Child onChange={() => setData(newData)} />
```

---

## 🟠 Common 에러

### Cannot update unmounted component

**메시지**: `Can't perform a React state update on an unmounted component`

**원인**: 언마운트 후 setState 호출

**해결책**:
```typescript
// ❌ 원인: cleanup 없음
useEffect(() => {
  fetchData().then(data => setData(data));
}, []);

// ✅ 해결 1: AbortController
useEffect(() => {
  const controller = new AbortController();

  fetchData({ signal: controller.signal })
    .then(data => setData(data))
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });

  return () => controller.abort();
}, []);

// ✅ 해결 2: isMounted 플래그 (덜 권장)
useEffect(() => {
  let isMounted = true;
  fetchData().then(data => {
    if (isMounted) setData(data);
  });
  return () => { isMounted = false; };
}, []);
```

---

### Each child should have a unique key

**원인**: 리스트 렌더링 시 key 누락

**해결책**:
```typescript
// ❌ 에러
{items.map(item => <Item {...item} />)}

// ❌ 안티패턴: index를 key로
{items.map((item, index) => <Item key={index} {...item} />)}

// ✅ 해결: 고유 ID 사용
{items.map(item => <Item key={item.id} {...item} />)}
```

---

### Cannot read property of undefined

**원인**: 데이터 로딩 전 접근

**해결책**:
```typescript
// ❌ 에러
function Component({ user }) {
  return <div>{user.name}</div>;  // user가 undefined일 수 있음
}

// ✅ 해결 1: optional chaining
return <div>{user?.name}</div>;

// ✅ 해결 2: 조기 반환
if (!user) return <Loading />;
return <div>{user.name}</div>;

// ✅ 해결 3: 기본값
function Component({ user = { name: 'Guest' } }) {
  return <div>{user.name}</div>;
}
```

---

## 🟡 Warning

### React does not recognize the X prop

**원인**: DOM 요소에 커스텀 prop 전달

**해결책**:
```typescript
// ❌ 경고
<div isActive={true}>...</div>  // isActive는 DOM 속성이 아님

// ✅ 해결 1: data- 접두사
<div data-active={true}>...</div>

// ✅ 해결 2: 구조분해로 필터링
const { isActive, ...domProps } = props;
<div {...domProps}>...</div>
```

---

### useEffect has missing dependencies

**원인**: 의존성 배열 누락

**해결책**:
```typescript
// ⚠️ 경고
useEffect(() => {
  fetchUser(userId);
}, []);  // userId 누락

// ✅ 해결 1: 의존성 추가
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// ✅ 해결 2: 의도적 생략 (주석 필수)
useEffect(() => {
  fetchUser(userId);
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []);  // 초기 로드만 의도
```

---

## 📊 에러 빈도

| 에러 | 빈도 | 심각도 |
|------|------|--------|
| Hydration Mismatch | 높음 | 높음 |
| Invalid Hook Call | 중간 | 높음 |
| Too Many Re-renders | 중간 | 높음 |
| Missing Key | 높음 | 낮음 |
| Missing Dependencies | 높음 | 낮음 |

---

## 🔧 디버깅 도구

```bash
# React DevTools
# 크롬 확장 설치

# Strict Mode 활성화 (이중 렌더링으로 버그 발견)
<StrictMode>
  <App />
</StrictMode>

# 프로파일러
# React DevTools > Profiler 탭
```

---

**META**
- Category: react
- Last Updated: 2026-01-30
