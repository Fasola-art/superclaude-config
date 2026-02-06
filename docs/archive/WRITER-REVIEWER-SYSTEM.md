# Writer-Reviewer System Detail

> 4-Agent parallel code review system documentation

---

## System Overview

Writer-Reviewer is a quality assurance system where 4 agents automatically review code generation in parallel.

---

## Architecture

```
[Code Request]
    │
    ▼
[Writer] ──────────────────────────────┐
    │                                  │
    ▼                                  ▼
[4-Agent Parallel Review]        [Code Generation]
    │
    ├── Quality Agent (30%)
    ├── Security Agent (30%)
    ├── Performance Agent (20%)
    └── Accessibility Agent (20%)
    │
    ▼
[Score Integration] ─── < 0.85 ──► [Re-review/Fix]
    │                                   │
    ▼                                   │
[Convergence Check] ◄──────────────────┘
    │
    ▼
[Complete]
```

---

## Configuration

### Default Settings
```yaml
# ~/.claude/WRITER-REVIEWER.md
target_score: 0.85
max_iterations: 10
convergence_threshold: 0.015
```

### Weights by Code Type
| Type     | Quality  | Security | Performance | Accessibility |
|----------|----------|----------|-------------|---------------|
| frontend | 0.25     | 0.25     | 0.20        | **0.30**      |
| backend  | 0.25     | **0.40** | 0.25        | 0.10          |
| utility  | **0.35** | 0.25     | 0.30        | 0.10          |
| database | 0.20     | **0.40** | **0.35**    | 0.05          |

---

## Agent Details

### Quality Agent
**Checks:**
- Code readability (naming, structure)
- Type safety
- Error handling
- SOLID principles
- DRY principle

### Security Agent
**Checks:**
- XSS vulnerabilities
- SQL Injection
- Authentication/Authorization
- Sensitive data exposure
- Input validation

### Performance Agent
**Checks:**
- Algorithm efficiency
- Memory management
- Unnecessary renders
- N+1 queries
- Bundle size

### Accessibility Agent
**Checks:**
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Color contrast
- Focus management

---

## Convergence Conditions

### Early Exit
- Target score (0.85) achieved
- All categories >= 0.80
- 2 consecutive changes < 0.015

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

## Flags

| Flag               | Effect                         |
|--------------------|--------------------------------|
| `--no-review`      | Disable (except security code) |
| `--review-strict`  | Target 0.90                    |
| `--review-quick`   | Max 3 iterations               |
| `--review-verbose` | Detailed output                |

---

## References

- `~/.claude/WRITER-REVIEWER.md` - Main configuration
- `~/.claude/hooks/PreToolUse/writer-reviewer-hook.py` - Hook implementation
