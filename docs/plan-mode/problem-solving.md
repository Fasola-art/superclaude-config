# Case 4: Problem Solving

> 5 Whys + 병렬 진단

## Phase 1: Quick Diagnosis (Parallel)

```yaml
parallel:
  - LSP: getDiagnostics, goToDefinition, findReferences
  - Error KB: Search ~/.claude/error-kb/
  - Browser: read_console_messages, read_network_requests
```

## Phase 2: Cause Estimation

```yaml
actions:
  - Git: git log, git diff (when did it occur?)
  - Task(Explore): Codebase exploration
  - Browser: browser_evaluate
```

## Phase 3: Solution Search

```yaml
actions:
  - WebSearch: Error message search
  - Context7: Library documentation reference
```

## Phase 4: Verification

```yaml
actions:
  - Browser: navigate, read_console_messages
  - Code fix + Test execution
```

---

## Safety Guards

```yaml
safety_guards:
  max_iterations: 10
  consecutive_failures_limit: 5
  checkpoint_every: "on round completion"

hard_stop:  # Auto halt
  - DB schema changes
  - Auth logic changes
  - Payment related
  - Data deletion
```

## Hard Stop Conditions

| Condition | Reason |
|-----------|--------|
| DB schema changes | 데이터 무결성 위험 |
| Auth logic changes | 보안 위험 |
| Payment related | 금전적 위험 |
| Data deletion | 복구 불가능 |

---

**Related**: [index.md](index.md)
