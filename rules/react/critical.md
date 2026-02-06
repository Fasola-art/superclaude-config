# React Critical Rules (ASYNC + BUNDLE)

## ASYNC: Async Optimization

### ASYNC-001: Parallel Data Fetching
```typescript
// BAD: Sequential
const user = await getUser(id);
const posts = await getPosts(id);

// GOOD: Parallel (60-70% faster)
const [user, posts] = await Promise.all([getUser(id), getPosts(id)]);
```

### ASYNC-002: Prevent Waterfall
```typescript
// BAD: Sequential in component
async function Page() {
  const data1 = await fetch('/api/1');
  const data2 = await fetch('/api/2');
}

// GOOD: Parallel
const [data1, data2] = await Promise.all([fetch('/api/1'), fetch('/api/2')]);
```

### ASYNC-003: Promise.all / allSettled
```typescript
// All must succeed
const results = await Promise.all(ids.map(id => fetchItem(id)));

// Allow partial failures
const results = await Promise.allSettled(ids.map(id => fetchItem(id)));
```

### ASYNC-004: Streaming Response
```typescript
<Suspense fallback={<Loading />}>
  <SlowComponent />
</Suspense>
```

### ASYNC-005: Suspense Boundaries
```typescript
<Suspense fallback={<HeaderSkeleton />}><Header /></Suspense>
<Suspense fallback={<ContentSkeleton />}><Content /></Suspense>
```

---

## BUNDLE: Bundle Optimization

### BUNDLE-001: No Barrel Imports
```typescript
// BAD: import { Button } from '@/components';
// GOOD (60% smaller)
import { Button } from '@/components/Button';
```

### BUNDLE-002: Dynamic Import
```typescript
const HeavyChart = dynamic(
  () => import('@/components/HeavyChart'),
  { loading: () => <ChartSkeleton />, ssr: false }
);
```

### BUNDLE-003: Tree Shaking
```typescript
// BAD: import _ from 'lodash';
// GOOD
import debounce from 'lodash/debounce';
```

### BUNDLE-004: Audit Dependencies
```bash
npx @next/bundle-analyzer
npx depcheck
npx size-limit
```

### BUNDLE-005: Chunk Splitting
```typescript
// next.config.js
experimental: {
  optimizePackageImports: ['lucide-react', '@radix-ui/react-icons', 'date-fns']
}
```
