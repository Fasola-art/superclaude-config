# Vercel React Best Practices (49 Rules)

> **Version**: 2026.01
> **Target**: Next.js 14+, React 18+
> **Goal**: 50-70% faster loading, 30-60% smaller bundle

---

## Priority Summary

| Priority | Category | Rules | Key Effect                       |
|----------|----------|-------|----------------------------------|
| CRITICAL | ASYNC    | 5     | 50-70% faster loading            |
| CRITICAL | BUNDLE   | 5     | 30-60% smaller bundle            |
| HIGH     | RENDER   | 5     | 50% smaller client bundle        |
| HIGH     | SERVER   | 5     | 90%+ TTFB reduction              |
| MEDIUM   | CACHE    | 5     | 90% faster response              |
| MEDIUM   | IMAGE    | 5     | 50% faster image loading         |
| MEDIUM   | RERENDER | 7     | 90% fewer unnecessary rerenders  |
| LOW      | JS-OPT   | 12    | Runtime performance improvement  |

---

## CRITICAL: ASYNC (Async Optimization)

### ASYNC-001: Parallel Data Fetching
```typescript
// BAD: Sequential execution
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);

// GOOD: Parallel execution
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);
```
**Effect**: 60-70% faster loading

### ASYNC-002: Prevent Waterfall
```typescript
// BAD: Sequential fetch in component
async function Page() {
  const data1 = await fetch('/api/1');
  const data2 = await fetch('/api/2'); // Starts after data1 completes
}

// GOOD: Parallel fetch
async function Page() {
  const [data1, data2] = await Promise.all([
    fetch('/api/1'),
    fetch('/api/2')
  ]);
}
```

### ASYNC-003: Use Promise.all
```typescript
// Process multiple independent tasks concurrently
const results = await Promise.all(
  ids.map(id => fetchItem(id))
);

// Allow partial failures
const results = await Promise.allSettled(
  ids.map(id => fetchItem(id))
);
```

### ASYNC-004: Streaming Response
```typescript
// GOOD: Streaming SSR
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <Header /> {/* Renders immediately */}
      <Suspense fallback={<Loading />}>
        <SlowComponent /> {/* Streams */}
      </Suspense>
    </div>
  );
}
```

### ASYNC-005: Set Suspense Boundaries
```typescript
// Appropriate Suspense boundaries
<Suspense fallback={<HeaderSkeleton />}>
  <Header />
</Suspense>
<Suspense fallback={<ContentSkeleton />}>
  <Content />
</Suspense>
<Suspense fallback={<SidebarSkeleton />}>
  <Sidebar />
</Suspense>
```
**Effect**: Progressive rendering improves perceived speed

---

## CRITICAL: BUNDLE (Bundle Optimization)

### BUNDLE-001: Avoid Barrel Imports
```typescript
// BAD: Barrel import (includes entire bundle)
import { Button } from '@/components';

// GOOD: Direct import
import { Button } from '@/components/Button';
```
**Effect**: Up to 60% smaller bundle

### BUNDLE-002: Dynamic Import
```typescript
// BAD: Static import
import HeavyChart from '@/components/HeavyChart';

// GOOD: Dynamic import
const HeavyChart = dynamic(
  () => import('@/components/HeavyChart'),
  {
    loading: () => <ChartSkeleton />,
    ssr: false // Client-only
  }
);
```

### BUNDLE-003: Tree Shaking Optimization
```typescript
// BAD: Import entire library
import _ from 'lodash';
_.debounce(fn, 300);

// GOOD: Import only needed function
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

### BUNDLE-004: Audit Dependencies
```bash
# Bundle analysis
npx @next/bundle-analyzer

# Check duplicate dependencies
npx depcheck

# Check bundle size
npx size-limit
```

### BUNDLE-005: Chunk Splitting
```typescript
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: [
      'lucide-react',
      '@radix-ui/react-icons',
      'date-fns'
    ]
  }
};
```

---

## HIGH: RENDER (Rendering Optimization)

### RENDER-001: Separate RSC/RCC
```typescript
// Server Component (default)
// app/page.tsx
async function Page() {
  const data = await fetchData(); // Runs on server
  return <div>{data}</div>;
}

// Client Component (only when interaction needed)
// components/Counter.tsx
'use client';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```
**Principle**: Default to Server Component, minimize 'use client'

### RENDER-002: Streaming Rendering
```typescript
// app/page.tsx
export default async function Page() {
  return (
    <>
      <StaticHeader />
      <Suspense fallback={<Loading />}>
        <DynamicContent />
      </Suspense>
    </>
  );
}
```

### RENDER-003: Selective Hydration
```typescript
// Prioritize critical parts for hydration
<Suspense fallback={<Skeleton />}>
  <CriticalInteractiveComponent />
</Suspense>
<Suspense fallback={<Skeleton />}>
  <LessImportantComponent />
