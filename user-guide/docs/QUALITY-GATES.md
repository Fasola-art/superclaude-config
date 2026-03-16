# Quality Gates (8단계 품질 검증)

> 코드 품질 검증 체크포인트

---

## 검증 파이프라인

```
1.Syntax → 2.Type → 3.Lint → 4.Security → 5.Test → 6.Performance → 7.Docs → 8.Integration
```

---

## 단계별 상세

### 1단계: Syntax (구문 검사)
```yaml
tool: TypeScript Compiler
command: tsc --noEmit
pass_condition: 컴파일 성공
blocking: true
```

### 2단계: Type (타입 검사)
```yaml
tool: tsc --noEmit
command: npx tsc --noEmit --strict
pass_condition: 0 에러
blocking: true
```

### 3단계: Lint (정적 분석)
```yaml
tool: ESLint
command: npm run lint
pass_condition: 0 에러
blocking: true (에러), false (경고)
```

### 4단계: Security (보안 검사)
```yaml
tools:
  - npm audit
  - 수동 보안 검토
command: npm audit --audit-level=high
pass_condition: 0 고위험 취약점
blocking: true
```

### 5단계: Test (테스트)
```yaml
tools:
  - Vitest (Unit)
  - Playwright (E2E)
command: npm run test:coverage
pass_condition:
  - 커버리지 ≥ 80%
  - 모든 테스트 통과
blocking: true
```

### 6단계: Performance (성능)
```yaml
tools:
  - Lighthouse
  - 번들 분석기
command: npm run lighthouse
pass_condition:
  - LCP < 2.5s
  - FID < 100ms
  - CLS < 0.1
  - 번들 크기 < 500KB
blocking: false (경고)
```

### 7단계: Docs (문서화)
```yaml
tool: TSDoc
command: npm run docs:check
pass_condition:
  - Public API 100% 문서화
  - JSDoc 주석 완성
blocking: false (경고)
```

### 8단계: Integration (통합)
```yaml
tool: Playwright
command: npm run test:e2e
pass_condition:
  - 크리티컬 패스 100% 통과
  - 주요 시나리오 테스트 통과
blocking: true
```

---

## 게이트별 우선순위

| 게이트 | 우선순위 | 차단 여부 |
|--------|---------|----------|
| Syntax | P0 | 🔴 차단 |
| Type | P0 | 🔴 차단 |
| Lint | P0 | 🔴 차단 (에러) |
| Security | P0 | 🔴 차단 |
| Test | P1 | 🔴 차단 |
| Performance | P1 | 🟡 경고 |
| Docs | P2 | 🟡 경고 |
| Integration | P1 | 🔴 차단 |

---

## 자동화 설정

### Pre-commit Hook
```bash
# .husky/pre-commit
npm run lint-staged
npm run type-check
```

### CI/CD 파이프라인
```yaml
# .github/workflows/quality.yml
jobs:
  quality-gates:
    steps:
      - name: Type Check
        run: npm run type-check
      - name: Lint
        run: npm run lint
      - name: Security
        run: npm audit
      - name: Test
        run: npm run test:coverage
      - name: E2E
        run: npm run test:e2e
```

---

## 면제 조건

| 조건 | 면제 게이트 | 사유 |
|------|------------|------|
| 핫픽스 | Performance, Docs | 긴급 수정 |
| 프로토타입 | Test, Docs | 실험 코드 |
| 설정 변경 | Test | 코드 변경 없음 |

---

## 실패 시 대응

```yaml
failure_response:
  syntax_error:
    action: "컴파일 에러 수정"
    escalation: "즉시"

  type_error:
    action: "타입 오류 수정"
    escalation: "즉시"

  lint_error:
    action: "npm run lint --fix 실행"
    escalation: "PR 블록"

  security_error:
    action: "취약점 패치 또는 의존성 업데이트"
    escalation: "보안팀 알림"

  test_failure:
    action: "실패 테스트 수정"
    escalation: "PR 블록"
```
