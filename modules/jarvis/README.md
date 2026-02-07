# Jarvis - AI Personal Assistant Module

로컬 메모리 기반 개인 비서 모듈

## Features

- **자연어 이해 (NLU)**: 한국어/영어 명령 파싱
- **작업 관리**: 우선순위, 태그, 기한 관리
- **일정 관리**: 캘린더 이벤트 관리
- **컨텍스트 추적**: 대화 및 작업 히스토리
- **장소 추천/예약**: Brave Search 기반 맛집/카페/숙소 검색, 즐겨찾기, 예약 관리
- **GitHub 통합**: 이슈/PR 모니터링 (준비 중)

## Installation

```bash
cd ~/.claude/modules/jarvis
pip install -r requirements.txt  # (필요시)
```

## Database Setup

```bash
cd schema
cat core.sql tasks.sql tracking.sql extended.sql places.sql | sqlite3 ../jarvis.db
```

## Usage

### Basic Import

```python
from jarvis import TaskManager, CalendarManager, ContextManager, NLUParser, PlaceSearcher, PlaceManager
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

### Place Search & Booking

```python
searcher = PlaceSearcher()
results = searcher.search("대구 인터불고 호텔")
bookings = searcher.search_for_booking("인터불고 호텔 대구")

pm = PlaceManager()
place_id = pm.save_place({"name": "인터불고", "category": "accommodation", "google_place_id": "id1"})
pm.add_reservation(place_id, "주말 숙박", "2026-02-14", "15:00", party_size=2)
pm.get_reservations()  # 예약 목록 조회
```

### Natural Language Parsing

```python
parser = NLUParser()

result = parser.parse("내일 오후 3시 미팅 일정 추가")
print(result['intent'])     # "add_event"
print(result['entities'])   # {"date": "2026-02-06", "time": "3:00", ...}

result = parser.parse("제주도 카페 추천")
print(result['intent'])     # "search_place"
print(result['entities'])   # {"place_category": "cafe", "region": "제주도", ...}
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

### Places Tables
- `places`: 장소 즐겨찾기 (맛집/카페/숙소/관광지)
- `reservations`: 예약 추적

### Integration Tables
- `github_events`: GitHub 이슈/PR 캐시

## Project Structure

```
jarvis/
├── jarvis/
│   ├── __init__.py
│   ├── memory.py          # Database managers
│   ├── nlu.py             # Natural language parser
│   ├── nlu_patterns.py    # NLU intent/entity patterns
│   └── modules/
│       ├── github.py      # GitHub integration
│       ├── places.py      # Place search (Brave API)
│       └── place_manager.py # Bookmark & reservation DB
├── schema/
│   ├── core.sql
│   ├── tasks.sql
│   ├── tracking.sql
│   ├── extended.sql
│   └── places.sql
├── tests/
│   ├── test_jarvis.py
│   └── test_places.py
├── examples/
│   └── demo.py
└── README.md
```

## Test Results

```
test_jarvis.py:  5/5  passed (imports, nlu, task, calendar, context)
test_places.py:  6/6  passed (imports, save/get, reservation, visit, nlu, bookmark)
Total: 11/11
```

## Version

- 0.2.0 (2026-02-07): 장소 추천/예약 기능, NLU 패턴 분리, Brave Search 연동
- 0.1.0 (2026-02-05): 초기 릴리스
