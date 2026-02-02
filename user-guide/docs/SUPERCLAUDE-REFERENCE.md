# SuperClaude 종합 레퍼런스

> **버전**: 2.0.9
> **플랫폼**: Mac Studio Ultra M2
> **최종 업데이트**: 2026-01-30

---

## 아키텍처

```
~/.claude/
├── CLAUDE.md                 # 메인 설정 (엔트리 포인트)
├── settings.json             # 권한, Hooks, 설정값
├── docs/                     # 상세 문서
│   ├── WRITER-REVIEWER-SYSTEM.md
│   ├── HOOKS-SYSTEM.md
│   ├── PERSONAS.md
│   ├── QUALITY-GATES.md
│   ├── PROJECT-PLANNING.md
│   └── ...
├── profiles/                 # 언어별 프로필
│   ├── typescript.md
│   └── rust.md
├── skills/                   # 34개 스킬
├── hooks/                    # 훅 스크립트
├── mcp-router/               # MCP 라우터
├── jarvis/                   # 개인 비서 시스템
└── cheatsheets/              # 빠른 참조
```

---

## 설정 파일 (settings.json)

### 권한 시스템 (permissions)

| 카테고리 | 설정 |
|---------|------|
| ✔ Allow | 파일 읽기/쓰기, Git (push 제외), npm/pip, supabase, gh CLI |
| ✘ Deny | git push, rm -rf, sudo, .env 접근 |
| Auto | acceptEdits (편집 자동 수락) |

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

## 컨텍스트 관리 (context_management)

| 임계값 | 동작 |
|--------|------|
| ⚠ 75% | 경고 (cleanup 권장) |
| 🔴 90% | Critical (DCP 압축 제안) |
| 🚨 95% | Emergency (강제 압축) |

**전략**: deduplication, error_cleanup, file_summarize

---

## Ralph Loop (에러 자동 해결)

```json
"ralph_loop": {
  "enabled": true,
  "max_retries": 10,
  "auto_triggers": ["npm run build", "npm run test", "npm run lint"],
  "success_patterns": ["success", "completed", "PASSED"]
}
```

---

## Quality Gate (품질 검증)