</Suspense>
```

### RENDER-004: Partial Prerendering (PPR)
```typescript
// next.config.js
module.exports = {
  experimental: {
    ppr: true
  }
};

// app/page.tsx
export default function Page() {
  return (
    <main>
      <StaticShell /> {/* Static prerender */}
      <Suspense fallback={<Loading />}>
        <DynamicContent /> {/* Dynamic streaming */}
      </Suspense>
    </main>
  );
}
```

### RENDER-005: Layout Stability (CLS 0)
```typescript
// Specify image dimensions
<Image
  src="/photo.jpg"
  width={800}
  height={600}
  alt="Photo"
/>

// Reserve space with skeleton
<div className="min-h-[200px]">
  <Suspense fallback={<Skeleton className="h-[200px]" />}>
    <DynamicContent />
  </Suspense>
</div>
```

---

## HIGH: SERVER (Server Optimization)

### SERVER-001: Prefer Server Components
```typescript
// Fetch data on server
async function ProductList() {
  const products = await db.product.findMany();
  return (
    <ul>
      {products.map(p => <ProductCard key={p.id} product={p} />)}
    </ul>
  );
}
```

### SERVER-002: Server Actions
```typescript
// app/actions.ts
'use server';

export async function createPost(formData: FormData) {
  const title = formData.get('title');
  await db.post.create({ data: { title } });
  revalidatePath('/posts');
}

// components/PostForm.tsx
export function PostForm() {
  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">Create</button>
    </form>
  );
}
```

### SERVER-003: Edge Functions
```typescript
// app/api/geo/route.ts
export const runtime = 'edge';

export async function GET(request: Request) {
  const country = request.headers.get('x-vercel-ip-country');
  return Response.json({ country });
}
```
**Effect**: 90%+ TTFB reduction (runs at edge location)

### SERVER-004: ISR (Incremental Static Regeneration)
```typescript
// app/posts/[id]/page.tsx
export const revalidate = 60; // Regenerate every 60 seconds

export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map(post => ({ id: post.id }));
}
```

### SERVER-005: SSR Optimization
```typescript
// Use caching
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // 1 hour cache
  });
  return <div>{data}</div>;
}
```

---

## MEDIUM: CACHE (Caching)

### CACHE-001: Configure fetch Cache
```typescript
// Force cache (default)
fetch(url, { cache: 'force-cache' });

// No cache
fetch(url, { cache: 'no-store' });

// Time-based revalidation
fetch(url, { next: { revalidate: 3600 } });

// Tag-based revalidation
fetch(url, { next: { tags: ['posts'] } });
```

### CACHE-002: Use unstable_cache
```typescript
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (id: string) => await db.user.findUnique({ where: { id } }),
  ['user'],
  { revalidate: 3600, tags: ['user'] }
);
```

### CACHE-003: Tag-Based Revalidation
```typescript
// Data fetching
const posts = await fetch('/api/posts', {
  next: { tags: ['posts'] }
});

// Trigger revalidation
import { revalidateTag } from 'next/cache';
revalidateTag('posts');
```

### CACHE-004: Path Revalidation
```typescript
import { revalidatePath } from 'next/cache';

// Revalidate specific path
revalidatePath('/posts');

// Revalidate including layout
revalidatePath('/posts', 'layout');
```

### CACHE-005: React cache()
```typescript
import { cache } from 'react';

// Prevent duplicate calls within request
const getUser = cache(async (id: string) => {
  return await db.user.findUnique({ where: { id } });
});

// Multiple calls within same request execute only once
const user1 = await getUser('1');
const user2 = await getUser('1'); // Returns from cache
```

---

## MEDIUM: IMAGE (Image Optimization)

### IMAGE-001: Use next/image
```typescript
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // LCP image
/>
```

### IMAGE-002: Responsive Images
```typescript
<Image
  src="/photo.jpg"
  alt="Photo"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="object-cover"
/>
```

### IMAGE-003: Lazy Loading
```typescript
// Default: lazy loading
<Image src="/below-fold.jpg" alt="..." width={800} height={600} />

// LCP images use priority
<Image src="/hero.jpg" alt="..." width={1200} height={600} priority />
```

### IMAGE-004: Format Optimization
```typescript
// next.config.js
module.exports = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  }
};
```

### IMAGE-005: Use Placeholder
```typescript
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,/9j/4AAQ..."
/>
```

---

## MEDIUM: RERENDER (Prevent Rerenders)

### RERENDER-001: Use React.memo
```typescript
const ExpensiveComponent = React.memo(function ExpensiveComponent({ data }) {
  return <div>{/* Complex rendering */}</div>;
});
```

### RERENDER-002: Cache Computations with useMemo
```typescript
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.price - b.price);
}, [items]);
```

### RERENDER-003: Cache Functions with useCallback
```typescript
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

