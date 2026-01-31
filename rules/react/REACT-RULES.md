# Vercel React Best Practices (49개 규칙)

> **버전**: 2026.01
> **적용 대상**: Next.js 14+, React 18+
> **목표**: 로딩 시간 50-70% 단축, 번들 크기 30-60% 감소

---

## 우선순위 요약

| 우선순위 | 카테고리 | 규칙 수 | 핵심 효과 |
|---------|---------|--------|----------|
| 🔴 CRITICAL | ASYNC | 5 | 로딩 시간 50-70% 단축 |
| 🔴 CRITICAL | BUNDLE | 5 | 번들 크기 30-60% 감소 |
| 🟠 HIGH | RENDER | 5 | 클라이언트 번들 50% 감소 |
| 🟠 HIGH | SERVER | 5 | TTFB 90%+ 감소 |
| 🟡 MEDIUM | CACHE | 5 | 응답 시간 90% 감소 |
| 🟡 MEDIUM | IMAGE | 5 | 이미지 로딩 50% 빠름 |
| 🟡 MEDIUM | RERENDER | 7 | 불필요한 리렌더 90% 감소 |
| 🟢 LOW | JS-OPT | 12 | 런타임 성능 개선 |

---

## 🔴 CRITICAL: ASYNC (비동기 최적화)

### ASYNC-001: 병렬 데이터 페칭
```typescript
// ❌ BAD: 순차 실행
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);

// ✅ GOOD: 병렬 실행
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);
```
**효과**: 로딩 시간 60-70% 단축

### ASYNC-002: Waterfall 방지
```typescript
// ❌ BAD: 컴포넌트 내 연속 fetch
async function Page() {
  const data1 = await fetch('/api/1');
  const data2 = await fetch('/api/2'); // data1 완료 후 시작
}

// ✅ GOOD: 병렬 fetch
async function Page() {
  const [data1, data2] = await Promise.all([
    fetch('/api/1'),
    fetch('/api/2')
  ]);
}
```

### ASYNC-003: Promise.all 활용
```typescript
// ✅ 여러 독립적 작업 동시 처리
const results = await Promise.all(
  ids.map(id => fetchItem(id))
);

// ✅ 일부 실패 허용 시
const results = await Promise.allSettled(
  ids.map(id => fetchItem(id))
);
```

### ASYNC-004: Streaming 응답
```typescript
// ✅ GOOD: Streaming SSR
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <Header /> {/* 즉시 렌더링 */}
      <Suspense fallback={<Loading />}>
        <SlowComponent /> {/* 스트리밍 */}
      </Suspense>
    </div>
  );
}
```

### ASYNC-005: Suspense 경계 설정
```typescript
// ✅ 적절한 Suspense 경계
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
**효과**: 점진적 렌더링으로 체감 속도 향상

---

## 🔴 CRITICAL: BUNDLE (번들 최적화)

### BUNDLE-001: Barrel Import 회피
```typescript
// ❌ BAD: Barrel import (전체 번들 포함)
import { Button } from '@/components';

// ✅ GOOD: 직접 import
import { Button } from '@/components/Button';
```
**효과**: 번들 크기 최대 60% 감소

### BUNDLE-002: Dynamic Import
```typescript
// ❌ BAD: 정적 import
import HeavyChart from '@/components/HeavyChart';

// ✅ GOOD: 동적 import
const HeavyChart = dynamic(
  () => import('@/components/HeavyChart'),
  {
    loading: () => <ChartSkeleton />,
    ssr: false // 클라이언트 전용
  }
);
```

### BUNDLE-003: Tree Shaking 최적화
```typescript
// ❌ BAD: 전체 라이브러리 import
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ GOOD: 필요한 함수만 import
import debounce from 'lodash/debounce';
debounce(fn, 300);
```

### BUNDLE-004: 의존성 감사
```bash
# 번들 분석
npx @next/bundle-analyzer

# 중복 의존성 확인
npx depcheck

# 번들 크기 확인
npx size-limit
```

### BUNDLE-005: Chunk 분할
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

## 🟠 HIGH: RENDER (렌더링 최적화)

### RENDER-001: RSC/RCC 분리
```typescript
// ✅ Server Component (기본값)
// app/page.tsx
async function Page() {
  const data = await fetchData(); // 서버에서 실행
  return <div>{data}</div>;
}

