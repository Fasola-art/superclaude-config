# Claude Code 오케스트레이터/에이전트/스킬/훅 완벽 가이드

> 실제 구현 코드와 함께하는 SuperClaude v2.0.9 심층 활용법

---

## 목차

1. [시스템 아키텍처](#시스템-아키텍처)
2. [훅 시스템 상세](#훅-시스템-상세)
3. [병렬 에이전트 실행](#병렬-에이전트-실행)
4. [Vibe/Mode 키워드](#vibemode-키워드)
5. [Writer-Reviewer 루프](#writer-reviewer-루프)
6. [오케스트레이터 워크플로우](#오케스트레이터-워크플로우)
7. [실전 사용 시나리오](#실전-사용-시나리오)
8. [Quick Reference](#quick-reference)

---

## 시스템 아키텍처

### 핵심 구성 요소

```
┌─────────────────────────────────────────────────────────────┐
│                    사용자 프롬프트                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            UserPromptSubmit 훅 (7개 훅 순차 실행)             │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────┐ │
│  │ keyword-detector │ │ plan-mode-analyzer│ │ language-   │ │
│  │ (Vibe/Mode 감지) │ │ (PRD 감지)        │ │ enforcer    │ │
│  └──────────────────┘ └──────────────────┘ └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code 처리                         │
│   ┌───────────────────────────────────────────────────────┐ │
│   │              PreToolUse 훅                             │ │
│   │  • writer-reviewer-hook.py (4-agent 품질 검토 설정)     │ │
│   └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    도구 실행 (Edit/Write/Bash)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│            PostToolUse 훅 (12개 훅 조건부 실행)               │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────┐ │
│  │ format-python.py │ │ quality-gate.py  │ │ run-tests.py │ │
│  │ (ruff 포맷)      │ │ (8단계 검증)      │ │ (자동 테스트)│ │
│  └──────────────────┘ └──────────────────┘ └──────────────┘ │
│  ┌──────────────────┐ ┌──────────────────┐                  │
│  │ ralph-loop-      │ │ pattern-tracker  │                  │
│  │ checker.py       │ │.py               │                  │
│  │ (무한루프 감지)   │ │ (패턴 학습)       │                  │
│  └──────────────────┘ └──────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### 컴포넌트 관계도

```
┌─────────────────────────────────────────────────────────────┐
│                        SuperClaude v2.0.9                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │    Hooks    │───▶│   Agents    │───▶│   Skills    │      │
│  │  (자동화)   │    │  (병렬처리)  │    │  (재사용)   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │  Keywords   │    │  Personas   │    │  Commands   │      │
│  │ (트리거)    │    │  (역할)     │    │  (명령)     │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 훅 시스템 상세

### 1. 훅 이벤트 타입

| 이벤트 | 발생 시점 | 용도 | 예시 훅 |
|--------|----------|------|---------|
| `UserPromptSubmit` | 사용자가 프롬프트 전송 직후 | 키워드 감지, 모드 설정 | keyword-detector, plan-mode-analyzer |
| `PreToolUse` | 도구 실행 직전 | 권한 확인, W-R 설정 | writer-reviewer-hook |
| `PostToolUse` | 도구 실행 직후 | 포맷팅, 테스트, 품질 검사 | format-python, quality-gate |
| `Stop` | 세션 종료 시 | 세션 저장, 상태 기록 | session-saver |

### 2. 현재 활성화된 훅 목록

#### UserPromptSubmit (7개)
| 훅 | 파일 | 기능 |
|----|------|------|
| JARVIS 브리핑 | `jarvis-morning-briefing.py` | 시스템 상태 브리핑 |
| 키워드 감지 | `keyword-detector.py` | Vibe/Mode 키워드 감지 |
| 컨텍스트 정리 | `context-cleaner.py` | 컨텍스트 자동 압축 |
| 플랜 모드 분석 | `plan-mode-analyzer.py` | PRD 감지 및 플랜 모드 진입 |
| Todo 연속 | `todo-continuation.py` | 이전 작업 이어하기 |
| 언어 강제 | `language-enforcer.py` | 한국어 응답 강제 |
| 페르소나 활성화 | `persona-activator.py` | 자동 페르소나 선택 |

#### PreToolUse (1개)
| 훅 | 파일 | 기능 |
|----|------|------|
| Writer-Reviewer | `writer-reviewer-hook.py` | 4-agent 품질 검토 설정 |

#### PostToolUse (12개)
| 훅 | 매처 | 기능 |
|----|------|------|
| 작업 추적 | `Edit\|Write\|...` | 작업 기록 |
| 태스크 완료 | `TodoWrite\|TaskUpdate` | 완료 알림 |
| 세션 스냅샷 | `Edit\|Write\|MultiEdit` | 변경 기록 |
| Python 포맷 | `Edit\|Write\|MultiEdit` | ruff 자동 포맷 |
| JS/TS 포맷 | `Edit\|Write\|MultiEdit` | prettier 자동 포맷 |
| 테스트 실행 | `Edit\|Write\|MultiEdit` | 관련 테스트 자동 실행 |
| 품질 게이트 | `Edit\|Write\|MultiEdit` | 8단계 검증 |
| 패턴 추적 | `Edit\|Write\|MultiEdit` | 코딩 패턴 학습 |
| 백그라운드 알림 | `Bash` | 백그라운드 작업 완료 알림 |
| 에러 자동 해결 | `Bash` | 에러 KB 기반 자동 해결 |
| Ralph 루프 체커 | `Task` | 무한 루프 감지 |

#### Stop (1개)
| 훅 | 파일 | 기능 |
|----|------|------|
| 세션 저장 | `session-saver.py` | 세션 상태 저장 |

### 3. 훅 코드 상세 분석

#### keyword-detector.py

```python
# 13개 Vibe 키워드
VIBE_KEYWORDS = {
    # 실행 제어
    "빠르게": {"aliases": ["qk", "quick"], "action": "skip_validation"},
    "실험": {"aliases": ["exp"], "action": "snapshot_experiment"},
    "동시에": {"aliases": ["para"], "action": "parallel_agents"},

    # 수정/복구
    "고쳐": {"aliases": ["fix"], "action": "error_kb_healing"},
    "되돌려": {"aliases": ["undo"], "action": "rollback_snapshot"},
    "계속": {"aliases": ["cont"], "action": "continue_state"},

    # 검증
    "확인해": {"aliases": ["chk"], "action": "full_validation"},
    "테스트해": {"aliases": ["tst"], "action": "run_tests"},

    # 배포/정리
    "배포해": {"aliases": ["dep"], "action": "deploy_checklist"},
    "정리해": {"aliases": ["clean"], "action": "code_cleanup"},

    # 분석/계획
    "성능": {"aliases": ["perf"], "action": "performance_analysis"},
    "계획": {"aliases": ["plan"], "action": "planning_docs"},
    "분석": {"aliases": ["map"], "action": "codebase_analysis"},
}

# 4개 Mode 키워드
MODE_KEYWORDS = {
    "ultrawork": {"aliases": ["ulw"], "personas": ["explorer", "librarian", "analyzer"]},
    "deepsearch": {"aliases": ["ds"], "personas": ["explorer"]},
    "strategic": {"aliases": ["str"], "personas": ["architect"]},
    "visual": {"aliases": ["vis"], "personas": ["multimodal", "frontend"]},
}
```

#### quality-gate.py

```python
# 8단계 품질 게이트 (가중치 합계 = 1.0)
QUALITY_GATES = [
    {"name": "Syntax", "cmd": "check_syntax", "weight": 0.15},
    {"name": "Type", "cmd": "check_types", "weight": 0.15},
    {"name": "Lint", "cmd": "check_lint", "weight": 0.10},
    {"name": "Security", "cmd": "check_security", "weight": 0.20},  # 가장 중요
    {"name": "Test", "cmd": "run_tests", "weight": 0.15},
    {"name": "Performance", "cmd": "check_perf", "weight": 0.10},
    {"name": "Docs", "cmd": "check_docs", "weight": 0.05},
    {"name": "Integration", "cmd": "check_integration", "weight": 0.10},
]

# 파일 타입별 검사 명령어
# TypeScript: npx tsc --noEmit, npx eslint, npx vitest
# Python: python -m py_compile, pylint, pytest
```

#### ralph-loop-checker.py

```python
MAX_CONSECUTIVE_FAILURES = 5  # 최대 연속 실패 횟수
TIME_WINDOW_MINUTES = 5       # 시간 윈도우

# 동작:
# - 5분 내 5회 연속 실패 시 🛑 경고
# - 3회 이상 실패 시 ⚠️ 조기 경고
# - 성공 시 상태 리셋
```

---

## 병렬 에이전트 실행

### superclaude-config.json 설정

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

### 적응형 스케일링 동작

```
시작: 10개 동시 실행
       │
       ├── 3회 연속 성공 → 15개로 증가 (+5)
       │                    │
       │                    ├── 3회 연속 성공 → 20개로 증가
       │                    │
       │                    └── 1회 실패 → 17개로 감소 (-3)
       │
       └── 1회 실패 → 7개로 감소 (-3)
```

### 사용 가능한 에이전트 (79개)

| 카테고리 | 에이전트 예시 | 용도 |
|---------|-------------|------|
| 코드 리뷰 | code-reviewer | 버그, 보안, 품질 리뷰 |
| 코드 탐색 | code-explorer | 코드베이스 분석 |
| 테스트 | pr-test-analyzer | PR 테스트 커버리지 분석 |
| 설계 | code-architect | 기능 아키텍처 설계 |
| 타입 | type-design-analyzer | 타입 설계 분석 |
| 간소화 | code-simplifier | 코드 간소화 |
| 주석 | comment-analyzer | 주석 분석 |
| 실패 탐지 | silent-failure-hunter | 조용한 실패 탐지 |

### 병렬 실행 트리거 방법

```bash
# 방법 1: "동시에" 또는 "para" 키워드
> "para 이 코드 분석하고 테스트 생성해줘"
🎯 vibe:동시에

# 방법 2: Task 도구로 여러 에이전트 동시 호출
# (내부적으로 자동 병렬 처리)
```

---

## Vibe/Mode 키워드

### Vibe 키워드 (13개)

| 키워드 | 단축어 | 동작 | 사용 예시 |
|--------|-------|------|----------|
| 빠르게 | qk, quick | 검증 스킵 | `"qk 버튼 색상 바꿔"` |
| 실험 | exp | 스냅샷 후 실험 | `"exp 이 방식 시도해봐"` |
| 동시에 | para | 병렬 에이전트 | `"para 분석하고 문서화해"` |
| 고쳐 | fix | 에러 KB 기반 수정 | `"fix 이 에러 고쳐"` |
| 되돌려 | undo | 스냅샷 롤백 | `"undo 이전 상태로"` |
| 계속 | cont | 이전 상태 계속 | `"cont 이어서 진행"` |
| 확인해 | chk | 전체 검증 | `"확인해 품질 검사"` |
| 테스트해 | tst | 테스트 실행 | `"tst 모든 테스트 실행"` |
| 배포해 | dep | 배포 체크리스트 | `"dep 프로덕션 배포"` |
| 정리해 | clean | 코드 정리 | `"clean 불필요 코드 제거"` |
| 성능 | perf | 성능 분석 | `"perf 병목 찾아줘"` |
| 계획 | plan | 계획 문서화 | `"plan 구현 계획 세워"` |
| 분석 | map | 코드베이스 분석 | `"map 구조 파악해줘"` |

### Mode 키워드 (4개)

| 모드 | 단축어 | 활성화 페르소나 | 용도 |
|------|-------|---------------|------|
| ultrawork | ulw | explorer, librarian, analyzer | 집중 작업 모드 |
| deepsearch | ds | explorer | 깊은 탐색 모드 |
| strategic | str | architect | 전략적 설계 모드 |
| visual | vis | multimodal, frontend | 시각적 작업 모드 |

### 사용 예시

```bash
# Vibe 키워드
> "qk API 엔드포인트 추가"
🎯 vibe:빠르게
→ 검증 스킵하고 바로 실행

> "para 보안 점검하고 성능 분석해"
🎯 vibe:동시에
→ 두 작업 병렬 실행

# Mode 키워드
> "ulw 이 기능 구현해줘"
🎯 mode:ultrawork
→ explorer, librarian, analyzer 페르소나 활성화

> "ds 이 버그 원인 찾아"
🎯 mode:deepsearch
→ explorer 페르소나로 깊은 탐색
```

---

## Writer-Reviewer 루프

### 개요

Writer-Reviewer는 코드 작성 시 4개의 리뷰어 에이전트가 병렬로 검토하여 품질을 보장하는 시스템입니다.

### 4-Agent 구성

```
┌─────────────────────────────────────────────────────────────┐
│                      Writer (코드 작성)                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   4 Reviewers (병렬 실행)                    │
├─────────────────┬─────────────────┬─────────────────┬───────┤
│ Quality (30%)   │ Security (30%)  │ Performance(20%)│A11y   │
│                 │                 │                 │(20%)  │
│ • 코드 품질     │ • 취약점 검사   │ • 병목 분석     │• 접근성│
│ • 가독성        │ • 인증/인가     │ • 메모리 누수   │• ARIA  │
│ • 유지보수성    │ • 인젝션 방지   │ • 알고리즘 효율 │• 키보드│
└─────────────────┴─────────────────┴─────────────────┴───────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              점수 합산 (targetScore: 0.85)                   │
│                                                              │
│   현재 점수 < 0.85 → 피드백 기반 재작성 (최대 10회)          │
│   현재 점수 ≥ 0.85 → ✅ 완료                                 │
│   수렴 임계값: 0.015 (개선폭이 이보다 작으면 조기 종료)       │
└─────────────────────────────────────────────────────────────┘
```

### 코드 타입별 가중치 자동 조정

```python
CODE_TYPE_PATTERNS = {
    'frontend': {
        'keywords': ['component', 'tsx', 'jsx', 'ui', 'form', 'button'],
        'weights': {
            'quality': 0.25,
            'security': 0.25,
            'performance': 0.20,
            'accessibility': 0.30  # 프론트엔드: 접근성 중요
        }
    },
    'backend': {
        'keywords': ['api', 'route', 'endpoint', 'controller', 'service'],
        'weights': {
            'quality': 0.25,
            'security': 0.40,       # 백엔드: 보안 중요
            'performance': 0.25,
            'accessibility': 0.10
        }
    },
    'database': {
        'keywords': ['query', 'sql', 'database', 'migration', 'schema'],
        'weights': {
            'quality': 0.20,
            'security': 0.40,       # DB: 보안 매우 중요
            'performance': 0.35,    # 쿼리 성능도 중요
            'accessibility': 0.05
        }
    },
    'utility': {
        'keywords': ['util', 'helper', 'lib', 'function', 'hook'],
        'weights': {
            'quality': 0.35,        # 유틸: 품질 중요
            'security': 0.25,
            'performance': 0.30,
            'accessibility': 0.10
        }
    }
}
```

### 스킵 조건

다음 파일들은 W-R 루프를 스킵합니다:
- 설정 파일: `.json`, `.env`, `tsconfig`, `eslint`, `prettier`
- 문서: `.md`
- 락 파일: `.lock`
- Git 관련: `git`, `config`

### 설정값

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

## 오케스트레이터 워크플로우

### /orchestrator 명령어

복잡한 연구 주제를 체계적으로 조사하고 종합 보고서를 생성합니다.

### 6단계 워크플로우

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Query Analysis (질문 분석)                                │
│    • 사용자 질문 명확화                                      │
│    • 핵심 키워드 추출                                        │
│    • 연구 범위 정의                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Research Brief (연구 개요)                                │
│    • 연구 질문 구조화                                        │
│    • 하위 질문 도출                                          │
│    • 가설 설정                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Strategy (전략 수립)                                      │
│    • 연구 방법론 결정                                        │
│    • 데이터 소스 선정                                        │
│    • 에이전트 할당                                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Parallel Research (병렬 리서치) ⚡ 핵심 단계              │
│                                                              │
│    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│    │   학술 연구   │ │   기술 조사   │ │  데이터 분석  │       │
│    │  (논문, 학회) │ │ (GitHub,문서) │ │ (통계,트렌드) │       │
│    └──────────────┘ └──────────────┘ └──────────────┘       │
│           │               │               │                  │
│           └───────────────┴───────────────┘                  │
│                           │                                  │
│                    ┌──────────────┐                          │
│                    │   팩트체크    │                          │
│                    │ (정보 검증)   │                          │
│                    └──────────────┘                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Synthesis (종합)                                          │
│    • 여러 소스 통합                                          │
│    • 충돌 정보 해결                                          │
│    • 인사이트 도출                                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Report (보고서 생성)                                      │
│    • 최종 문서화                                             │
│    • 구조화된 보고서                                         │
│    • 참고 자료 정리                                          │
└─────────────────────────────────────────────────────────────┘
```

### 오케스트레이터 에이전트 구조

| 에이전트 | 역할 | 담당 작업 |
|---------|------|----------|
| research-orchestrator | 전체 조율 | 워크플로우 관리, 에이전트 할당 |
| academic-researcher | 학술 연구 | 논문, 연구 데이터 수집 |
| technical-researcher | 기술 조사 | 기술 문서, GitHub, 공식 문서 |
| data-analyst | 데이터 분석 | 통계, 트렌드 분석 |
| fact-checker | 팩트체크 | 정보 검증, 출처 확인 |
| research-synthesizer | 결과 종합 | 여러 소스 통합 |
| report-generator | 보고서 생성 | 최종 문서화 |

### 사용 방법

```bash
# 명령어로 호출
/orchestrator AI가 암호화에 미치는 영향

# 또는 Task 도구로 직접 호출
Task 도구:
  subagent_type: general-purpose
  prompt: "다음 주제에 대해 Open Deep Research 방법론으로
          종합 연구를 수행하세요: [주제]"
```

---

## 실전 사용 시나리오

### 시나리오 1: 빠른 코드 수정

```bash
> "qk 로그인 버튼 색상 파란색으로 바꿔줘"

동작 흐름:
1. keyword-detector: "qk" 감지
   🎯 vibe:빠르게 → action: skip_validation
2. W-R 루프 스킵
3. 즉시 Edit 실행
4. PostToolUse 훅 최소 실행
5. ✅ 완료

예상 시간: 5초
```

### 시나리오 2: 보안 중심 API 개발

```bash
> "사용자 결제 API 엔드포인트 만들어줘"

동작 흐름:
1. writer-reviewer-hook: 'api' 키워드 감지
   → 코드 타입: backend
   → 가중치: security 40%, quality 25%, perf 25%, a11y 10%

2. Writer가 코드 작성

3. 4-Agent 병렬 리뷰:
   - Quality Agent: 코드 품질 체크
   - Security Agent: 인증, SQL 인젝션, XSS 검사 (가중치 40%)
   - Performance Agent: 응답 시간, 메모리 사용량
   - Accessibility Agent: API 응답 형식

4. 점수 계산:
   첫 번째 반복: 0.72 < 0.85 → 재작성
   두 번째 반복: 0.81 < 0.85 → 재작성
   세 번째 반복: 0.88 ≥ 0.85 → ✅ 완료

5. PostToolUse:
   - quality-gate.py 실행
   - run-tests.py 실행

예상 시간: 2-3분
```

### 시나리오 3: 병렬 분석 작업

```bash
> "para 이 코드베이스 분석하고 문서화하고 테스트 생성해줘"

동작 흐름:
1. keyword-detector: "para" 감지
   🎯 vibe:동시에 → action: parallel_agents

2. 3개 Task 동시 실행:
   ┌────────────────────────────────────────────┐
   │ Task 1: code-explorer                      │
   │ • 코드베이스 구조 분석                      │
   │ • 의존성 파악                               │
   │ • 아키텍처 문서화                           │
   ├────────────────────────────────────────────┤
   │ Task 2: sc:document                        │
   │ • README 생성                              │
   │ • API 문서 생성                            │
   │ • 사용법 가이드                            │
   ├────────────────────────────────────────────┤
   │ Task 3: generate-tests                     │
   │ • 함수별 테스트 케이스                     │
   │ • 엣지 케이스                              │
   │ • 통합 테스트                              │
   └────────────────────────────────────────────┘

3. 결과 병합 및 반환

예상 시간: 순차 실행 대비 60% 단축
```

### 시나리오 4: 무한 루프 방지

```bash
> 복잡한 작업 중 연속 에러 발생

동작 흐름:
1. 첫 번째 실패:
   └── ralph-loop-checker: 상태 기록 (failures: 1)

2. 두 번째 실패:
   └── 상태 기록 (failures: 2)

3. 세 번째 실패:
   └── ⚠️ Loop:3/5 경고 출력
   └── 사용자에게 알림

4. 네 번째 실패:
   └── ⚠️ Loop:4/5 경고

5. 다섯 번째 실패:
   └── 🛑 Loop:5회 → 수동 개입
   └── 자동 실행 중단
   └── 사용자 수동 개입 요청

복구 방법:
- 에러 수정 후 성공 시 자동 리셋
- "고쳐" 키워드로 에러 KB 기반 수정 시도
```

### 시나리오 5: PRD 기반 프로젝트 시작

```bash
> "이 PRD 문서를 기반으로 프로젝트 시작해줘"
> [PRD.md 파일 첨부]

동작 흐름:
1. plan-mode-analyzer:
   • PRD 파일 패턴 감지: .*PRD\.md$ → confidence: 90%
   • 기능 목록 감지: features_count: 12
   • 분석 깊이 결정: 'think-hard'

2. 자동 플랜 모드 진입:
   {
     "status": "detected",
     "type": "file",
     "confidence": 0.9,
     "features_count": 12,
     "analysis_depth": "think-hard",
     "action": "enter_plan_mode"
   }

3. 프로젝트 계획 수립:
   • 기능별 구현 순서 결정
   • 의존성 분석
   • 마일스톤 설정

4. TodoWrite로 태스크 생성:
   [ ] 프로젝트 초기화
   [ ] 기능 1 구현
   [ ] 기능 2 구현
   ...

5. 순차적 구현 시작
```

### 시나리오 6: 딥서치 모드로 버그 탐색

```bash
> "ds 이 메모리 누수 원인 찾아줘"

동작 흐름:
1. keyword-detector: "ds" 감지
   🎯 mode:deepsearch
   → 활성화 페르소나: explorer

2. explorer 페르소나로 깊은 탐색:
   • 코드 히스토리 분석
   • 관련 이슈 검색
   • 메모리 프로파일링 제안
   • 의심 지점 식별

3. 단계별 분석 보고:
   • 1단계: 증상 분석
   • 2단계: 관련 코드 추적
   • 3단계: 원인 가설 수립
   • 4단계: 검증 방법 제안

4. 해결책 제시
```

---

## Quick Reference

### 자주 쓰는 키워드

| 상황 | 키워드 | 효과 |
|------|--------|------|
| 빠른 수정 | `qk` | 검증 스킵 |
| 병렬 작업 | `para` | 에이전트 병렬 실행 |
| 에러 수정 | `fix` | 에러 KB 기반 수정 |
| 품질 검사 | `확인해` | 전체 검증 실행 |
| 테스트 | `tst` | 테스트 실행 |
| 성능 분석 | `perf` | 성능 병목 분석 |
| 깊은 탐색 | `ds` | 딥서치 모드 |

### 자주 쓰는 명령어

| 명령어 | 용도 |
|--------|------|
| `/orchestrator [주제]` | 종합 연구 |
| `/generate-tests [파일]` | 테스트 생성 |
| `/project-plan` | 프로젝트 계획 |
| `/commit` | Git 커밋 |
| `/review-pr` | PR 리뷰 |
| `/sc:analyze` | 코드 분석 |

### 주요 설정 파일

| 파일 | 위치 | 용도 |
|------|------|------|
| CLAUDE.md | `~/.claude/CLAUDE.md` | 전역 지침 |
| settings.json | `~/.claude/settings.json` | 권한/훅 설정 |
| superclaude-config.json | `~/.claude/superclaude-config.json` | 병렬/W-R 설정 |
| servers.json | `~/.claude/mcp-router/servers.json` | MCP 서버 |

### 훅 출력 해석

| 출력 | 의미 |
|------|------|
| `🎯 vibe:빠르게` | 빠르게 모드 활성화 |
| `🎯 mode:deepsearch` | 딥서치 모드 활성화 |
| `🔍 QG:python → '확인해'로 검증` | 품질 게이트 대기 중 |
| `⚠️ Loop:3/5` | 연속 실패 경고 |
| `🛑 Loop:5회 → 수동 개입` | 무한 루프 감지 |

---

## 문제 해결

### Q: W-R 루프가 계속 반복됨

```bash
# 해결: 수렴 임계값 확인
convergenceThreshold: 0.015
# 점수 개선폭이 1.5% 미만이면 자동 종료

# 또는 maxIterations 조정
maxIterations: 10 → 5로 줄이기
```

### Q: 병렬 에이전트가 느림

```bash
# 해결: 동시 실행 수 조정
# superclaude-config.json에서:
"initial": 10 → 5로 줄이기
"maximum": 24 → 12로 줄이기
```

### Q: 특정 파일에서 훅이 안 됨

```bash
# 해결: 스킵 조건 확인
SKIP_CONDITIONS = ['git', 'config', '.md', '.json', ...]
# 해당 패턴에 포함되면 훅 스킵됨
```

---

## 결론

> SuperClaude v2.0.9는 훅 기반 자동화 + 병렬 에이전트 + Writer-Reviewer 루프를 통해
> 고품질 코드를 효율적으로 생성하는 시스템입니다.

### 핵심 활용 포인트

1. **Vibe 키워드로 동작 제어**: `qk`, `para`, `fix`, `확인해` 등
2. **Mode 키워드로 페르소나 활성화**: `ulw`, `ds`, `str`, `vis`
3. **자동 품질 게이트**: 코드 변경 시 8단계 자동 검증
4. **병렬 에이전트**: 최대 24개 동시 실행 (M2 Ultra 최적화)
5. **Writer-Reviewer 루프**: 목표 점수(0.85) 달성까지 자동 개선
6. **무한 루프 방지**: 5분 내 5회 실패 시 자동 중단

---

**META**
- Generated: 2026-01-31
- Tool: Claude Code (SuperClaude v2.0.9)
- Version: 2.0.9
- Platform: macOS (Mac Studio Ultra M2)
