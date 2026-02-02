# React Rules Quick Reference

## CRITICAL (Must Apply)

### Parallel Fetch
```typescript
// Use Promise.all
const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()]);
```

### No Barrel Imports
```typescript
// BAD: import { Button } from '@/components';
// GOOD: import { Button } from '@/components/Button';
```

### Dynamic Import
```typescript
const Chart = dynamic(() => import('@/components/Chart'), { ssr: false });
```

---

## HIGH (Strongly Recommended)

### Server Component Default
```typescript
// app/page.tsx - Server Component without 'use client'
async function Page() {
  const data = await fetchData();
  return <div>{data}</div>;
}
```

### Suspense Boundary
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

## MEDIUM (Recommended)

### Use next/image
```typescript
<Image src="/img.jpg" width={800} height={600} alt="..." />
```

### Cache Configuration
```typescript
fetch(url, { next: { revalidate: 3600 } });
```

### Use memo
```typescript
const Item = React.memo(function Item({ data }) { ... });
```

---

## LOW (Optional)

### useMemo / useCallback
```typescript
const sorted = useMemo(() => items.sort(...), [items]);
const handler = useCallback(() => {...}, []);
```

### Unique Key
```typescript
{items.map(item => <Item key={item.id} />)}
```

---

## Validation Commands

```bash
# Project check
python3 ~/.claude/rules/react/react-checker.py /path/to/project

# ESLint check
npx eslint . --config ~/.claude/rules/react/eslint-react.json
```
