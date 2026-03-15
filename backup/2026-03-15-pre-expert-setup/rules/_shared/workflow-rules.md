# Workflow Rules (CLAUDE.md에서 분리)

## Slash Commands

| Command | Action |
|---------|--------|
| /prd-create | Generate PRD from idea |
| /project-plan | Initialize project from PRD |
| /project-status | Check current progress |
| /project-continue | Resume previous work |
| /scaffold | Quick TypeScript CLI project setup |
| /ideation | Multi-persona ideation discussion |
| /research | Deep research |
| /error-search | Search Error KB |
| /recover | Session recovery |
| /tdd | Start TDD workflow |
| /e2e | Create E2E tests |
| /workflow | Claude-Codex collaboration |

## Skill Capture Rules

**Trigger conditions (if any met, create skill):**
- New project/tool creation completed
- Reusable workflow implemented
- Complex integration completed (API, etc.)
- User mentions "reuse later" / "나중에 재사용"

**Save location**: `~/.claude/skills/<skill-name>.md`

**Structure**:
```markdown
---
name: <skill-name>
description: <one-line description>
version: "1.0.0"
triggers:
  - /<command>
  - <natural language trigger>
---
# <Skill Name>
## Usage
## Execution Instructions
## Reference
```

**Post-completion**: Notify user with reuse command.

## Documentation Reference

| Topic | Path |
|-------|------|
| Full System | `docs/SUPERCLAUDE-REFERENCE.md` |
| Thinking Modes | `docs/THINKING-MODES.md` |
| Project Planning | `docs/PROJECT-PLANNING.md` |
| Hook System | `docs/HOOKS-SYSTEM.md` |
| Personas | `docs/PERSONAS.md` |
| Quality Gates | `docs/QUALITY-GATES.md` |
