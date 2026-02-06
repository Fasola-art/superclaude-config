# Hook System Details

> 이벤트 타입별 훅 상세

## Hook Event Types

| Event | Trigger Point | Purpose | Example |
|-------|---------------|---------|---------|
| `UserPromptSubmit` | 프롬프트 제출 후 | 키워드 감지, 모드 설정 | keyword-detector |
| `PreToolUse` | 도구 실행 전 | 권한 확인, W-R 설정 | writer-reviewer-hook |
| `PostToolUse` | 도구 실행 후 | 포맷팅, 테스팅, 품질 검사 | format-python |
| `Stop` | 세션 종료 | 세션 저장, 상태 기록 | session-saver |

---

## UserPromptSubmit (7)

| Hook | File | Function |
|------|------|----------|
| JARVIS Briefing | `jarvis-morning-briefing.py` | 시스템 상태 브리핑 |
| Keyword Detection | `keyword-detector.py` | Vibe/Mode 키워드 감지 |
| Context Cleanup | `context-cleaner.py` | 자동 컨텍스트 압축 |
| Plan Mode Analysis | `plan-mode-analyzer.py` | PRD 감지, 플랜 모드 진입 |
| Todo Continuation | `todo-continuation.py` | 이전 작업 재개 |
| Language Enforcement | `language-enforcer.py` | 한국어 응답 강제 |
| Persona Activation | `persona-activator.py` | 자동 페르소나 선택 |

## PreToolUse (1)

| Hook | File | Function |
|------|------|----------|
| Writer-Reviewer | `writer-reviewer-hook.py` | 4-agent 품질 리뷰 |

## PostToolUse (12)

| Hook | Matcher | Function |
|------|---------|----------|
| Task Tracking | `Edit\|Write\|...` | 작업 기록 |
| Task Completion | `TodoWrite\|TaskUpdate` | 완료 알림 |
| Session Snapshot | `Edit\|Write\|MultiEdit` | 변경 기록 |
| Python Format | `Edit\|Write\|MultiEdit` | ruff 자동 포맷 |
| JS/TS Format | `Edit\|Write\|MultiEdit` | prettier 자동 포맷 |
| Test Execution | `Edit\|Write\|MultiEdit` | 관련 테스트 자동 실행 |
| Quality Gate | `Edit\|Write\|MultiEdit` | 8단계 검증 |
| Pattern Tracking | `Edit\|Write\|MultiEdit` | 코딩 패턴 학습 |
| Background Notification | `Bash` | 백그라운드 작업 완료 알림 |
| Auto Error Resolution | `Bash` | Error KB 기반 자동 수정 |
| Ralph Loop Checker | `Task` | 무한 루프 감지 |

## Stop (1)

| Hook | File | Function |
|------|------|----------|
| Session Save | `session-saver.py` | 세션 상태 저장 |

---

## 핵심 훅 코드

### quality-gate.py

```python
# 8단계 품질 게이트 (가중치 합 = 1.0)
QUALITY_GATES = [
    {"name": "Syntax", "cmd": "check_syntax", "weight": 0.15},
    {"name": "Type", "cmd": "check_types", "weight": 0.15},
    {"name": "Lint", "cmd": "check_lint", "weight": 0.10},
    {"name": "Security", "cmd": "check_security", "weight": 0.20},  # 최우선
    {"name": "Test", "cmd": "run_tests", "weight": 0.15},
    {"name": "Performance", "cmd": "check_perf", "weight": 0.10},
    {"name": "Docs", "cmd": "check_docs", "weight": 0.05},
    {"name": "Integration", "cmd": "check_integration", "weight": 0.10},
]
```

### ralph-loop-checker.py

```python
MAX_CONSECUTIVE_FAILURES = 5  # 최대 연속 실패 횟수
TIME_WINDOW_MINUTES = 5       # 시간 윈도우

# 동작:
# - 5분 내 5회 연속 실패 → 🛑 경고
# - 3회+ 실패 → ⚠️ 조기 경고
# - 성공 시 → 상태 리셋
```

---

**Related**: [system-architecture.md](system-architecture.md), [vibe-mode-keywords.md](vibe-mode-keywords.md)
