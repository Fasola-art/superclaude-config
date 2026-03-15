# E2E User Flow Testing

## FLOW-001: Identify Critical Paths

```typescript
// Priority 1: Revenue-generating
// - User registration → Purchase → Checkout
// - Login → Browse → Add to cart → Payment

// Priority 2: Core functionality
// - Search → Filter → View results
// - Create account → Verify email

// Priority 3: Error recovery
// - Failed payment → Retry → Success
// - Session timeout → Re-login
```

## FLOW-002: Complete User Journeys

```typescript
test('user can complete purchase', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'user@example.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="login-btn"]');

  // Add item to cart
  await page.goto('/products/widget-123');
  await page.click('[data-testid="add-to-cart"]');

  // Checkout
  await page.click('[data-testid="checkout-btn"]');
  await page.fill('[data-testid="card-number"]', '4242424242424242');
  await page.click('[data-testid="pay-btn"]');

  // Verify
  await expect(page.locator('[data-testid="success-message"]'))
    .toBeVisible();
});
```

## FLOW-003: Test Real Scenarios

```typescript
// BAD: Testing in isolation
test('button is clickable', async ({ page }) => {
  await page.click('button');
});

// GOOD: Test user intent
test('user can submit contact form', async ({ page }) => {
  await page.goto('/contact');
  await page.fill('[data-testid="name"]', 'John Doe');
  await page.fill('[data-testid="email"]', 'john@example.com');
  await page.fill('[data-testid="message"]', 'Hello!');
  await page.click('[data-testid="submit"]');

  await expect(page.locator('[data-testid="success-toast"]'))
    .toContainText('Message sent');
});
```

## FLOW-004: Error States

```typescript
test('shows error for invalid payment', async ({ page }) => {
  await loginAndAddToCart(page);

  await page.fill('[data-testid="card-number"]', '4000000000000002');
  await page.click('[data-testid="pay-btn"]');

  await expect(page.locator('[data-testid="error-message"]'))
    .toContainText('Card declined');
  await expect(page.locator('[data-testid="retry-btn"]'))
    .toBeVisible();
});
```

---

## Async Handling

### Auto-Wait (Preferred)
```typescript
await page.click('[data-testid="submit"]');  // Auto-waits
await expect(page.locator('.success')).toBeVisible();
```

### Explicit Waits
```typescript
await page.waitForURL('/dashboard');
await page.waitForLoadState('networkidle');

await Promise.all([
  page.waitForResponse('/api/users'),
  page.click('[data-testid="load-users"]'),
]);
```

### Avoid Fixed Timeouts
```typescript
// BAD: await page.waitForTimeout(3000);
// GOOD
await expect(page.locator('[data-testid="result"]'))
  .toBeVisible({ timeout: 10000 });
```
