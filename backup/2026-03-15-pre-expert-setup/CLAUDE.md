# SuperClaude v2.1.0 - Mac Studio Ultra M2

> macOS | Opus 4.6 | Korean Response

---

## Primary Rule: Korean Response

All responses in Korean. Exceptions: code syntax, commands, filenames, technical terms.

## Instruction Translation Rule

User's natural language → Claude-optimized technical terminology.
- "껍데기만 만들지 마" → "No stub/placeholder code"
- "표 정렬 맞춰" → "Use fixed-width text formatting for tables"

---

## Efficiency Rules

| Rule | Instruction |
|------|-------------|
| Execution | Clear intent → execute immediately. Ambiguous → ask once. |
| Output | Max 3-line summary. Success: "✅ Complete" + essential info. |
| Context | Hook injection: 1 line max. |
| File Export | After creation, run `open -R <path>`. |
| Tables | Fixed-width plain text format. |

---

## Line Limits (STRICT)

**Before ANY modification: `wc -l <file>` → verify within limits.**

| Type | Range | Split Trigger |
|------|-------|---------------|
| Logic/Utils | 50~100 | 3+ functions |
| UI Components | 100~150 | 4+ states |
| API/Server | 80~120 | Error handling obscures logic |
| types/constants | ≤20 | Type-only or const-only |
| utils/hooks | ≤50 | Single-purpose functions |
| Hook scripts (.py) | 50~150 | Complex logic split to _shared/ |
| Rules/Guides (.md) | 50~120 | 3+ sections |
| Reference (.md) | 80~150 | Single topic only |

**MIN 20 lines** (merge instead) | **2+ usage → extract** | **Split requires barrel export**
**Violation = Immediate rollback + refactor**

---

## Development Rules

**PROHIBITED**: `pass`, `...`, `TODO`, `FIXME`, `NotImplementedError`, empty bodies, placeholders.

**REQUIRED**: Complete implementation, actual API calls + error handling, config activation, verify execution.

---

## Core Rules (8)

| Rule | Instruction |
|------|-------------|
| Writer-Reviewer Loop | 4-agent parallel review on code generation |
| TodoWrite | REQUIRED for 3+ step tasks |
| Response Language | Korean (including code comments) |
| Project Planning | Auto-enter plan mode on PRD receipt |
| PRD Creation | Use /prd-create for idea → PRD |
| Skill Capture | Save completed dev work as reusable skill |
| TDD/E2E Suggestion | On feature request, ask "TDD/E2E로 진행할까요?" |
| Agent Rules | Include `rules/_shared/agent-rules.md` in prompt |

### Agent/Task Prompt Injection

On Task tool invocation, prepend:
```
[MANDATORY RULES]
1. 파일: 50~150줄 범위 유지
2. Python: 타입 힌트 + docstring 필수
3. 기존 코드 먼저 확인: ~/.claude/modules/
4. No stub/placeholder - 완전한 구현만
5. 응답: 한국어
```

Module-specific: trading → `modules/trading/CLAUDE.md`, sql → `modules/sql-trading/CLAUDE.md`

Post-verification: `wc -l` → 150줄 초과 시 분할, 50줄 미만 시 병합.

---

## Safety Rules

**Auto-Allowed**: Git read/write (except push), npm, File ops, supabase
**Requires Approval**: `git push`, `.env`, `rm -rf`, `sudo`

## API Key Rules

1. Check `~/.claude/credentials/api-keys.json` first
2. If exists: use automatically | If not: request from user

## MCP Router

**NEVER** register directly in mcp.json. ALWAYS use MCP Router: `~/.claude/mcp-router/servers.json`

## Session Continuity

- Stop hook generates `~/.claude/HANDOFF.md` automatically
- Next session loads and archives it via handoff-loader hook
- Use `cc` (--continue) or `cr` (--resume) for session recovery

---

## References

- Slash Commands / Skill Capture / Docs: `rules/_shared/workflow-rules.md`
- Agent Rules: `rules/_shared/agent-rules.md`
- Language Rules: `rules/{go,python,react,sql}/`
- Testing: `rules/testing/`

---

## Test Strategy

| Target | Method |
|--------|--------|
| 공통함수/utils | TDD 필수 |
| 비즈니스 로직 | TDD 권장 |
| 결제/인증 플로우 | E2E 필수 |
| UI/프로토타입 | 수동 테스트 |

---

**META**: v2.1.0 | Korean | macOS (Mac Studio Ultra M2)
