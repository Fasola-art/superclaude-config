# TDD Cycle Rules

## CYCLE-001: Red First

**Always start with a failing test.**

```typescript
describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});
// Calculator doesn't exist → Test fails ✓
```

## CYCLE-002: Minimal Green

**Write simplest code to pass.**

```typescript
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}
// Test passes → Move to refactor
```

**Anti-pattern**: Don't over-engineer.

## CYCLE-003: Refactor Safely

**Improve code, tests stay green.**

```typescript
class Calculator {
  add(a: number, b: number): number { return a + b; }
  subtract(a: number, b: number): number { return a - b; }
}
// Run tests after each refactor → All green ✓
```

## CYCLE-004: Small Steps

```typescript
// BAD: Writing large test suites first
describe('UserService', () => {
  it('should create user');
  it('should update user');
  // ... 20 more tests
});

// GOOD: One test at a time
describe('UserService', () => {
  it('should create user with valid email', () => {
    // Red → Green → Refactor
  });
  // Then add next test
});
```

---

## TEST-FIRST: Discipline

### Define Behavior First

```typescript
describe('EmailValidator', () => {
  it('should accept valid email', () => {
    expect(validator.isValid('user@example.com')).toBe(true);
  });
  it('should reject email without @', () => {
    expect(validator.isValid('userexample.com')).toBe(false);
  });
});
```

### Test Edge Cases Early

```typescript
describe('divide', () => {
  it('should divide numbers', () => { expect(divide(10, 2)).toBe(5); });
  it('should throw on zero', () => { expect(() => divide(10, 0)).toThrow(); });
  it('should handle negatives', () => { expect(divide(-10, 2)).toBe(-5); });
});
```

### Tests as Documentation

```typescript
describe('ShoppingCart', () => {
  describe('when adding items', () => {
    it('should increase item count', () => { /* ... */ });
    it('should update total price', () => { /* ... */ });
  });
});
```
