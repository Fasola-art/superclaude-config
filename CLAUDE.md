# SuperClaude v2.2.0 - Windows Laptop RTX 4090

## Codex Role Profile (Persistent Default)

For Codex/Agent collaboration tasks, always apply:

- `~/.claude/modules/codex/roles/claude-role.md`
- `~/.claude/modules/codex/roles/agent-role.md`
- `~/.claude/modules/codex/index.md`
- `~/.claude/modules/codex/task-template.md`

Operational requirements:
- Use `task-template.md` 10-section spec for non-trivial implementation work.
- Keep role split strict: Claude = architecture/verification, agent = implementation execution.
- Enforce explicit validation commands and completion checklist.

> **Platform**: Windows (RTX 4090 Laptop) | **Version**: 2.2.0

---

## Primary Rule: Korean Response

**All responses MUST be in Korean.**
- Questions, explanations, guides, code comments, error messages: Korean
- Exceptions: code syntax, commands, filenames, technical terms: original language

---

## Instruction Translation Rule

**When user provides instructions in natural language:**
1. DO NOT copy user's words verbatim into config/rules
2. ALWAYS translate to Claude-optimized technical terminology
3. Use imperative commands and precise technical terms
4. Prefer English keywords for better model comprehension

Example:
- User says: "껍데기만 만들지 마" → Write: "No stub/placeholder code"
- User says: "표 정렬 맞춰" → Write: "Use fixed-width text formatting for tables"

---

## Efficiency Rules

| Rule            | Instruction                                                                               |
|-----------------|-------------------------------------------------------------------------------------------|
| Execution       | Skip pre-execution explanations. Clear intent → execute immediately. Ambiguous → ask once. |
| Output          | Max 3-line summary. On success: "✅ Complete" + essential info only.                       |
| Context         | Hook injection: 1 line max. Disable always-load.                                          |
| File Export     | After file creation, run `explorer <path>` to reveal in Explorer.                          |
| Markdown Tables | Use fixed-width plain text format (monospace-compatible).                                 |
| Context Mgmt    | At session end: run `/compact` or update TASKS.md with current progress summary.          |

---

## Pre-Task Checklist (MANDATORY)

**Before ANY code modification:**
1. Run `wc -l <file>` - verify within limits
2. If exceeds limit → split first, then modify

**Line Limits (STRICT):**
| Type | Range | Split Trigger |
|------|-------|---------------|
| Logic/Utils | 50~80 | 3+ functions or complex regex |
| UI Components | 100~120 | 4+ states or deep DOM |
| API/Server | 80~100 | Error handling obscures logic |
| types/constants | ≤20 | Type-only or const-only |
| utils/hooks | ≤50 | Single-purpose functions |

**Critical Rules:**
- **MIN 20 lines**: No file under 20 lines (merge instead)
- **2+ usage → extract**: Shared logic → common module
- **Split requires**: barrel export (index.ts/\_\_init\_\_.py)

**Test Strategy:**
| Target | Method |
|--------|--------|
| 공통함수/utils | TDD 필수 |
| 비즈니스 로직 | TDD 권장 |
| 결제/인증 플로우 | E2E 필수 |
| UI/프로토타입 | 수동 테스트 |

**Standard Folder Structure:**
```
feature/
├── index.ts       # barrel export
├── types.ts       # ≤20 lines
├── constants.ts   # ≤20 lines
├── utils.ts       # ≤50 lines
├── hooks.ts       # ≤50 lines
├── Component.tsx  # main component
└── *.test.ts      # tests
```

**Violation = Immediate rollback + refactor**

---

## Markdown File Rules (MANDATORY)

**Apply Pre-Task Checklist to ALL .md files:**

| Type | Range | Split Trigger |
|------|-------|---------------|
| Rules/Guides | 50~100 | 3+ sections or mixed topics |
| Reference docs | 80~120 | Single topic only |
| Index files | 20~50 | Links + brief descriptions |
| Templates | ≤30 | Minimal, no examples |

**Modularization Principles:**
- **2+ references → extract**: Shared content → `_shared/` module
- **Single responsibility**: One topic per file
- **Barrel pattern**: Each folder has `index.md` with links
- **No redundancy**: Zero duplicate content across files

**Efficiency Rules:**
- **Minimal code**: Shortest syntax achieving same result
- **No boilerplate**: Skip obvious headers/footers
- **Active voice**: Direct imperatives only
- **Tables over prose**: Structured data in tables

