# Claude Skills User Guide

> SuperClaude v2.0.9 Skill System

---

## Overview

Skills are predefined workflows that perform specific tasks.
Invoke with `/` commands to execute automated multi-step operations.

---

## Core Skills

### PRD Generation

| Command | Description |
|---------|-------------|
| `/prd-create` | Idea -> Business viability check -> PRD generation |

**Workflow**
1. Receive and refine idea/concept
2. Business viability review (Go/No-Go)
3. Technical/Design research
4. PRD document generation
5. Confirmation + Next steps

**Mode Options**
| Mode | Agents | Sections |
|------|--------|----------|
| quick | None | 1-10 |
| standard | PRD team (4) | 1-10 |
| thorough | Full (Business+Tech+PRD) | 1-10 |
| enterprise | Full + Legal/Cost/Risk | 1-26 |

---

### Project Management

| Command | Description |
|---------|-------------|
| `/project-plan` | Start project from PRD |
| `/project-status` | Check current progress |
| `/project-continue` | Continue previous work |

**Project Plan Workflow**
```
Step 1: Deep analysis + Questions + Ideas
├── 5 Layer Analysis (Business/Functional/Technical/UX/Risk)
├── Questions (Red:Must/Yellow:Confirm/White:Later)
└── AI idea suggestions

Step 2: Blueprint + Approval [Single approval point]
├── BLUEPRINT.md (screens, journeys, data, sections)
└── "Building as follows. Proceed?"

Step 3: Adaptive Parallel Auto-Development
├── Steel Thread implementation
├── Adaptive parallel (start with 10)
└── Completion report
```

---

### Ideation Discussion

| Command | Description |
|---------|-------------|
| `/ideation` | Multi-persona idea discussion |

**Mode Selection**
| Mode | Description |
|------|-------------|
| sequential | Sequential discussion (round-based) - Deep analysis |
| debate | Pro/Con debate (team opposition) - Go/No-Go decision |
| brainstorm | Brainstorming (parallel ideas) - Diverse ideas |

**Depth Selection**
| Depth | Persona Count | Use Case |
|-------|---------------|----------|
| quick | 5 | Quick review |
| standard | 10 | General ideation |
| deep | 15+ | Important decisions |
| full | 27 | Strategic decisions |

---

### Research

| Command | Description |
|---------|-------------|
| `/research` | General deep research |

**Features**
- Web search integration
- Document crawling
- Summarization and analysis
- Source compilation

---

### Error Handling

| Command | Description |
|---------|-------------|
| `/error-search` | Search Error KB |

**Usage**
```bash
/error-search "Cannot find module"
/error-search --type typescript
/error-search --pending
/error-search --stats
```

---

### Recovery

| Command | Description |
|---------|-------------|
| `/recover` | Session recovery |

**Options**
```bash
/recover           # Recover last snapshot
/recover --list    # List snapshots
/recover --id X    # Recover specific snapshot
```

---

## Skill Extension

### Custom Skill Creation

```yaml
# ~/.claude/skills/my-skill.yaml
name: my-skill
description: "My custom skill"
trigger: "/my-skill"
steps:
  - action: read_files
    pattern: "src/**/*.ts"
  - action: analyze
    type: "dependencies"
  - action: generate_report
    format: "markdown"
```

### Skill Installation

```bash
# Install from marketplace
claude skill install <skill-name>

# Install from local file
claude skill install ./my-skill.yaml
```
