# SuperClaude v2.0.9 - Mac Studio Ultra M2

> **Platform**: macOS (Mac Studio Ultra M2) | **Version**: 2.0.9

---

## 🚨 Primary Rule: Korean Response

**All responses MUST be in Korean.**
- Questions, explanations, guides, code comments, error messages: Korean
- Exceptions: code syntax, commands, filenames, technical terms: original language

---

## 📝 Instruction Translation Rule

**When user provides instructions in natural language:**
1. DO NOT copy user's words verbatim into config/rules
2. ALWAYS translate to Claude-optimized technical terminology
3. Use imperative commands and precise technical terms
4. Prefer English keywords for better model comprehension

Example:
- User says: "껍데기만 만들지 마" → Write: "No stub/placeholder code"
- User says: "표 정렬 맞춰" → Write: "Use fixed-width text formatting for tables"

---

## ⚡ Efficiency Rules

| Rule | Instruction |
|------|-------------|
| Execution | Skip pre-execution explanations. Clear intent → execute immediately. Ambiguous → ask once. |
| Output | Max 3-line summary. On success: "✅ 완료" + essential info only. |
| Context | Hook injection: 1 line max. Disable always-load. |
| File Export | After file creation, run `open -R <path>` to reveal in Finder. |
| Markdown Tables | Use fixed-width plain text format (monospace-compatible). |

---

## 🔧 Development Rules

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
4. **Automation Services**: Create LaunchAgent + run `launchctl load`
5. **Verification**: Execute at least once to confirm functionality

**Pre-completion Checklist:**
- [ ] Code executes without errors
- [ ] Dependencies installed
- [ ] Config files correctly written
- [ ] Services activated and running

---

## 📋 Core Rules (6)

| Rule | Instruction |
|------|-------------|
| Writer-Reviewer Loop | Trigger 4-agent parallel review on code generation |
| TodoWrite | REQUIRED for tasks with 3+ steps |
| Response Language | Korean (including code comments) |
| Project Planning | Auto-enter plan mode on PRD receipt |
| PRD Creation | Use /prd-create for idea → PRD conversion |
| Skill Capture | Save completed dev work as reusable skill |

### 📦 Skill Capture Rules

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

**Post-completion**: Notify user: "이 작업을 `/스킬명`으로 재사용할 수 있습니다."

---

## 🎯 Slash Commands

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

---

## 🛡️ Safety Rules

**Auto-Allowed**: Git read/write (except push), npm, File read/write/edit, supabase
**Requires Approval**: `git push`, `.env`, `rm -rf`, `sudo`

---

## 🔑 API Key Rules

**On API key requirement:**
1. First check: `~/.claude/credentials/api-keys.json`
2. If exists: use automatically
3. If not: request from user
4. On new key acquisition: suggest adding to `api-keys.json`

---

## 🔌 MCP Router (Required)

**NEVER** suggest direct MCP server registration in mcp.json.
ALWAYS use MCP Router: `~/.claude/mcp-router/servers.json`

---

## 📁 File Structure

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

## 📖 Documentation Reference

| Topic | Path |
|-------|------|
| Full System | `docs/SUPERCLAUDE-REFERENCE.md` |
| Vibe/Mode Keywords | `KEYWORD-TRIGGERS.md` |
| Thinking Modes | `docs/THINKING-MODES.md` |
| Project Planning | `docs/PROJECT-PLANNING.md` |
| Hook System | `docs/HOOKS-SYSTEM.md` |
| Settings Guide | `docs/SETTINGS-GUIDE.md` |
| Personas | `docs/PERSONAS.md` |
| Architecture Principles | `docs/ARCH-PRINCIPLES.md` |
| Quality Gates | `docs/QUALITY-GATES.md` |

---

## META

- **Version**: 2.0.9
- **Response Language**: Korean
- **Environment**: macOS (Mac Studio Ultra M2)