**File Creation Checklist:**
1. Check if content exists elsewhere → reference instead
2. Verify line count within limits
3. Extract shared patterns to `_shared/`
4. Create index.md if new folder

---

## Development Rules

### Full Implementation Required (No Stub/Placeholder/Skeleton Code)

**PROHIBITED patterns:**
- `pass`, `...`, `TODO`, `FIXME`, `NotImplementedError`
- Empty function bodies
- Placeholder comments like "implement later"
- Partial implementations

**REQUIRED for every feature:**
1. **Functions/Classes**: Complete working implementation
2. **API Integration**: Actual endpoint calls + error handling
3. **Hooks/Triggers**: Config modification + activation
4. **Automation Services**: Create Windows Task Scheduler or background service
5. **Verification**: Execute at least once to confirm functionality

**Pre-completion Checklist:**
- [ ] Code executes without errors
- [ ] Dependencies installed
- [ ] Config files correctly written
- [ ] Services activated and running

---

## Core Rules (8)

| Rule                 | Instruction                                        |
|----------------------|----------------------------------------------------|
| Writer-Reviewer Loop | Trigger 4-agent parallel review on code generation |
| TodoWrite            | REQUIRED for tasks with 3+ steps                   |
| Project Planning     | Auto-enter plan mode on PRD receipt                |
| PRD Creation         | Use /prd-create for idea → PRD conversion          |
| Skill Capture        | Save completed dev work as reusable skill          |
| TDD/E2E Suggestion   | On feature request, ask "TDD/E2E로 진행할까요?"     |
| **Agent/Skill Rules** | **Include `rules/_shared/agent-rules.md` in prompt** |

### Master-Subagent Orchestration (Claude + Codex)

**Role split:**
| Role | Tool | Responsibility |
|------|------|---------------|
| Master (Strategy) | Claude | Architecture, planning, context mgmt, code review |
| Subagent (Execution) | Codex `--yolo` | Implementation, bug fixes, file writes, tests |

**Workflow:**
1. Claude writes `plan.md` + `TASKS.md` with precise task specs
2. Claude delegates to Codex: "Implement TASK-N per plan.md"
3. Codex executes autonomously (yolo mode = no interruptions)
4. Claude reviews output, updates `context.md` with decisions
5. Repeat until feature complete

**Codex delegation format:**
```
[CODEX TASK]
Ref: plan.md > Section X
Goal: <specific outcome>
Constraints: <file limits, patterns, no placeholders>
Output: <expected files/functions>
```

**When to use Codex subagent:**
- Any file write / code generation task
- Bug fixes requiring multiple file edits
- Test implementation
- Repetitive refactoring

### Agent/Skill/PlanMode Mandatory

**On Task tool invocation, ALWAYS prepend to prompt:**
```
[MANDATORY RULES]
1. Python: 타입 힌트 + docstring 필수
2. 기존 코드 먼저 확인: ~/.claude/modules/
```

**모듈별 추가 규칙 (해당 시 포함):**
- trading: `~/.claude/modules/trading/CLAUDE.md` 참조 지시
- sql: `~/.claude/modules/sql-trading/CLAUDE.md` 참조 지시

**Post-verification (MANDATORY):** Pre-Task Checklist 라인 제한 기준 적용.

### Skill Capture Rules

**Trigger conditions (if any met, create skill):**
- New project/tool creation completed
- Reusable workflow implemented
- Complex integration completed (API, etc.)
- User mentions "reuse later" / "나중에 재사용"

**Save location**: `~/.claude/skills/<skill-name>.md`

**Skill file structure**:
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

**Post-completion**: Notify user: "This work can be reused with `/skill-name`."

---

## Slash Commands

### Core 커맨드

| Command | 설명 | Description |
|---------|------|-------------|
| /j | JARVIS 브리핑 | JARVIS Briefing |
| /ctx | 컨텍스트 사용량 요약 | Context Summary |
| /todo | TODO 리스트 관리 | TODO list management |
| /vibe | 세션 분위기 확인/설정 | Check and set session vibe |
| /recover | 세션/시스템 복구 | Recover session or system |
| /handoff | 세션 인수인계 문서 생성 | Generate HANDOFF.md for next session |
| /half-clone | 컨텍스트 85%+ 핵심 추출 | Extract core context + /compact guide |

### 프로젝트 관리

