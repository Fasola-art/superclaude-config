# Writer-Reviewer v2.0 System

> 4-Agent Parallel Code Review System

---

## Default Settings

```yaml
target_score: 0.85           # Target score
max_iterations: 10           # Maximum iterations
convergence_threshold: 0.015 # Convergence threshold
```

---

## Adaptive Weights by Code Type

| Type | Quality | Security | Performance | Accessibility |
|------|---------|----------|-------------|---------------|
| frontend_component | 0.25 | 0.25 | 0.20 | **0.30** |
| backend_api | 0.25 | **0.40** | 0.25 | 0.10 |
| utility_function | **0.35** | 0.25 | 0.30 | 0.10 |
| database_query | 0.20 | **0.40** | **0.35** | 0.05 |

---

## Type Detection

```yaml
frontend:
  keywords: [component, tsx, jsx, ui, form, button, modal]
  file_patterns: ["*.tsx", "*.jsx", "components/"]

backend:
  keywords: [api, route, endpoint, controller, service, handler]
  file_patterns: ["/api/", "/routes/", "*.controller.ts"]

utility:
  keywords: [util, helper, lib, function, hook]
  file_patterns: ["/utils/", "/lib/", "/hooks/"]

database:
  keywords: [query, sql, database, migration, schema]
  file_patterns: ["/db/", "/migrations/", "*.sql"]
```

---

## Agent Details

### Quality Agent (30%)

**Checks**
- Code readability (naming, structure)
- Type safety (TypeScript usage)
- Error handling (try-catch, edge cases)
- SOLID principles compliance
- Code duplication minimization (DRY)

**Deduction Rules**
| Item | Deduction |
|------|-----------|
| react-hook-form not used | -0.15 |
| Inline constant definition | -0.10 |
| Missing Zod validation | -0.20 |
| Missing permission check | -0.30 |
| Pattern mismatch | -0.10 |

---

### Security Agent (30%)

**Checks**
- XSS vulnerability prevention
- SQL/Command Injection prevention
- Authentication/Authorization handling
- Sensitive information exposure prevention
- Input validation

**Critical Issues (Immediate Fix Required)**
- SQL Injection possibility
- XSS vulnerability
- Hardcoded password/API key
- Authentication bypass possibility
- CSRF vulnerability

**When critical found: max_score = 0.3**

---

### Performance Agent (20%)

**Checks**
- Algorithm efficiency (time/space complexity)
- Unnecessary rendering (React)
- Memory leak possibility
- N+1 query problem
- Bundle size impact

**React Specific**
- Appropriate useMemo/useCallback usage
- Unnecessary state updates
- React.memo necessity
- Lazy loading opportunities

---

### Accessibility Agent (20%)

**Checks**
- Semantic HTML usage
- ARIA label appropriateness
- Keyboard navigation
- Color contrast
- Focus management

**Standard: WCAG 2.1 AA**

---

## Convergence Conditions

### Early Exit Conditions
- Target score (0.85) achieved
- All categories 0.80 or above
- 2 consecutive iterations with score change < 0.015

### Security Minimum Score

```yaml
security_minimum:
  score: 0.85
  block_early_exit_if:
    security_score < 0.85
    has_critical_issues: true
    any_category < 0.70
```

---

## Output Format

```
[Code Block]
---
Quality Score: 86% (3 iterations)
├── Quality: 87% | Security: 88% | Performance: 83% | Accessibility: 86%
└── Issues: [Resolved issues summary]
```

---

## Flags

| Flag | Effect |
|------|--------|
| --no-review | Disable Writer-Reviewer (except security code) |
| --review-strict | Raise target score to 0.90 |
| --review-quick | Maximum 3 iterations |
| --review-verbose | Verbose output for each iteration |
