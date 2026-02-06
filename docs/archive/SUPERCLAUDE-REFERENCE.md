# SuperClaude Complete Reference

> **Version**: 2.0.9
> **Platform**: Mac Studio Ultra M2
> **Last Updated**: 2026-01-30

---

## Architecture

```
~/.claude/
├── CLAUDE.md                 # Main config (entry point)
├── settings.json             # Permissions, Hooks, Settings
├── docs/                     # Detailed documentation
│   ├── WRITER-REVIEWER-SYSTEM.md
│   ├── HOOKS-SYSTEM.md
│   ├── PERSONAS.md
│   ├── QUALITY-GATES.md
│   ├── PROJECT-PLANNING.md
│   └── ...
├── profiles/                 # Language profiles
│   ├── typescript.md
│   └── rust.md
├── skills/                   # 34 skills
├── hooks/                    # Hook scripts
├── mcp-router/               # MCP router
├── jarvis/                   # Personal assistant system
└── cheatsheets/              # Quick reference
```

---

## Configuration (settings.json)

### Permission System

| Category | Setting                                                       |
|----------|---------------------------------------------------------------|
| ✔ Allow  | File read/write, Git (except push), npm/pip, supabase, gh CLI |
| ✘ Deny   | git push, rm -rf, sudo, .env access                           |
| Auto     | acceptEdits (auto-accept edits)                               |

```json
"permissions": {
  "allow": [
    "Read:**", "Write:**", "Edit:**",
    "Bash:git status", "Bash:git add*", "Bash:git commit*",
    "Bash:npm install*", "Bash:npm run*",
    "Bash:supabase gen types*", "Bash:supabase migration*"
  ],
  "deny": [
    "Bash:git push*", "Bash:rm -rf*", "Bash:sudo*",
    "Read:.env*", "Write:.env*"
  ]
}
```

---

## Context Management

| Threshold | Action                          |
|-----------|---------------------------------|
| ⚠ 75%    | Warning (cleanup recommended)   |
| 🔴 90%   | Critical (DCP compression)      |
| 🚨 95%   | Emergency (forced compression)  |

**Strategies**: deduplication, error_cleanup, file_summarize

---

## Ralph Loop (Auto Error Resolution)

```json
"ralph_loop": {
  "enabled": true,
  "max_retries": 10,
  "auto_triggers": ["npm run build", "npm run test", "npm run lint"],
  "success_patterns": ["success", "completed", "PASSED"]
}
```

---

## Quality Gate

```json
"quality_gate": {
  "enabled": true,
  "threshold": 0.85,     // 85% pass required
  "max_iterations": 10,
  "weights": {
    "quality": 0.3,      // 30%
    "security": 0.3,     // 30%
    "performance": 0.2,  // 20%
    "accessibility": 0.2 // 20%
  }
}
```

---

## Parallel Execution

```json
"parallel_execution": {
  "max_agents": "unlimited",  // Unlimited
  "smart_grouping": true      // Auto dependency detection
}
```

---

## Writer-Reviewer System

### How It Works

```
Code Request → Writer Agent → 4 Parallel Reviewers → Score < 85%? → Iterate (max 10)
```

### 4-Agent Parallel Review

| Agent         | Weight | Checks                                             |
|---------------|--------|----------------------------------------------------|
| Quality       | 30%    | Readability, types, SOLID, DRY, UI/Hook separation |
| Security      | 30%    | XSS, injection, auth, OWASP Top 10                 |
| Performance   | 20%    | Algorithm, rendering, memory, N+1                  |
| Accessibility | 20%    | Semantic HTML, ARIA, keyboard, WCAG 2.1            |

### v2.1 Features

| Feature             | Description                                             |
|---------------------|---------------------------------------------------------|
| Security Hardening  | Prompt injection defense, review bypass prevention      |
| Adaptive Weights    | Auto weight adjustment by code type                     |
| Incremental Review  | Diff-only review from 2nd iteration (40-60% token save) |
| Forced Convergence  | <1.5% change × 2 → early exit                           |
| Conflict Resolution | Security > Quality > Performance > A11y                 |

---

## Code Architecture Principles

| Principle          | Description                               |
|--------------------|-------------------------------------------|
| UI/Hook Separation | Components for UI only, logic in use-*.ts |
| Extract Common     | 2+ repetitions → shared component         |
| SSOT               | Single source, derive computed values     |

---

## Hook Automation System

### UserPromptSubmit (6 hooks)

