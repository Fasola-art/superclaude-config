# Claude Code 환경 최적화 PRD + 워크플로우

## Context

**문제**: 4개 URL에서 수집한 Claude Code 최신 팁 (Advent of Claude 2025, Bash for AI Engineers, ykdojo 45 Tips, 요즘IT 70 Tips)을 분석한 결과, 현재 SuperClaude v2.0.9 환경에 **즉시 적용 가능한 개선사항 15개**를 식별함.

**현재 환경 진단 요약**:

| 항목 | 현황 | 문제 |
|------|------|------|
| CLAUDE.md | 294줄 | 자체 규칙 100줄 상한의 2.9배 초과 |
| settings.local.json | 167개 Bash 허용 | 일회성 명령 누적, 보안 위험 |
| .zshrc | API 키 하드코딩 | `sk-ant-api03-...` 평문 노출 |
| Hook 5개 파일 | 120줄 상한 초과 | 200, 170, 171, 135, 130줄 |
| MCP | mcp.json + router 중복 | github, postgres 이중 등록 |
| 세션 관리 | last-session.json만 저장 | HANDOFF.md 패턴 미구현 |
| 앨리어스 | `c`, `cc`, `cr` 없음 | 일상 단축키 부재 |

**의도된 결과**: 토큰 효율 40%+ 개선, 세션 연속성 확보, 보안 강화, 자체 규칙 준수

**사용자 선택 사항**:
- API 키: macOS Keychain 이전 ✅
- CLAUDE.md: 보수적 슬리밍 (294줄→150줄) — 주요 섹션 유지, 예시+중복만 제거
- Phase 7: 음성 전사 + 커스텀 Status Line + 컨테이너 격리 모두 적용 ✅

---

## Phase 1: 즉시 적용 (Day 1) — 설정만으로 해결

### 1-1. 터미널 앨리어스 추가

**파일**: `~/.zshrc`

```bash
# Claude Code 단축 앨리어스
alias c='claude'
alias cc='claude --continue'
alias cr='claude --resume'
alias cj='claude -p'                    # JSON/pipe 모드
alias cplan='claude -p "/plan"'

# 프로젝트별 세션
alias cw='claude --resume work'
alias ct='claude --resume trading'
```

### 1-2. API 키 보안 강화

**현재**: `~/.zshrc`에 API 키 평문 하드코딩
**목표**: macOS Keychain 활용

```bash
# 1. Keychain에 키 저장
security add-generic-password -s "anthropic-api-key-1" -a "reim" -w "sk-ant-api03-..."

# 2. ~/.zshrc 수정
alias claude1='ANTHROPIC_API_KEY="$(security find-generic-password -s anthropic-api-key-1 -w)" claude'
```

### 1-3. settings.local.json 정리

**현재**: 167개 Bash 허용 항목 (일회성 누적)
**목표**: 파일 삭제 또는 10개 이내로 축소

대부분의 항목이 settings.json에 이미 포함되어 있거나, 와일드카드로 커버됨:
- `Bash(find:*)` → settings.json에 없지만 필요 → 유지
- `Bash(grep:*)` → settings.json에 없지만 필요 → 유지
- `Bash(wc:*)` → settings.json에 없지만 필요 → 유지
- `Bash(tree:*)` → 유용 → 유지
- `Bash(du:*)` → 유용 → 유지
- 나머지 162개: 일회성 복합 명령 → **삭제**

### 1-4. puppeteer MCP 항목 제거

**파일**: `~/.claude/mcp.json`
- puppeteer 항목 삭제 (Chromium 미설치로 비활성 상태)
- mcp-router의 playwright가 이미 활성화됨

---

## Phase 2: HANDOFF.md 세션 연속성 시스템 (Day 2)

**근거**: 수집 팁에서 가장 많이 강조된 패턴. 주제 혼합 시 성능 39% 저하 연구.

### 2-1. Stop Hook 확장: HANDOFF.md 자동 생성

**파일**: `~/.claude/hooks/Stop/session-saver.py` (55줄 → ~90줄)

현재 `last-session.json`만 저장하는 로직에 추가:
- `git diff --name-only` → 작업 중인 파일
- `git rev-parse HEAD` → 마지막 커밋
- `git branch --show-current` → 현재 브랜치
- `~/.claude/todos/active.json` → 미완료 TODO
- 전체를 `~/.claude/HANDOFF.md`로 마크다운 출력

