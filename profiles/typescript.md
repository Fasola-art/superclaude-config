# TypeScript/React/Next.js Language Profile

> **Version**: 1.0.0
> **Target**: TypeScript 5.x, React 18+, Next.js 14+
> **Auto-detect**: Presence of `package.json` or `tsconfig.json`

---

## Goal

**Primary Outcome**: Generate type-safe and performance-optimized code in the TypeScript ecosystem

**Success Criteria**:
- [ ] Comply with `strict: true` mode
- [ ] Zero `any` types
- [ ] Bundle size optimized (no barrel imports)
- [ ] Proper Server/Client component separation

**Failure Cases**:
- `@ts-ignore` usage → Requires type fix
- Runtime type error → Add type guard

---

## Quick Reference

### Required Rules (Build fails on violation)

| Rule | Description | Example |
|------|-------------|---------|
| **strict mode** | tsconfig.json strict: true | No implicit any |
| **explicit return type** | Explicit function return types | `function fn(): string` |
| **null check** | Use optional chaining | `user?.name` |
| **no barrel** | Direct import | `from '@/Button'` |

### Recommended Rules

| Rule | Reason | Alternative |
|------|--------|-------------|
| `unknown` > `any` | Type safety | Narrow with type guard |
| `const assertion` | Preserve literal types | `as const` |
| `satisfies` | Type validation + inference | TS 4.9+ |

---

## Section 1: Type System Rules

### Type Definition Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `interface` | Object structure, extension needed | `interface User { name: string }` |
| `type` | Union, utility, complex types | `type Status = 'ok' \| 'error'` |
| `enum` | Avoid (tree-shaking issues) | `const STATUS = { ... } as const` |
| `const assertion` | Preserve literal values | `['a', 'b'] as const` |

### Type Writing Rules

```typescript
// GOOD: Explicit types
interface User {
  id: string;
  name: string;
  email: string | null;  // explicit null
  createdAt: Date;
}

// GOOD: Union types
type APIResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

// GOOD: Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### Anti-patterns

```typescript
// BAD: any usage
function process(data: any) { ... }

// BAD: Type assertion abuse
const user = response as User;  // without validation

// BAD: enum usage
enum Status { Active, Inactive }  // increases bundle size
```

### Exception Handling

| Situation | Solution |
|-----------|----------|
| External library has no types | `declare module 'lib'` or install `@types` |
| Complex type inference impossible | Add explicit type annotation |
| Legacy JS code integration | `// @ts-check` + JSDoc or gradual migration |

---

## Section 2: React Component Rules

### Component Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Server Component** | Data fetching, static UI | Default (no use client) |
| **Client Component** | Interaction, hooks | `'use client'` declaration |
| **Suspense boundary** | Async loading | `<Suspense fallback={...}>` |

### Component Type Patterns

```typescript
// GOOD: Props interface
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';  // optional
  children: React.ReactNode;
  onClick?: () => void;
}

// GOOD: Function component
function Button({ variant, size = 'md', children, onClick }: ButtonProps) {
  return (
    <button
      className={cn(styles[variant], styles[size])}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

// GOOD: forwardRef pattern
const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, ...props }, ref) {
    return <input ref={ref} {...props} />;
  }
);
```

### React Anti-patterns

```typescript
// BAD: React.FC usage (implicit children issue)
const Button: React.FC<Props> = ({ ... }) => { ... };

// BAD: Inline objects/functions (unnecessary re-renders)
<Child style={{ color: 'red' }} onClick={() => handle()} />

// BAD: Barrel import
import { Button, Input, Card } from '@/components';
```

### Exception Handling

| Situation | Solution |
|-----------|----------|
| Complex children type | Use `React.ReactNode` |
| Event type | `React.MouseEvent<HTMLButtonElement>` |
| Need ref forwarding | `forwardRef` pattern |

---

## Section 3: Next.js App Router Rules

### Routing Patterns

| File | Purpose | Notes |
|------|---------|-------|
| `page.tsx` | Route page | Server Component default |
| `layout.tsx` | Layout | Nestable, state preserved |
| `loading.tsx` | Loading UI | Auto Suspense applied |
| `error.tsx` | Error UI | `'use client'` required |
| `route.ts` | API Route | Export GET, POST, etc. |

### Data Fetching Patterns

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

### Next.js Anti-patterns

```typescript
// BAD: Unnecessary data fetching in Client Component
'use client';
function Page() {
  const [data, setData] = useState(null);
  useEffect(() => { fetch(...) }, []);  // Should be on server
}

// BAD: Sequential data fetching (waterfall)
const user = await getUser();
const posts = await getPosts(user.id);  // Parallelize if no dependency

// BAD: Excessive 'use client'
'use client';  // Unnecessary for static UI
function StaticCard() { return <div>...</div>; }
```