| Command | 설명 | Description |
|---------|------|-------------|
| /prd-create | PRD 문서 생성 | Create PRD document |
| /project-plan | 프로젝트 계획 생성 | Create project plan |
| /project-status | 프로젝트 상태 확인 | Check project status |
| /project-continue | 중단된 프로젝트 재개 | Continue interrupted project |
| /feature-dev | 기능 개발 (아키텍처 중심) | Feature development |
| /ideation | 멀티 페르소나 아이디어 토론 | Multi-persona ideation |
| /fork | 실험적 방향 분기점 생성 | Create FORK_CONTEXT.md + git branch guide |

### Git & 코드 리뷰

| Command | 설명 | Description |
|---------|------|-------------|
| /commit | Git 커밋 생성 | Create a git commit |
| /commit-push-pr | 커밋+푸시+PR 생성 | Commit, push, and create PR |
| /code-review | PR 코드 리뷰 | Code review a pull request |
| /review-pr | 에이전트 기반 PR 리뷰 | Comprehensive PR review |
| /clean_gone | 삭제된 원격 브랜치 정리 | Clean deleted remote branches |

### 테스팅

| Command | 설명 | Description |
|---------|------|-------------|
| /tdd | TDD 워크플로우 | TDD workflow |
| /e2e | E2E 테스트 생성 | E2E test creation |
| /generate-tests | 테스트 자동 생성 | Auto-generate tests |

### 트레이딩 & 데이터

| Command | 설명 | Description |
|---------|------|-------------|
| /sql | SQL 쿼리/대체 데이터 분석 | SQL query and alt-data analysis |
| /orchestrator | 리서치 오케스트레이터 | Research Orchestrator |
| /sns | SNS 자동화 워크플로우 | SNS automation workflow |

### 플러그인 & 자동화

| Command | 설명 | Description |
|---------|------|-------------|
| /hookify | 대화 분석으로 훅 생성 | Create hooks from conversation |
| /configure | Hookify 규칙 활성화/비활성화 | Enable/disable hookify rules |
| /list | Hookify 규칙 목록 조회 | List hookify rules |
| /create-plugin | 플러그인 생성 | Plugin creation workflow |
| /new-sdk-app | Agent SDK 앱 생성 | Create Agent SDK application |
| /revise-claude-md | CLAUDE.md 업데이트 | Update CLAUDE.md with learnings |
| /review-claudemd | CLAUDE.md 분석 (수정 X) | Analyze token efficiency, detect duplicates |

### 유틸리티

| Command | 설명 | Description |
|---------|------|-------------|
| /sync-guide | 가이드 동기화 | Synchronize instruction files |
| /music-lesson | 음악 레슨 자동화 | Music lesson recording pipeline |
| /telegram | 텔레그램 모니터링 | Telegram message monitoring |
| /search-history | 대화 이력 키워드 검색 | Search past Claude sessions by keyword |

### Ralph Loop

| Command | 설명 | Description |
|---------|------|-------------|
| /ralph-loop | Ralph Loop 시작 | Start Ralph Loop |
| /cancel-ralph | Ralph Loop 취소 | Cancel active Ralph Loop |
| /help | Ralph Loop 도움말 | Ralph Loop plugin help |

### Stripe

| Command | 설명 | Description |
|---------|------|-------------|
| /test-cards | 테스트 카드번호 표시 | Display test card numbers |
| /explain-error | 에러 코드 설명 | Explain error codes |
| /error-search | Error KB 검색 | Search Error KB |

### SC (SuperClaude) 서브커맨드

| Command | 설명 | Description |
|---------|------|-------------|
| /sc:index | SC 커맨드 목록 | List SC commands |
| /sc:analyze | 코드/프로젝트 분석 | Analyze code or project |
| /sc:build | 프로젝트 빌드 | Build project |
| /sc:calendar | 경제 지표 발표 일정 | Economic calendar |
| /sc:cleanup | 코드 정리 | Cleanup code |
| /sc:design | 시스템/컴포넌트 설계 | Design system |
| /sc:document | 문서 생성 | Generate documentation |
| /sc:estimate | 작업 범위 추정 | Estimate task scope |
| /sc:explain | 코드/개념 설명 | Explain code or concept |
| /sc:git | Git 작업 도우미 | Git operations helper |
| /sc:implement | 기능 구현 | Implement feature |
| /sc:improve | 코드 개선 | Improve code |
| /sc:load | 컨텍스트 로드 | Load context |
| /sc:news | 뉴스 수집/요약 | News collection and summary |
| /sc:report | 일일 경제 리포트 생성 | Daily economic report |
| /sc:spawn | 에이전트 생성 | Spawn agent |
| /sc:task | 작업 관리 | Manage tasks |
| /sc:test | 테스트 실행 | Run tests |
| /sc:troubleshoot | 문제 해결 | Troubleshoot issues |
| /sc:workflow | 워크플로우 실행 | Execute workflow |

