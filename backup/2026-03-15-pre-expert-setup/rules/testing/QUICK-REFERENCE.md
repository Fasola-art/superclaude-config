# Testing Quick Reference

## TDD Cycle

| Step | Action | Rule |
|------|--------|------|
| 🔴 Red | Write failing test | CYCLE-001 |
| 🟢 Green | Minimal code to pass | CYCLE-002 |
| 🔵 Refactor | Clean up, tests green | CYCLE-003 |

**Golden Rule**: Never write production code without a failing test first.

---

## Test Structure (AAA)

```typescript
it('should apply discount', () => {
  // Arrange
  const order = new Order();
  order.addItem({ price: 100 });

  // Act
  order.applyDiscount(10);

  // Assert
  expect(order.total).toBe(90);
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

## E2E Selectors

```typescript
// GOOD: Stable
await page.click('[data-testid="submit-btn"]');
await page.getByRole('button', { name: 'Submit' });

// BAD: Fragile
await page.click('.btn-primary');
await page.click('button:nth-child(2)');
```

---

## Mocking Quick Guide

```typescript
// Stub: Returns canned data
const stub = { findById: () => ({ id: '1' }) };

// Mock: Verifies interactions
const mock = { save: vi.fn() };
expect(mock.save).toHaveBeenCalled();

// Spy: Wraps real implementation
const spy = vi.spyOn(repo, 'findById');
```

---

## Commands

```bash
# TypeScript
npm test -- --watch --coverage

# Python
pytest -v --cov=src

# Go
go test -race -cover ./...

# Playwright
npx playwright test --ui
```

---

**Related**: [index.md](index.md) | [tdd/](tdd/) | [e2e/](e2e/)
