# PDCA File Templates

## state.json

```json
{
  "feature": "",
  "current_stage": "plan",
  "iteration": 1,
  "max_iterations": 5,
  "pass_threshold": 0.90,
  "stages": {
    "plan": {"status": "pending", "score": null},
    "do": {"status": "pending", "score": null},
    "check": {"status": "pending", "score": null},
    "act": {"status": "pending", "score": null}
  },
  "created_at": "",
  "updated_at": ""
}
```

### Status Values
- `pending`: 미시작
- `in_progress`: 진행 중
- `completed`: 완료

---

## .pdca/ Directory

```
.pdca/
├── state.json
├── plan.md
├── do-log.md
├── check-results.md
├── act-actions.md
└── history/
    ├── iteration-1.json
    └── iteration-2.json
```

---

## history/iteration-{n}.json

```json
{
  "iteration": 1,
  "stages": {
    "plan": {"status": "completed", "score": null},
    "do": {"status": "completed", "score": null},
    "check": {"status": "completed", "score": 0.85},
    "act": {"status": "completed", "score": null}
  },
  "summary": "",
  "completed_at": ""
}
```

---

## .gitignore Addition

```
.pdca/
```
