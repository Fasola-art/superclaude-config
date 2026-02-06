# JARVIS Actions - 확장 기능

## 새로운 기능

### Book (예약 관리)
- `book_reservation()`: 식당/미용실/병원 등 예약 생성
- `get_bookings()`: 예약 목록 조회 (서비스/상태 필터)
- `cancel_booking()`: 예약 취소

**사용 예시:**
```python
from actions import book_reservation, get_bookings

# 예약 생성
booking_id = book_reservation(
    service="식당",
    datetime_str="2026-02-10T19:00:00",
    details="4인 예약",
    location="강남구 XX 레스토랑"
)

# 예약 조회
bookings = get_bookings(service="식당", status="pending")
```

### Plan (계획 관리)
- `create_plan()`: 여행/이벤트 계획 생성
- `add_plan_item()`: 계획에 세부 아이템 추가
- `get_plan()`: 계획 상세 조회

**사용 예시:**
```python
from actions import create_plan, add_plan_item, get_plan

# 계획 생성
plan_id = create_plan(
    event_name="제주도 여행",
    date="2026-03-15",
    description="3박 4일"
)

# 아이템 추가
add_plan_item(plan_id, "공항 도착", "09:00")
add_plan_item(plan_id, "호텔 체크인", "15:00")

# 조회
plan = get_plan(plan_id)
```

### Search (통합 검색)
- `search_web()`: 웹 검색 (Google)
- `search_local()`: 로컬 파일 검색 (Spotlight)
- `search_memory()`: JARVIS 메모리 검색
- `search_all()`: 통합 검색

**사용 예시:**
```python
from actions import search_local, search_memory, search_all

# 로컬 파일 검색
files = search_local("jarvis", "~/.claude")

# 메모리 검색
memories = search_memory("trading")

# 통합 검색
results = search_all("project", "~/workspace")
```

## 테스트
```bash
python3 actions/test_book.py
python3 actions/test_plan.py
python3 actions/test_search.py
```

## 파일 구조
```
actions/
├── book.py           # 예약 관리 (100줄)
├── plan.py           # 계획 관리 (89줄)
├── search.py         # 통합 검색 (97줄)
├── test_book.py
├── test_plan.py
└── test_search.py
```
