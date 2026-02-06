# React High Priority Rules (RENDER + SERVER)

## RENDER: Rendering Optimization

### RENDER-001: RSC vs RCC
```typescript
// Server Component (default)
async function Page() {
  const data = await fetchData();
  return <div>{data}</div>;
}

// Client Component (only when needed)
'use client';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### RENDER-002: Streaming Rendering
```typescript
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
experimental: { ppr: true }
```

### RENDER-005: Layout Stability (CLS 0)
```typescript
<Image src="/photo.jpg" width={800} height={600} alt="Photo" />

<div className="min-h-[200px]">
  <Suspense fallback={<Skeleton className="h-[200px]" />}>
    <DynamicContent />
  </Suspense>
</div>
```

---

## SERVER: Server Optimization

### SERVER-001: Server Components
```typescript
async function ProductList() {
  const products = await db.product.findMany();
  return <ul>{products.map(p => <ProductCard key={p.id} product={p} />)}</ul>;
}
```

### SERVER-002: Server Actions
```typescript
'use server';
export async function createPost(formData: FormData) {
  await db.post.create({ data: { title: formData.get('title') } });
  revalidatePath('/posts');
}
```

### SERVER-003: Edge Functions
```typescript
export const runtime = 'edge';
export async function GET(request: Request) {
  const country = request.headers.get('x-vercel-ip-country');
  return Response.json({ country });
}
```

### SERVER-004: ISR
```typescript
export const revalidate = 60;
export async function generateStaticParams() {
  return (await getPosts()).map(post => ({ id: post.id }));
}
```

### SERVER-005: SSR Caching
```typescript
const data = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 }
});
```
