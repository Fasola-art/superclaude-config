# Goal-Based Persona & Agent Optimal Configuration

> 3 Goals: Trading, Music/Composition, Development
> Total: 79 Agents + 41 Personas

---

## Table of Contents

1. [Trading (Side Hustle → Main)](#-goal-1-trading-side-hustle--main)
2. [Music Teacher + Composer (Main)](#-goal-2-music-teacher--composer-main)
3. [Developer (Claude Code)](#-goal-3-developer-claude-code)
4. [Integrated Workflow](#-integrated-workflow-recommended)
5. [Quick Command Summary](#-quick-command-summary)

---

## 🎯 Goal 1: Trading (Side Hustle → Main)

### Required Agents

| Agent                  | Role                                       |
|------------------------|--------------------------------------------|
| `quant-analyst`        | Quant strategy analysis, backtesting design |
| `data-analyst`         | Market data analysis, visualization        |
| `data-scientist`       | ML model (FinBERT, YOLO) design            |
| `data-engineer`        | Data pipeline construction                 |
| `performance-profiler` | System performance optimization            |

### Recommended Personas

| Persona       | Usage                                          |
|---------------|------------------------------------------------|
| `analyzer`    | Market pattern analysis, root cause tracking   |
| `architect`   | Trading system architecture design             |
| `performance` | Execution speed optimization, latency reduction |
| `risk_analyst` | Risk management strategy                       |
| `cfo`         | Fund management, ROI analysis                  |

### Immediate Usage Examples

```bash
# Start quant analysis
> "str para design trading pipeline.
   Jetson(FinBERT) + RPi5(YOLO) + 4090(Main) integration"

# Backtesting optimization
> "perf analyze backtesting performance.
   Currently takes too long to process 5 years of data"

# Data pipeline
> "data-engineer agent to build real-time news → sentiment analysis pipeline"
```

### Trading System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     24-Hour Automation Pipeline                  │
└─────────────────────────────────────────────────────────────────┘

     News API          Exchange API       Chart Screenshot
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Jetson Orin    │ │  4090 Laptop    │ │  Raspberry Pi   │
│  ────────────── │ │  ────────────── │ │  ────────────── │
│  FinBERT Anal.  │ │  Real-time Price│ │  YOLO Pattern   │
│  Sentiment Score│ │  Order Execution│ │  Candle/Pattern │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                   ┌─────────────────┐
                   │   Integrated    │
                   │     Signal      │
                   │  (Weighted)     │
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
         Telegram      Auto Order      Dashboard
          Alert        Execution      (Tab/Phone)
```

---

## 🎵 Goal 2: Music Teacher + Composer (Main)

### Recommended Agents

| Agent                     | Role                                |
|---------------------------|-------------------------------------|
| `content-marketer`        | Lesson content marketing            |
| `social-media-copywriter` | SNS promotional copy                |
| `technical-writer`        | Textbook/curriculum documentation   |
| `video-editor`            | Lesson video editing advice         |
| `seo-analyzer`            | Online lesson promotion optimization |

### Recommended Personas

| Persona         | Usage                                               |
|-----------------|-----------------------------------------------------|
| `mentor`        | Education content design, learning stage structure  |
| `creative`      | Composition idea brainstorming (ideation session)   |
| `content`       | Lesson material storytelling                        |
| `marketing`     | Lesson branding, differentiation strategy           |
| `user_advocate` | Student perspective consideration                   |

### Immediate Usage Examples

```bash
# Lesson curriculum design
> "mentor persona to design 12-week beginner piano curriculum"

# Idea discussion
> "/ideation new song concept: electronic music + traditional Korean fusion"

# Promotional content
> "content-marketer agent to create Instagram lesson promotion series"
```

### Music Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Music Workflow                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │   Mac Studio     │         │  Galaxy Tab S8   │              │
│  │   M2 Ultra       │         │  Ultra           │              │
│  ├──────────────────┤         ├──────────────────┤              │
│  │ • Logic Pro X    │         │ • Sheet display  │              │
│  │ • Plugins (VST)  │    ───▶ │ • Lesson material│              │
│  │ • Mastering      │         │ • Notes (S Pen)  │              │
│  │ • AI composition │         │ • Student video  │              │
│  └──────────────────┘         └──────────────────┘              │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │    LG Gram       │                                           │
│  ├──────────────────┤                                           │
│  │ • External lesson│                                           │
│  │ • Light editing  │                                           │
│  │ • Material prep  │                                           │
│  └──────────────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 Goal 3: Developer (Claude Code)

### Core Agents (System Registered)

| Agent                 | Role                                      |
|-----------------------|-------------------------------------------|
| `code-architect`      | Architecture design, scalability analysis |
| `code-reviewer`       | Code quality review, security check       |
| `code-explorer`       | Codebase analysis, structure mapping      |
| `code-simplifier`     | Complex code simplification               |
| `fullstack-developer` | Fullstack development support             |
| `security-engineer`   | Security vulnerability analysis           |
| `devops-engineer`     | CI/CD, deployment automation              |
| `test-engineer`       | Test coverage, quality assurance          |

### Recommended Personas (Auto-Activated)

| Persona     | Usage                                             |
|-------------|---------------------------------------------------|
| `security`  | Auto-activate on auth/payment code (90% priority) |
| `architect` | Activate on system design                         |
| `backend`   | Activate on API development                       |
| `frontend`  | Activate on UI component development              |
| `qa`        | Activate on test code writing                     |
| `devops`    | Activate on deployment configuration              |

### Auto-Activation Keywords

```yaml
security (auto): auth, login, password, token, session, payment
architect (auto): architecture, design, structure, system
frontend (auto): component, ui, form, button, css
backend (auto): api, endpoint, database, server
qa (auto): test, e2e, coverage, bug, quality
devops (auto): deploy, ci, cd, docker, kubernetes
```

### Development Environment

```
┌─────────────────────────────────────────────────────────────────┐
│                      Development Environment                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────┐               │
│  │              Mac Studio M2 Ultra              │               │
│  │                  (Main Dev)                   │               │
│  ├──────────────────────────────────────────────┤               │
│  │ • Claude Code + SuperClaude v2.0.9           │               │
│  │ • Xcode (iOS/macOS apps)                     │               │
│  │ • Docker, Kubernetes                         │               │
│  │ • 24 parallel agents concurrent              │               │
│  └──────────────────────────────────────────────┘               │
│                          │                                       │
│           ┌──────────────┼──────────────┐                       │
│           ▼              ▼              ▼                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │ Raspberry Pi│ │ Jetson      │ │ Office PC   │               │
│  │ (Test Server)│ │ (AI Test)  │ │ (Build Srv) │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔥 Integrated Workflow (Recommended)

### Trading System Development

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

### Daily Workflow

| Time      | Task                                                      |
|-----------|-----------------------------------------------------------|
| Morning   | Development (Mac Studio) - architect, security activated  |
| Afternoon | Music lessons (Mac + Tab) - mentor persona                |
| Evening   | Trading (4090) - analyzer, performance activated          |
| Night     | Composition (Mac) - creative persona + ideation           |

---

## 📋 Quick Command Summary

| Goal        | Command                         | Effect                               |
|-------------|---------------------------------|--------------------------------------|
| Trading     | `str para pipeline design`      | architect + analyzer + performance   |
| Analysis    | `perf backtesting optimization` | performance + data-analyst           |
| Lesson      | `mentor curriculum design`      | mentor + content                     |
| Composition | `/ideation song concept`        | Multi creative persona discussion    |
| Development | `str system design`             | architect + security + backend       |
| Review      | `/review-pr`                    | code-reviewer parallel execution     |

---

## 📊 Full Agent List (79)

### Development/Code

- `code-architect`, `code-explorer`, `code-reviewer`, `code-simplifier`
- `fullstack-developer`, `frontend-developer`, `backend-architect`
- `typescript-pro`, `python-pro`, `golang-pro`, `sql-pro`

### Security/Quality

- `security-engineer`, `security-auditor`, `api-security-audit`
- `test-engineer`, `feature-code-reviewer`, `silent-failure-hunter`

### Data/AI

- `data-analyst`, `data-scientist`, `data-engineer`
- `quant-analyst`, `ml-engineer`, `model-evaluator`

### Infrastructure/Deployment

- `devops-engineer`, `cloud-architect`, `database-architect`
- `vercel-deployment-specialist`, `performance-profiler`

### Research/Analysis

- `research-orchestrator`, `research-synthesizer`, `academic-researcher`
- `technical-researcher`, `fact-checker`, `competitive-intelligence-analyst`

### Content/Marketing

- `content-marketer`, `social-media-copywriter`, `social-media-clip-creator`
- `seo-analyzer`, `video-editor`, `technical-writer`

### Special/Other

- `business-analyst`, `product-strategist`, `prompt-engineer`
- `mcp-expert`, `ai-ethics-advisor`, `agent-creator`

---

## 📊 Full Persona List (41)

### Development (14)

`security`, `architect`, `backend`, `performance`, `frontend`, `qa`,
`devops`, `analyzer`, `refactorer`, `explorer`, `librarian`, `mentor`,
`scribe`, `multimodal`

### Business (6)

`ceo`, `cfo`, `coo`, `sales`, `bd`, `legal`

### Marketing (5)

`marketing`, `growth`, `content`, `community`, `pr`

### Innovation (5)

`innovator`, `futurist`, `visionary`, `disruptor`, `inventor`

### Design (3)

`designer`, `ux`, `user_advocate`

### Verification (4)

`critic`, `realist`, `devil_advocate`, `risk_analyst`

### Research (3)

`researcher`, `ethnographer`, `competitor`

### Special (1)

`moderator`

---

**META**
- Generated: 2026-01-31
- Tool: Claude Code (SuperClaude v2.0.9)
- Total: 79 Agents + 41 Personas