---

## Section 4: Import/Export Rules

### Import Order

```typescript
// 1. React/Next.js
import { useState } from 'react';
import Link from 'next/link';

// 2. External libraries
import { clsx } from 'clsx';
import { format } from 'date-fns';

// 3. Internal modules (absolute path)
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/lib/utils';

// 4. Relative path (same folder)
import { helpers } from './helpers';

// 5. Types (type-only import)
import type { User } from '@/types';

// 6. Styles
import styles from './styles.module.css';
```

### Export Patterns

```typescript
// GOOD: Named export (tree-shakable)
export function Button() { ... }
export function Input() { ... }

// GOOD: Separate type export
export type { ButtonProps, InputProps };

// GOOD: Constant export
export const BUTTON_VARIANTS = ['primary', 'secondary'] as const;
```

### Import Anti-patterns

```typescript
// BAD: Barrel import (increases bundle size)
import { Button, Input, Card, Modal } from '@/components';

// BAD: Import entire library
import _ from 'lodash';
import * as R from 'ramda';

// BAD: default export (refactoring difficult)
export default function Button() { ... }
```

---

## Section 5: Error Handling Rules

### Error Handling Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `Result<T, E>` | Expected failures | API calls, parsing |
| `try/catch` | Exceptional situations | External library calls |
| `Error Boundary` | React render errors | Prevent component crash |

### Error Handling Patterns

```typescript
// GOOD: Result type pattern
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) {
      return { ok: false, error: new Error(`HTTP ${res.status}`) };
    }
    const user = await res.json();
    return { ok: true, value: user };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e : new Error(String(e)) };
  }
}

// GOOD: Usage
const result = await fetchUser('123');
if (!result.ok) {
  console.error(result.error);
  return;
}
console.log(result.value.name);  // type safe
```

### Error Handling Anti-patterns

```typescript
// BAD: Ignore error
try {
  await riskyOperation();
} catch (e) {
  // do nothing
}

// BAD: any catch
catch (e: any) {
  console.log(e.message);
}

// BAD: throw string
throw 'Something went wrong';
```

---

## Section 6: Performance Optimization Rules

### Optimization Checklist

| Item | How to Check | Target |
|------|--------------|--------|
| **Bundle size** | `npx @next/bundle-analyzer` | < 100KB (initial) |
| **LCP** | Lighthouse | < 2.5s |
| **CLS** | Lighthouse | < 0.1 |
| **Re-renders** | React DevTools Profiler | Zero unnecessary re-renders |

### Optimization Patterns

```typescript
// GOOD: Dynamic import
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <Skeleton />,
  ssr: false
});

// GOOD: Memoization
const sortedItems = useMemo(
  () => items.sort((a, b) => a.price - b.price),
  [items]
);

// GOOD: Image optimization
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // LCP image
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

---

## Section 7: Testing Rules

### Test Strategy

| Test Type | Tool | Coverage Target |
|-----------|------|-----------------|
| Unit Test | Vitest/Jest | 80% |
| Component Test | Testing Library | 100% core components |
| E2E Test | Playwright | 100% Happy Path |
| Type Test | tsd, expect-type | Utility types |

### Test Patterns

```typescript
// GOOD: Component test
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('clicking button increments counter', async () => {
  render(<Counter />);

  await userEvent.click(screen.getByRole('button', { name: /increment/i }));

  expect(screen.getByText('1')).toBeInTheDocument();
});

// GOOD: Type test
import { expectTypeOf } from 'expect-type';

test('fetchUser return type', () => {
  expectTypeOf(fetchUser).returns.toMatchTypeOf<Promise<Result<User>>>();
});
```

---

## Self-Diagnosis Checklist

### Critical (Must Complete)
- [ ] `tsconfig.json` has `strict: true`
- [ ] Zero `any` type usage
- [ ] Zero barrel import usage
- [ ] Proper Server/Client component separation

### Important (80%+)
- [ ] All functions have explicit return types
- [ ] Unified error handling patterns
- [ ] Removed unnecessary re-renders
- [ ] Applied image optimization

### Nice-to-have
- [ ] Written type tests
- [ ] Performed bundle analysis
- [ ] Achieved Lighthouse 90+

**Pass Criteria**: Critical 100% + Important 80%+

---

## References

| Document | Link |
|----------|------|
| TypeScript Official | https://www.typescriptlang.org/docs/ |
| React Official | https://react.dev/ |
| Next.js Official | https://nextjs.org/docs |
| Vercel Best Practices | `~/.claude/rules/react/REACT-RULES.md` |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Auto-detect: `package.json`, `tsconfig.json`
