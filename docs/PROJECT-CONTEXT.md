# Project Context Management

> Project context maintenance and restoration strategy

---

## Overview

Project context is essential for ensuring work continuity and efficient development.

---

## Context Components

### 1. Project Metadata
```yaml
project:
  name: [project name]
  path: [path]
  type: [nextjs | react | node | ...]
  created: [creation date]
  last_active: [last activity date]
```

### 2. Work State
```yaml
state:
  current_task: [current task]
  milestone: [current milestone]
  progress: [progress rate]
  blockers: [blocking factors]
```

### 3. File Context
```yaml
files:
  recently_modified:
    - path: [file path]
      modified: [modification date]
  frequently_accessed:
    - path: [file path]
      count: [access count]
```

---

## Context Storage Location

```
~/.claude/
├── session-env/
│   ├── current-project.json
│   └── session-state.json
├── projects/
│   └── [project-hash]/
│       ├── context.json
│       └── history.json
└── file-history/
    └── [date]/
        └── changes.json
```

---

## Context Restoration

### Auto Restoration
Auto-load last project context on session start

### Manual Restoration
```
/project-continue    # Continue last project
/recover            # Session recovery
/sc:load --project  # Load project context
```

---

## Context Cleanup

### DCP (Dynamic Context Pruning)
- 75%: Warning
- 90%: Auto compression
- 95%: Forced compression

### Preserved Items
- Current task
- Active TodoWrite
- Recently modified files
- CLAUDE.md rules