---

## Code Structure Rules

> **See Pre-Task Checklist above for complete rules**

---

## Platform Rules (Windows)

**WSL2 Environment (Configured ✅):**
| Item | Status | Detail |
|------|--------|--------|
| Distro | ✅ Ubuntu 24.04 | `wsl -d Ubuntu` |
| Node.js | ✅ v24.13.1 | via nvm (`~/.nvm`) |
| Claude Code | ✅ v2.1.44 | `npm i -g @anthropic-ai/claude-code` |
| Auth | ✅ API Key | `ANTHROPIC_API_KEY` in `~/.bashrc` |

- Project files: keep inside WSL2 filesystem (`~/projects/` not `/mnt/c/`)
- Launch: `wsl -d Ubuntu` → `cd ~/projects/<name>` → `claude`
- Re-auth check: `claude auth status`

**Runtime Preference (Bun over Node.js):**
- Prefer `bun` / `bunx` over `node` / `npx` for all JS/TS execution
- Bun: faster startup, native TS support, fewer compatibility errors
- Fallback to Node.js only when Bun incompatibility confirmed

**Port Conflict Resolution:**
- On port conflict: `lsof -ti:<PORT> | xargs kill -9` (WSL/Mac)
- On Windows: `netstat -ano | findstr :<PORT>` → `taskkill /PID <PID> /F`
- Auto-resolve before starting dev server; never leave zombie processes

**Cost Strategy:**
| Task Type | Model |
|-----------|-------|
| Core logic, complex features, architecture | Max plan (Opus) |
| Standard dev, code review, refactoring | Sonnet (default) |
| Simple edits, quick questions, formatting | Haiku (low-cost) |

**Context Loss Prevention (3-File System):**
- Manual `/compact` REQUIRED at each task unit boundary (auto-compact = data loss risk)
- Maintain 3 files in real-time across sessions:

| File | Purpose | Format |
|------|---------|--------|
| `plan.md` | Strategy, architecture decisions | What to build |
| `context.md` | Key decisions, variables, constraints | Why we decided |
| `TASKS.md` | Checklist, current progress | Status/Done/Next/Blockers |

- On session start: load all 3 files before proceeding
- On session end: update all 3 files before `/compact`

---

## Safety Rules

**Auto-Allowed**: Git read/write (except push), npm, File read/write/edit, supabase
**Requires Approval**: `git push`, `.env`, `rm -rf`, `sudo`

---

## API Key Rules

**On API key requirement:**
1. First check: `~/.claude/credentials/api-keys.json`
2. If exists: use automatically
3. If not: request from user
4. On new key acquisition: suggest adding to `api-keys.json`

---

## MCP Router (Required)

**NEVER** suggest direct MCP server registration in mcp.json.
ALWAYS use MCP Router: `~/.claude/mcp-router/servers.json`

---

## File Structure

```
~/.claude/
├── CLAUDE.md                 # This file
├── superclaude-config.json   # Config (parallel execution, W-R, etc.)
├── settings.json             # Claude Code official settings
├── docs/                     # Detailed documentation (reference as needed)
├── hooks/                    # Automation hooks
├── personas/                 # Personas (45+)
├── skills/                   # Skill definitions
├── error-kb/                 # Error knowledge base
├── modules/                  # trading, news-collector, realtime-analysis
├── profiles/                 # Language profiles (TypeScript, Rust, Python, Go)
└── rules/                    # Language-specific coding rules
```

---

## Documentation Reference

| Topic                   | Path                              |
|-------------------------|-----------------------------------|
| Full System             | `docs/archive/SUPERCLAUDE-REFERENCE.md` |
| Vibe/Mode Keywords      | `KEYWORD-TRIGGERS.md`             |
| Thinking Modes          | `docs/THINKING-MODES.md`          |
| Project Planning        | `docs/archive/PROJECT-PLANNING.md`        |
| Hook System             | `docs/archive/HOOKS-SYSTEM.md`            |
| Settings Guide          | `docs/archive/SETTINGS-GUIDE.md`          |
| Personas                | `docs/archive/PERSONAS.md`                |
| Architecture Principles | `docs/ARCH-PRINCIPLES.md`         |
| Quality Gates           | `docs/QUALITY-GATES.md`           |

---

## META

- **Version**: 2.2.0
- **Response Language**: Korean
- **Environment**: Windows (RTX 4090 Laptop, 32GB RAM, 16GB VRAM)
