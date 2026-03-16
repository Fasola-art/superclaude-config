---
description: "세션 또는 시스템 복구 | Recover session or system"
argument-hint: "[session_id]"
---

# Session Recovery

Recover interrupted sessions or restore system state.

## Behavior

1. Search session history in `~/.claude/sessions/`
2. Restore shell state from `~/.claude/shell-snapshots/`
3. Check file change history in `~/.claude/file-history/`
4. Restore to last stable state

## Recovery Types

### Session Recovery
```
/recover              # Recover last session
/recover session_id   # Recover specific session
```

### File Recovery
```
/recover --file path/to/file   # Restore file to previous version
```

### Full Recovery
```
/recover --full   # Restore full system state
```

## Output Format

```
🔄 Session Recovery

Session ID: [session_id]
Start time: [timestamp]
Last activity: [timestamp]

Recovered Items:
- Project path: [path]
- Task state: [N] items restored
- File history: [N] items checked
- Shell state: Restored

Recovery complete. Continue previous work?
```
