---
description: "Create project plan"
argument-hint: "[project_name or PRD_path]"
---

# Project Plan

Create project execution plan based on PRD (Product Requirements Document).

## Behavior

1. Analyze PRD file or project requirements
2. Set phased milestones
3. Identify Steel Thread
4. Decompose tasks and define dependencies
5. Generate planning documents in `.planning/` folder

## Generated Documents

```
.planning/
├── PROJECT.md      # Project overview
├── ROADMAP.md      # Milestones and schedule
├── STATE.md        # Current progress state
├── ARCHITECTURE.md # Architecture design
└── TASKS.md        # Detailed task list
```

## Usage Examples

```
/project-plan my-app
/project-plan ./docs/PRD.md
```

## Output Format

```
📋 Project Plan Created

Project: [Project name]
Estimated phases: [N] milestones
Steel Thread: [Core feature list]

Milestones:
M1: [Foundation] - N tasks
M2: [Core features] - N tasks
M3: [Integration/Testing] - N tasks

Planning documents created in .planning/ folder.
```
