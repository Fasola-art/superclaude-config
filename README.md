# SuperClaude v2.1.0 — 환경 최적화 요약

> Mac Studio Ultra M2 | Opus 4.6 | 2026-02-19 적용 완료

---

## Before / After

```
항목                      Before          After           변화
──────────────────────────────────────────────────────────────────
CLAUDE.md                 294줄           132줄           -55%
settings.local.json       179개 허용      22개 허용       -88%
하드코딩 크리덴셜         9개 평문        0개             -100%
Hook 초과 파일            5개 (>120줄)    0개 (>150줄)    해결
MCP 중복 서버             2개             0개             해결
세션 연속성               없음            HANDOFF.md 자동  신규
터미널 앨리어스           0개             8개             신규
음성 입력 (STT)           없음            Fisper (무료)   신규
컨테이너 격리             없음            cdocker         신규
```

---

## Phase별 변경 내역

### Phase 1: 즉시 적용

| 항목 | 변경 |
|------|------|
| ~/.zshrc | 앨리어스 8개 추가 (c, cc, cr, cj, cplan, cw, ct, cdocker) |
| API 키 보안 | 9개 키 → macOS Keychain 이전 (`security` 명령) |
| settings.local.json | 179 → 22개로 정리 (와일드카드 패턴만 유지) |
| mcp.json | puppeteer 제거, 크리덴셜 → `${ENV_VAR}` 참조 |

### Phase 2: 세션 연속성 (HANDOFF.md)

| 파일 | 역할 |
|------|------|
| hooks/Stop/session-saver.py | 세션 종료 시 HANDOFF.md 자동 생성 |
| hooks/UserPromptSubmit/handoff-loader.py | 세션 시작 시 HANDOFF.md 로드 → 아카이브 |

### Phase 3: CLAUDE.md 슬리밍

| 파일 | 줄 수 | 내용 |
|------|-------|------|
| CLAUDE.md | 132줄 | 핵심 규칙만 유지 (v2.0.9 → v2.1.0) |
| rules/_shared/workflow-rules.md | 57줄 | 분리: 슬래시 커맨드, Skill Capture, 문서 참조 |

### Phase 4: Hook 리팩토링

| 파일 | Before → After | 방법 |
|------|----------------|------|
| auto-context-manager.py | 200 → 111줄 | 공통 유틸 추출 |
| writer-reviewer-hook.py | 170 → 84줄 | 인라인 간소화 |
| sql-alert-monitor.py | 171 → 67줄 | sql_utils 분리 |
| sql-data-collector.py | 135 → 69줄 | sql_utils 공유 |
| rollback-guard.py | 130 → 107줄 | 코드 축약 |

신규 공통 모듈:
- `hooks/_shared/hook_utils.py` (69줄) — 상태 관리, 키워드 추출
- `hooks/_shared/sql_utils.py` (54줄) — SQL hook 공통 로직

### Phase 5: MCP 통합

- mcp.json: github, postgres 중복 제거 (mcp-router만 유지)
- mcp-router/servers.json: github 크리덴셜 → `${GITHUB_PAT}`
- 전체 크리덴셜 환경변수화 확인 완료

### Phase 6: 워크플로우 자동화

| 커맨드 | 용도 |
|--------|------|
| /daily-start | 아침 루틴: HANDOFF 로드, TODO 확인, 우선순위 제안 |
| /daily-end | 종료 루틴: HANDOFF 생성, TODO 갱신, 통계 출력 |

### Phase 7: 고급 최적화

| 항목 | 설명 |
|------|------|
| claude-container.sh | Docker 격리 실행 (node/python/go/rust, 네트워크 차단) |
| Fisper | 무료 로컬 STT (Whisper, F5 키로 음성 입력) |
| statusline.sh | 상태바: 모델 / Git branch / 시간 |

---

## 보안 현황

```
✅ 하드코딩 크리덴셜: 0개 (전부 macOS Keychain)
✅ Keychain 저장 키: anthropic-api-key-1, github-pat, slack-bot,
   brave-api-key, sentry-token, linear-api-key, exa-api-key,
   kie-api-key, notion-token
✅ MCP 토큰: 전부 ${ENV_VAR} 참조
✅ .zshrc: Keychain lookup만 사용
```

---

## 줄 수 제한 정책 (v2.1.0)

| 타입 | 범위 | 분할 기준 |
|------|------|-----------|
| Logic/Utils | 50~100줄 | 3+ 함수 |
| UI Components | 100~150줄 | 4+ 상태 |
| API/Server | 80~120줄 | 에러 처리 복잡 |
| Hook scripts (.py) | 50~150줄 | 복잡 로직 → _shared/ |
| Rules/Guides (.md) | 50~120줄 | 3+ 섹션 |
| Reference (.md) | 80~150줄 | 단일 주제 |

---

## 앨리어스 요약

```bash
c       # claude
cc      # claude --continue
cr      # claude --resume
cj      # claude -p (JSON/pipe)
cplan   # claude -p "/plan"
cw      # claude --resume work
ct      # claude --resume trading
cdocker # Docker 격리 실행
```

---

## 디렉토리 구조

```
~/.claude/
├── CLAUDE.md               # 메인 규칙 (132줄)
├── README.md               # 이 파일
├── settings.json           # 공식 설정 (hooks 등록)
├── settings.local.json     # 허용 권한 (22개)
├── mcp.json                # MCP 서버 설정
├── mcp-router/             # MCP 라우터
├── hooks/
│   ├── _shared/            # 공통 유틸 (hook_utils, sql_utils)
│   ├── UserPromptSubmit/   # 입력 시 실행 (8개)
│   ├── PreToolUse/         # 도구 실행 전 (4개)
│   ├── PostToolUse/        # 도구 실행 후 (12개)
│   └── Stop/               # 세션 종료 시 (1개)
├── commands/               # 슬래시 커맨드 (36개)
├── scripts/                # 유틸 스크립트 (5개)
├── rules/                  # 언어별 코딩 규칙
│   ├── _shared/            # 공통 (agent-rules, workflow-rules)
│   ├── go/                 # Go 38 규칙
│   ├── python/             # Python 42 규칙
│   ├── react/              # React 49 규칙
│   ├── sql/                # SQL Trading 규칙
│   └── testing/            # TDD + E2E
├── modules/                # trading, sql-trading 등
├── session-env/            # 세션 상태
├── handoff-archive/        # HANDOFF 아카이브
└── todos/                  # TODO (세션별 자동 생성)
```

---

**META**: v2.1.0 | 2026-02-19 | SuperClaude 환경 최적화 완료