// Pass to child component
<List items={items} onItemClick={handleClick} />
```

### RERENDER-004: Separate State
```typescript
// BAD: One large state
const [state, setState] = useState({ user: null, posts: [], settings: {} });

// GOOD: Separate related state
const [user, setUser] = useState(null);
const [posts, setPosts] = useState([]);
const [settings, setSettings] = useState({});
```

### RERENDER-005: Separate Context
```typescript
// BAD: One large Context
const AppContext = createContext({ user, theme, settings });

// GOOD: Separate by purpose
const UserContext = createContext(null);
const ThemeContext = createContext(null);
const SettingsContext = createContext(null);
```

### RERENDER-006: Children Pattern
```typescript
// Children don't rerender when state changes
function Parent({ children }) {
  const [count, setCount] = useState(0);
  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      {children} {/* No rerender */}
    </div>
  );
}
```

### RERENDER-007: Optimize Component Structure
```typescript
// BAD: Parent manages state
function Parent() {
  const [inputValue, setInputValue] = useState('');
  return (
    <>
      <Input value={inputValue} onChange={setInputValue} />
      <ExpensiveList /> {/* Rerenders every time */}
    </>
  );
}

// GOOD: Manage state close to where it's used
function Parent() {
  return (
    <>
      <InputWithState /> {/* State managed internally */}
      <ExpensiveList /> {/* No rerender */}
    </>
  );
}
```

---

## LOW: JS-OPT (JavaScript Optimization)

### JS-OPT-001: Maintain Immutability
```typescript
// BAD: Direct mutation
state.items.push(newItem);

// GOOD: Create new array
setState(prev => ({ ...prev, items: [...prev.items, newItem] }));
```

### JS-OPT-002: Optimize Conditional Rendering
```typescript
// Early return
if (!data) return <Loading />;
if (error) return <Error />;
return <Content data={data} />;
```

### JS-OPT-003: Optimize Event Handlers
```typescript
// BAD: Inline function (new function each render)
<button onClick={() => handleClick(id)}>Click</button>

// GOOD: Use data attributes
<button data-id={id} onClick={handleClick}>Click</button>

function handleClick(e) {
  const id = e.currentTarget.dataset.id;
}
```

### JS-OPT-004: Debounce/Throttle
```typescript
const debouncedSearch = useMemo(
  () => debounce((query) => search(query), 300),
  []
);

useEffect(() => {
  debouncedSearch(query);
  return () => debouncedSearch.cancel();
}, [query, debouncedSearch]);
```

### JS-OPT-005: Virtualization (Large Data)
```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }) {
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div key={virtualRow.key}>{items[virtualRow.index]}</div>
        ))}
      </div>
    </div>
  );
}
```

### JS-OPT-006: Web Workers
```typescript
// heavy-task.worker.ts
self.onmessage = (e) => {
  const result = heavyComputation(e.data);
  self.postMessage(result);
};

// component.tsx
const worker = new Worker(new URL('./heavy-task.worker.ts', import.meta.url));
worker.postMessage(data);
worker.onmessage = (e) => setResult(e.data);
```

### JS-OPT-007: Lazy Initialization
```typescript
// BAD: Computed every time
const [state, setState] = useState(expensiveComputation());

// GOOD: Computed once on initial render
const [state, setState] = useState(() => expensiveComputation());
```

### JS-OPT-008: Avoid Conditional Hooks
```typescript
// BAD: Conditional Hook (error)
if (condition) {
  useEffect(() => {}, []);
}

// GOOD: Handle condition inside Hook
useEffect(() => {
  if (condition) {
    // Logic
  }
}, [condition]);
```

### JS-OPT-009: Key Optimization
```typescript
// BAD: Using index as key
{items.map((item, index) => <Item key={index} />)}

// GOOD: Use unique ID
{items.map(item => <Item key={item.id} />)}
```

### JS-OPT-010: Use Fragment
```typescript
// BAD: Unnecessary div
return (
  <div>
    <Header />
    <Content />
  </div>
);

// GOOD: Fragment
return (
  <>
    <Header />
    <Content />
  </>
);
```

### JS-OPT-011: Optional Chaining
```typescript
// BAD
const name = user && user.profile && user.profile.name;

// GOOD
const name = user?.profile?.name;
```

### JS-OPT-012: Nullish Coalescing
```typescript
// BAD
const value = data !== null && data !== undefined ? data : defaultValue;

// GOOD
const value = data ?? defaultValue;
```

---

## Checklist

### New Project Setup
- [ ] Use Server Components by default
- [ ] Minimize 'use client'
- [ ] Configure next/image
- [ ] Set up bundle analyzer

### Code Review
- [ ] Using Promise.all
- [ ] No barrel imports
- [ ] Appropriate cache strategy
- [ ] Appropriate memo/useMemo/useCallback usage

### Before Deploy
- [ ] Check bundle size
- [ ] Lighthouse score
- [ ] Core Web Vitals (LCP, FID, CLS)