```json
"quality_gate": {
  "enabled": true,
  "threshold": 0.85,     // 85% 이상 통과
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

## 병렬 실행 (parallel_execution)

```json
"parallel_execution": {
  "max_agents": "unlimited",  // 무제한
  "smart_grouping": true      // 종속성 자동 감지
}
```

---

## Writer-Reviewer 시스템

### 작동 원리

```
코드 요청 → Writer Agent → 4개 Reviewer 병렬 검수 → Score < 85%? → 반복 (최대 10회)
```

### 4-Agent 병렬 검수

| Agent | 가중치 | 검사 항목 |
|-------|--------|----------|
| Quality | 30% | 가독성, 타입, SOLID, DRY, UI/Hook 분리 |
| Security | 30% | XSS, 인젝션, 인증/인가, OWASP Top 10 |
| Performance | 20% | 알고리즘, 렌더링, 메모리, N+1 |
| Accessibility | 20% | 시맨틱 HTML, ARIA, 키보드, WCAG 2.1 |

### v2.1 신규 기능

| 기능 | 설명 |
|------|------|
| Security Hardening | 프롬프트 인젝션 방어, 검수 우회 방지 |
| Adaptive Weights | 코드 유형별 가중치 자동 조정 |
| Incremental Review | 2회차부터 diff만 검토 (40-60% 토큰 절감) |
| Forced Convergence | 1.5% 미만 변화 × 2회 → 조기 종료 |
| Conflict Resolution | Security > Quality > Performance > A11y |

---

## 코드 아키텍처 원칙

| 원칙 | 설명 |
|------|------|
| UI/Hook 분리 | 컴포넌트는 UI만, 로직은 use-*.ts 훅으로 |
| 공통 기능 추출 | 2회 이상 반복 → 공통 컴포넌트 |
| SSOT | 단일 출처, 파생 값은 계산 |

---

## Hooks 자동화 시스템

### UserPromptSubmit (6개 훅)

| 훅 | 목적 |
|----|------|
| plan-mode-analyzer.py | PRD 감지 → 플랜 모드 진입 |
| context-cleaner.js | 컨텍스트 70%+ → 자동 정리 |
| keyword-detector.js | 13개 Vibe + 4개 Mode 키워드 감지 |
| persona-activator.js | 작업 타입별 페르소나 활성화 |
| task-continuation-enforcer.js | 미완료 Todo 복원 |
| daily-update-checker.js | 1일 1회 업데이트 확인 |

### PreToolUse (2개 훅)

| 훅 | 매처 | 목적 |
|----|------|------|
| writer-reviewer-hook.py | Edit\|Write\|MultiEdit | Writer-Reviewer 루프 활성화 |
| error-warning-hook.js | Edit\|Write\|MultiEdit | Error KB 패턴 경고 |

### PostToolUse (8개 훅)

| 훅 | 매처 | 목적 |
|----|------|------|
| quality-gate.js | Write\|Edit\|MultiEdit | 8단계 Quality Gate |
| error-auto-resolver.js | Bash\|Task | Ralph Loop (최대 10회 재시도) |
| session-snapshot.js | Todo\|Bash\|Write\|Edit | 세션 자동 스냅샷 |
| infinite-loop-checker.js | Bash\|Task | 무한 루프 감지 (5회 동일 에러 → 중단) |
| pattern-tracker.js | Task | 패턴 학습 |
| empty-task-response-detector.js | Task | 빈 응답 감지 |
| background-notification.js | Task | 백그라운드 완료 알림 |

---

## 키워드 트리거 시스템

### Vibe 키워드 (13개)

| 키워드 | Alias | 동작 |
|--------|-------|------|
| 빠르게 | qk | 검증 스킵, 즉시 실행 |
| 실험 | exp | 스냅샷 → 실행 → 롤백 옵션 |
| 동시에 | para | 병렬 에이전트 실행 |
| 고쳐 | fix | Error KB + Self-Healing |
| 되돌려 | undo | 마지막 스냅샷으로 롤백 |
| 계속 | cont | 이전 작업 계속 (STATE.md 복원) |
| 확인해 | chk | Type + Lint + Build 검증 |
| 테스트해 | tst | 관련 테스트 실행 |
| 배포해 | dep | 배포 체크리스트 |
| 정리해 | clean | 코드 정리 (unused imports, console.log) |
| 성능 | perf | 성능 분석 |
| 계획 | plan | .planning/ 문서 생성 |
| 분석 | map | 코드베이스 분석 |

### Mode 키워드 (4개)

| 키워드 | 동작 | 활성 페르소나 |
|--------|------|--------------|
| ultrawork (ulw) | 최대 병렬 에이전트 | explorer, librarian, analyzer |
| deepsearch (ds) | /research 스킬 연결 | explorer |
| strategic (str) | 트레이드오프 분석 | architect |
| visual (vis) | 이미지/UI 분석 | multimodal, frontend |

---

## MCP Router 시스템

### MCP Router인가?

- **등록**: 모든 MCP 도구가 system prompt에 노출 → 컨텍스트 폭발
- **Router**: 단일 진입점, 필요 시에만 동적 로딩 → 컨텍스트 절약

### 등록된 서버 (servers.json)

| 서버 | 용도 | 주요 도구 |
|------|------|----------|
| context7 | 라이브러리 문서 검색 | resolve-library-id, query-docs |
| mana | 코드 분석/심볼 검색 | find_symbol, search_for_pattern, rename_symbol |
| playwright | 브라우저 자동화 | browser_navigate, browser_click, browser_type |
| playwright-test | E2E 테스트 | test_list, test_run, test_debug |

---

## 페르소나 시스템

### 기술 페르소나 (14개)

| 페르소나 | 역할 | 활성화 키워드 |
|----------|------|--------------|
| architect | 시스템 설계, 확장성 | design, architecture, scale |
| frontend | UI/UX, 접근성 | UI, component, style |
| backend | API, 데이터 | API, server, database |
| security | 보안 (항상 ON) | auth, login, password, token |
| analyzer | 근본 원인 분석 | error, bug, debugging |
| performance | 최적화 | performance, slow, memory |
| tester | 테스트 | test, coverage, E2E |
| refactorer | 코드 품질 | refactoring, cleanup, DRY |
| devops | 배포, 인프라 | deploy, CI/CD, docker |
| mentor | 교육 | explain, why, how |
| scribe | 문서화 | document, README |
| explorer | 코드 탐색 | find, search, where |
| librarian | 문서 참조 | docs, reference |
| multimodal | 이미지 분석 | visual, screenshot |

### Ideation 페르소나 (27개)

**카테고리별 분류:**
- 비즈니스 (6): ceo, cfo, coo, sales, bd, legal
- 마케팅 (5): marketing, growth, content, community, pr
| 혁신 (5): innovator, futurist, visionary, disruptor, inventor
- 디자인 (3): designer, ux, user_advocate
- 분석 (4): critic, realist, devil_advocate, risk_analyst
- 리서치 (3): researcher, ethnographer, competitor
- 진행 (1): moderator

---

## Language Profiles

### TypeScript Profile

**활성화**: package.json 감지 시

| 원칙 | 내용 |
|------|------|
| Never Throws | Result<T, E> 패턴 사용 |
| Zod Validation | 스키마 우선 개발 |
| 상태 계층 | TanStack Query → Zustand → React Hook Form → nuqs |
| Strict 모드 | strict: true, noUncheckedIndexedAccess |

**자동 감지:**
- <Image> 사용 → next/image 권장
- import _ from 'lodash' → tree-shakable import 권장
- useQuery staleTime 없음 → 설정 권장

### Rust Profile

**활성화**: Cargo.toml 감지 시

| 원칙 | 내용 |
|------|------|
| Never Panics | Result<T, E> 필수 |
| Memory Leaks | RAII, Drop 구현 |
| Data Corruption | 불변성 유지 |

**도구:**
- cargo clippy -- -D warnings
- cargo fmt --check
- cargo +nightly miri test

---

## 스킬 시스템

### 주요 스킬 (34개+)

| 카테고리 | 스킬 |
|----------|------|
| 문서 | pdf, docx, pptx, xlsx |
| 디자인 | frontend-design, canvas-design, algorithmic-art |
| 개발 | frontend-dev, mcp-builder, webapp-testing |
| 기획 | prd-create, ideation, research, agent-team |
| 발표 | presentation-orchestrator, brand-guidelines |

### 핵심 스킬 명령어

| 명령어 | 용도 |
|--------|------|
| /prd-create | 아이디어 → PRD 생성 |
| /project-plan | PRD → 프로젝트 플랜 |
| /project-status | 진행 상황 확인 |
| /research | 범용 딥리서치 |
| /ideation | 다중 페르소나 토론 |

---

## 프로젝트 플래닝

### 8-Step 워크플로우

1. **Phase 1**: 깊은 분석 + 질문 + 아이디어
2. **Phase 2**: 5 Layer 분석 (Business/Functional/Technical/UX/Risk)
3. **Phase 3**: 질문 우선순위 (🔴 필수 / 🟡 확인 / ⚪ 나중에)
4. **Phase 4**: AI 아이디어 제안
5. **Phase 5**: 청사진 + 승인 (★ 유일한 승인 시점)
6. **Phase 6**: BLUEPRINT.md 생성 (화면 구성도, 사용자 여정, 데이터 구조)
7. **Phase 7**: 실행 계획 (Section → Milestone → Task)
8. **Phase 8**: 적응형 병렬 자동 개발

### 산출물
- BLUEPRINT.md (화면 구성도, 사용자 여정, 데이터 구조)
- 실행 계획 (Section → Milestone → Task)
- 완료 보고서 자동 생성

### 실행 특징
- Steel Thread 구현 (아키텍처 검증)
- 5개 시작 → 성공률에 따라 조절 (최대 무제한)
- 적응형 병렬 자동 개발

---

## 응형 병렬 실행

```yaml
초기: 5개 동시
조건:
  연속 3개 성공 → +5
  1개 실패 → -3 (최소 3)
