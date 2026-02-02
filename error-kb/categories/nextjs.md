# Next.js Error Patterns

> **Category**: nextjs
> **Updated**: 2026-01-30

---

## 🔴 Critical Errors

### Module not found: Can't resolve 'X'

**Cause**: Module resolution failed

**Solutions**:
```typescript
// Cause 1: Path error
import { Button } from '@/components/button';  // Check case sensitivity

// Fix: Exact path
import { Button } from '@/components/Button';

// Cause 2: Server-only module
import fs from 'fs';  // Cannot use in client

// Fix: Dynamic import or use only in server component
```

---

### You're importing a component that needs useState (Client Component)

**Message**: `You're importing a component that needs useState. It only works in a Client Component`

**Cause**: Client features used in Server Component

**Solutions**:
```typescript
// ❌ Error: Hook in Server Component
// app/page.tsx (default Server Component)
import { useState } from 'react';  // Error

export default function Page() {
  const [count, setCount] = useState(0);  // Error
  return <div>{count}</div>;
}

// ✅ Fix 1: Add 'use client'
'use client';

import { useState } from 'react';

export default function Page() {
  const [count, setCount] = useState(0);
  return <div>{count}</div>;
}

// ✅ Fix 2: Separate Client Component
// components/Counter.tsx
'use client';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// app/page.tsx (keep as Server Component)
import { Counter } from '@/components/Counter';
export default function Page() {
  return <Counter />;
}
```

---

### Error: Unsupported Server Component type

**Cause**: Non-serializable value passed from Server to Client

**Solutions**:
```typescript
// ❌ Error: Passing function from Server → Client
<ClientComponent onClick={() => console.log('click')} />

// ✅ Fix 1: Use Server Action
'use server';
async function handleClick() {
  console.log('click');
}

<ClientComponent onClick={handleClick} />

// ✅ Fix 2: Define in Client Component
// ClientComponent.tsx
'use client';
export function ClientComponent() {
  const handleClick = () => console.log('click');
  return <button onClick={handleClick}>Click</button>;
}
```

---

## 🟠 Build Errors

### Dynamic server usage

**Message**: `Dynamic server usage: Page couldn't be rendered statically`

**Cause**: Dynamic API used in static page

**Solutions**:
```typescript
// Cause: Using cookies(), headers(), etc.
import { cookies } from 'next/headers';

export default function Page() {
  const cookieStore = cookies();  // Requires dynamic rendering
  return <div>...</div>;
}

// Fix 1: Set dynamic
export const dynamic = 'force-dynamic';

// Fix 2: Change to dynamic route
// app/[slug]/page.tsx

// Fix 3: Provide generateStaticParams
export async function generateStaticParams() {
  return [{ slug: 'a' }, { slug: 'b' }];
}
```

---

### Error during SSG

**Cause**: Error during static generation

**Solutions**:
```typescript
// Cause: External API failure
export async function generateStaticParams() {
  const posts = await fetchPosts();  // Build fails if API fails
  return posts.map(p => ({ id: p.id }));
}

// Fix: Error handling
export async function generateStaticParams() {
  try {
    const posts = await fetchPosts();
    return posts.map(p => ({ id: p.id }));
  } catch {
    return [];  // Return empty array
  }
}
```

---

## 🟡 Runtime Errors

### NEXT_REDIRECT

**Message**: `NEXT_REDIRECT` error (normal behavior)

**Explanation**: Normal behavior of `redirect()` function

**Solutions**:
```typescript
// redirect() internally throws an error
// Be careful not to catch in try-catch

// ❌ Problem
try {
  redirect('/login');
} catch (e) {
  console.log(e);  // NEXT_REDIRECT caught
}

// ✅ Fix: Check redirect type
import { isRedirectError } from 'next/dist/client/components/redirect';

try {
  redirect('/login');
} catch (e) {
  if (isRedirectError(e)) throw e;  // Re-throw
  console.log(e);
}
```

---

### fetch failed

**Cause**: Fetch failed in server component

**Solutions**:
```typescript
// Add error handling
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 }
  });

  if (!res.ok) {
    // Route to error page
    throw new Error('Failed to fetch data');
  }

  return res.json();
}

// Or use notFound()
import { notFound } from 'next/navigation';

async function getData(id: string) {
  const res = await fetch(`/api/items/${id}`);
  if (!res.ok) notFound();
  return res.json();
}
```

---

## 🔧 Config Errors

### Invalid next.config.js options

**Solutions**:
```javascript
// next.config.js type check
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Use only valid options
};

module.exports = nextConfig;
```

---

### Conflicting paths

**Cause**: Route conflict

**Solutions**:
```
// Conflict example
app/blog/[slug]/page.tsx
app/blog/new/page.tsx      // Conflicts with [slug]

// Fix: Reorder or use route groups
app/blog/(list)/page.tsx
app/blog/(detail)/[slug]/page.tsx
```

---

## 📊 Error Frequency

| Error | Frequency | Severity |
|-------|-----------|----------|
| Server/Client confusion | High | High |
| Hydration Mismatch | High | Medium |
| Dynamic server usage | Medium | Medium |
| Module not found | Medium | Low |

---

## 🔧 Debugging

```bash
# Detailed build logs
next build --debug

# Bundle analysis
ANALYZE=true next build

# Local production mode
next build && next start
```

---

**META**
- Category: nextjs
- Last Updated: 2026-01-30