HANDOFF.md 포맷:
```markdown
# Session Handoff — {날짜} {시간}
## 작업 상태
- Branch: {branch}
- Last Commit: {hash} — {message}
- Working Files: {list}
## 미완료 작업
{todo items}
## 다음 단계
{extracted from recent context}
```

### 2-2. UserPromptSubmit Hook: HANDOFF 자동 로드

**파일**: `~/.claude/hooks/UserPromptSubmit/handoff-loader.py` (새 파일, ~50줄)

- 세션 시작 시 `~/.claude/HANDOFF.md` 존재 확인
- 존재하면 내용을 `system-reminder` 형태로 주입
- 로드 후 `~/.claude/handoff-archive/` 로 이동 (날짜 접미사)
- **settings.json에 hook 등록 필요** (UserPromptSubmit 배열에 추가)

---

## Phase 3: CLAUDE.md 슬리밍 (Day 3-4)

**근거**: ykdojo 58개 패치로 19k→10k 토큰. Opus 4.6은 반복 강조 불필요.

### 3-1. 현재 CLAUDE.md (294줄) → 150줄로 보수적 축소

**제거 대상** (중복 또는 이미 폴더에 존재):
- Slash Commands 테이블 15줄 → `commands/` 폴더가 이미 존재
- File Structure 트리 10줄 → 이미 알고 있는 구조
- Documentation Reference 테이블 12줄 → `docs/index.md` 참조 1줄
- Pre-Task Checklist의 중복 라인 제한 테이블 → 1개로 통합 (2곳→1곳)
- Code Structure Rules 섹션 → Pre-Task Checklist에 이미 포함
- Skill Capture Rules 상세 예시 → 핵심 트리거 조건만 유지
- "MANDATORY", "STRICT" 등 반복 강조 → 한 번만

**유지 대상** (주요 섹션 전부):
1. Korean Response + Translation Rule (10줄)
2. Efficiency Rules (8줄)
3. Pre-Task Checklist — 테이블 1개 + 핵심 규칙 (20줄)
4. Development Rules (15줄)
5. Core Rules 8개 — 테이블 + Agent 주입 규칙 (25줄)
6. Safety Rules + API Key Rules + MCP Router (15줄)
7. Markdown File Rules — 간략화 (10줄)

**분리 대상** (별도 파일):
- `~/.claude/rules/_shared/workflow-rules.md` (50줄): 슬래시 커맨드 상세, Skill Capture 상세

### 3-2. Tiered Loading 구조

```
Tier 0 (항상): CLAUDE.md (~150줄, ~4k 토큰) — 주요 규칙 전부 유지
Tier 1 (프로젝트별): {project}/.claude/CLAUDE.md
Tier 2 (언어감지): keyword-detector.py가 rules/ 자동 로드
Tier 3 (에이전트): agent-rules-injector.py가 주입
```

기존 keyword-detector.py의 언어 감지 로직은 유지. 슬래시 커맨드/Skill Capture 상세만 workflow-rules.md로 분리.

---

## Phase 4: Hook 시스템 리팩토링 (Day 5-7)

### 4-1. 초과 파일 분할

| 파일 | 현재 | 목표 | 분할 방법 |
|------|------|------|----------|
| auto-context-manager.py | 200줄 | 80+50줄 | 컨텍스트 추정 유틸 분리 |
| writer-reviewer-hook.py | 170줄 | 90+50줄 | 리뷰 유틸 분리 |
| sql-alert-monitor.py | 171줄 | 80+60줄 | SQL 공통 유틸 분리 |
| sql-data-collector.py | 135줄 | 80줄 | SQL 공통 유틸 공유 |
| rollback-guard.py | 130줄 | 90줄 | 가드 로직 간략화 |

### 4-2. 공통 유틸 추출

**새 파일**: `~/.claude/hooks/_shared/hook_utils.py` (~60줄)
```python
# 모든 hook에서 공유하는 유틸리티:
# - get_input_data(): stdin JSON 파싱
# - load_state(name): 상태 파일 로드
# - save_state(name, data): 상태 파일 저장
# - extract_keywords(text): 키워드 추출
# - estimate_tokens(text): 토큰 수 추정
```

**새 파일**: `~/.claude/hooks/_shared/sql_utils.py` (~50줄)
```python
# SQL 관련 hook 공유:
# - connect_db(): PostgreSQL 연결
# - execute_query(): 쿼리 실행
# - format_alert(): 알림 포맷
```

---

## Phase 5: MCP 통합 및 정리 (Day 8)

### 5-1. 중복 MCP 서버 정리

**현재 중복**:
- `mcp.json` github + `mcp-router` github → router만 유지
- `mcp.json` postgres + `mcp-router` postgresql → router만 유지

