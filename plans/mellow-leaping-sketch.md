# 🤖 JARVIS 자동화 워크플로우 구현 계획

> **목표**: 코드 구조화 지침 적용 + 미구현 기능 완성 + 자율자동 시스템

---

## 현재 상태 (65% 완료)

| 파일 | 줄 수 | 상태 | 조치 |
|-----|------|------|------|
| memory/manager.py | 360줄 | ✅ 완전 | 🔧 6개 파일로 분할 |
| memory/ml_predictor.py | 235줄 | ✅ 완전 | 🔧 3개 파일로 분할 |
| automation/task_executor.py | 311줄 | ⚠️ 부분 | 🔧 8개 파일로 분할 |
| automation/browser.py | 189줄 | ✅ 완전 | 🔧 2개 파일로 분할 |
| daemon.py | 147줄 | ✅ 완전 | 🔧 2개 파일로 분할 |

---

## Phase 1: 리팩토링 (코드 구조화 지침 적용)

### 1.1 TaskExecutor 분할 (311줄 → 8개 파일)

```
jarvis/automation/executor/
├── __init__.py           # barrel export
├── types.py              # IntentResult, ExecuteResult (~20줄)
├── patterns.py           # 의도 분석 패턴 (~40줄)
├── intent_analyzer.py    # analyze_intent (~60줄)
├── task_handler.py       # add/list/complete task (~70줄)
├── event_handler.py      # add/list event (~60줄)
├── context_handler.py    # remember/recall (~50줄)
├── booking_handler.py    # 예약 처리 (~80줄) ⭐신규
└── executor.py           # 메인 클래스 (~70줄)
```

### 1.2 MemoryManager 분할 (360줄 → 6개 파일)

```
jarvis/memory/models/
├── __init__.py
├── work_session.py       # WorkSessionManager (~60줄)
├── task.py               # TaskManager (~60줄)
├── calendar.py           # CalendarManager (~50줄)
├── context.py            # ContextManager (~45줄)
└── usage_pattern.py      # UsagePatternTracker (~55줄)
```

### 1.3 공통함수 추출

```python
# jarvis/utils/parsers.py (~50줄)
def parse_title(command: str) -> str | None: ...
def extract_id(command: str) -> int | None: ...
def build_response(success: bool, message: str, **kwargs) -> dict: ...
```

---

## Phase 2: 미구현 기능 완성

### 2.1 NLU 모듈 (신규)

```
jarvis/nlu/
├── __init__.py
├── parser.py             # 자연어 파싱 (~80줄) TDD✓
├── intent.py             # 의도 분류 (~70줄) TDD✓
└── entities.py           # 엔티티 추출 (~60줄) TDD✓
```

### 2.2 GitHub Monitor (신규)

```
jarvis/modules/github/
├── __init__.py
├── types.py              # PR, Issue, Review 타입 (~40줄)
├── client.py             # GitHub API 클라이언트 (~100줄)
├── monitor.py            # PR/Issue 모니터링 (~80줄)
└── notifier.py           # 알림 처리 (~50줄)
```

### 2.3 Habit Tracker (신규)

```
jarvis/modules/habit/
├── __init__.py
├── models.py             # Habit, Streak 모델 (~50줄)
├── tracker.py            # HabitTracker (~80줄)
└── analytics.py          # 스트릭 분석 (~60줄)
```

### 2.4 Booking/Planning (미완성 → 완성)

```
jarvis/automation/executor/
├── booking_handler.py    # 레스토랑/영화/숙박 예약 (~80줄)
└── planning_handler.py   # 데이트/여행 코스 생성 (~80줄)
```

---

## Phase 3: 자율자동 + 랄프 루프 (Task #25)

### 3.1 Agent 아키텍처

```
jarvis/agents/
├── __init__.py
├── base.py               # BaseAgent 추상 클래스 (~50줄)
├── ralph_loop.py         # Writer-Reviewer Loop (~80줄)
├── autonomous.py         # 자율 실행 에이전트 (~100줄)
└── coordinator.py        # 에이전트 조율 (~80줄)
```

