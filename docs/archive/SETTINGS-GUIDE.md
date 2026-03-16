# System Settings Guide

> Detailed manual for settings.json

---

## File Location

```
~/.claude/settings.json
```

---

## Full Structure

```json
{
  "$schema": "https://claude.ai/schemas/settings.json",
  "version": "2.0.9",
  "platform": "macOS",
  "hardware": { ... },
  "permissions": { ... },
  "parallelExecution": { ... },
  "context": { ... },
  "writerReviewer": { ... },
  "errorKB": { ... },
  "session": { ... },
  "language": { ... },
  "hooks": { ... }
}
```

---

## Section Details

### hardware

```json
{
  "hardware": {
    "model": "Mac Studio Ultra M2",
    "cpu_cores": 24,
    "gpu_cores": 76,
    "memory_gb": 192,
    "storage_tb": 8
  }
}
```

**Purpose**: Used for adaptive parallel execution optimization

---

### permissions

```json
{
  "permissions": {
    "allow": [
      "Read:**",
      "Write:**",
      "Bash:npm install*",
      "Bash:git status*"
    ],
    "deny": [
      "Bash:git push*",
      "Bash:rm -rf*",
      "Read:.env*"
    ],
    "ask": []
  }
}
```

**Pattern syntax**:
- `*`: Wildcard
- `**`: Recursive wildcard
- Exact command matching

---

### parallelExecution

```json
{
  "parallelExecution": {
    "initial": 10,
    "scaleUp": 5,
    "scaleDown": 3,
    "maximum": 24,
    "consecutiveSuccessForScaleUp": 3
  }
}
```

| Setting                      | Description                | Default |
|------------------------------|----------------------------|---------|
| initial                      | Starting concurrent count  | 10      |
| scaleUp                      | Increment on success       | 5       |
| scaleDown                    | Decrement on failure       | 3       |
| maximum                      | Max concurrent (CPU cores) | 24      |
| consecutiveSuccessForScaleUp | Scale-up trigger condition | 3       |

---

### context

```json
{
  "context": {
    "warningThreshold": 75,
    "criticalThreshold": 90,
    "emergencyThreshold": 95,
    "autoArchive": true
  }
}
```

| Setting            | Description          | Default |
|--------------------|----------------------|---------|
| warningThreshold   | Warning threshold    | 75%     |
| criticalThreshold  | Auto DCP threshold   | 90%     |
| emergencyThreshold | Forced compression   | 95%     |
| autoArchive        | Auto archive enabled | true    |

---

### writerReviewer

```json
{
  "writerReviewer": {
    "enabled": true,
    "targetScore": 0.85,
    "maxIterations": 10,
    "convergenceThreshold": 0.015,
    "agents": {
      "quality": { "weight": 0.30 },
      "security": { "weight": 0.30, "minScore": 0.85 },
      "performance": { "weight": 0.20 },
      "accessibility": { "weight": 0.20 }
    }
  }
}
```

| Setting              | Description           | Default |
|----------------------|-----------------------|---------|
| enabled              | Enable/disable        | true    |
| targetScore          | Target score          | 0.85    |
| maxIterations        | Max iterations        | 10      |
| convergenceThreshold | Convergence threshold | 0.015   |

---

### errorKB

```json
{
  "errorKB": {
    "enabled": true,
    "similarityThreshold": 0.70,
    "maxRalphLoopRetries": 10,
    "autoLearnOnSuccess": true
  }
}
```

| Setting             | Description                  | Default |
|---------------------|------------------------------|---------|
| enabled             | Enable/disable               | true    |
| similarityThreshold | Jaccard similarity threshold | 0.70    |
| maxRalphLoopRetries | Ralph Loop max retries       | 10      |
| autoLearnOnSuccess  | Auto-learn on success        | true    |

---

### session

```json
{
  "session": {
    "autoSnapshot": true,
    "maxSnapshots": 10,
    "autoResume": true
  }
}
```

| Setting      | Description        | Default |
|--------------|--------------------|---------|
| autoSnapshot | Auto snapshot      | true    |
| maxSnapshots | Max snapshot count | 10      |
| autoResume   | Auto resume        | true    |

---

### language

```json
{
  "language": {
    "response": "ko",
    "codeComments": "ko"
  }
}
```

| Setting      | Description           | Default |
|--------------|-----------------------|---------|
| response     | Response language     | ko      |
| codeComments | Code comment language | ko      |

---

### hooks

```json
{
  "hooks": {
    "enabled": true,
    "path": "~/.claude/hooks"
  }
}
```

| Setting | Description     | Default         |
|---------|-----------------|-----------------|
| enabled | Enable hooks    | true            |
| path    | Hooks directory | ~/.claude/hooks |

---

## Environment Override

### settings.local.json

Local environment specific settings (excluded from git)

```json
{
  "permissions": {
    "allow": [
      "Bash:sudo*"
    ]
  }
}
```

**Priority**: settings.local.json > settings.json

---

## Settings Validation

```bash
# Validate settings
claude config validate

# Show current settings
claude config show
```
