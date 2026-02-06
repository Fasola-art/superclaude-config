# Next.js App Router Rules

## Routing Patterns

| File | Purpose | Notes |
|------|---------|-------|
| `page.tsx` | Route page | Server Component default |
| `layout.tsx` | Layout | Nestable, state preserved |
| `loading.tsx` | Loading UI | Auto Suspense |
| `error.tsx` | Error UI | `'use client'` required |
| `route.ts` | API Route | Export GET, POST, etc. |

## Data Fetching Patterns

```typescript
// GOOD: Direct fetch in Server Component
async function ProductList() {
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 }  // ISR
  });
  return <div>{/* ... */}</div>;
}

// GOOD: Parallel data fetching
async function Dashboard() {
  const [user, posts, stats] = await Promise.all([
    getUser(),
    getPosts(),
    getStats()
  ]);
  return <div>{/* ... */}</div>;
}

// GOOD: Server Action
'use server';
export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  await db.post.create({ data: { title } });
  revalidatePath('/posts');
}
```

## Anti-patterns

```typescript
// BAD: Client-side fetch when server works
'use client';
function Page() {
  const [data, setData] = useState(null);
  useEffect(() => { fetch(...) }, []);  // Should be server
}

// BAD: Sequential fetch (waterfall)
const user = await getUser();
const posts = await getPosts(user.id);  // Parallelize if no dependency

// BAD: Excessive 'use client'
'use client';  // Unnecessary for static UI
function StaticCard() { return <div>...</div>; }
```
