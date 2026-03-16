# Session Management System

> Auto Snapshot and Recovery Strategy

---

## Auto Snapshot Triggers

```yaml
triggers:
  - "On Todo completion"
  - "On Git commit"
  - "On file modification"
  - "Every 10 minutes auto"
```

---

## Configuration

```yaml
session_recovery:
  auto_snapshot: true
  max_snapshots: 10
  auto_resume: true
  snapshot_interval: 600  # seconds (10 min)
```

---

## Snapshot Contents

```yaml
snapshot_contents:
  - current_task: "Currently in-progress task"
  - todo_items: "TodoWrite items"
  - modified_files: "Modified file list"
  - context_summary: "Context summary"
  - state_md: "STATE.md contents"
  - timestamp: "Snapshot time"
```

---

## Recovery Commands

| Command | Description |
|---------|-------------|
| /recover | Recover last snapshot |
| /recover --list | List snapshots |
| /recover --id X | Recover specific snapshot |
| continue | Continue previous work (Vibe keyword) |

---

## Recovery Process

```
1. Select Snapshot
   └── Default: Last snapshot
   └── Option: Select specific with --id

2. Restore State
   ├── Load STATE.md
   ├── Restore TodoWrite items
   └── Load context summary

3. Resume Work
   ├── Verify breakpoint
   ├── Show incomplete tasks
   └── Continue after user confirmation
```

---

## Snapshot Storage Location

```
~/.claude/shell-snapshots/
├── snapshot_2026-01-29_12-00-00.json
├── snapshot_2026-01-29_12-10-00.json
├── snapshot_2026-01-29_12-20-00.json
└── ...
```

---

## Snapshot Format

```json
{
  "id": "snap_abc123",
  "timestamp": "2026-01-29T12:00:00.000Z",
  "session_id": "session_xyz789",
  "task": {
    "current": "API endpoint implementation",
    "progress": 60
  },
  "todos": [
    {
      "id": 1,
      "status": "completed",
      "subject": "Define User model"
    },
    {
      "id": 2,
      "status": "in_progress",
      "subject": "Implement Auth middleware"
    }
  ],
  "modified_files": [
    "src/models/user.ts",
    "src/middleware/auth.ts"
  ],
  "context_summary": "Implementing user authentication system...",
  "state_md_hash": "sha256:abc123..."
}
```

---

## Auto Cleanup

```yaml
cleanup:
  trigger: "When max_snapshots exceeded"
  strategy: "Delete oldest snapshots"
  preserve: "Last 10"
```
