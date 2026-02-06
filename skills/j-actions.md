# JARVIS Actions

자율 실행, 컨텍스트 관리, 생활 도우미, 비즈니스 기능

## remember - 컨텍스트 저장

작업 내용을 저장하여 나중에 복원

```python
import sys
sys.path.insert(0, "/Users/reim/.claude/jarvis")

from actions.remember import remember_context

# 기본 사용
remember_context("프로젝트 X의 인증 로직 수정 중")

# 상세 정보 포함
remember_context(
    summary="프로젝트 X 인증 로직 수정",
    project_path="/path/to/project",
    last_file="auth/login.py",
    last_action="editing"
)
```

### 출력 예시

```
💾 컨텍스트 저장 완료

📝 요약: 프로젝트 X 인증 로직 수정
📁 프로젝트: /path/to/project
📄 마지막 파일: auth/login.py
🔧 작업: editing
⏰ 저장 시각: 2026-02-05 14:23:15
```

## recall - 컨텍스트 복원

저장된 작업 내용 복원

```python
from actions.recall import recall_context

# 마지막 컨텍스트 복원
context = recall_context()

# 출력
print(f"📝 {context['summary']}")
print(f"📁 {context['project_path']}")
print(f"📄 {context['last_file']}")
```

### 출력 예시

```
🔄 컨텍스트 복원

📝 프로젝트 X 인증 로직 수정
📁 /path/to/project
📄 auth/login.py
🔧 editing
⏰ 2시간 전 (2026-02-05 12:30)

💡 다음 작업: auth/login.py 파일 열기
```

## do - 자율 실행

명령을 분석하고 자율적으로 실행

```python
from actions.do import execute_autonomous

# 기본 실행
result = execute_autonomous("오늘 마감인 작업 확인")

# 출력
if result['success']:
    print(f"✅ {result['summary']}")
    print(result['output'])
```

### 지원하는 명령

| 명령 예시 | 실행 내용 |
|----------|----------|
| "오늘 작업 확인" | TaskManager.get_today_tasks() |
| "내일 일정 추가: 미팅" | CalendarManager.add_event() |
| "마지막 작업 복원" | recall_context() |
| "프로젝트 상태" | ProjectMonitor.get_status() |

### 출력 예시

```
🤖 명령 실행 중...

📋 분석: 오늘 마감 작업 조회
⚙️  실행: TaskManager.get_today_tasks()

✅ 완료

오늘 마감 작업 2개:
1. [!] 프로젝트 리뷰
2. [!] 문서 제출
```

## project status - 프로젝트 상태

진행 중인 프로젝트 상태 확인

```python
import sys
sys.path.insert(0, "/Users/reim/.claude/jarvis")

from modules.project.monitor import ProjectMonitor

monitor = ProjectMonitor(project_path="/path/to/project")

# 상태 조회
status = monitor.get_status()
print(f"📊 진행률: {status['progress']}%")
print(f"📝 작업: {status['completed_tasks']}/{status['total_tasks']}")

# Git 상태
git_status = monitor.get_git_status()
print(f"🌿 브랜치: {git_status['branch']}")
print(f"📤 커밋: {git_status['unpushed_commits']}개 미푸시")

# 최근 활동
activity = monitor.get_recent_activity(days=7)
```

### 출력 예시

```
📊 프로젝트 상태: jarvis-v2

🎯 진행률: 75% (15/20 작업 완료)

🌿 Git 상태
  • 브랜치: feature/auto-actions
  • 변경: 3개 파일 수정
  • 커밋: 2개 미푸시

📅 최근 7일 활동
  • 커밋: 12개
  • 파일 수정: 28개
  • 가장 활발한 시간: 14:00-16:00

⏰ 마지막 업데이트: 30분 전
```

## Integration Example

여러 명령 조합

```python
# 1. 현재 작업 저장
remember_context("인증 API 개발 중")

# 2. 작업 추가
TaskManager.add_task("인증 API 테스트 작성", priority=2)

# 3. 프로젝트 상태 확인
monitor = ProjectMonitor()
status = monitor.get_status()

# 4. 나중에 복원
context = recall_context()
print(f"이어서 작업: {context['summary']}")
```

## 생활 도우미 (NEW)

### book - 예약

```python
from actions.book import make_reservation

# 식당 예약
make_reservation(
    place="강남 맛집",
    date="2026-02-10 19:00",
    party_size=4
)
```

### plan - 계획 생성

```python
from actions.plan import create_plan

# 여행 계획
plan = create_plan(
    topic="제주도 3박 4일",
    preferences=["자연", "맛집", "호텔"]
)
```

### search - 통합 검색

```python
from actions.search import unified_search

# 작업, 일정, 메모 통합 검색
results = unified_search("프로젝트 X")
```

### weather - 날씨

```python
from actions.weather import get_weather

# 오늘 날씨
weather = get_weather()
print(f"{weather['temp']}°C, {weather['condition']}")
```

---

## 비즈니스 (NEW)

### client - 클라이언트 관리

```python
from modules.business import ClientManager

manager = ClientManager()

# 추가
client_id = manager.add_client(
    name="회사 A",
    contact="contact@company.com"
)

# 목록
clients = manager.get_all_clients()
```

### work log - 작업 시간 기록

```python
from modules.business import TimeTracker

tracker = TimeTracker()

# 시작
tracker.start_work(project="프로젝트 X")

# 종료
tracker.stop_work()  # 자동으로 시간 계산
```

---

## Reference

- 구현: `~/.claude/jarvis/actions/`
- 메인: [j.md](j.md)
- 고급: [j-advanced.md](j-advanced.md)
