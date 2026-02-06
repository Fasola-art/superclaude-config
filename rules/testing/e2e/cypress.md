# Cypress Guide

## Configuration

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

## Custom Commands

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

## Network Interception

```typescript
cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers');
cy.visit('/users');
cy.wait('@getUsers');
cy.get('[data-testid="user-list"]').should('have.length', 10);
```

## Visual Testing

```typescript
// Using cypress-image-snapshot
import { addMatchImageSnapshotCommand } from 'cypress-image-snapshot/command';
addMatchImageSnapshotCommand();

describe('Visual Regression', () => {
  it('homepage matches snapshot', () => {
    cy.visit('/');
    cy.matchImageSnapshot('homepage');
  });
});
```

---

## Commands

```bash
npx cypress open      # Interactive mode
npx cypress run       # Headless mode
npx cypress run --spec "path/to/spec"
```

---

## vs Playwright

| Feature | Cypress | Playwright |
|---------|---------|------------|
| Browser | Chrome, Firefox, Edge | All + Safari |
| Multi-tab | ❌ | ✅ |
| API testing | Plugin | Built-in |
| Network | cy.intercept | page.route |
| Speed | Fast | Faster |
