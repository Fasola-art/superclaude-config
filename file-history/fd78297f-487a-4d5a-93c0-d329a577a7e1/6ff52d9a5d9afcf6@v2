# E2E 가이드 (End-to-End 테스트)

> **버전**: 2026.01
> **대상**: Playwright, Cypress
> **목표**: 완전한 사용자 워크플로우를 신뢰성 있게 테스트

---

## ⚡ 빠른 시작

| 단계 | 행동 | 결과 |
|------|------|------|
| 1 | 핵심 사용자 플로우 식별 | 플로우 목록 |
| 2 | 테스트 시나리오 작성 | 테스트 스펙 |
| 3 | 페이지 객체로 구현 | 테스트 파일 |
| 4 | CI 파이프라인에서 실행 | 자동 검증 |

**황금 규칙**: 구현 세부사항이 아닌, 사용자가 하는 것을 테스트하세요.

---

## 우선순위 요약

| 우선순위 | 카테고리 | 규칙 수 | 핵심 효과 |
|----------|----------|---------|-----------|
| CRITICAL | FLOW | 4 | 핵심 경로 커버리지 |
| CRITICAL | SELECTOR | 3 | 안정적인 요소 선택 |
| HIGH | PATTERN | 5 | 유지보수 가능한 테스트 코드 |
| HIGH | WAIT | 3 | 신뢰성 있는 비동기 처리 |
| MEDIUM | A11Y | 3 | 접근성 준수 |
| MEDIUM | TOOL | 7 | Playwright/Cypress 모범 사례 |
| LOW | CI | 3 | CI/CD 통합 |

---

## CRITICAL: FLOW (사용자 플로우 테스트)

### FLOW-001: 핵심 경로 식별

**비즈니스에 가장 중요한 플로우를 테스트하세요.**

```typescript
// 우선순위 1: 수익 창출 플로우
// - 사용자 가입 → 구매 → 결제
// - 로그인 → 둘러보기 → 장바구니 추가 → 결제

// 우선순위 2: 핵심 기능
// - 검색 → 필터 → 결과 보기
// - 계정 생성 → 이메일 인증

// 우선순위 3: 오류 복구
// - 결제 실패 → 재시도 → 성공
// - 세션 타임아웃 → 재로그인
```

### FLOW-002: 완전한 사용자 여정

```typescript
// 전체 플로우를 테스트, 개별 단계가 아님
test('사용자가 구매를 완료할 수 있다', async ({ page }) => {
  // 로그인
  await page.goto('/login');
  await page.fill('[data-testid="email"]', 'user@example.com');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="login-btn"]');

  // 장바구니에 아이템 추가
  await page.goto('/products/widget-123');
  await page.click('[data-testid="add-to-cart"]');

  // 결제
  await page.click('[data-testid="checkout-btn"]');
  await page.fill('[data-testid="card-number"]', '4242424242424242');
  await page.click('[data-testid="pay-btn"]');

  // 성공 확인
  await expect(page.locator('[data-testid="success-message"]'))
    .toBeVisible();
});
```

### FLOW-003: 실제 시나리오 테스트

```typescript
// BAD: 고립된 테스트
test('버튼이 클릭 가능하다', async ({ page }) => {
  await page.click('button');
});

// GOOD: 사용자 의도 테스트
test('사용자가 문의 폼을 제출할 수 있다', async ({ page }) => {
  await page.goto('/contact');
  await page.fill('[data-testid="name"]', 'John Doe');
  await page.fill('[data-testid="email"]', 'john@example.com');
  await page.fill('[data-testid="message"]', '안녕하세요!');
  await page.click('[data-testid="submit"]');

  await expect(page.locator('[data-testid="success-toast"]'))
    .toContainText('메시지가 전송되었습니다');
});
```

### FLOW-004: 오류 상태 커버

```typescript
test('잘못된 결제에 대해 오류를 표시한다', async ({ page }) => {
  await loginAndAddToCart(page);

  // 유효하지 않은 카드 사용
  await page.fill('[data-testid="card-number"]', '4000000000000002');
  await page.click('[data-testid="pay-btn"]');

  // 오류 처리 확인
  await expect(page.locator('[data-testid="error-message"]'))
    .toContainText('카드가 거부되었습니다');

  // 복구 가능 확인
  await expect(page.locator('[data-testid="retry-btn"]'))
    .toBeVisible();
});
```

