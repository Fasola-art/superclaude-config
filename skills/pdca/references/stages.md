# PDCA Stage Details

## Plan Stage

### Inputs
- Feature description from user
- Project context (existing files, architecture)

### Outputs
- `.pdca/plan.md` with goals, tasks, success criteria
- TaskCreate items for each task

### Quality Criteria
- Clear success criteria (measurable)
- Tasks are atomic (1 task = 1 change)
- Risk assessment included
- Time estimate per task

---

## Do Stage

### Inputs
- Approved plan from Plan stage
- TaskList with pending items

### Execution Flow
1. Pick next pending task (lowest ID)
2. Set task → in_progress
3. Implement the change
4. Auto-Retry Loop activates on Edit/Write
5. If gate passes → mark task completed
6. Log to `.pdca/do-log.md`
7. Repeat until all tasks done

### Integration with Auto-Retry
- Edit/Write → quality gate → pass/fail
- Fail → feedback → Claude fixes → retry
- Max 5 retries per file

---

## Check Stage

### Verification Steps

| Step | Command | Pass Criteria |
|------|---------|---------------|
| Syntax | `py_compile` / `tsc` | Zero errors |
| Type | `mypy` / `tsc --noEmit` | Zero errors |
| Lint | `ruff` / `eslint` | Zero warnings |
| Test | `pytest` / `vitest` | All pass |
| Coverage | `--cov` | ≥ 80% |

### Scoring
```
score = (passed_checks / total_checks) * 100
```

### Threshold
- ≥ 90%: iteration 성공
- 70-89%: 개선 필요
- < 70%: 재작업 필요

---

## Act Stage

### Analysis Framework
1. **성공 항목**: 무엇이 잘 됐는가?
2. **실패 항목**: 무엇이 안 됐는가?
3. **근본 원인**: 왜 실패했는가?
4. **개선 액션**: 다음에 무엇을 바꿀 것인가?

### Output
- `.pdca/act-actions.md` with improvement actions
- Updated task list for next iteration

---

## Iteration Rules

| Condition | Action |
|-----------|--------|
| score ≥ 90% | Suggest completion |
| score < 90% + iterations < max | Auto-iterate |
| iterations = max | Force report |

---

**Related**: [templates.md](templates.md)