// ✅ Client Component (인터랙션 필요 시만)
// components/Counter.tsx
'use client';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```
**원칙**: 기본은 Server Component, 'use client'는 최소화

### RENDER-002: Streaming 렌더링
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
// 중요한 부분만 우선 hydrate
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
      <StaticShell /> {/* 정적 프리렌더 */}
      <Suspense fallback={<Loading />}>
        <DynamicContent /> {/* 동적 스트리밍 */}
      </Suspense>
    </main>
  );
}
```

### RENDER-005: Layout Stability (CLS 0)
```typescript
// ✅ 이미지 크기 명시
<Image
  src="/photo.jpg"
  width={800}
  height={600}
  alt="Photo"
/>

// ✅ 스켈레톤으로 공간 확보
<div className="min-h-[200px]">
  <Suspense fallback={<Skeleton className="h-[200px]" />}>
    <DynamicContent />
  </Suspense>
</div>
```

---

## 🟠 HIGH: SERVER (서버 최적화)

### SERVER-001: Server Components 우선
```typescript
// ✅ 데이터 페칭은 서버에서
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
**효과**: TTFB 90%+ 감소 (엣지 위치에서 실행)

### SERVER-004: ISR (Incremental Static Regeneration)
```typescript
// app/posts/[id]/page.tsx
export const revalidate = 60; // 60초마다 재생성

export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map(post => ({ id: post.id }));
}
```

### SERVER-005: SSR 최적화
```typescript
// 캐시 활용
export default async function Page() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 } // 1시간 캐시
  });
  return <div>{data}</div>;
}
```

---

## 🟡 MEDIUM: CACHE (캐싱)

### CACHE-001: fetch 캐시 설정
```typescript
// 강제 캐시 (기본값)
fetch(url, { cache: 'force-cache' });

// 캐시 없음
fetch(url, { cache: 'no-store' });

// 시간 기반 재검증
fetch(url, { next: { revalidate: 3600 } });

// 태그 기반 재검증
fetch(url, { next: { tags: ['posts'] } });
```

### CACHE-002: unstable_cache 활용
```typescript
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (id: string) => await db.user.findUnique({ where: { id } }),
  ['user'],
  { revalidate: 3600, tags: ['user'] }
);
```

### CACHE-003: 태그 기반 재검증
```typescript
// 데이터 페칭
const posts = await fetch('/api/posts', {
  next: { tags: ['posts'] }
});

// 재검증 트리거
import { revalidateTag } from 'next/cache';
revalidateTag('posts');
```

### CACHE-004: 경로 재검증
```typescript
import { revalidatePath } from 'next/cache';

// 특정 경로 재검증
revalidatePath('/posts');

// 레이아웃 포함 재검증
revalidatePath('/posts', 'layout');
```

### CACHE-005: React cache()
```typescript
import { cache } from 'react';

// 요청 내 중복 호출 방지
const getUser = cache(async (id: string) => {
  return await db.user.findUnique({ where: { id } });
});

// 같은 요청 내에서 여러 번 호출해도 1번만 실행
const user1 = await getUser('1');
const user2 = await getUser('1'); // 캐시에서 반환
```

---

## 🟡 MEDIUM: IMAGE (이미지 최적화)

### IMAGE-001: next/image 사용
```typescript
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // LCP 이미지
/>
```

### IMAGE-002: 반응형 이미지
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
// 기본값: lazy loading
<Image src="/below-fold.jpg" alt="..." width={800} height={600} />

// LCP 이미지는 priority
<Image src="/hero.jpg" alt="..." width={1200} height={600} priority />
```

### IMAGE-004: 포맷 최적화
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

### IMAGE-005: Placeholder 사용
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

## 🟡 MEDIUM: RERENDER (리렌더 방지)

### RERENDER-001: React.memo 활용
```typescript
const ExpensiveComponent = React.memo(function ExpensiveComponent({ data }) {
  return <div>{/* 복잡한 렌더링 */}</div>;
});
```

### RERENDER-002: useMemo로 계산 캐싱
```typescript
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.price - b.price);
}, [items]);
```

### RERENDER-003: useCallback으로 함수 캐싱
```typescript
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

// 자식 컴포넌트에 전달
<List items={items} onItemClick={handleClick} />
```

### RERENDER-004: 상태 분리
```typescript
// ❌ BAD: 하나의 큰 상태
const [state, setState] = useState({ user: null, posts: [], settings: {} });

// ✅ GOOD: 관련된 상태끼리 분리
const [user, setUser] = useState(null);
const [posts, setPosts] = useState([]);
const [settings, setSettings] = useState({});
```

