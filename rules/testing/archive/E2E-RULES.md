# E2E Rules (End-to-End Testing)

> **Version**: 2026.01
> **Target**: Playwright, Cypress
> **Goal**: Test complete user workflows reliably

---

## ⚡ Quick Start

| Phase | Action | Output |
|-------|--------|--------|
| 1 | Identify critical user flows | Flow list |
| 2 | Write test scenarios | Test specs |
| 3 | Implement with page objects | Test files |
| 4 | Run in CI pipeline | Automated verification |

**Golden Rule**: Test what users do, not implementation details.

---

## Priority Summary

| Priority | Category | Rules | Key Effect |
|----------|----------|-------|------------|
| CRITICAL | FLOW | 4 | Critical path coverage |
| CRITICAL | SELECTOR | 3 | Stable element selection |
| HIGH | PATTERN | 5 | Maintainable test code |
| HIGH | WAIT | 3 | Reliable async handling |
| MEDIUM | A11Y | 3 | Accessibility compliance |
| MEDIUM | TOOL | 7 | Playwright/Cypress best practices |
| LOW | CI | 3 | CI/CD integration |

---

## CRITICAL: FLOW (User Flow Testing)

### FLOW-001: Identify Critical Paths

**Test the flows that matter most to business.**

```typescript
// Priority 1: Revenue-generating flows
// - User registration → Purchase → Checkout
// - Login → Browse → Add to cart → Payment

// Priority 2: Core functionality
// - Search → Filter → View results
// - Create account → Verify email

// Priority 3: Error recovery
// - Failed payment → Retry → Success
// - Session timeout → Re-login
```

### FLOW-002: Complete User Journeys

```typescript
// Test the full flow, not isolated steps
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

  // Verify success
  await expect(page.locator('[data-testid="success-message"]'))
    .toBeVisible();
});
```

### FLOW-003: Test Real Scenarios

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

### FLOW-004: Cover Error States

```typescript
test('shows error for invalid payment', async ({ page }) => {
  await loginAndAddToCart(page);

  // Use invalid card
  await page.fill('[data-testid="card-number"]', '4000000000000002');
  await page.click('[data-testid="pay-btn"]');

  // Verify error handling
  await expect(page.locator('[data-testid="error-message"]'))
    .toContainText('Card declined');

  // Verify recovery is possible
  await expect(page.locator('[data-testid="retry-btn"]'))
    .toBeVisible();
});
```

---

## CRITICAL: SELECTOR (Element Selection)

### SEL-001: Use data-testid Attributes

```typescript
// BAD: Fragile selectors
await page.click('.btn-primary');           // CSS class can change
await page.click('button:nth-child(2)');    // Position can change
await page.click('//div[@class="header"]'); // XPath is brittle

// GOOD: Stable test IDs
await page.click('[data-testid="submit-btn"]');
await page.fill('[data-testid="email-input"]', 'test@example.com');
```

### SEL-002: Semantic Selectors as Fallback

```typescript
// When data-testid not available, use semantic selectors
await page.getByRole('button', { name: 'Submit' });
await page.getByLabel('Email address');
await page.getByPlaceholder('Enter your email');
await page.getByText('Welcome back');
```

### SEL-003: Avoid Implementation Details

```typescript
// BAD: Testing implementation
await page.click('#react-select-2-option-0');
await page.locator('.MuiButton-root');

// GOOD: Testing user-visible behavior
await page.getByRole('combobox').click();
await page.getByRole('option', { name: 'United States' }).click();
```

---

## HIGH: PATTERN (Test Patterns)

### PAT-001: Page Object Model

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="login-btn"]');
  }

  async getErrorMessage() {
    return this.page.locator('[data-testid="error"]').textContent();
  }
}

