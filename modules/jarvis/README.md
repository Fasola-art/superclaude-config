# Jarvis - AI Personal Assistant Module

로컬 메모리 기반 개인 비서 모듈

## Features

- **자연어 이해 (NLU)**: 한국어/영어 명령 파싱
- **작업 관리**: 우선순위, 태그, 기한 관리
- **일정 관리**: 캘린더 이벤트 관리
- **컨텍스트 추적**: 대화 및 작업 히스토리
- **GitHub 통합**: 이슈/PR 모니터링 (준비 중)

## Installation

```bash
cd ~/.claude/modules/jarvis
pip install -r requirements.txt  # (필요시)
```

## Database Setup

```bash
cd schema
cat core.sql tasks.sql tracking.sql extended.sql | sqlite3 ../jarvis.db
```

## Usage

### Basic Import

```python
from jarvis import TaskManager, CalendarManager, ContextManager, NLUParser
```

### Task Management

```python
tm = TaskManager()

# 작업 추가
task_id = tm.add_task(
    title="보고서 작성",
    priority=8,
    tags=["work", "urgent"]
)

# 작업 조회
tasks = tm.get_tasks(status="todo")

# 작업 완료
tm.complete_task(task_id)
```

### Calendar Management

```python
cm = CalendarManager()

# 일정 추가
event_id = cm.add_event(
    title="팀 회의",
    start_time="2026-02-06 15:00",
    location="회의실 A"
)

# 일정 조회
events = cm.get_events(start_date="2026-02-05")
```

### Natural Language Parsing

```python
parser = NLUParser()

result = parser.parse("내일 오후 3시 미팅 일정 추가")
print(result['intent'])     # "add_event"
print(result['entities'])   # {"date": "2026-02-06", "time": "3:00", ...}
```

## Testing

```bash
# 전체 테스트
python3 tests/test_jarvis.py

# 데모 실행
python3 examples/demo.py
```

## Database Schema

### Core Tables
- `memories`: 사용자 컨텍스트 및 대화 기억
- `projects`: 프로젝트 상태 추적
- `tasks`: 작업 목록 및 상태
- `calendar_events`: 일정 관리
- `context_history`: 대화 컨텍스트 히스토리

### Tracking Tables
- `reminders`: 리마인더
- `habits`: 습관 정의
- `habit_logs`: 습관 실행 기록

### Integration Tables
- `github_events`: GitHub 이슈/PR 캐시

## Project Structure

```
jarvis/
├── jarvis/
│   ├── __init__.py
│   ├── memory.py          # Database managers
│   ├── nlu.py             # Natural language parser
│   └── modules/
│       └── github.py      # GitHub integration
├── schema/
│   ├── core.sql
│   ├── tasks.sql
│   ├── tracking.sql
│   └── extended.sql
├── tests/
│   └── test_jarvis.py
├── examples/
│   └── demo.py
└── README.md
```

## Test Results

```
✅ imports            : PASS
✅ nlu_parser         : PASS
✅ task_manager       : PASS
✅ calendar_manager   : PASS
✅ context_manager    : PASS

Total: 5/5 tests passed
```

## Version

- 0.1.0 (2026-02-05)
