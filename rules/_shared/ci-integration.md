# CI/CD Integration (Shared)

> Common CI/CD patterns for all testing types

---

## GitHub Actions Template

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: coverage/
```

---

## Parallel Execution

```yaml
# Matrix strategy
strategy:
  matrix:
    node: [18, 20]
    os: [ubuntu-latest, macos-latest]
```

---

## Test Sharding

```yaml
# Distribute across machines
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4
```

---

## Language-Specific

### TypeScript
```bash
npm test -- --coverage
```

### Python
```bash
pytest -v --cov=src --cov-report=xml
```

### Go
```bash
go test -race -coverprofile=coverage.out ./...
```

---

**Related**: [test-fundamentals.md](test-fundamentals.md)
