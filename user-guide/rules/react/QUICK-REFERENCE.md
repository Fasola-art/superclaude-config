# React 규칙 퀵 레퍼런스

## 🔴 CRITICAL (반드시 적용)

### 병렬 fetch
```typescript
// ✅ Promise.all 사용
const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()]);
```

### Barrel Import 금지
```typescript
// ❌ import { Button } from '@/components';
// ✅ import { Button } from '@/components/Button';
```

### Dynamic Import
```typescript
const Chart = dynamic(() => import('@/components/Chart'), { ssr: false });
```

---

## 🟠 HIGH (강력 권장)

### Server Component 기본
```typescript
// app/page.tsx - 'use client' 없으면 Server Component
async function Page() {
  const data = await fetchData();
  return <div>{data}</div>;
}
```

### Suspense 경계
```typescript
<Suspense fallback={<Loading />}>
  <AsyncComponent />
</Suspense>
```

### Server Actions
```typescript
'use server';
export async function action(formData: FormData) { ... }
```

---

## 🟡 MEDIUM (권장)

### next/image 사용
```typescript
<Image src="/img.jpg" width={800} height={600} alt="..." />
```

### 캐시 설정
```typescript
fetch(url, { next: { revalidate: 3600 } });
```

### memo 사용
```typescript
const Item = React.memo(function Item({ data }) { ... });
```

---

## 🟢 LOW (선택)

### useMemo / useCallback
```typescript
const sorted = useMemo(() => items.sort(...), [items]);
const handler = useCallback(() => {...}, []);
```

### 고유 key 사용
```typescript
{items.map(item => <Item key={item.id} />)}
```

---

## 검사 명령어

```bash
# 프로젝트 검사
python3 ~/.claude/rules/react/react-checker.py /path/to/project

# ESLint 검사
npx eslint . --config ~/.claude/rules/react/eslint-react.json
```
