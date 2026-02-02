# Claude Code User Guide

> SuperClaude v2.0.9 | Mac Studio Ultra M2
> Generated: 2026-02-01

---

## Table of Contents

 1. Quick Start
 2. Slash Commands
 3. Vibe/Mode Keywords
 4. Parallel Agents
 5. Orchestrator
 6. Plan Mode
 7. Persona System
 8. Hook System
 9. JARVIS System
10. Skill List
11. Shortcuts and Triggers
12. Automation Services

---

## 1. Quick Start

### Core Principles

  Response Language    All responses in Korean
  Efficiency           Execute immediately, 3-line summary max
  Automation           Hooks auto-verify/format

### Frequently Used Commands

  /j               JARVIS briefing (today's tasks, yesterday's work)
  /commit          Create git commit
  /market          Economic market report
  /project-status  Project progress status

---

## 2. Slash Commands

### Project Management

  /project-plan      Create project plan from PRD
  /project-status    Check current progress
  /project-continue  Continue previous work

### Development Tools

  /commit            Create git commit
  /commit-push-pr    Commit -> Push -> Create PR
  /code-review       PR code review
  /generate-tests    Auto-generate tests
  /review-pr         Expert agent PR review

### Research & Analysis

  /orchestrator      Comprehensive research (parallel agents)
  /ideation          Multi-persona idea discussion
  /research          Deep research

### Utilities

  /j                 JARVIS briefing
  /market            Economic market report
  /recover           Session/system recovery
  /error-search      Search Error KB
  /ctx               Context summary
  /vibe              Check/change current Vibe settings
  /daily             Frequently used paths collection
  /telegram          Telegram monitoring

### SuperClaude Commands (sc:)

  /sc:analyze        Code/project analysis
  /sc:implement      Feature implementation
  /sc:test           Run tests
  /sc:build          Build project
  /sc:git            Git operations helper
  /sc:task           Task management
  /sc:design         System/component design
  /sc:explain        Code/concept explanation
  /sc:improve        Code improvement
  /sc:cleanup        Code cleanup
  /sc:document       Generate documentation
  /sc:workflow       Execute workflow
  /sc:spawn          Spawn agent
  /sc:estimate       Estimate task scope
  /sc:troubleshoot   Troubleshoot issues
  /sc:news           News collection and summary
  /sc:report         Generate daily economic report
  /sc:calendar       Economic indicator release schedule
  /sc:index          List SC commands
  /sc:load           Load context

---

## 3. Vibe/Mode Keywords

Auto-detected when included in prompts.

### Vibe Keywords (Natural Language Triggers)

  Keyword     Alias    Action
  -----------------------------------------------------
  quick       qk       Skip verification, execute immediately
  experiment  exp      Snapshot -> Execute -> Rollback option
  parallel    para     Parallel agent execution
  fix         fix      Error KB + Self-Healing
  undo        undo     Rollback to last snapshot
  continue    cont     Continue previous work
  check       chk      Type + Lint + Build verification
  detail      det      Detailed analysis mode
  summarize   sum      Brief summary only
  compare     cmp      A/B comparison analysis
  optimize    opt      Performance optimization
  security    sec      Enhanced security review
  document    doc      Auto-generate documentation

### Mode Keywords

  Keyword          Action
  -----------------------------------------------------
  plan             Enter plan mode
  yolo             Execute without verification
  strategic        Strategic analysis mode
  visual           Visualization-focused

### Usage Examples

  "quick build login page"               -> Skip verification, implement immediately
  "parallel test 3 APIs"                 -> Parallel agent execution
  "fix this code"                        -> Reference Error KB + auto-fix
  "continue"                             -> Resume previous work

---

## 4. Parallel Agents

### Basic Usage

Use "parallel" keyword for automatic parallel execution:

  "parallel run tests, lint, and build"

### Available Agent Types

  Agent                     Description
  -----------------------------------------------------
  Explore                   Codebase exploration
  Plan                      Implementation planning
  Bash                      Command execution
  code-reviewer             Code review
  code-explorer             Codebase analysis
  code-architect            Architecture design
  code-simplifier           Code simplification
  silent-failure-hunter     Silent failure detection
  type-design-analyzer      Type design analysis
  pr-test-analyzer          PR test analysis
  comment-analyzer          Comment analysis

### Parallel Execution Settings

  max_agents: unlimited
  smart_grouping: true (auto dependency detection)

---

## 5. Orchestrator

### Usage

  /orchestrator <research topic>

### Examples

  /orchestrator Impact of AI on cryptography
  /orchestrator Korean real estate market outlook 2026
  /orchestrator Quantum computing applications in finance

