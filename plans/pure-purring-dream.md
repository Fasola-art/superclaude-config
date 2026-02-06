# JARVIS 모듈 리팩토링 계획 (J-01, J-05, J-07)

> **생성**: 2026-02-05
> **업데이트**: 2026-02-05 01:40
> **모듈**: MemoryManager, ProjectMonitor, GitHubMonitor

---

## 📊 현황 분석 완료

### 발견사항: 모든 모듈 이미 구현됨!

| 모듈 | 위치 | 줄 수 | 상태 |
|------|------|-------|------|
| **GitHubMonitor** | `modules/github/monitor.py` | 83줄 | ✅ 완성 (기준 내) |
| **ProjectMonitor** | `modules/project/monitor.py` | 93줄 | ✅ 완성 (기준 내) |
| **MemoryManager** | `memory/manager.py` | 197줄 | ❌ **기준 초과** |

### MemoryManager 구조 (197줄)

```python
# 5개 Manager 클래스로 구성
1. WorkSessionManager (작업 세션 관리)
2. TaskManager (작업 관리)
3. CalendarManager (일정 관리)
4. ContextManager (컨텍스트 스냅샷)
5. UsagePatternTracker (사용 패턴 추적)
```

### CLAUDE.md 지침 위반

**Line Limits (STRICT):**
- Logic/Utils: 50~80줄
- API/Server: 80~100줄
- **MemoryManager: 197줄 → 100줄 초과!**

**위반 = 즉시 분할 필수**

---

## 🎯 최종 계획: 통합 테스트 작성

**사용자 선택**: 3개 모듈 통합 테스트

---

## 📝 통합 테스트 설계

### 테스트 파일 구조

```
tests/
└── integration/
    └── test_three_modules.py  (60~80줄)
```

### 시나리오 1: 프로젝트 작업 세션 기록
```python
1. ProjectMonitor로 프로젝트 스캔
2. MemoryManager.WorkSessionManager로 세션 시작
3. 프로젝트 변경사항 감지
4. 세션 종료 및 요약 저장
```

### 시나리오 2: GitHub 활동 추적
```python
1. GitHubMonitor로 PR/Issue 확인
2. MemoryManager.TaskManager로 TODO 추가
3. PR 리뷰 완료 후 TaskManager.complete_task()
```

### 시나리오 3: 전체 워크플로우
```python
1. ProjectMonitor.scan_project()
2. WorkSessionManager.start_session()
3. GitHubMonitor.check_for_updates()
4. 변경사항 발생
5. WorkSessionManager.end_session()
6. ContextManager.save_context() (remember 기능)
```

---

## 🔧 구현 세부사항

### 파일: `tests/integration/test_three_modules.py`

**Import 구조:**
```python
from modules.github import GitHubMonitor, GitHubClient
from modules.project import ProjectMonitor
from memory.manager import (
    WorkSessionManager,
    TaskManager,
    ContextManager
)
```

**테스트 함수 (3개):**
1. `test_project_session_workflow()` (15~20줄)
2. `test_github_task_integration()` (15~20줄)
3. `test_full_workflow()` (20~30줄)

**Helper 함수:**
- `setup_test_project()`: 임시 프로젝트 생성
- `cleanup_db()`: 테스트 DB 초기화

---

## ✅ 검증 계획

### 1. 단위 테스트 실행
```bash
python3 tests/integration/test_three_modules.py
```

### 2. 통합 확인 항목
- [ ] ProjectMonitor 스캔 성공
- [ ] MemoryManager DB 연결 성공
- [ ] GitHubMonitor API 호출 성공 (MCP 사용)
- [ ] 3개 모듈 데이터 흐름 정상

### 3. 에러 처리 확인
- [ ] DB 초기화 실패 시 graceful fallback
- [ ] GitHub API 실패 시 계속 진행
- [ ] ProjectMonitor 경로 없음 에러 핸들링

---

## 📂 핵심 파일

### 수정할 파일
- **생성**: `tests/integration/test_three_modules.py` (~70줄)

### 참조할 파일
- `modules/github/test_monitor.py` (테스트 패턴)
- `modules/project/test_monitor.py` (테스트 패턴)
- `memory/manager.py` (Manager 클래스)
- `memory/db.py` (DB 초기화)

---

## 🚀 실행 순서

1. DB 초기화: `memory.db.init_database()`
2. 테스트 실행: `pytest tests/integration/test_three_modules.py -v`
3. 결과 확인: 3개 테스트 모두 PASS

---

## 📌 주의사항

### CLAUDE.md 지침 준수
- 테스트 파일: 60~80줄 목표
- 함수별 단일 책임 원칙
- 명확한 AAA (Arrange-Act-Assert) 패턴

### 실제 API 호출 최소화
- GitHub API: Mock 또는 제한적 호출
- ProjectMonitor: 임시 디렉토리 사용
- MemoryManager: 별도 테스트 DB 사용