| Hook                          | Purpose                            |
|-------------------------------|------------------------------------|
| plan-mode-analyzer.py         | PRD detection → enter plan mode    |
| context-cleaner.js            | Context 70%+ → auto cleanup        |
| keyword-detector.js           | 13 Vibe + 4 Mode keyword detection |
| persona-activator.js          | Task-type persona activation       |
| task-continuation-enforcer.js | Restore incomplete todos           |
| daily-update-checker.js       | Daily update check                 |

### PreToolUse (2 hooks)

| Hook                    | Matcher               | Purpose                       |
|-------------------------|-----------------------|-------------------------------|
| writer-reviewer-hook.py | Edit\|Write\|MultiEdit | Activate Writer-Reviewer loop |
| error-warning-hook.js   | Edit\|Write\|MultiEdit | Error KB pattern warning      |

### PostToolUse (8 hooks)

| Hook                            | Matcher                 | Purpose                                         |
|---------------------------------|-------------------------|-------------------------------------------------|
| quality-gate.js                 | Write\|Edit\|MultiEdit  | 8-stage Quality Gate                            |
| error-auto-resolver.js          | Bash\|Task              | Ralph Loop (max 10 retries)                     |
| session-snapshot.js             | Todo\|Bash\|Write\|Edit | Auto session snapshot                           |
| infinite-loop-checker.js        | Bash\|Task              | Infinite loop detection (5 same errors → stop)  |
| pattern-tracker.js              | Task                    | Pattern learning                                |
| empty-task-response-detector.js | Task                    | Empty response detection                        |
| background-notification.js      | Task                    | Background completion notification              |

---

## Keyword Trigger System

### Vibe Keywords (13)

| Keyword    | Alias | Action                                      |
|------------|-------|---------------------------------------------|
| fast       | qk    | Skip validation, immediate execution        |
| experiment | exp   | Snapshot → execute → rollback option        |
| parallel   | para  | Parallel agent execution                    |
| fix        | fix   | Error KB + Self-Healing                     |
| undo       | undo  | Rollback to last snapshot                   |
| continue   | cont  | Continue previous work (STATE.md)           |
| check      | chk   | Type + Lint + Build verification            |
| test       | tst   | Run related tests                           |
| deploy     | dep   | Deployment checklist                        |
| cleanup    | clean | Code cleanup (unused imports, console.log)  |
| perf       | perf  | Performance analysis                        |
| plan       | plan  | Generate .planning/ docs                    |
| analyze    | map   | Codebase analysis                           |

### Mode Keywords (4)

| Keyword         | Action                  | Active Personas               |
|-----------------|-------------------------|-------------------------------|
| ultrawork (ulw) | Max parallel agents     | explorer, librarian, analyzer |
| deepsearch (ds) | Connect /research skill | explorer                      |
| strategic (str) | Tradeoff analysis       | architect                     |
| visual (vis)    | Image/UI analysis       | multimodal, frontend          |

---

## MCP Router System

### Why MCP Router?

- **Direct Registration**: All MCP tools in system prompt → context explosion
- **Router**: Single entry point, dynamic loading → context savings

### Registered Servers (servers.json)

| Server          | Purpose            | Main Tools                                   |
|-----------------|--------------------|----------------------------------------------|
| context7        | Library doc search | resolve-library-id, query-docs               |
| mana            | Code analysis      | find_symbol, search_for_pattern, rename_symbol |
| playwright      | Browser automation | browser_navigate, browser_click, browser_type |
| playwright-test | E2E testing        | test_list, test_run, test_debug              |

---

## Persona System

### Technical Personas (14)

| Persona     | Role                 | Activation Keywords          |
|-------------|----------------------|------------------------------|
| architect   | System design        | design, architecture, scale  |
| frontend    | UI/UX, accessibility | UI, component, style         |
| backend     | API, data            | API, server, database        |
| security    | Security (always ON) | auth, login, password, token |
| analyzer    | Root cause analysis  | error, bug, debugging        |
| performance | Optimization         | performance, slow, memory    |
| tester      | Testing              | test, coverage, E2E          |
| refactorer  | Code quality         | refactoring, cleanup, DRY    |
| devops      | Deploy, infra        | deploy, CI/CD, docker        |
| mentor      | Education            | explain, why, how            |
| scribe      | Documentation        | document, README             |
| explorer    | Code exploration     | find, search, where          |
| librarian   | Doc reference        | docs, reference              |
| multimodal  | Image analysis       | visual, screenshot           |