### Workflow

  1. Query Analysis     Clarify questions
  2. Research Brief     Structure research questions
  3. Strategy           Develop research strategy
  4. Parallel Research  Execute parallel research
  5. Synthesis          Synthesize results
  6. Report             Generate final report

### Agents Used

  Agent                   Role
  -----------------------------------------------------
  research-orchestrator   Overall coordination
  academic-researcher     Academic research
  technical-researcher    Technical investigation
  data-analyst            Data analysis
  fact-checker            Fact checking
  research-synthesizer    Result synthesis
  report-generator        Report generation

---

## 6. Plan Mode

### Entry Methods

  1. Auto     Auto-enter when PRD document sent
  2. Manual   Use "plan" keyword
  3. Explicit "plan mode for ~"

### Plan Mode Workflow

  PRD received -> Enter plan mode -> Explore codebase -> Write plan -> User approval -> Implement

### Exiting Plan Mode

  - Enter "exit plan mode" or "approve"
  - ExitPlanMode tool auto-invoked

### Plan File Location

  ~/.claude/plans/<plan-name>.md

---

## 7. Persona System

### Persona Categories

#### Development (dev) - 14

  Persona        Specialty
  -----------------------------------------------------
  backend        Backend development
  frontend       Frontend development
  architect      System architecture
  devops         DevOps/Infrastructure
  security       Security
  qa             Testing/Quality
  performance    Performance optimization
  analyzer       Code analysis
  refactorer     Refactoring
  explorer       Codebase exploration
  librarian      Library management
  mentor         Code education
  multimodal     Multimodal
  scribe         Documentation

#### Finance (finance) - 13

  Persona                 Specialty
  -----------------------------------------------------
  macro_economist         Macroeconomic analysis
  chart_analyst           Chart analysis
  bond_analyst            Bond analysis
  fx_trader               FX trading
  commodity_specialist    Commodity specialist
  derivatives_specialist  Derivatives specialist
  quant_strategist        Quant strategy
  risk_manager            Risk management
  sentiment_analyst       Sentiment analysis
  onchain_analyst         On-chain analysis
  kr_stock_analyst        Korean stocks
  us_stock_analyst        US stocks

#### Ideation (ideation) - 27

  Persona         Role
  -----------------------------------------------------
  ceo             CEO perspective
  cfo             Financial perspective
  coo             Operations perspective
  marketing       Marketing strategy
  sales           Sales strategy
  bd              Business development
  designer        Design perspective
  ux              User experience
  futurist        Future outlook
  visionary       Vision articulation
  innovator       Innovation ideas
  inventor        Inventor perspective
  disruptor       Disruptive innovation
  critic          Critical review
  devil_advocate  Counter arguments
  realist         Realistic analysis
  risk_analyst    Risk analysis
  moderator       Discussion facilitation
  researcher      Research perspective
  user_advocate   User advocacy
  ethnographer    User research
  competitor      Competitor perspective
  content         Content strategy
  community       Community management
  growth          Growth strategy
  pr              PR strategy
  legal           Legal perspective

### Persona Activation

Auto-activation: Automatically applied when prompt keywords detected

  "design backend API"          -> backend persona activated
  "analyze macroeconomics"      -> macro_economist activated

---

## 8. Hook System

### Hook Event Types

  Event               Trigger Point              Purpose
  -----------------------------------------------------------------
  UserPromptSubmit    After prompt sent          Keyword detection, Mode setting
  PreToolUse          Before tool execution      Permission check, W-R setup
  PostToolUse         After tool execution       Formatting, Testing, Quality check
  Stop                Session end                Session save

### Currently Active Hooks

#### UserPromptSubmit (7)

  Hook                          Purpose
  -----------------------------------------------------
  jarvis-morning-briefing       JARVIS morning briefing
  keyword-detector              Vibe/Mode keyword detection
  context-cleaner               Auto context cleanup
  plan-mode-analyzer            PRD detection -> Plan mode
  todo-continuation             Restore incomplete tasks
  language-enforcer             Force Korean response
  persona-activator             Auto persona activation

#### PreToolUse (1)

  Hook                    Purpose
  -----------------------------------------------------
  writer-reviewer-hook    4-agent quality review

#### PostToolUse (10)

  Hook                        Matcher           Purpose
  -----------------------------------------------------------------
  jarvis-work-tracker         Edit|Write|Bash   Work tracking
  jarvis-task-completion      TodoWrite         Task completion tracking
  session-snapshot            Edit|Write        Session snapshot
  format-python               Edit|Write        Python ruff format
  format-js-ts                Edit|Write        JS/TS format
  run-tests                   Edit|Write        Auto test
  quality-gate                Edit|Write        8-step quality verification
  pattern-tracker             Edit|Write        Pattern learning
  background-notification     Bash              Background completion alert
  error-auto-resolver         Bash              Ralph Loop error resolution
  ralph-loop-checker          Task              Infinite loop detection

