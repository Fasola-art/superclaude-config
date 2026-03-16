# Claude Code Orchestrator/Agent/Skill/Hook Complete Guide

> Implementation-focused SuperClaude v2.0.9 deep usage guide

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Hook System Details](#hook-system-details)
3. [Parallel Agent Execution](#parallel-agent-execution)
4. [Vibe/Mode Keywords](#vibemode-keywords)
5. [Writer-Reviewer Loop](#writer-reviewer-loop)
6. [Orchestrator Workflow](#orchestrator-workflow)
7. [Real-World Scenarios](#real-world-scenarios)
8. [Quick Reference](#quick-reference)

---

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                      User Prompt                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            UserPromptSubmit Hook (7 hooks sequential)        │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────┐ │
│  │ keyword-detector │ │ plan-mode-analyzer│ │ language-   │ │
│  │ (Vibe/Mode detect)│ │ (PRD detection)   │ │ enforcer    │ │
│  └──────────────────┘ └──────────────────┘ └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code Processing                   │
│   ┌───────────────────────────────────────────────────────┐ │
│   │              PreToolUse Hook                           │ │
│   │  • writer-reviewer-hook.py (4-agent quality review)    │ │
│   └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Tool Execution (Edit/Write/Bash)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            PostToolUse Hook (12 hooks conditional)           │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────┐ │
│  │ format-python.py │ │ quality-gate.py  │ │ run-tests.py │ │
│  │ (ruff format)    │ │ (8-step verify)  │ │ (auto test)  │ │
│  └──────────────────┘ └──────────────────┘ └──────────────┘ │
│  ┌──────────────────┐ ┌──────────────────┐                  │
│  │ ralph-loop-      │ │ pattern-tracker  │                  │
│  │ checker.py       │ │.py               │                  │
│  │ (infinite loop)  │ │ (pattern learn)  │                  │
│  └──────────────────┘ └──────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### Component Relationship

```
┌─────────────────────────────────────────────────────────────┐
│                        SuperClaude v2.0.9                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │    Hooks    │───▶│   Agents    │───▶│   Skills    │      │
│  │ (automation)│    │ (parallel)  │    │ (reusable)  │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  Keywords   │    │  Personas   │    │  Commands   │      │
│  │ (triggers)  │    │  (roles)    │    │ (commands)  │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Hook System Details

### 1. Hook Event Types

| Event              | Trigger Point                  | Purpose                             | Example Hooks                       |
|--------------------|--------------------------------|-------------------------------------|-------------------------------------|
| `UserPromptSubmit` | After user prompt submission   | Keyword detection, mode setting     | keyword-detector, plan-mode-analyzer |
| `PreToolUse`       | Before tool execution          | Permission check, W-R setup         | writer-reviewer-hook                |
| `PostToolUse`      | After tool execution           | Formatting, testing, quality check  | format-python, quality-gate         |
| `Stop`             | Session end                    | Session save, state recording       | session-saver                       |

### 2. Active Hook List

#### UserPromptSubmit (7)
| Hook                 | File                          | Function                  |
|----------------------|-------------------------------|---------------------------|
| JARVIS Briefing      | `jarvis-morning-briefing.py`  | System status briefing    |
| Keyword Detection    | `keyword-detector.py`         | Vibe/Mode keyword detection |
| Context Cleanup      | `context-cleaner.py`          | Auto context compression  |
| Plan Mode Analysis   | `plan-mode-analyzer.py`       | PRD detection, plan mode entry |
| Todo Continuation    | `todo-continuation.py`        | Resume previous work      |
| Language Enforcement | `language-enforcer.py`        | Force Korean response     |
| Persona Activation   | `persona-activator.py`        | Auto persona selection    |

#### PreToolUse (1)
| Hook            | File                      | Function                     |
|-----------------|---------------------------|------------------------------|
| Writer-Reviewer | `writer-reviewer-hook.py` | 4-agent quality review setup |

#### PostToolUse (12)
| Hook                    | Matcher                 | Function                          |
|-------------------------|-------------------------|-----------------------------------|
| Task Tracking           | `Edit\|Write\|...`      | Task recording                    |
| Task Completion         | `TodoWrite\|TaskUpdate` | Completion notification           |
| Session Snapshot        | `Edit\|Write\|MultiEdit` | Change recording                  |
| Python Format           | `Edit\|Write\|MultiEdit` | ruff auto format                  |
| JS/TS Format            | `Edit\|Write\|MultiEdit` | prettier auto format              |
| Test Execution          | `Edit\|Write\|MultiEdit` | Related test auto run             |
| Quality Gate            | `Edit\|Write\|MultiEdit` | 8-step verification               |
| Pattern Tracking        | `Edit\|Write\|MultiEdit` | Coding pattern learning           |
| Background Notification | `Bash`                  | Background task completion alert  |
| Auto Error Resolution   | `Bash`                  | Error KB-based auto fix           |
| Ralph Loop Checker      | `Task`                  | Infinite loop detection           |

#### Stop (1)
| Hook         | File               | Function           |
|--------------|--------------------|--------------------|
| Session Save | `session-saver.py` | Session state save |

### 3. Hook Code Analysis

#### keyword-detector.py

```python
# 13 Vibe Keywords
VIBE_KEYWORDS = {
    # Execution Control
    "빠르게": {"aliases": ["qk", "quick"], "action": "skip_validation"},
    "실험": {"aliases": ["exp"], "action": "snapshot_experiment"},
    "동시에": {"aliases": ["para"], "action": "parallel_agents"},

    # Fix/Recovery
    "고쳐": {"aliases": ["fix"], "action": "error_kb_healing"},
    "되돌려": {"aliases": ["undo"], "action": "rollback_snapshot"},
    "계속": {"aliases": ["cont"], "action": "continue_state"},

    # Verification
    "확인해": {"aliases": ["chk"], "action": "full_validation"},
    "테스트해": {"aliases": ["tst"], "action": "run_tests"},

    # Deploy/Cleanup
    "배포해": {"aliases": ["dep"], "action": "deploy_checklist"},
    "정리해": {"aliases": ["clean"], "action": "code_cleanup"},

    # Analysis/Planning
    "성능": {"aliases": ["perf"], "action": "performance_analysis"},
    "계획": {"aliases": ["plan"], "action": "planning_docs"},
    "분석": {"aliases": ["map"], "action": "codebase_analysis"},
}

# 4 Mode Keywords
MODE_KEYWORDS = {
    "ultrawork": {"aliases": ["ulw"], "personas": ["explorer", "librarian", "analyzer"]},
    "deepsearch": {"aliases": ["ds"], "personas": ["explorer"]},
    "strategic": {"aliases": ["str"], "personas": ["architect"]},
    "visual": {"aliases": ["vis"], "personas": ["multimodal", "frontend"]},
}
```

#### quality-gate.py

```python
# 8-Step Quality Gate (weight sum = 1.0)
QUALITY_GATES = [
    {"name": "Syntax", "cmd": "check_syntax", "weight": 0.15},
    {"name": "Type", "cmd": "check_types", "weight": 0.15},
    {"name": "Lint", "cmd": "check_lint", "weight": 0.10},
    {"name": "Security", "cmd": "check_security", "weight": 0.20},  # Highest priority
    {"name": "Test", "cmd": "run_tests", "weight": 0.15},
    {"name": "Performance", "cmd": "check_perf", "weight": 0.10},
    {"name": "Docs", "cmd": "check_docs", "weight": 0.05},
    {"name": "Integration", "cmd": "check_integration", "weight": 0.10},
]

# File type check commands
# TypeScript: npx tsc --noEmit, npx eslint, npx vitest
# Python: python -m py_compile, pylint, pytest
```

#### ralph-loop-checker.py

```python
MAX_CONSECUTIVE_FAILURES = 5  # Max consecutive failure count
TIME_WINDOW_MINUTES = 5       # Time window

# Behavior:
# - 5 consecutive failures within 5 min → 🛑 Warning
# - 3+ failures → ⚠️ Early warning
# - On success → State reset
```

---

## Parallel Agent Execution

### superclaude-config.json Settings

```json
{
  "parallelExecution": {
    "enabled": true,
    "adaptive": true,
    "initial": 10,
    "minimum": 3,
    "maximum": 24,
    "scaleUp": {
      "increment": 5,
      "condition": "3 consecutive successes"
    },
    "scaleDown": {
      "decrement": 3,
      "condition": "1 failure"
    },
    "optimization": "M2 Ultra CPU cores (24 cores)"
  },
  "personas": {
    "maxConcurrent": 8,
    "priority": ["security", "architect", "analyzer"],
    "autoActivate": true
  }
}
```

### Adaptive Scaling Behavior

```
Start: 10 concurrent executions
       │
       ├── 3 consecutive successes → Increase to 15 (+5)
       │                    │
       │                    ├── 3 consecutive successes → Increase to 20
       │                    │
       │                    └── 1 failure → Decrease to 17 (-3)
       │
       └── 1 failure → Decrease to 7 (-3)
```

### Available Agents (79)

| Category          | Agent Examples        | Purpose                       |
|-------------------|-----------------------|-------------------------------|
| Code Review       | code-reviewer         | Bug, security, quality review |
| Code Exploration  | code-explorer         | Codebase analysis             |
| Testing           | pr-test-analyzer      | PR test coverage analysis     |
| Design            | code-architect        | Feature architecture design   |
| Types             | type-design-analyzer  | Type design analysis          |
| Simplification    | code-simplifier       | Code simplification           |
| Comments          | comment-analyzer      | Comment analysis              |
| Failure Detection | silent-failure-hunter | Silent failure detection      |

### Parallel Execution Trigger Methods

```bash
# Method 1: "동시에" or "para" keyword
> "para analyze this code and generate tests"
🎯 vibe:동시에

# Method 2: Multiple agents via Task tool
# (Internal auto parallel processing)
```

---

## Vibe/Mode Keywords

### Vibe Keywords (13)

| Keyword  | Alias     | Action                   | Usage Example                        |
|----------|-----------|--------------------------|--------------------------------------|
| 빠르게   | qk, quick | Skip validation          | `"qk change button color"`           |
| 실험     | exp       | Snapshot then experiment | `"exp try this approach"`            |
| 동시에   | para      | Parallel agents          | `"para analyze and document"`        |
| 고쳐     | fix       | Error KB-based fix       | `"fix this error"`                   |
| 되돌려   | undo      | Snapshot rollback        | `"undo to previous state"`           |
| 계속     | cont      | Continue previous state  | `"cont continue work"`               |
| 확인해   | chk       | Full validation          | `"확인해 quality check"`             |
| 테스트해 | tst       | Run tests                | `"tst run all tests"`                |
| 배포해   | dep       | Deploy checklist         | `"dep production deploy"`            |
| 정리해   | clean     | Code cleanup             | `"clean remove unused code"`         |
| 성능     | perf      | Performance analysis     | `"perf find bottleneck"`             |
| 계획     | plan      | Planning documentation   | `"plan create implementation plan"`  |
| 분석     | map       | Codebase analysis        | `"map understand structure"`         |

### Mode Keywords (4)

| Mode       | Alias | Activated Personas              | Purpose               |
|------------|-------|----------------------------------|-----------------------|
| ultrawork  | ulw   | explorer, librarian, analyzer   | Focused work mode     |
| deepsearch | ds    | explorer                        | Deep search mode      |
| strategic  | str   | architect                       | Strategic design mode |
| visual     | vis   | multimodal, frontend            | Visual work mode      |

### Usage Examples

```bash
# Vibe Keywords
> "qk add API endpoint"
🎯 vibe:빠르게
→ Skip validation, execute immediately

> "para security check and performance analysis"
🎯 vibe:동시에
→ Execute both tasks in parallel

# Mode Keywords
> "ulw implement this feature"
🎯 mode:ultrawork
→ Activate explorer, librarian, analyzer personas

> "ds find this bug cause"
🎯 mode:deepsearch
→ Deep exploration with explorer persona
```

---

## Writer-Reviewer Loop

### Overview

Writer-Reviewer ensures code quality through 4 parallel reviewer agents during code generation.

### 4-Agent Structure

```
┌─────────────────────────────────────────────────────────────┐
│                      Writer (Code Generation)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   4 Reviewers (Parallel)                     │
├─────────────────┬─────────────────┬─────────────────┬───────┤
│ Quality (30%)   │ Security (30%)  │ Performance(20%)│A11y   │
│                 │                 │                 │(20%)  │
│ • Code quality  │ • Vulnerability │ • Bottleneck    │• A11y │
│ • Readability   │ • Auth/Authz    │ • Memory leak   │• ARIA │
│ • Maintainability│ • Injection    │ • Algorithm eff.│• Keybd│
└─────────────────┴─────────────────┴─────────────────┴───────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Score Aggregation (targetScore: 0.85)           │
│                                                              │
│   Current score < 0.85 → Rewrite with feedback (max 10x)    │
│   Current score ≥ 0.85 → ✅ Complete                         │
│   Convergence threshold: 0.015 (early exit if below)        │
└─────────────────────────────────────────────────────────────┘
```

### Auto Weight Adjustment by Code Type

```python
CODE_TYPE_PATTERNS = {
    'frontend': {
        'keywords': ['component', 'tsx', 'jsx', 'ui', 'form', 'button'],
        'weights': {
            'quality': 0.25,
            'security': 0.25,
            'performance': 0.20,
            'accessibility': 0.30  # Frontend: accessibility priority
        }
    },
    'backend': {
        'keywords': ['api', 'route', 'endpoint', 'controller', 'service'],
        'weights': {
            'quality': 0.25,
            'security': 0.40,       # Backend: security priority
            'performance': 0.25,
            'accessibility': 0.10
        }
    },
    'database': {
        'keywords': ['query', 'sql', 'database', 'migration', 'schema'],
        'weights': {
            'quality': 0.20,
            'security': 0.40,       # DB: security very important
            'performance': 0.35,    # Query performance important
            'accessibility': 0.05
        }
    },
    'utility': {
        'keywords': ['util', 'helper', 'lib', 'function', 'hook'],
        'weights': {
            'quality': 0.35,        # Utility: quality priority
            'security': 0.25,
            'performance': 0.30,
            'accessibility': 0.10
        }
    }
}
```

### Skip Conditions

W-R loop skips these files:
- Config files: `.json`, `.env`, `tsconfig`, `eslint`, `prettier`
- Documentation: `.md`
- Lock files: `.lock`
- Git related: `git`, `config`

### Configuration

```json
{
  "writerReviewer": {
    "enabled": true,
    "targetScore": 0.85,
    "maxIterations": 10,
    "convergenceThreshold": 0.015,
    "agents": {
      "quality": 0.30,
      "security": 0.30,
      "performance": 0.20,
      "accessibility": 0.20
    }
  }
}
```

---

## Orchestrator Workflow

### /orchestrator Command

Systematically investigate complex research topics and generate comprehensive reports.

### 6-Step Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Query Analysis                                            │
│    • Clarify user question                                   │
│    • Extract key keywords                                    │
│    • Define research scope                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Research Brief                                            │
│    • Structure research questions                            │
│    • Derive sub-questions                                    │
│    • Set hypotheses                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Strategy                                                  │
│    • Determine research methodology                          │
│    • Select data sources                                     │
│    • Assign agents                                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Parallel Research ⚡ Core Step                            │
│                                                              │
│    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│    │   Academic   │ │   Technical  │ │     Data     │       │
│    │  (papers)    │ │ (GitHub,docs)│ │  (stats)     │       │
│    └──────────────┘ └──────────────┘ └──────────────┘       │
│           │               │               │                  │
│           └───────────────┴───────────────┘                  │
│                           │                                  │
│                    ┌──────────────┐                          │
│                    │  Fact-check  │                          │
│                    │ (verification)│                         │
│                    └──────────────┘                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Synthesis                                                 │
│    • Integrate multiple sources                              │
│    • Resolve conflicting information                         │
│    • Extract insights                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Report Generation                                         │
│    • Final documentation                                     │
│    • Structured report                                       │
│    • Reference compilation                                   │
└─────────────────────────────────────────────────────────────┘
```

### Orchestrator Agent Structure

| Agent                 | Role                   | Responsibility                              |
|-----------------------|------------------------|---------------------------------------------|
| research-orchestrator | Overall coordination   | Workflow management, agent assignment       |
| academic-researcher   | Academic research      | Paper, research data collection             |
| technical-researcher  | Technical investigation | Tech docs, GitHub, official docs            |
| data-analyst          | Data analysis          | Statistics, trend analysis                  |
| fact-checker          | Fact verification      | Information verification, source confirmation |
| research-synthesizer  | Result synthesis       | Multi-source integration                    |
| report-generator      | Report generation      | Final documentation                         |

### Usage

```bash
# Command invocation
/orchestrator AI impact on encryption

# Or direct Task tool invocation
Task tool:
  subagent_type: general-purpose
  prompt: "Conduct comprehensive research using Open Deep Research
          methodology on topic: [topic]"
```

---

## Real-World Scenarios

### Scenario 1: Quick Code Fix

```bash
> "qk change login button color to blue"

Flow:
1. keyword-detector: "qk" detected
   🎯 vibe:빠르게 → action: skip_validation
2. W-R loop skipped
3. Execute Edit immediately
4. Minimal PostToolUse hooks
5. ✅ Complete

Expected time: 5 seconds
```

### Scenario 2: Security-Focused API Development

```bash
> "create user payment API endpoint"

Flow:
1. writer-reviewer-hook: 'api' keyword detected
   → Code type: backend
   → Weights: security 40%, quality 25%, perf 25%, a11y 10%

2. Writer generates code

3. 4-Agent parallel review:
   - Quality Agent: Code quality check
   - Security Agent: Auth, SQL injection, XSS check (weight 40%)
   - Performance Agent: Response time, memory usage
   - Accessibility Agent: API response format

4. Score calculation:
   First iteration: 0.72 < 0.85 → Rewrite
   Second iteration: 0.81 < 0.85 → Rewrite
   Third iteration: 0.88 ≥ 0.85 → ✅ Complete

5. PostToolUse:
   - quality-gate.py execution
   - run-tests.py execution

Expected time: 2-3 minutes
```

### Scenario 3: Parallel Analysis Work

```bash
> "para analyze this codebase, document it, and generate tests"

Flow:
1. keyword-detector: "para" detected
   🎯 vibe:동시에 → action: parallel_agents

2. 3 Tasks simultaneous execution:
   ┌────────────────────────────────────────────┐
   │ Task 1: code-explorer                      │
   │ • Codebase structure analysis              │
   │ • Dependency mapping                       │
   │ • Architecture documentation               │
   ├────────────────────────────────────────────┤
   │ Task 2: sc:document                        │
   │ • README generation                        │
   │ • API documentation                        │
   │ • Usage guide                              │
   ├────────────────────────────────────────────┤
   │ Task 3: generate-tests                     │
   │ • Function-level test cases                │
   │ • Edge cases                               │
   │ • Integration tests                        │
   └────────────────────────────────────────────┘

3. Merge results and return

Expected time: 60% reduction vs sequential
```

### Scenario 4: Infinite Loop Prevention

```bash
> Complex task with consecutive errors

Flow:
1. First failure:
   └── ralph-loop-checker: Record state (failures: 1)

2. Second failure:
   └── Record state (failures: 2)

3. Third failure:
   └── ⚠️ Loop:3/5 warning output
   └── User notification

4. Fourth failure:
   └── ⚠️ Loop:4/5 warning

5. Fifth failure:
   └── 🛑 Loop:5 → Manual intervention
   └── Auto execution halt
   └── Request user manual intervention

Recovery:
- Auto reset on success after error fix
- Try "fix" keyword for Error KB-based fix
```

### Scenario 5: PRD-Based Project Start

```bash
> "start project based on this PRD document"
> [PRD.md file attached]

Flow:
1. plan-mode-analyzer:
   • PRD file pattern detected: .*PRD\.md$ → confidence: 90%
   • Feature list detected: features_count: 12
   • Analysis depth decision: 'think-hard'

2. Auto plan mode entry:
   {
     "status": "detected",
     "type": "file",
     "confidence": 0.9,
     "features_count": 12,
     "analysis_depth": "think-hard",
     "action": "enter_plan_mode"
   }

3. Project planning:
   • Determine feature implementation order
   • Dependency analysis
   • Milestone setting

4. Generate tasks via TodoWrite:
   [ ] Project initialization
   [ ] Feature 1 implementation
   [ ] Feature 2 implementation
   ...

5. Begin sequential implementation
```

### Scenario 6: Deep Search Bug Investigation

```bash
> "ds find this memory leak cause"

Flow:
1. keyword-detector: "ds" detected
   🎯 mode:deepsearch
   → Activated persona: explorer

2. Deep exploration with explorer persona:
   • Code history analysis
   • Related issue search
   • Memory profiling suggestion
   • Suspect point identification

3. Step-by-step analysis report:
   • Step 1: Symptom analysis
   • Step 2: Related code tracing
   • Step 3: Root cause hypothesis
   • Step 4: Verification method proposal

4. Solution proposal
```

---

## Quick Reference

### Frequently Used Keywords

| Situation            | Keyword | Effect                          |
|----------------------|---------|---------------------------------|
| Quick fix            | `qk`    | Skip validation                 |
| Parallel work        | `para`  | Parallel agent execution        |
| Error fix            | `fix`   | Error KB-based fix              |
| Quality check        | `확인해` | Full validation run             |
| Testing              | `tst`   | Run tests                       |
| Performance analysis | `perf`  | Performance bottleneck analysis |
| Deep search          | `ds`    | Deep search mode                |

### Frequently Used Commands

| Command                  | Purpose                |
|--------------------------|------------------------|
| `/orchestrator [topic]`  | Comprehensive research |
| `/generate-tests [file]` | Test generation        |
| `/project-plan`          | Project planning       |
| `/commit`                | Git commit             |
| `/review-pr`             | PR review              |
| `/sc:analyze`            | Code analysis          |

### Key Configuration Files

| File                    | Location                               | Purpose                |
|-------------------------|----------------------------------------|------------------------|
| CLAUDE.md               | `~/.claude/CLAUDE.md`                  | Global instructions    |
| settings.json           | `~/.claude/settings.json`              | Permission/hook settings |
| superclaude-config.json | `~/.claude/superclaude-config.json`    | Parallel/W-R settings  |
| servers.json            | `~/.claude/mcp-router/servers.json`    | MCP servers            |

### Hook Output Interpretation

| Output                              | Meaning                      |
|-------------------------------------|------------------------------|
| `🎯 vibe:빠르게`                    | Quick mode activated         |
| `🎯 mode:deepsearch`                | Deep search mode activated   |
| `🔍 QG:python → '확인해' for verify` | Quality gate pending         |
| `⚠️ Loop:3/5`                       | Consecutive failure warning  |
| `🛑 Loop:5 → Manual intervention`   | Infinite loop detected       |

---

## Troubleshooting

### Q: W-R loop keeps repeating

```bash
# Solution: Check convergence threshold
convergenceThreshold: 0.015
# Auto exit if improvement < 1.5%

# Or adjust maxIterations
maxIterations: 10 → reduce to 5
```

### Q: Parallel agents are slow

```bash
# Solution: Adjust concurrent execution count
# In superclaude-config.json:
"initial": 10 → reduce to 5
"maximum": 24 → reduce to 12
```

### Q: Hook not working on specific files

```bash
# Solution: Check skip conditions
SKIP_CONDITIONS = ['git', 'config', '.md', '.json', ...]
# Hook skipped if pattern matches
```

---

## Conclusion

> SuperClaude v2.0.9 generates high-quality code efficiently through
> hook-based automation + parallel agents + Writer-Reviewer loop.

### Key Usage Points

1. **Vibe keywords for action control**: `qk`, `para`, `fix`, `확인해`, etc.
2. **Mode keywords for persona activation**: `ulw`, `ds`, `str`, `vis`
3. **Auto quality gate**: 8-step auto verification on code changes
4. **Parallel agents**: Up to 24 concurrent execution (M2 Ultra optimized)
5. **Writer-Reviewer loop**: Auto improvement until target score (0.85)
6. **Infinite loop prevention**: Auto halt on 5 failures within 5 minutes

---

**META**
- Generated: 2026-01-31
- Tool: Claude Code (SuperClaude v2.0.9)
- Version: 2.0.9
- Platform: macOS (Mac Studio Ultra M2)
