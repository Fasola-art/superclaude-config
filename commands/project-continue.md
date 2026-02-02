---
description: "Continue interrupted project"
---

# Project Continue

Resume work on a previously interrupted project.

## Behavior

1. Load last session state from `~/.claude/session-env/`
2. Check `.planning/STATE.md` file
3. Check in-progress tasks from `todo.md`
4. Auto-resume from last work point

## Restored Items

- Current project path
- In-progress task list
- Last modified files
- Active personas
- Context state

## Usage Example

```
/project-continue
```

## Output Format

```
🔄 Project Restored

Project: [Project name]
Path: [Project path]

📋 Restored Tasks:
- [x] Completed task 1
- [ ] In progress: Task 2 ← Resume here
- [ ] Pending: Task 3

Last work: [Filename] (modified date)

Continue?
```
