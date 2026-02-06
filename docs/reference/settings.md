# Settings Configuration

> settings.json 기반 시스템 설정

## Permission System

| Category | Setting |
|----------|---------|
| ✔ Allow | File read/write, Git (except push), npm/pip, supabase, gh CLI |
| ✘ Deny | git push, rm -rf, sudo, .env access |
| Auto | acceptEdits (auto-accept edits) |

```json
"permissions": {
  "allow": [
    "Read:**", "Write:**", "Edit:**",
    "Bash:git status", "Bash:git add*", "Bash:git commit*",
    "Bash:npm install*", "Bash:npm run*",
    "Bash:supabase gen types*", "Bash:supabase migration*"
  ],
  "deny": [
    "Bash:git push*", "Bash:rm -rf*", "Bash:sudo*",
    "Read:.env*", "Write:.env*"
  ]
}
```

---

## Context Management

| Threshold | Action |
|-----------|--------|
| ⚠ 75% | Warning (cleanup recommended) |
| 🔴 90% | Critical (DCP compression) |
| 🚨 95% | Emergency (forced compression) |

**Strategies**: deduplication, error_cleanup, file_summarize

---

## Ralph Loop (Auto Error Resolution)

```json
"ralph_loop": {
  "enabled": true,
  "max_retries": 10,
  "auto_triggers": ["npm run build", "npm run test", "npm run lint"],
  "success_patterns": ["success", "completed", "PASSED"]
}
```

---

## Quality Gate

```json
"quality_gate": {
  "enabled": true,
  "threshold": 0.85,     // 85% pass required
  "max_iterations": 10,
  "weights": {
    "quality": 0.3,      // 30%
    "security": 0.3,     // 30%
    "performance": 0.2,  // 20%
    "accessibility": 0.2 // 20%
  }
}
```

---

## Parallel Execution

```json
"parallel_execution": {
  "max_agents": "unlimited",  // Unlimited
  "smart_grouping": true      // Auto dependency detection
}
```

---

## Adaptive Parallel Execution

```yaml
initial: 5 concurrent
conditions:
  3 consecutive success → +5
  1 failure → -3 (min 3)
maximum: unlimited
```

---

**Related**: [../orchestrator/parallel-agents.md](../orchestrator/parallel-agents.md)
