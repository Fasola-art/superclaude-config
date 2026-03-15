# Test Fundamentals (Shared)

> Common testing patterns for unit/integration/E2E

---

## AAA Pattern

```typescript
it('should process order', () => {
  // Arrange: Set up test data
  const order = new Order();
  order.addItem({ name: 'Widget', price: 100 });

  // Act: Execute behavior
  order.applyDiscount(10);

  // Assert: Verify result
  expect(order.total).toBe(90);
});
```

---

## Test Naming

```typescript
// Pattern: should [expected behavior] when [condition]
it('should return empty array when no users found');
it('should throw ValidationError when email is invalid');
it('should retry 3 times on network failure');
```

---

## Test Isolation

```typescript
describe('User', () => {
  let user: User;

  beforeEach(() => {
    user = createUser({ name: 'Alice' });  // Fresh instance
  });

  afterEach(() => {
    vi.clearAllMocks();  // Reset mocks
  });

  it('test 1', () => { /* ... */ });
  it('test 2', () => { /* ... */ });
});
```

---

## Coverage Strategy

| Type | Focus |
|------|-------|
| Happy Path | Normal operation |
| Error Path | Exception handling |
| Boundary | Edge cases (0, null, max) |

---

**Related**: [ci-integration.md](ci-integration.md)