---

## CRITICAL: SELECTOR (요소 선택)

### SEL-001: data-testid 속성 사용

```typescript
// BAD: 취약한 셀렉터
await page.click('.btn-primary');           // CSS 클래스는 변경될 수 있음
await page.click('button:nth-child(2)');    // 위치는 변경될 수 있음
await page.click('//div[@class="header"]'); // XPath는 취약함

// GOOD: 안정적인 테스트 ID
await page.click('[data-testid="submit-btn"]');
await page.fill('[data-testid="email-input"]', 'test@example.com');
```

### SEL-002: 시맨틱 셀렉터를 대안으로

```typescript
// data-testid가 없을 때 시맨틱 셀렉터 사용
await page.getByRole('button', { name: '제출' });
await page.getByLabel('이메일 주소');
await page.getByPlaceholder('이메일을 입력하세요');
await page.getByText('다시 오신 것을 환영합니다');
```

### SEL-003: 구현 세부사항 피하기

```typescript
// BAD: 구현 테스트
await page.click('#react-select-2-option-0');
await page.locator('.MuiButton-root');

// GOOD: 사용자에게 보이는 동작 테스트
await page.getByRole('combobox').click();
await page.getByRole('option', { name: '대한민국' }).click();
```

---

## HIGH: PATTERN (테스트 패턴)

