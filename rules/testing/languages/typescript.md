# TypeScript Testing (Vitest/Jest)

## Type-Safe Mocks

```typescript
import { vi, type Mock } from 'vitest';

interface UserRepository {
  findById(id: string): Promise<User | null>;
}

const mockRepo: UserRepository = {
  findById: vi.fn(),
};

it('should find user', async () => {
  vi.mocked(mockRepo.findById).mockResolvedValue({ id: '1', name: 'Alice' });

  const user = await service.getUser('1');
  expect(user?.name).toBe('Alice');
});
```

## Async Testing

```typescript
// async/await
it('should fetch user', async () => {
  const user = await fetchUser('123');
  expect(user.name).toBe('Alice');
});

// Promise rejection
it('should reject invalid id', () => {
  return expect(fetchUser('')).rejects.toThrow('Invalid ID');
});
```

## Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      reporter: ['text', 'json', 'html'],
      threshold: { lines: 80, branches: 80 },
    },
  },
});
```

## Parallel Tests

```typescript
describe.concurrent('API tests', () => {
  it('should fetch users', async () => { /* ... */ });
  it('should fetch posts', async () => { /* ... */ });
});
```

---

## Commands

```bash
npm test              # Run all
npm test -- --watch   # Watch mode
npm test -- --coverage
```