### Writer-Reviewer System

  Code writing -> 4 Reviewers parallel review -> Score < 85%? -> Repeat (max 10)

  Agent           Weight   Checks
  -----------------------------------------------------------------
  Quality         30%      Readability, Types, SOLID, DRY
  Security        30%      XSS, Injection, OWASP Top 10
  Performance     20%      Algorithm, Rendering, Memory
  Accessibility   20%      Semantic HTML, ARIA, WCAG

---

## 9. JARVIS System

### Briefing Command

  /j              Show briefing
  /j briefing     Show briefing

### Briefing Contents

  1. Yesterday's summary      Completed work list
  2. Today's schedule         Planned tasks
  3. Incomplete tasks         In-progress tasks
  4. Running services         LaunchAgent status
  5. Next task suggestion     ML-based recommendation

### JARVIS Hooks

  Hook                        Function
  -----------------------------------------------------
  jarvis-morning-briefing     Auto morning briefing
  jarvis-work-tracker         Work history tracking
  jarvis-task-completion      Task completion recording

---

## 10. Skill List

### Development Tools

  Skill                         Description
  -----------------------------------------------------
  agent-development             Agent development guide
  command-development           Slash command development
  skill-development             Skill development guide
  hook-development              Hook development guide
  plugin-structure              Plugin structure guide
  mcp-integration               MCP server integration
  frontend-design               Frontend design

### Project Management

  Skill                         Description
  -----------------------------------------------------
  claude-automation-recommender Automation recommendations
  claude-md-improver            CLAUDE.md improvement
  prd-create                    PRD generation
  project-scaffold              Project scaffold

### Finance/Data

  Skill            Description
  -----------------------------------------------------
  market           Economic market report
  daily            Frequently used paths collection
  telegram         Telegram monitoring
  sns-automation   SNS automation

### Stripe

  Skill                   Description
  -----------------------------------------------------
  stripe-best-practices   Stripe best practices
  test-cards              Stripe test cards
  explain-error           Stripe error explanation

---

## 11. Shortcuts and Triggers

### Keyboard Shortcuts

  Shortcut     Action
  -----------------------------------------------------
  Ctrl + C     Cancel execution
  Ctrl + D     End session
  Ctrl + L     Clear screen
  Tab          Auto-complete
  Arrow Up/Down    History navigation

### Natural Language Triggers

  Trigger      Action
  -----------------------------------------------------
  "quick"      Immediate execution mode
  "parallel"   Parallel agents
  "fix"        Error fix mode
  "continue"   Resume previous work
  "check"      Verification mode

### PRD Auto-Detection

PRD document sent auto-enters plan mode:

  # Project Name
  ## Goals
  ## Functional Requirements
  ## Tech Stack

---

## 12. Automation Services

### LaunchAgent Schedule

  Service                Time       Description
  -----------------------------------------------------------------
  fred-monitor           21:55      FRED economic indicators
  evening-report         22:00      Evening report
  cot-report             Sat 06:00  COT weekly report
  music-lesson-watcher   Always     Music lesson summary (GAS)
  mcp-router             Always     MCP server routing

### Notification Settings

  Telegram   FRED, COT, Evening report completion alerts
  macOS      Background task completion alerts

---

## File Structure

  ~/.claude/
  ├── CLAUDE.md                  Main configuration
  ├── settings.json              Permissions, Hooks
  ├── CLAUDE-CODE-USER-GUIDE.md  This file
  ├── docs/                      Detailed documentation
  ├── skills/                    Skill definitions (22)
  ├── personas/                  Personas (45+)
  │   ├── dev/                   Development (14)
  │   ├── finance/               Finance (13)
  │   └── ideation/              Ideation (27)
  ├── hooks/                     Hook scripts
  ├── modules/                   Automation modules
  │   ├── trading/               Trading
  │   ├── music-lesson/          Music lesson
  │   └── news-collector/        News collection
  ├── scripts/                   Scripts
  ├── credentials/               API keys
  ├── mcp-router/                MCP router
  └── plans/                     Plan files

---

## Help

  /help      Claude Code help
  /tasks     Running tasks
  /compact   Context compression
  /clear     Clear screen

---

META
- Generated: 2026-02-01
- Version: SuperClaude v2.0.9
- Tool: Claude Code
