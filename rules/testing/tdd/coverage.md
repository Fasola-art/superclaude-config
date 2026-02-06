# Coverage Strategy

## COV-001: Happy Path First

```typescript
describe('PaymentProcessor', () => {
  it('should process valid payment', () => {
    const result = processor.charge({
      amount: 100,
      cardNumber: '4242424242424242',
      expiry: '12/25',
    });
    expect(result.success).toBe(true);
  });
});
```

## COV-002: Error Paths

```typescript
describe('PaymentProcessor', () => {
  it('should reject expired card', () => {
    expect(() => processor.charge({
      amount: 100,
      cardNumber: '4242424242424242',
      expiry: '01/20',
    })).toThrow('Card expired');
  });

  it('should handle network timeout', async () => {
    mockNetwork.simulateTimeout();
    await expect(processor.charge(validPayment))
      .rejects.toThrow('Network timeout');
  });
});
```

## COV-003: Boundary Conditions

```typescript
describe('Pagination', () => {
  it('should return first page', () => {
    expect(paginate(items, { page: 1 })).toHaveLength(10);
  });

  it('should return empty beyond data', () => {
    expect(paginate(items, { page: 999 })).toHaveLength(0);
  });

  it('should treat page 0 as page 1', () => {
    expect(paginate(items, { page: 0 })).toEqual(
      paginate(items, { page: 1 })
    );
  });

  it('should reject negative pages', () => {
    expect(() => paginate(items, { page: -1 }))
      .toThrow('Invalid page number');
  });
});
```

---

## Test Structure (AAA)

```typescript
it('should apply discount', () => {
  // Arrange
  const order = new Order();
  order.addItem({ name: 'Widget', price: 100 });
  const discount = new PercentDiscount(10);

  // Act
  order.applyDiscount(discount);

  // Assert
  expect(order.total).toBe(90);
});
```

## One Concept Per Test

```typescript
// BAD: Multiple unrelated assertions
it('should process order', () => {
  expect(order.isValid).toBe(true);
  expect(order.total).toBe(100);
  expect(user.orders.length).toBe(1);
});

// GOOD: Separate tests
it('should validate order', () => { expect(order.isValid).toBe(true); });
it('should calculate total', () => { expect(order.total).toBe(100); });
```

## Descriptive Names

```typescript
// BAD: 'should work', 'test user'
// GOOD
it('should return empty array when no users found');
it('should throw ValidationError when email is invalid');
it('should retry 3 times on network failure');
```
