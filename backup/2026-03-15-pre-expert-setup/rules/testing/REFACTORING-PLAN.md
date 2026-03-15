# Testing Rules Refactoring Plan

> **Created**: 2026-02-04
> **Goal**: Split 1,403 lines into maintainable modules (50-100 lines each)

---

## Current State

| File | Lines | Issues |
|------|-------|--------|
| TDD-RULES.md | 730 | 9x over limit |
| E2E-RULES.md | 673 | 8.4x over limit |
| **Total** | **1,403** | **Requires 14-17 files** |

---

## Proposed Structure

```
rules/testing/
├── index.md                    # 50줄: 오버뷰 + 빠른 참조
├── QUICK-REFERENCE.md          # 80줄: 핵심 패턴만
│
├── fundamentals/
│   ├── tdd-cycle.md            # 60줄: Red-Green-Refactor
│   ├── test-structure.md       # 70줄: AAA, 명명규칙, 격리
│   └── coverage-strategy.md    # 60줄: Happy/Error/Boundary
│
├── patterns/
│   ├── mocking.md              # 80줄: Stub/Mock/Spy
│   ├── fixtures.md             # 60줄: 테스트 데이터 관리
│   └── async-testing.md        # 70줄: Promise, 비동기 패턴
│
├── languages/
│   ├── typescript-testing.md   # 90줄: Vitest/Jest
│   ├── python-testing.md       # 90줄: pytest
│   └── go-testing.md           # 80줄: testing package
│
├── e2e/
│   ├── user-flows.md           # 70줄: Critical path 테스팅
│   ├── selectors.md            # 50줄: data-testid 전략
│   ├── page-objects.md         # 80줄: POM 패턴
│   ├── playwright-guide.md     # 100줄: Playwright 전용
│   ├── cypress-guide.md        # 80줄: Cypress 전용
│   └── accessibility.md        # 60줄: A11y 테스팅
│
└── infrastructure/
    ├── ci-integration.md       # 70줄: GitHub Actions
    └── performance.md          # 50줄: 병렬 실행, 최적화
```

**Total**: 17 files, 평균 70줄/파일

---

## Duplication Elimination

### 1. 테스트 구조 (통합 → fundamentals/test-structure.md)

**현재 중복:**
- TDD STRUCT-001~004
- E2E PAT-001~005

**통합 후:**
```markdown
# Test Structure Patterns

## AAA Pattern (All Test Types)
## Test Isolation
## Naming Conventions
## Fixtures vs Helpers
```

### 2. CI/CD (통합 → infrastructure/ci-integration.md)

**현재 중복:**
- TDD CI-001~003
- E2E CI-001~003

**통합 후:**
```markdown
# CI/CD Integration

## GitHub Actions Template
## Parallel Execution
## Artifact Management
## Language-Specific Configs
  - npm test
  - pytest
  - go test
  - playwright test
```

### 3. 언어별 패턴 (분리 → languages/)

**현재 중복:**
- TDD LANG: TS-001~003, PY-001~003, GO-001~003
- E2E TOOL: Playwright/Cypress 설정

**분리 후:**
```
languages/
├── typescript-testing.md
│   ├── Unit Testing (Vitest/Jest)
│   └── E2E Setup (Playwright)
├── python-testing.md
│   ├── pytest Patterns
│   └── Fixtures
└── go-testing.md
    ├── Table-Driven Tests
    └── Subtests
```

---

## Migration Steps

### Phase 1: Core Fundamentals (Week 1)

1. **Create index.md**
   - 테스팅 전략 오버뷰
   - 파일 구조 설명
   - 빠른 링크

2. **Create QUICK-REFERENCE.md**
   - TDD: Red-Green-Refactor 3단계
   - E2E: Critical path 체크리스트
   - 명령어 모음