### 3.2 Ralph Loop 핵심 로직

```python
class RalphLoop:
    """4-agent parallel review pattern"""
    async def execute(self, task: Task) -> Result:
        draft = await self.writer.generate(task)
        reviews = await asyncio.gather(*[
            r.review(draft) for r in self.reviewers
        ])
        while not all(r.approved for r in reviews):
            draft = await self.writer.revise(draft, reviews)
            reviews = await asyncio.gather(...)
        return draft
```

### 3.3 Autonomous Agent (Task #21)

```python
class AutonomousAgent:
    """File change detection + auto-fix"""
    analyzers = {
        'frontend': FrontendAnalyzer(),
        'backend': BackendAnalyzer(),
        'server': ServerAnalyzer(),
        'api': APIAnalyzer(),
        'other': OtherAnalyzer()
    }
```

---

## Phase 4: 검증 계획

### 테스트 전략

| 대상 | 방식 | 커버리지 |
|-----|------|---------|
| utils/, nlu/ | TDD 필수 | 90%+ |
| agents/, modules/ | TDD 권장 | 80%+ |
| 전체 워크플로우 | E2E | 주요 플로우 |

### 성공 기준

- [x] 파일당 줄 수: 80~100줄 이내
- [ ] 단위 테스트 통과율: 100%
- [ ] 코드 커버리지: 80%+
- [ ] mypy strict 통과
- [ ] ruff check 통과

### 검증 명령어

```bash
pytest jarvis/tests/ -v --cov=jarvis
mypy jarvis/ --strict
ruff check jarvis/
```

---

## 구현 순서

| Week | 작업 | 파일 수 |
|------|------|--------|
| 1 | Phase 1: 리팩토링 | ~20개 분할 |
| 2 | Phase 2: NLU + Ralph Loop | ~8개 신규 |
| 3 | Phase 2: GitHub + Habit | ~8개 신규 |
| 4 | Phase 3: 자율자동 + 통합 | ~5개 신규 |

---

## Critical Files

```
~/.claude/jarvis/
├── automation/task_executor.py  # 🔴 최우선 분할
├── memory/manager.py            # 🔴 분할 필요
├── JARVIS-SPEC.md              # 📋 요구사항 참조
├── daemon.py                   # Ralph Loop 통합 지점
└── memory/ml_predictor.py      # 자율 실행 활용
```

---

## 최종 폴더 구조

```
jarvis/
├── __init__.py              # barrel export
├── core/
│   ├── types.py             # 공통 타입 (30줄)
│   ├── constants.py         # 상수 (20줄)
│   └── config.py            # 설정 (50줄)
├── utils/
│   ├── parsers.py           # 파싱 유틸 (50줄)
│   └── validators.py        # 검증 유틸 (40줄)
├── nlu/
│   ├── parser.py            # NLU 파서 (80줄)
│   ├── intent.py            # 의도 분류 (70줄)
│   └── entities.py          # 엔티티 추출 (60줄)
├── memory/
│   ├── db.py                # DB 연결 (40줄)
│   └── models/              # 6개 모델 파일
├── automation/
│   ├── executor/            # 8개 핸들러 파일
│   └── browser/             # 2개 자동화 파일
├── agents/
│   ├── ralph_loop.py        # W-R 루프 (80줄)
│   ├── autonomous.py        # 자율 실행 (100줄)
│   └── coordinator.py       # 조율 (80줄)
├── modules/
│   ├── github/              # 4개 파일
│   ├── habit/               # 3개 파일
│   └── health/              # 6개 파일 (workout+diet)
└── tests/
    ├── unit/                # TDD 테스트
    ├── integration/         # 통합 테스트
    └── e2e/                 # E2E 테스트
```

---

**META**
- Plan ID: mellow-leaping-sketch
- Created: 2026-02-03
- Task: JARVIS 자동화 워크플로우 + 코드 구조화 지침 테스트
