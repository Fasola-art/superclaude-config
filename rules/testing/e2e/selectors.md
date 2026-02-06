# E2E Selectors

## SEL-001: data-testid Attributes

```typescript
// BAD: Fragile selectors
await page.click('.btn-primary');           // CSS class changes
await page.click('button:nth-child(2)');    // Position changes
await page.click('//div[@class="header"]'); // XPath brittle

// GOOD: Stable test IDs
await page.click('[data-testid="submit-btn"]');
await page.fill('[data-testid="email-input"]', 'test@example.com');
```

## SEL-002: Semantic Fallback

```typescript
// When data-testid not available
await page.getByRole('button', { name: 'Submit' });
await page.getByLabel('Email address');
await page.getByPlaceholder('Enter your email');
await page.getByText('Welcome back');
```

## SEL-003: Avoid Implementation Details

```typescript
// BAD: Testing implementation
await page.click('#react-select-2-option-0');
await page.locator('.MuiButton-root');

// GOOD: User-visible behavior
await page.getByRole('combobox').click();
await page.getByRole('option', { name: 'United States' }).click();
```

---

## Selector Priority

| Priority | Selector Type | Example |
|----------|--------------|---------|
| 1 | data-testid | `[data-testid="submit"]` |
| 2 | Role | `getByRole('button')` |
| 3 | Label | `getByLabel('Email')` |
| 4 | Placeholder | `getByPlaceholder('Enter')` |
| 5 | Text | `getByText('Submit')` |
| ❌ | CSS Class | `.btn-primary` |
| ❌ | XPath | `//div[@class]` |

---

## Adding Test IDs

```tsx
// React component
<button data-testid="submit-btn" onClick={handleSubmit}>
  Submit
</button>

<input
  data-testid="email-input"
  type="email"
  placeholder="Email"
/>
```

## Convention

```
data-testid="[component]-[element]-[modifier]"

Examples:
- login-form-submit-btn
- user-profile-avatar
- cart-item-remove-btn
- modal-close-btn
```