### Ideation Personas (27)

**Categories:**
- Business (6): ceo, cfo, coo, sales, bd, legal
- Marketing (5): marketing, growth, content, community, pr
- Innovation (5): innovator, futurist, visionary, disruptor, inventor
- Design (3): designer, ux, user_advocate
- Analysis (4): critic, realist, devil_advocate, risk_analyst
- Research (3): researcher, ethnographer, competitor
- Facilitation (1): moderator

---

## Language Profiles

### TypeScript Profile

**Activation**: package.json detected

| Principle      | Content                                           |
|----------------|---------------------------------------------------|
| Never Throws   | Use Result<T, E> pattern                          |
| Zod Validation | Schema-first development                          |
| State Layers   | TanStack Query → Zustand → React Hook Form → nuqs |
| Strict Mode    | strict: true, noUncheckedIndexedAccess            |

**Auto-detection:**
- <Image> usage → recommend next/image
- import _ from 'lodash' → recommend tree-shakable import
- useQuery without staleTime → recommend setting

### Rust Profile

**Activation**: Cargo.toml detected

| Principle       | Content               |
|-----------------|-----------------------|
| Never Panics    | Result<T, E> required |
| Memory Leaks    | RAII, Drop impl       |
| Data Corruption | Maintain immutability |

**Tools:**
- cargo clippy -- -D warnings
- cargo fmt --check
- cargo +nightly miri test

---

## Skill System

### Main Skills (34+)

| Category  | Skills                                         |
|-----------|------------------------------------------------|
| Documents | pdf, docx, pptx, xlsx                          |
| Design    | frontend-design, canvas-design, algorithmic-art |
| Dev       | frontend-dev, mcp-builder, webapp-testing      |
| Planning  | prd-create, ideation, research, agent-team     |
| Present   | presentation-orchestrator, brand-guidelines    |

### Key Skill Commands

| Command         | Purpose                  |
|-----------------|--------------------------|
| /prd-create     | Idea → PRD generation    |
| /project-plan   | PRD → project plan       |
| /project-status | Check progress           |
| /research       | General deep research    |
| /ideation       | Multi-persona discussion |

---

## Project Planning

### 8-Step Workflow

1. **Phase 1**: Deep analysis + questions + ideas
2. **Phase 2**: 5 Layer analysis (Business/Functional/Technical/UX/Risk)
3. **Phase 3**: Question priority (🔴 Required / 🟡 Confirm / ⚪ Later)
4. **Phase 4**: AI idea suggestions
5. **Phase 5**: Blueprint + approval (★ Only approval point)
6. **Phase 6**: BLUEPRINT.md (screens, user journey, data structure)
7. **Phase 7**: Execution plan (Section → Milestone → Task)
8. **Phase 8**: Adaptive parallel auto-development

### Deliverables
- BLUEPRINT.md (screens, user journey, data structure)
- Execution plan (Section → Milestone → Task)
- Auto-generated completion report

### Execution Features
- Steel Thread implementation (architecture validation)
- Start with 5 → adjust by success rate (max unlimited)
- Adaptive parallel auto-development

---

## Adaptive Parallel Execution

```yaml
initial: 5 concurrent
conditions:
  3 consecutive success → +5
  1 failure → -3 (min 3)
maximum: unlimited
```

---

## Summary Statistics

| Item               | Count                |
|--------------------|----------------------|
| Hooks              | 17                   |
| Vibe Keywords      | 13                   |
| Mode Keywords      | 4                    |
| Technical Personas | 14                   |
| Ideation Personas  | 27                   |
| Skills             | 34+                  |
| Language Profiles  | 2 (TypeScript, Rust) |
| MCP Servers        | 4                    |

---

## Jarvis System

### Overview
Personal assistant system providing work continuity, ML-based prediction, and autonomous task execution.

### Folder Structure
```
~/.claude/jarvis/
├── memory/
│   ├── manager.py         # Memory manager (SQLite)
│   ├── jarvis.db          # SQLite database
│   └── ml_predictor.py    # ML pattern learning & prediction
├── automation/
│   ├── browser.py         # Browser automation
│   └── task_executor.py   # Task execution engine
├── data/
│   ├── tasks.json         # Task list
│   └── calendar.json      # Calendar
├── daemon.py              # Background Daemon
└── test_jarvis.py         # Tests
```

### Core Features (6 Phases)