3. **Create fundamentals/**
   ```bash
   # Extract from TDD-RULES.md
   - CYCLE-001~004 → tdd-cycle.md
   - STRUCT-001~004 → test-structure.md
   - COV-001~003 → coverage-strategy.md
   ```

### Phase 2: Patterns (Week 2)

4. **Create patterns/**
   ```bash
   # Extract from both files
   - TDD MOCK-001~004 → mocking.md
   - TDD/E2E fixtures → fixtures.md
   - TDD ASYNC, E2E WAIT → async-testing.md
   ```

### Phase 3: Language-Specific (Week 3)

5. **Create languages/**
   ```bash
   # Split from TDD LANG section
   - TS-001~003 + E2E Playwright → typescript-testing.md
   - PY-001~003 → python-testing.md
   - GO-001~003 → go-testing.md
   ```

### Phase 4: E2E Specific (Week 4)

6. **Create e2e/**
   ```bash
   # Extract from E2E-RULES.md
   - FLOW-001~004 → user-flows.md
   - SEL-001~003 → selectors.md
   - PAT-001~005 → page-objects.md
   - PW-001~003 → playwright-guide.md
   - CY-001~004 → cypress-guide.md
   - A11Y-001~003 → accessibility.md
   ```

### Phase 5: Infrastructure (Week 5)

7. **Create infrastructure/**
   ```bash
   # Merge duplicates
   - TDD CI + E2E CI → ci-integration.md
   - TDD PERF + E2E parallel → performance.md
   ```

### Phase 6: Cleanup (Week 6)

8. **Archive old files**
   ```bash
   mv TDD-RULES.md archive/TDD-RULES-v2026.01.md
   mv E2E-RULES.md archive/E2E-RULES-v2026.01.md
   ```

9. **Update references**
   - CLAUDE.md → rules/testing/index.md
   - Create barrel export pattern

---

## File Templates

### index.md Template

```markdown
# Testing Rules Index

## Quick Start

| Type | Guide | Lines |
|------|-------|-------|
| TDD Workflow | [fundamentals/tdd-cycle.md](fundamentals/tdd-cycle.md) | 60 |
| E2E Flows | [e2e/user-flows.md](e2e/user-flows.md) | 70 |
| Quick Ref | [QUICK-REFERENCE.md](QUICK-REFERENCE.md) | 80 |

## By Language

- [TypeScript](languages/typescript-testing.md) - Vitest, Playwright
- [Python](languages/python-testing.md) - pytest
- [Go](languages/go-testing.md) - testing package

## By Topic

**Fundamentals**
- [TDD Cycle](fundamentals/tdd-cycle.md)
- [Test Structure](fundamentals/test-structure.md)
- [Coverage Strategy](fundamentals/coverage-strategy.md)

**Patterns**
- [Mocking](patterns/mocking.md)
- [Fixtures](patterns/fixtures.md)
- [Async Testing](patterns/async-testing.md)

**E2E**
- [User Flows](e2e/user-flows.md)
- [Selectors](e2e/selectors.md)
- [Page Objects](e2e/page-objects.md)
- [Playwright Guide](e2e/playwright-guide.md)
- [Cypress Guide](e2e/cypress-guide.md)
- [Accessibility](e2e/accessibility.md)

**Infrastructure**
- [CI Integration](infrastructure/ci-integration.md)
- [Performance](infrastructure/performance.md)

---

**Version**: 2026.02
**Last Updated**: 2026-02-04
```

### Individual File Template

```markdown
# [Topic Name]

> **Version**: 2026.02
> **Category**: [Fundamentals/Patterns/E2E/Language]
> **Lines**: ~[target lines]

---

## Priority Summary

| Priority | Rules | Key Effect |
|----------|-------|------------|
| CRITICAL | 3 | [effect] |
| HIGH | 4 | [effect] |
| MEDIUM | 2 | [effect] |

---

## [SECTION-001]: [Name]

[Content]

---

## Quick Reference

```[language]
// Key patterns
```

---

**Related**
- [Link to related file]
- [Link to related file]
```

---

## Validation Criteria

### Per-File Checks

- [ ] 50-100줄 사이
- [ ] 단일 책임 원칙 (하나의 주제)
- [ ] 중복 콘텐츠 없음
- [ ] 명확한 Priority Summary
- [ ] Related links 포함

### Overall Structure

- [ ] index.md에서 모든 파일 참조
- [ ] QUICK-REFERENCE.md 독립적으로 사용 가능
- [ ] 언어별 가이드 독립 실행 가능
- [ ] E2E 가이드 도구별 분리
- [ ] CI/CD 통합 가이드 단일화

---

## Commands

```bash
# 파일 크기 검증
wc -l rules/testing/**/*.md

# 중복 검사
grep -r "AAA Pattern" rules/testing/

# 링크 검증
python3 ~/.claude/scripts/validate-links.py rules/testing/
```

---

**META**
- Created: 2026-02-04
- Status: PROPOSED
- Estimated Effort: 6 weeks
- Breaking Changes: YES (파일 구조 전면 변경)