### PAT-001: 페이지 객체 모델

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
test('성공적인 로그인', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

### PAT-002: 컴포넌트 객체

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

### PAT-003: 테스트 Fixture

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

### PAT-004: 테스트 데이터 관리

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

// API 설정으로 테스트 데이터
async function seedTestData(request: APIRequestContext) {
  await request.post('/api/test/seed', {
    data: { users: testUsers },
  });
}
```

### PAT-005: 인증 상태 재사용

**반복 로그인을 피하기 위해 인증 상태를 저장하세요.**

```typescript
// auth.setup.ts - 모든 테스트 전 한 번 실행
import { test as setup } from '@playwright/test';

const authFile = '.auth/user.json';

setup('인증', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="email"]', process.env.TEST_USER!);
  await page.fill('[data-testid="password"]', process.env.TEST_PASS!);
  await page.click('[data-testid="login-btn"]');
  await page.waitForURL('/dashboard');

  // 재사용을 위해 인증 상태 저장
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

## HIGH: WAIT (비동기 처리)

### WAIT-001: 자동 대기 (선호)

```typescript
// Playwright가 요소를 자동으로 기다림
await page.click('[data-testid="submit"]');  // 요소 대기
await expect(page.locator('.success')).toBeVisible();  // 조건 대기
```

### WAIT-002: 필요시 명시적 대기

```typescript
// 특정 조건 대기
await page.waitForURL('/dashboard');
await page.waitForLoadState('networkidle');
await page.waitForSelector('[data-testid="loaded"]');

// API 응답 대기
await Promise.all([
  page.waitForResponse('/api/users'),
  page.click('[data-testid="load-users"]'),
]);
```

### WAIT-003: 고정 타임아웃 피하기

```typescript
// BAD: 고정 대기
await page.waitForTimeout(3000);

// GOOD: 조건 대기
await expect(page.locator('[data-testid="result"]'))
  .toBeVisible({ timeout: 10000 });

// GOOD: 네트워크 대기
await page.waitForLoadState('networkidle');
```

---

## MEDIUM: A11Y (접근성 테스트)

### A11Y-001: 자동 접근성 검사

**axe-core를 사용한 자동 WCAG 준수 테스트.**

```typescript
// @axe-core/playwright 사용
import AxeBuilder from '@axe-core/playwright';

test('홈페이지에 접근성 위반이 없다', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page }).analyze();

  expect(results.violations).toEqual([]);
});

// 특정 WCAG 레벨 검사
test('WCAG 2.1 AA 표준을 충족한다', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### A11Y-002: 키보드 내비게이션

```typescript
test('폼이 키보드로 탐색 가능하다', async ({ page }) => {
  await page.goto('/contact');

  // 폼 요소를 Tab으로 이동
  await page.keyboard.press('Tab');
  await expect(page.locator('[data-testid="name"]')).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(page.locator('[data-testid="email"]')).toBeFocused();

  // Enter로 제출
  await page.keyboard.press('Enter');
  await expect(page.locator('[data-testid="success"]')).toBeVisible();
});
```

### A11Y-003: 스크린 리더 테스트

```typescript
test('이미지에 alt 텍스트가 있다', async ({ page }) => {
  await page.goto('/');

  const images = page.locator('img');
  const count = await images.count();

  for (let i = 0; i < count; i++) {
    const alt = await images.nth(i).getAttribute('alt');
    expect(alt).toBeTruthy();
  }
});

test('폼 입력에 라벨이 있다', async ({ page }) => {
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

## MEDIUM: TOOL (도구별 패턴)

### Playwright

#### PW-001: 설정

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

#### PW-002: API 테스트

```typescript
test('API가 올바르게 응답한다', async ({ request }) => {
  const response = await request.get('/api/users');
  expect(response.ok()).toBeTruthy();

  const users = await response.json();
  expect(users).toHaveLength(10);
});
```

#### PW-003: 비주얼 테스트

```typescript
test('홈페이지 비주얼 리그레션', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixels: 100,
  });
});
```

### Cypress

#### CY-001: 설정

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

#### CY-002: 커스텀 커맨드

```typescript
// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.get('[data-testid="email"]').type(email);
  cy.get('[data-testid="password"]').type(password);
  cy.get('[data-testid="login-btn"]').click();
  cy.url().should('include', '/dashboard');
});

// 사용
cy.login('user@example.com', 'password');
```

#### CY-003: 네트워크 인터셉트

```typescript
cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers');
cy.visit('/users');
cy.wait('@getUsers');
cy.get('[data-testid="user-list"]').should('have.length', 10);
```

#### CY-004: 비주얼 테스트

```typescript
// cypress-image-snapshot 사용
describe('비주얼 리그레션', () => {
  it('홈페이지가 스냅샷과 일치한다', () => {
    cy.visit('/');
    cy.matchImageSnapshot('homepage');
  });

  it('로그인 폼이 스냅샷과 일치한다', () => {
    cy.visit('/login');
    cy.get('[data-testid="login-form"]').matchImageSnapshot('login-form');
  });
});
```

---

## LOW: CI (CI/CD 통합)

### CI-001: GitHub Actions (Playwright)

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

      - name: 의존성 설치
        run: npm ci

      - name: Playwright 브라우저 설치
        run: npx playwright install --with-deps

      - name: E2E 테스트 실행
        run: npm run test:e2e

      - name: 테스트 결과 업로드
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

### CI-002: GitHub Actions (Cypress)

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

      - name: 의존성 설치
        run: npm ci

      - name: Cypress 실행
        uses: cypress-io/github-action@v6
        with:
          build: npm run build
          start: npm start
          wait-on: 'http://localhost:3000'

      - name: 스크린샷 업로드
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: cypress-screenshots
          path: cypress/screenshots/
```

### CI-003: 테스트 샤딩

```yaml
# 여러 머신에서 테스트 실행
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - run: npx playwright test --shard=${{ matrix.shard }}/4
```

---

## 체크리스트

### 테스트 작성 전
- [ ] 핵심 사용자 플로우 식별됨
- [ ] 테스트 데이터 전략 정의됨
- [ ] 컴포넌트에 data-testid 속성 추가됨
- [ ] 페이지 객체 구조 계획됨

### 테스트 구현
- [ ] 테스트가 독립적으로 실행됨
- [ ] 고정 타임아웃 없음 (명시적 대기 사용)
- [ ] 오류 시나리오 커버됨
- [ ] 비주얼 리그레션 추적됨

### CI/CD 통합
- [ ] 모든 PR에서 테스트 실행
- [ ] 실패한 테스트가 머지 차단
- [ ] 디버깅을 위한 아티팩트 업로드됨
- [ ] 병렬 실행 설정됨

---

## 명령어

```bash
# Playwright
npx playwright test                    # 모든 테스트 실행
npx playwright test --ui               # 인터랙티브 UI 모드
npx playwright test --debug            # 디버그 모드
npx playwright show-report             # HTML 리포트 보기
npx playwright codegen                 # 테스트 생성

# Cypress
npx cypress open                       # 인터랙티브 모드
npx cypress run                        # 헤드리스 모드
npx cypress run --spec "path/to/spec"  # 특정 스펙 실행
```

---

**META**
- 버전: 2026.01
- 최종 수정: 2026-02-01
- 카테고리: E2E 테스트
