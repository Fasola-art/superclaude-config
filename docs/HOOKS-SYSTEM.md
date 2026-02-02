# Hooks Automation System

> 17 Hook Definitions

---

## Hook Trigger Types

| Trigger          | Timing                    | Hook Count |
|------------------|---------------------------|------------|
| UserPromptSubmit | On user prompt submission | 7          |
| PreToolUse       | Before tool execution     | 2          |
| PostToolUse      | After tool execution      | 8          |
| Stop             | On session termination    | 1          |

---

## UserPromptSubmit Hooks (7)

### 1. jarvis-morning-briefing.py
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "Generate morning briefing"
timeout: 5000ms
actions:
  - Generate daily summary
  - Notify incomplete tasks
  - Display scheduled work
```

### 2. plan-mode-analyzer.py
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "Detect PRD → Enter plan mode"
timeout: 3000ms
detection:
  keywords: ["PRD", "requirements", "create project"]
  file_patterns: ["*.prd.md", "PRD.md"]
actions:
  - Detect PRD document
  - Auto-enter plan mode
  - Determine analysis depth
```

### 3. context-cleaner.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "Auto-clean context"
timeout: 2000ms
thresholds:
  warning: 75%
  critical: 90%
  emergency: 95%
actions:
  - Check context usage
  - Execute DCP strategy
  - Report cleanup results
```

### 4. keyword-detector.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "Detect Vibe/Mode keywords"
timeout: 1000ms
keywords:
  vibe: 13
  mode: 4
actions:
  - Parse keywords
  - Trigger corresponding actions
  - Activate personas
```

### 5. persona-activator.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "Auto-activate personas"
timeout: 1500ms
rules:
  max_concurrent: 3
  priority: [security, architect, analyzer]
  security_keywords: [auth, login, password, token]
actions:
  - Analyze context
  - Select persona
  - Activate persona
```

### 6. todo-continuation-enforcer.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "Verify todo persistence"
timeout: 1000ms
actions:
  - Check incomplete todos
  - Ensure continuity
  - Notify missing tasks
```

### 7. auto-update-checker.js
```yaml
trigger: UserPromptSubmit
matcher: "*"
purpose: "Check for updates"
timeout: 5000ms
frequency: "Once per day"
actions:
  - Check version
  - Notify updates
  - Display changelog
```

---

## PreToolUse Hooks (2)

### 1. writer-reviewer-hook.py
```yaml
trigger: PreToolUse
matcher: "Edit|Write|MultiEdit"
purpose: "Activate Writer-Reviewer Loop"
timeout: 30000ms
config:
  target_score: 0.85
  max_iterations: 10
actions:
  - Detect code type
  - Execute 4-Agent review
  - Calculate score and iterate
```

### 2. error-warning-hook.js
```yaml
trigger: PreToolUse
matcher: "Edit|Write|MultiEdit"
purpose: "Error KB-based warnings"
timeout: 2000ms
actions:
  - Search similar error patterns
  - Display pre-warnings
  - Suggest recommendations
```

---

## PostToolUse Hooks (8)

### 1. jarvis-work-tracker.py
```yaml
trigger: PostToolUse
matcher: ".*"
purpose: "Track work"
timeout: 1000ms
actions:
  - Log work
  - Update statistics
  - Calculate progress
```

### 2. error-auto-resolver.js
```yaml
trigger: PostToolUse
matcher: "Bash|Task"
purpose: "Ralph Loop - Auto-resolve errors"
timeout: 30000ms
config:
  max_retries: 10
  similarity_threshold: 0.70
actions:
  - Detect errors
  - Search Error KB
  - Attempt auto-resolution
```

### 3. ralph-loop-checker.js
```yaml
trigger: PostToolUse
matcher: "Bash|Task"
purpose: "Detect infinite loops"
timeout: 1000ms
config:
  max_consecutive_failures: 5
actions:
  - Track failure count
  - Detect infinite loops
  - Force stop
```

### 4. jarvis-task-completion.py
```yaml
trigger: PostToolUse
matcher: "TodoWrite|Bash|Write|Edit"
purpose: "Handle task completion"
timeout: 2000ms
actions:
  - Update task status
  - Notify completion
  - Suggest next task
```

### 5. session-snapshot.js
```yaml
trigger: PostToolUse
matcher: "TodoWrite|Bash|Write|Edit"
purpose: "Auto session snapshot"
timeout: 3000ms
config:
  max_snapshots: 10
actions:
  - Capture state
  - Save snapshot
  - Clean old snapshots
```

### 6. quality-gate.js
```yaml
trigger: PostToolUse
matcher: "Write|Edit|MultiEdit"
purpose: "8-stage quality verification"
timeout: 60000ms
gates: [Syntax, Type, Lint, Security, Test, Performance, Docs, Integration]
actions:
  - Execute gates sequentially
  - Notify on failure
  - Generate result report
```

### 7. pattern-tracker.js
```yaml
trigger: PostToolUse
matcher: "Task"
purpose: "Track/learn patterns"
timeout: 2000ms
actions:
  - Record success patterns
  - Record failure patterns
  - Analyze patterns
```

### 8. background-notification.js
```yaml
trigger: PostToolUse
matcher: "Task"
purpose: "Background task notifications"
timeout: 1000ms
actions:
  - Detect background task completion
  - Send notification
  - Summarize results
```

---

## Stop Hook (1)

### todo-continuation-enforcer.js
```yaml
trigger: Stop
purpose: "Save incomplete todos"
timeout: 5000ms
actions:
  - Save incomplete tasks
  - Save session state
  - Record recovery information
```

---

## Hook Configuration Example

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/UserPromptSubmit/keyword-detector.py",
            "timeout": 1000
          }
        ]
      }
    ]
  }
}
```
