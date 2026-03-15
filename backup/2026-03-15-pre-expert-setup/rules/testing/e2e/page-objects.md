# Page Object Model

## PAT-001: Page Objects

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

## PAT-002: Component Objects

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

## PAT-003: Test Fixtures

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
    await use(new LoginPage(page));
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

## PAT-004: Test Data

```typescript
export const testUsers = {
  standard: { email: 'standard@test.com', password: 'Test123!' },
  admin: { email: 'admin@test.com', password: 'Admin123!' },
};

async function seedTestData(request: APIRequestContext) {
  await request.post('/api/test/seed', { data: { users: testUsers } });
}
```

## PAT-005: Auth State Reuse

```typescript
// auth.setup.ts
const authFile = '.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', process.env.TEST_USER!);
  await page.fill('[data-testid="password"]', process.env.TEST_PASS!);
  await page.click('[data-testid="login-btn"]');
  await page.waitForURL('/dashboard');
  await page.context().storageState({ path: authFile });
});

// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  { name: 'chromium', dependencies: ['setup'],
    use: { storageState: '.auth/user.json' } },
]
```
