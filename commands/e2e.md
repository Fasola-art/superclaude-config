---
description: E2E test creation for user workflows
argument-hint: "[flow-description]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "TodoWrite", "AskUserQuestion"]
---

# E2E Test Workflow

<e2e-command>

## Core Principles

1. **Test what users do** - Focus on complete user journeys
2. **Use stable selectors** - Prefer `data-testid` attributes
3. **Page Object pattern** - Keep tests maintainable
4. **Use TodoWrite** - Required for tasks with 3+ steps

---

## Phase 1: Identify User Flow

**Actions:**
1. List the critical user journey to test
2. Define start and end points
3. Identify key interactions and assertions

**Output:**
```markdown
## Flow: [Flow Name]

**User Journey:**
1. User navigates to [page]
2. User fills [form/input]
3. User clicks [button]
4. System shows [result]

**Critical Assertions:**
- [ ] Navigation works
- [ ] Form submission succeeds
- [ ] Success message appears
- [ ] Data persists correctly
```

---

## Phase 2: Plan Test Scenarios

**Actions:**
1. Happy path scenario
2. Error scenarios
3. Edge cases

**Template:**
```markdown
## Test Scenarios

### Happy Path
- [x] Complete flow works end-to-end

### Error Paths
- [ ] Invalid input shows error
- [ ] Network failure handled gracefully
- [ ] Session timeout handled

### Edge Cases
- [ ] Empty state
- [ ] Maximum data limits
- [ ] Concurrent actions
```

---

## Phase 3: Implement Tests

### Playwright (Recommended)

**Page Object:**
```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(private page: Page) {
    this.emailInput = page.locator('[data-testid="email"]');
    this.passwordInput = page.locator('[data-testid="password"]');
    this.submitButton = page.locator('[data-testid="login-btn"]');
    this.errorMessage = page.locator('[data-testid="error"]');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}
```

**Test File:**
```typescript
// e2e/tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Login Flow', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome"]'))
      .toContainText('Welcome');
  });

  test('invalid credentials show error', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'wrong');

    await expect(loginPage.errorMessage)
      .toContainText('Invalid credentials');
  });
});
```

### Cypress

**Page Object:**
```typescript
// cypress/pages/LoginPage.ts
export class LoginPage {
  visit() {
    cy.visit('/login');
  }

  fillEmail(email: string) {
    cy.get('[data-testid="email"]').type(email);
  }

  fillPassword(password: string) {
    cy.get('[data-testid="password"]').type(password);
  }

  submit() {
    cy.get('[data-testid="login-btn"]').click();
  }

  login(email: string, password: string) {
    this.fillEmail(email);
    this.fillPassword(password);
    this.submit();
  }
}
```

**Test File:**
```typescript
// cypress/e2e/login.cy.ts
import { LoginPage } from '../pages/LoginPage';

describe('Login Flow', () => {
  const loginPage = new LoginPage();

  it('successful login redirects to dashboard', () => {
    loginPage.visit();
    loginPage.login('user@example.com', 'password123');

    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="welcome"]').should('contain', 'Welcome');
  });
});
```

---

## Phase 4: Run & Validate

**Commands:**
```bash
# Playwright
npx playwright test                    # Run all
npx playwright test --ui               # Interactive mode
npx playwright test login.spec.ts      # Single file
npx playwright show-report             # View report

# Cypress
npx cypress open                       # Interactive mode
npx cypress run                        # Headless
npx cypress run --spec "cypress/e2e/login.cy.ts"
```

**Validation Checklist:**
- [ ] All tests pass locally
- [ ] Tests pass in headless mode
- [ ] No flaky tests (run 3x)
- [ ] Reasonable execution time

---

## Phase 5: CI Integration

**GitHub Actions (Playwright):**
```yaml
# .github/workflows/e2e-playwright.yml
name: E2E Tests (Playwright)

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - name: Upload report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

**GitHub Actions (Cypress):**
```yaml
# .github/workflows/e2e-cypress.yml
name: E2E Tests (Cypress)

on: [push, pull_request]

jobs:
  cypress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Cypress run
        uses: cypress-io/github-action@v6
        with:
          build: npm run build
          start: npm start
          wait-on: 'http://localhost:3000'

      - name: Upload screenshots
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: cypress-screenshots
          path: cypress/screenshots/
```

---

## Selector Strategy

**Priority Order:**
1. `data-testid` - Most stable
2. `role` + `name` - Semantic
3. `label` - Form elements
4. `placeholder` - Input hints
5. `text` - Last resort

**Examples:**
```typescript
// Best: data-testid
page.locator('[data-testid="submit-btn"]')

// Good: Semantic
page.getByRole('button', { name: 'Submit' })
page.getByLabel('Email address')

// Acceptable: Text content
page.getByText('Welcome back')

// Avoid: CSS classes, XPath, nth-child
```

---

## Summary Output Template

```
## E2E Test Summary

### Flow Tested
[Flow Name]: [Brief description]

### Files Created
- e2e/pages/[Name]Page.ts - Page object
- e2e/tests/[name].spec.ts - Test specs

### Test Coverage
- ✅ Happy path
- ✅ Error scenarios
- ✅ Edge cases

### Run Command
- Playwright: npx playwright test [name].spec.ts
- Cypress: npx cypress run --spec cypress/e2e/[name].cy.ts

### CI Status
- [ ] GitHub Actions configured
- [ ] Tests pass in CI
```

---

## Advanced Patterns

### API Mocking

```typescript
// Playwright - Route interception
test('shows cached data on network failure', async ({ page }) => {
  await page.route('/api/users', route => {
    route.fulfill({
      status: 200,
      body: JSON.stringify([{ id: 1, name: 'Cached User' }]),
    });
  });

  await page.goto('/users');
  await expect(page.locator('[data-testid="user-name"]'))
    .toContainText('Cached User');
});

// Cypress - cy.intercept
cy.intercept('POST', '/api/login', {
  statusCode: 200,
  body: { token: 'fake-jwt-token' },
}).as('login');
```

### Environment Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
  },
  projects: [
    {
      name: 'staging',
      use: { baseURL: 'https://staging.example.com' },
    },
    {
      name: 'production',
      use: { baseURL: 'https://example.com' },
    },
  ],
});
```

</e2e-command>