최대: unlimited
```

---

## 요약 통계

| 항목 | 수량 |
|------|------|
| Hooks | 17개 |
| Vibe 키워드 | 13개 |
| Mode 키워드 | 4개 |
| 기술 페르소나 | 14개 |
| Ideation 페르소나 | 27개 |
| 스킬 | 34개+ |
| Language Profiles | 2개 (TypeScript, Rust) |
| MCP 서버 | 4개 |

---

## Jarvis 시스템

### 개요
개인 비서 시스템으로 작업 연속성, ML 기반 예측, 자율 작업 실행을 제공합니다.

### 폴더 구조
```
~/.claude/jarvis/
├── memory/
│   ├── manager.py         # 메모리 관리 (SQLite)
│   ├── jarvis.db          # SQLite 데이터베이스
│   └── ml_predictor.py    # ML 패턴 학습 & 예측
├── automation/
│   ├── browser.py         # 브라우저 자동화
│   └── task_executor.py   # 작업 실행 엔진
├── data/
│   ├── tasks.json         # 작업 목록
│   └── calendar.json      # 일정
├── daemon.py              # Background Daemon
└── test_jarvis.py         # 테스트
```

### 핵심 기능 (6 Phase)

| Phase | 기능 | 설명 |
|-------|------|------|
| 1 | 아침 브리핑 | 첫 실행 시 어제 작업/오늘 일정/미완료 작업 자동 표시 |
| 2 | 작업 연속성 | `/j remember` - 마지막 작업 컨텍스트 복원 |
| 3 | 자율 작업 실행 | `/j do <작업>` - 작업 의도 분석 후 자동 실행 |
| 4 | ML 학습 & 예측 | scikit-learn 기반 시간대별 행동 패턴 학습 |
| 5 | 라이프 관리 | `/j book`, `/j plan` - 예약/이벤트 계획 |
| 6 | Background Daemon | 자동 재학습/백업/패턴 업데이트 |

### 명령어

| 명령어 | 용도 |
|--------|------|
| `/j` | Jarvis 호출 |
| `/j briefing` | 상세 브리핑 |
| `/j remember` | 작업 연속성 확인 |
| `/j do <작업>` | 시뮬 작업 수행 |
| `/j book <예약>` | 레스토랑/영화/숙박 예약 |
| `/j plan <이벤트>` | 여행/파티/프로젝트 계획 |

### 데이터베이스 스키마

| 테이블 | 용도 |
|--------|------|
| work_sessions | 작업 세션 기록 (시간, 프로젝트, 파일 등) |
| usage_patterns | ML 학습용 패턴 (요일, 시간, 작업 유형, 빈도) |
| tasks | 작업 목록 (제목, 상태, 우선순위, 마감일) |
| calendar_events | 일정 (제목, 시간, 장소, 이벤트 타입) |

### ML 학습 특징
- scikit-learn 기반 패턴 학습
- 시간대별/요일별 행동 예측 (신뢰도 포함)
- 최적 피크 시간 분석
- 최소 10개 이상의 패턴 필요

### 개인 정보 보호
- **Local-First**: 모든 데이터 로컬 SQLite 저장
- **클라우드 없음**: 외부 서버 전송 없음
- **선택적 암호화**: 데이터베이스 암호화 가능

---

## ultrawork (ulw) 워크플로우 상세

### 사용 예시
```
"ulw 이 프로젝트 전체 구조 파악해줘"
```

### 시퀀스 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│                    사용자 입력                               │
│  "ulw 이 코드베이스 전체 분석해서 구조 파악해줘"             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            Phase 1: UserPromptSubmit Hooks                  │
│  settings.json → hooks.UserPromptSubmit (6개 훅 순차 실행)  │
│                                                             │
│  #1 jarvis-morning-briefing.py                              │
│  #2 plan-mode-analyzer.py                                   │
│  #3 context-cleaner.js                                      │
│  #4 keyword-detector.js ◄── 🎯 여기서 "ulw" 감지!           │
│  #5 persona-activator.js                                    │
│  #6 todo-continuation-enforcer.js                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            Phase 2: keyword-detector.js 내부                │
│                                                             │
│  1. 환경변수에서 프롬프트 읽기                               │
│     const userPrompt = getEnv('CLAUDE_USER_PROMPT');        │
│                                                             │
│  2. 키워드 검색 (우선순위 순)                                │
│     priorityOrder = ['strategic', 'str', 'ultrawork',       │
│                      'ulw', ...]                            │
│                                                             │
│  3. 설정 로드                                                │
│     config = {                                              │
│       action: '병렬 에이전트 최대 활용',                     │
│       personas: ['explorer', 'librarian', 'analyzer'],      │
│       parallel: true,                                       │
│       flags: ['--think']                                    │
│     }                                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 3: 활성화 메시지 출력 (console.log → Claude 컨텍스트)│
│  ═══════════════════════════════════════════════════════    │
│  🚀 "ULW" 모드 활성화                                       │
│  🔧 동작: 병렬 에이전트 최대 활용                            │
│  👥 페르소나: explorer, librarian, analyzer                 │
│  ⚡ 병렬 실행: 활성화                                       │
│  ═══════════════════════════════════════════════════════    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Phase 4: Claude 행동 결정                      │
│                                                             │
│  parallel_execution.max_agents = "unlimited" 설정 참조      │
│  → Task 에이전트 다중 병렬 실행 결정                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Phase 5: 병렬 에이전트 실행                    │
│                                                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │ 🔍 Explorer  │ │ 📚 Librarian │ │ 📊 Analyzer  │        │
│  │   Agent 1    │ │   Agent 2    │ │   Agent 3    │        │
│  │ 파일 구조    │ │ README 분석  │ │ 의존성 분석  │        │
│  │ 분석         │ │ 문서 검색    │ │ 복잡도 측정  │        │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘        │
│         └────────────────┼────────────────┘                 │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    결과 통합                        │   │
│  │  • 프로젝트 구조도  • 핵심 파일 목록               │   │
│  │  • 의존성 그래프    • 아키텍처 분석               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 핵심 포인트 - 컨텍스트 주입 방식
- keyword-detector.js의 console.log() 출력이 Claude 컨텍스트로 주입
- Claude가 인식된 모드/페르소나를 "인식"하고 행동 결정
- 명령어가 아니라 "힌트/지시"를 주입하는 방식

### 페르소나의 역할

| 페르소나 | ultrawork에서의 역할 |
|----------|----------------------|
| explorer | 파일 구조 탐색, 패턴 검색 |
| librarian | 문서 참조, 라이브러리 정보 |
| analyzer | 의존성 분석, 복잡도 측정 |