**작업**: mcp.json에서 github, postgres 항목의 env에 있는 토큰을 mcp-router로 이전 확인 후 mcp.json에서 제거

### 5-2. 크리덴셜 하드코딩 제거

**현재**: mcp.json에 GitHub PAT, Slack 토큰 등 평문
**목표**: 환경 변수 참조로 전환

```json
// mcp.json 변경 전
"env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_실제토큰..." }

// 변경 후
"env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}" }
```

`~/.zshrc`에 추가:
```bash
export GITHUB_PAT="$(security find-generic-password -s github-pat -w 2>/dev/null)"
export SLACK_BOT_TOKEN="$(security find-generic-password -s slack-bot -w 2>/dev/null)"
```

---

## Phase 6: 일일 워크플로우 자동화 (Day 9-10)

### 6-1. Daily Start 스킬

**파일**: `~/.claude/commands/daily-start.md`

```markdown
---
description: "아침 시작 루틴: HANDOFF 로드 + 브리핑 + TODO 확인"
---
다음 순서로 오늘 하루를 시작해주세요:
1. ~/.claude/HANDOFF.md가 있으면 읽고 요약
2. JARVIS 브리핑 실행 (시장 동향, 일정)
3. git status로 미커밋 변경 확인
4. ~/.claude/todos/active.json에서 미완료 작업 표시
5. 오늘 우선순위 3개 제안
```

### 6-2. Daily End 스킬

**파일**: `~/.claude/commands/daily-end.md`

```markdown
---
description: "하루 종료 루틴: HANDOFF 생성 + TODO 갱신 + 통계"
---
다음 순서로 하루를 마무리해주세요:
1. 오늘 완료한 작업 요약
2. HANDOFF.md 생성 (다음 세션용)
3. 미완료 TODO 정리
4. 미커밋 변경사항 있으면 알림
5. 세션 통계 출력 (작업 시간, 토큰 사용량)
```

---

## Phase 7: 고급 최적화 (Day 11+)

### 7-1. 컨테이너 격리 ✅ 적용

**근거**: ykdojo Tip 21 - 위험한 작업 격리
**방법**: Docker/OrbStack으로 위험 작업 실행

**파일**: `~/.claude/scripts/claude-container.sh` (새 파일, ~30줄)
```bash
#!/bin/bash
# 위험한 작업을 Docker 컨테이너에서 격리 실행
# 사용: claude-container.sh [language] [command]
# 예시: claude-container.sh node "npm test"
#       claude-container.sh python "pytest"
```

**앨리어스 추가** (`~/.zshrc`):
```bash
alias cdocker='~/.claude/scripts/claude-container.sh'
```

### 7-2. 음성 전사 연동 ✅ 적용

**근거**: Tip 2 - superwhisper/MacWhisper
**방법**: superwhisper 설치 후 Claude Code 입력에 직접 전사

```bash
brew install --cask superwhisper
```

설치 후 설정:
- 전사 출력을 "현재 포커스된 앱에 삽입" 모드로 설정
- 단축키: Cmd+Shift+Space (기본) → Claude Code 터미널에서 바로 사용
- 한국어/영어 자동 감지 활성화

### 7-3. 커스텀 Status Line ✅ 적용

**근거**: Tip 0 - 상태바 커스터마이징
**방법**: `/statusline` 설정으로 Git branch, 토큰 사용량, 현재 모드 표시

**파일**: `~/.claude/statusline.sh` (새 파일, ~20줄)
```bash
#!/bin/bash
# Claude Code status line 스크립트
# 표시: [모델] | [Git branch] | [토큰 사용량] | [시간]
BRANCH=$(git branch --show-current 2>/dev/null || echo "no-git")
echo "opus-4.6 | $BRANCH | $(date +%H:%M)"
```

`/statusline` 명령으로 활성화

---

## 구현 로드맵

```
Week 1 (즉시 적용 + 핵심)
├── Day 1: Phase 1 — 앨리어스, API 키 보안, settings 정리 (1시간)
├── Day 2: Phase 2 — HANDOFF.md 시스템 구축 (3시간)
├── Day 3-4: Phase 3 — CLAUDE.md 슬리밍 294→80줄 (4시간)
└── Day 5: Phase 4 시작 — Hook 공통 유틸 추출 (2시간)

Week 2 (리팩토링 + 워크플로우)
├── Day 6-7: Phase 4 완료 — Hook 5개 파일 분할 (4시간)
├── Day 8: Phase 5 — MCP 통합, 크리덴셜 정리 (2시간)
└── Day 9-10: Phase 6 — daily-start/end 워크플로우 (3시간)

Week 3 (고급 최적화)
├── Day 11: Phase 7-1 — 컨테이너 격리 스크립트 (1시간)
├── Day 12: Phase 7-2 — superwhisper 설치 및 설정 (30분)
└── Day 13: Phase 7-3 — 커스텀 Status Line (1시간)
```

