# Goal 3: Developer (Claude Code)

## Core Agents (System Registered)

| Agent | Role |
|-------|------|
| `code-architect` | Architecture design, scalability analysis |
| `code-reviewer` | Code quality review, security check |
| `code-explorer` | Codebase analysis, structure mapping |
| `code-simplifier` | Complex code simplification |
| `fullstack-developer` | Fullstack development support |
| `security-engineer` | Security vulnerability analysis |
| `devops-engineer` | CI/CD, deployment automation |
| `test-engineer` | Test coverage, quality assurance |

## Recommended Personas (Auto-Activated)

| Persona | Usage |
|---------|-------|
| `security` | Auto-activate on auth/payment code (90% priority) |
| `architect` | Activate on system design |
| `backend` | Activate on API development |
| `frontend` | Activate on UI component development |
| `qa` | Activate on test code writing |
| `devops` | Activate on deployment configuration |

## Auto-Activation Keywords

```yaml
security (auto): auth, login, password, token, session, payment
architect (auto): architecture, design, structure, system
frontend (auto): component, ui, form, button, css
backend (auto): api, endpoint, database, server
qa (auto): test, e2e, coverage, bug, quality
devops (auto): deploy, ci, cd, docker, kubernetes
```

## Development Environment

```
┌──────────────────────────────────────────────┐
│              Mac Studio M2 Ultra              │
│                  (Main Dev)                   │
├──────────────────────────────────────────────┤
│ • Claude Code + SuperClaude v2.0.9           │
│ • Xcode (iOS/macOS apps)                     │
│ • Docker, Kubernetes                         │
│ • 24 parallel agents concurrent              │
└──────────────────────────────────────────────┘
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Raspberry Pi│ │ Jetson      │ │ Office PC   │
│ (Test Server)│ │ (AI Test)  │ │ (Build Srv) │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Integrated Workflow

```bash
# Step 1: Architecture Design
> "str trading bot architecture design.
   architect + analyzer + performance personas activated"

# Step 2: Code Implementation
> "para data-engineer + quant-analyst agents
   implement FinBERT news pipeline"

# Step 3: Quality Verification
> "code-reviewer + security-engineer + test-engineer
   parallel code review"
```

---

**Related**: [trading.md](trading.md), [music.md](music.md)
