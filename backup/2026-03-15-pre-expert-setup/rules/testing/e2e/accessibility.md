# E2E Accessibility Testing

## A11Y-001: Automated Checks (axe-core)

```typescript
import AxeBuilder from '@axe-core/playwright';

test('homepage has no a11y violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

// WCAG level specific
test('meets WCAG 2.1 AA', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

## A11Y-002: Keyboard Navigation

```typescript
test('form is keyboard navigable', async ({ page }) => {
  await page.goto('/contact');

  // Tab through elements
  await page.keyboard.press('Tab');
  await expect(page.locator('[data-testid="name"]')).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(page.locator('[data-testid="email"]')).toBeFocused();

  // Submit with Enter
  await page.keyboard.press('Enter');
  await expect(page.locator('[data-testid="success"]')).toBeVisible();
});
```

## A11Y-003: Screen Reader Support

### Images have alt text
```typescript
test('images have alt text', async ({ page }) => {
  await page.goto('/');

  const images = page.locator('img');
  const count = await images.count();

  for (let i = 0; i < count; i++) {
    const alt = await images.nth(i).getAttribute('alt');
    expect(alt).toBeTruthy();
  }
});
```

### Form inputs have labels
```typescript
test('form inputs have labels', async ({ page }) => {
  await page.goto('/signup');

  const inputs = page.locator('input:not([type="hidden"])');
  const count = await inputs.count();

  for (let i = 0; i < count; i++) {
    const input = inputs.nth(i);
    const id = await input.getAttribute('id');
    const label = page.locator(`label[for="${id}"]`);
    await expect(label).toBeVisible();
  }
});
```

---

## WCAG Checklist

| Level | Requirement |
|-------|-------------|
| A | Alt text, keyboard access, no auto-play |
| AA | Color contrast, resize text, focus visible |
| AAA | Sign language, extended audio, text alternatives |

---

## Common Issues

| Issue | Fix |
|-------|-----|
| Missing alt | Add `alt=""` for decorative, descriptive for meaningful |
| No focus indicator | Add `:focus-visible` styles |
| Low contrast | Ensure 4.5:1 for text, 3:1 for large text |
| No skip link | Add "Skip to content" link |
| Auto-playing media | Add pause/stop controls |
