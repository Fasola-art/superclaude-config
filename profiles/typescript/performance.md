# Performance & Testing Rules

## Performance Checklist

| Item | How to Check | Target |
|------|--------------|--------|
| **Bundle size** | `npx @next/bundle-analyzer` | < 100KB initial |
| **LCP** | Lighthouse | < 2.5s |
| **CLS** | Lighthouse | < 0.1 |
| **Re-renders** | React DevTools | Zero unnecessary |

## Optimization Patterns

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
  priority
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

---

## Testing Strategy

| Test Type | Tool | Coverage |
|-----------|------|----------|
| Unit Test | Vitest/Jest | 80% |
| Component | Testing Library | 100% core |
| E2E | Playwright | 100% Happy Path |
| Type Test | tsd, expect-type | Utility types |

## Test Patterns

```typescript
// Component test
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('clicking button increments counter', async () => {
  render(<Counter />);
  await userEvent.click(screen.getByRole('button', { name: /increment/i }));
  expect(screen.getByText('1')).toBeInTheDocument();
});

// Type test
import { expectTypeOf } from 'expect-type';

test('fetchUser return type', () => {
  expectTypeOf(fetchUser).returns.toMatchTypeOf<Promise<Result<User>>>();
});
```