### RERENDER-005: Context 분리
```typescript
// ❌ BAD: 하나의 큰 Context
const AppContext = createContext({ user, theme, settings });

// ✅ GOOD: 목적별 Context 분리
const UserContext = createContext(null);
const ThemeContext = createContext(null);
const SettingsContext = createContext(null);
```

### RERENDER-006: Children 패턴
```typescript
// ✅ 상태가 변해도 children은 리렌더되지 않음
function Parent({ children }) {
  const [count, setCount] = useState(0);
  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      {children} {/* 리렌더 안됨 */}
    </div>
  );
}
```

### RERENDER-007: 컴포넌트 구조 최적화
```typescript
// ❌ BAD: 부모에서 상태 관리
function Parent() {
  const [inputValue, setInputValue] = useState('');
  return (
    <>
      <Input value={inputValue} onChange={setInputValue} />
      <ExpensiveList /> {/* 매번 리렌더 */}
    </>
  );
}

// ✅ GOOD: 상태를 사용하는 곳 근처에서 관리
function Parent() {
  return (
    <>
      <InputWithState /> {/* 상태를 내부에서 관리 */}
      <ExpensiveList /> {/* 리렌더 안됨 */}
    </>
  );
}
```

---

## 🟢 LOW: JS-OPT (JavaScript 최적화)

### JS-OPT-001: 불변성 유지
```typescript
// ❌ BAD: 직접 수정
state.items.push(newItem);

// ✅ GOOD: 새 배열 생성
setState(prev => ({ ...prev, items: [...prev.items, newItem] }));
```

### JS-OPT-002: 조건부 렌더링 최적화
```typescript
// ✅ Early return
if (!data) return <Loading />;
if (error) return <Error />;
return <Content data={data} />;
```

### JS-OPT-003: 이벤트 핸들러 최적화
```typescript
// ❌ BAD: 인라인 함수 (매 렌더마다 새 함수)
<button onClick={() => handleClick(id)}>Click</button>

// ✅ GOOD: data 속성 사용
<button data-id={id} onClick={handleClick}>Click</button>

function handleClick(e) {
  const id = e.currentTarget.dataset.id;
}
```

### JS-OPT-004: 디바운스/쓰로틀
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

### JS-OPT-005: 가상화 (대량 데이터)
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

### JS-OPT-007: 지연 초기화
```typescript
// ❌ BAD: 매번 계산
const [state, setState] = useState(expensiveComputation());

// ✅ GOOD: 초기 렌더링 시 한 번만
const [state, setState] = useState(() => expensiveComputation());
```

### JS-OPT-008: 조건부 Hook 회피
```typescript
// ❌ BAD: 조건부 Hook (에러)
if (condition) {
  useEffect(() => {}, []);
}

// ✅ GOOD: Hook 내부에서 조건 처리
useEffect(() => {
  if (condition) {
    // 로직
  }
}, [condition]);
```

### JS-OPT-009: Key 최적화
```typescript
// ❌ BAD: index를 key로 사용
{items.map((item, index) => <Item key={index} />)}

// ✅ GOOD: 고유 ID 사용
{items.map(item => <Item key={item.id} />)}
```

### JS-OPT-010: Fragment 사용
```typescript
// ❌ BAD: 불필요한 div
return (
  <div>
    <Header />
    <Content />
  </div>
);

// ✅ GOOD: Fragment
return (
  <>
    <Header />
    <Content />
  </>
);
```

### JS-OPT-011: 선택적 체이닝
```typescript
// ❌ BAD
const name = user && user.profile && user.profile.name;

// ✅ GOOD
const name = user?.profile?.name;
```

### JS-OPT-012: 널 병합 연산자
```typescript
// ❌ BAD
const value = data !== null && data !== undefined ? data : defaultValue;

// ✅ GOOD
const value = data ?? defaultValue;
```

---

## 체크리스트

### 새 프로젝트 시작 시
- [ ] Server Components 기본 사용
- [ ] 'use client' 최소화
- [ ] next/image 설정
- [ ] 번들 분석기 설정

### 코드 리뷰 시
- [ ] Promise.all 사용 여부
- [ ] Barrel import 없는지
- [ ] 적절한 캐시 전략
- [ ] memo/useMemo/useCallback 적절성

### 배포 전
- [ ] 번들 크기 확인
- [ ] Lighthouse 점수
- [ ] Core Web Vitals (LCP, FID, CLS)