// tests/login.spec.ts
test('successful login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

### PAT-002: Component Objects

```typescript
// components/DataTable.ts
export class DataTable {
  constructor(private locator: Locator) {}

  async getRowCount() {
    return this.locator.locator('tbody tr').count();
  }

  async clickRow(index: number) {
    await this.locator.locator(`tbody tr:nth-child(${index + 1})`).click();
  }

  async sortByColumn(name: string) {
    await this.locator.getByRole('columnheader', { name }).click();
  }
}
```

### PAT-003: Test Fixtures

```typescript
// fixtures/auth.ts
import { test as base } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

type AuthFixtures = {
  loginPage: LoginPage;
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixtures>({
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'test@example.com');
    await page.fill('[data-testid="password"]', 'password');
    await page.click('[data-testid="login-btn"]');
    await page.waitForURL('/dashboard');
    await use(page);
  },
});
```

### PAT-004: Test Data Management

```typescript
// fixtures/testData.ts
export const testUsers = {
  standard: {
    email: 'standard@test.com',
    password: 'Test123!',
  },
  admin: {
    email: 'admin@test.com',
    password: 'Admin123!',
  },
};

// API setup for test data
async function seedTestData(request: APIRequestContext) {
  await request.post('/api/test/seed', {
    data: { users: testUsers },
  });
}
```

### PAT-005: Auth State Reuse

**Save authentication state to avoid repeated logins.**

```typescript
// auth.setup.ts - Run once before all tests
import { test as setup } from '@playwright/test';

const authFile = '.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', process.env.TEST_USER!);
  await page.fill('[data-testid="password"]', process.env.TEST_PASS!);
  await page.click('[data-testid="login-btn"]');
  await page.waitForURL('/dashboard');

  // Save auth state for reuse
  await page.context().storageState({ path: authFile });
});

// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      dependencies: ['setup'],
      use: { storageState: '.auth/user.json' },
    },
  ],
});
```

---

## HIGH: WAIT (Async Handling)

### WAIT-001: Auto-Wait (Preferred)

```typescript
// Playwright auto-waits for elements
await page.click('[data-testid="submit"]');  // Waits for element
await expect(page.locator('.success')).toBeVisible();  // Waits for condition
```

### WAIT-002: Explicit Waits When Needed

```typescript
// Wait for specific conditions
await page.waitForURL('/dashboard');
await page.waitForLoadState('networkidle');
await page.waitForSelector('[data-testid="loaded"]');

// Wait for API response
await Promise.all([
  page.waitForResponse('/api/users'),
  page.click('[data-testid="load-users"]'),
]);
```

### WAIT-003: Avoid Fixed Timeouts

```typescript
// BAD: Fixed sleep
await page.waitForTimeout(3000);

// GOOD: Wait for condition
await expect(page.locator('[data-testid="result"]'))
  .toBeVisible({ timeout: 10000 });

// GOOD: Wait for network
await page.waitForLoadState('networkidle');
```

---

## MEDIUM: A11Y (Accessibility Testing)

### A11Y-001: Automated Accessibility Checks

**Use axe-core for automated WCAG compliance testing.**

```typescript
// Playwright with @axe-core/playwright
import AxeBuilder from '@axe-core/playwright';

test('homepage has no accessibility violations', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page }).analyze();

  expect(results.violations).toEqual([]);
});

// Check specific WCAG levels
test('meets WCAG 2.1 AA standards', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### A11Y-002: Keyboard Navigation

```typescript
test('form is keyboard navigable', async ({ page }) => {
  await page.goto('/contact');

  // Tab through form elements
  await page.keyboard.press('Tab');
  await expect(page.locator('[data-testid="name"]')).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(page.locator('[data-testid="email"]')).toBeFocused();

  // Submit with Enter
  await page.keyboard.press('Enter');
  await expect(page.locator('[data-testid="success"]')).toBeVisible();
});
```

### A11Y-003: Screen Reader Testing

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

## MEDIUM: TOOL (Tool-Specific Patterns)

### Playwright

#### PW-001: Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 30000,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

#### PW-002: API Testing

```typescript
test('API responds correctly', async ({ request }) => {
  const response = await request.get('/api/users');
  expect(response.ok()).toBeTruthy();

  const users = await response.json();
  expect(users).toHaveLength(10);
});
```

#### PW-003: Visual Testing

```typescript
test('homepage visual regression', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100,
  });
});
```

### Cypress

#### CY-001: Configuration

```javascript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: false,
    screenshotOnRunFailure: true,
    retries: {
      runMode: 2,
      openMode: 0,
    },
  },
});
```

#### CY-002: Custom Commands

```typescript
// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.get('[data-testid="email"]').type(email);
  cy.get('[data-testid="password"]').type(password);
  cy.get('[data-testid="login-btn"]').click();
  cy.url().should('include', '/dashboard');
});

// Usage
cy.login('user@example.com', 'password');
```

#### CY-003: Intercept Network

```typescript
cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers');
cy.visit('/users');
cy.wait('@getUsers');
cy.get('[data-testid="user-list"]').should('have.length', 10);
```

#### CY-004: Visual Testing

```typescript
// Using cypress-image-snapshot
import { addMatchImageSnapshotCommand } from 'cypress-image-snapshot/command';
addMatchImageSnapshotCommand();

// In test file
describe('Visual Regression', () => {
  it('homepage matches snapshot', () => {
    cy.visit('/');
    cy.matchImageSnapshot('homepage');
  });

  it('login form matches snapshot', () => {
    cy.visit('/login');
    cy.get('[data-testid="login-form"]').matchImageSnapshot('login-form');
  });
});

// cypress.config.ts
export default defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      const { addMatchImageSnapshotPlugin } = require('cypress-image-snapshot/plugin');
      addMatchImageSnapshotPlugin(on, config);
    },
  },
});
```

---

## LOW: CI (CI/CD Integration)

### CI-001: GitHub Actions

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

### CI-002: Parallel Execution

```typescript
// playwright.config.ts
export default defineConfig({
  workers: process.env.CI ? 4 : undefined,
  fullyParallel: true,
});
```

### CI-003: Test Sharding

```yaml
# Run tests across multiple machines
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: npx playwright test --shard=${{ matrix.shard }}/4
```

---

## Checklist

### Before Writing Tests
- [ ] Critical user flows identified
- [ ] Test data strategy defined
- [ ] data-testid attributes added to components
- [ ] Page objects structure planned

### Test Implementation
- [ ] Tests run independently
- [ ] No fixed timeouts (use explicit waits)
- [ ] Error scenarios covered
- [ ] Visual regressions tracked

### CI/CD Integration
- [ ] Tests run on every PR
- [ ] Failed tests block merge
- [ ] Artifacts uploaded for debugging
- [ ] Parallel execution configured

---

## Commands

```bash
# Playwright
npx playwright test                    # Run all tests
npx playwright test --ui               # Interactive UI mode
npx playwright test --debug            # Debug mode
npx playwright show-report             # View HTML report
npx playwright codegen                 # Generate tests

# Cypress
npx cypress open                       # Interactive mode
npx cypress run                        # Headless mode
npx cypress run --spec "path/to/spec"  # Run specific spec
```

---

**META**
- Version: 2026.01
- Last Updated: 2026-02-01
- Category: E2E Testing