| Phase | Feature          | Description                                     |
|-------|------------------|-------------------------------------------------|
| 1     | Morning Briefing | Auto-display yesterday's work/today's schedule  |
| 2     | Work Continuity  | `/j remember` - restore last work context       |
| 3     | Auto Task Exec   | `/j do <task>` - analyze intent, auto-execute   |
| 4     | ML Learning      | scikit-learn based time-pattern learning        |
| 5     | Life Management  | `/j book`, `/j plan` - booking/event planning   |
| 6     | Background Daemon | Auto retraining/backup/pattern updates          |

### Commands

| Command           | Purpose                |
|-------------------|------------------------|
| `/j`              | Invoke Jarvis          |
| `/j briefing`     | Detailed briefing      |
| `/j remember`     | Check work continuity  |
| `/j do <task>`    | Execute task           |
| `/j book <item>`  | Restaurant/movie/hotel |
| `/j plan <event>` | Trip/party/project     |

### Database Schema

| Table           | Purpose                                           |
|-----------------|---------------------------------------------------|
| work_sessions   | Work session records (time, project, files)       |
| usage_patterns  | ML learning patterns (day, time, task type, freq) |
| tasks           | Task list (title, status, priority, deadline)     |
| calendar_events | Calendar (title, time, location, event type)      |

### ML Learning Features
- scikit-learn based pattern learning
- Time/day behavior prediction (with confidence)
- Peak time analysis
- Minimum 10 patterns required

### Privacy
- **Local-First**: All data in local SQLite
- **No Cloud**: No external server transmission
- **Optional Encryption**: Database encryption available

---

## ultrawork (ulw) Workflow Detail

### Usage Example
```
"ulw analyze the entire project structure"
```

### Sequence Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      User Input                              │
│  "ulw analyze this codebase and figure out the structure"   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            Phase 1: UserPromptSubmit Hooks                   │
│  settings.json → hooks.UserPromptSubmit (6 hooks sequential) │
│                                                              │
│  #1 jarvis-morning-briefing.py                               │
│  #2 plan-mode-analyzer.py                                    │
│  #3 context-cleaner.js                                       │
│  #4 keyword-detector.js ◄── 🎯 "ulw" detected here!          │
│  #5 persona-activator.js                                     │
│  #6 todo-continuation-enforcer.js                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            Phase 2: keyword-detector.js Internal             │
│                                                              │
│  1. Read prompt from env                                     │
│     const userPrompt = getEnv('CLAUDE_USER_PROMPT');         │
│                                                              │
│  2. Search keywords (priority order)                         │
│     priorityOrder = ['strategic', 'str', 'ultrawork',        │
│                      'ulw', ...]                             │
│                                                              │
│  3. Load config                                              │
│     config = {                                               │
│       action: 'Maximum parallel agent utilization',          │
│       personas: ['explorer', 'librarian', 'analyzer'],       │
│       parallel: true,                                        │
│       flags: ['--think']                                     │
│     }                                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: Activation Message (console.log → Claude context)  │
│  ═══════════════════════════════════════════════════════     │
│  🚀 "ULW" Mode Activated                                     │
│  🔧 Action: Maximum parallel agent utilization               │
│  👥 Personas: explorer, librarian, analyzer                  │
│  ⚡ Parallel: Enabled                                        │
│  ═══════════════════════════════════════════════════════     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Phase 4: Claude Decision                        │
│                                                              │
│  Reference parallel_execution.max_agents = "unlimited"       │
│  → Decide multi-parallel Task agent execution                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Phase 5: Parallel Agent Execution               │
│                                                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │
│  │ 🔍 Explorer  │ │ 📚 Librarian │ │ 📊 Analyzer  │         │
│  │   Agent 1    │ │   Agent 2    │ │   Agent 3    │         │
│  │ File struct  │ │ README       │ │ Dependency   │         │
│  │ analysis     │ │ Doc search   │ │ Complexity   │         │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘         │
│         └────────────────┼────────────────┘                  │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Result Integration                  │    │
│  │  • Project structure  • Key file list               │    │
│  │  • Dependency graph   • Architecture analysis       │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Key Point - Context Injection
- console.log() output from keyword-detector.js injected into Claude context
- Claude "recognizes" detected mode/personas and decides behavior
- Not commands, but "hints/directives" injection

### Persona Roles

| Persona   | Role in ultrawork               |
|-----------|----------------------------------|
| explorer  | File structure, pattern search   |
| librarian | Doc reference, library info      |
| analyzer  | Dependency analysis, complexity  |
