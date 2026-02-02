---
name: sync-guide
description: Synchronize instruction files to user guides. Convert English instructions to localized user documentation.
version: "1.0.0"
triggers:
  - /sync-guide
  - guide synchronization
  - update user guide
---

# Guide Synchronization Skill

Synchronize English instruction files to localized user guides.

## Usage

```
/sync-guide              # Full sync
/sync-guide CLAUDE.md    # Single file sync
/sync-guide --list       # List target files
```

## Execution Instructions

### Full Synchronization

```bash
python3 ~/.claude/scripts/sync_user_guide.py
```

### Single File Synchronization

```bash
python3 ~/.claude/scripts/sync_user_guide.py --file ~/.claude/docs/HOOKS-SYSTEM.md
```

### List Files

```bash
python3 ~/.claude/scripts/sync_user_guide.py --list
```

## Output Path

```
Source: ~/.claude/docs/HOOKS-SYSTEM.md
Output: ~/.claude/user-guide/docs/HOOKS-SYSTEM.md
```

## Automatic Synchronization

- Schedule: 1st of each month at 3am
- LaunchAgent: `com.superclaude.user-guide-sync`

## Cost

- Full sync: ~$0.20/run
- Single file: ~$0.005/run