**총 예상 소요**: 약 22시간

---

## 예상 효과

| 개선 | 정량적 효과 |
|------|------------|
| CLAUDE.md 슬리밍 | 매 프롬프트 ~3k 토큰 절약 (294줄→150줄) |
| HANDOFF.md | 세션 재시작 컨텍스트 복원 시간 90% 단축 |
| API 키 Keychain 이전 | 평문 노출 위험 제거 |
| settings.local.json 정리 | 167→5개, 불필요 허용 제거 |
| Hook 리팩토링 | 자체 규칙(120줄) 준수, 유지보수성 향상 |
| MCP 통합 | 중복 서버 제거, 단일 관리 포인트 |

---

## 검증 방법

### Phase별 검증

| Phase | 검증 방법 |
|-------|----------|
| 1 (앨리어스) | `source ~/.zshrc && c --version` 실행 |
| 1 (API 키) | `security find-generic-password -s anthropic-api-key-1 -w` 확인 |
| 2 (HANDOFF) | 세션 종료 → `cat ~/.claude/HANDOFF.md` 확인 → 새 세션에서 자동 로드 확인 |
| 3 (슬리밍) | `wc -l ~/.claude/CLAUDE.md` → 150줄 이내 확인. `/context` 로 토큰 소비 비교 |
| 4 (Hook) | `wc -l ~/.claude/hooks/**/*.py` → 모든 파일 120줄 이내 |
| 5 (MCP) | `claude mcp list` → 중복 없음 확인 |
| 6 (워크플로우) | `/daily-start`, `/daily-end` 실행 확인 |

### 전체 검증

```bash
# 1. 모든 hook 줄 수 확인
find ~/.claude/hooks -name "*.py" -exec sh -c 'echo "$(wc -l < "$1") $1"' _ {} \; | sort -rn

# 2. CLAUDE.md 줄 수 확인
wc -l ~/.claude/CLAUDE.md

# 3. settings.local.json 항목 수
grep -c 'Bash(' ~/.claude/settings.local.json

# 4. 크리덴셜 하드코딩 검사
grep -r 'sk-ant\|ghp_\|xoxb-' ~/.claude/*.json ~/.claude/mcp*.json 2>/dev/null
```

---

## 핵심 파일 목록

| 파일 | 작업 |
|------|------|
| `~/.zshrc` | 앨리어스 추가, API 키 Keychain 전환 |
| `~/.claude/CLAUDE.md` | 294줄→80줄 슬리밍 |
| `~/.claude/settings.local.json` | 167개→5개 정리 |
| `~/.claude/hooks/Stop/session-saver.py` | HANDOFF.md 생성 기능 추가 |
| `~/.claude/hooks/UserPromptSubmit/handoff-loader.py` | 새 파일 |
| `~/.claude/hooks/_shared/hook_utils.py` | 새 파일 (공통 유틸) |
| `~/.claude/hooks/_shared/sql_utils.py` | 새 파일 (SQL 유틸) |
| `~/.claude/hooks/UserPromptSubmit/auto-context-manager.py` | 200줄→80줄 분할 |
| `~/.claude/hooks/PreToolUse/writer-reviewer-hook.py` | 170줄→90줄 분할 |
| `~/.claude/hooks/PostToolUse/sql-alert-monitor.py` | 171줄→80줄 분할 |
| `~/.claude/hooks/PostToolUse/sql-data-collector.py` | 135줄→80줄 분할 |
| `~/.claude/hooks/PreToolUse/rollback-guard.py` | 130줄→90줄 간략화 |
| `~/.claude/rules/_shared/core-rules.md` | 새 파일 (CLAUDE.md에서 분리) |
| `~/.claude/rules/_shared/workflow-rules.md` | 새 파일 (CLAUDE.md에서 분리) |
| `~/.claude/settings.json` | handoff-loader hook 등록 |
| `~/.claude/mcp.json` | 중복 서버 제거, 크리덴셜 환경변수화 |
| `~/.claude/commands/daily-start.md` | 새 파일 |
| `~/.claude/commands/daily-end.md` | 새 파일 |
