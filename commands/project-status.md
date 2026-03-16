---
description: "프로젝트 상태 확인 | Check project status"
---

# Project Status

Check current project progress.

## Behavior

1. Load `.planning/STATE.md` file
2. Aggregate task status from `todo.md`
3. Calculate progress per milestone
4. Analyze recently modified files
5. Suggest next priority tasks

## Displayed Information

- Overall progress
- Status per milestone
- Steel Thread completion rate
- Recently completed tasks
- Next work suggestions

## Usage Example

```
/project-status
```

## Output Format

```
📊 Project Status

Project: [Project name]
Overall Progress: ████████░░░░░░░░░░░░ 43%

Milestones:
├── M1: Foundation    ████████████████████ 100%
├── M2: Core Features ████████████░░░░░░░░ 60%
└── M3: Integration   ░░░░░░░░░░░░░░░░░░░░ 0%

Steel Thread: ████████████████░░░░ 80%

Recently Completed:
- [x] API endpoint implementation
- [x] Database schema

Next Priority:
1. [ ] Frontend components (M2)
2. [ ] Write tests (M2)
```
