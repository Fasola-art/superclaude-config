# JARVIS HabitTracker

습관 추적 및 분석 모듈

## 기능

| 기능 | 메서드 | 설명 |
|------|--------|------|
| 습관 추가 | `add_habit(name, frequency)` | 새 습관 등록 |
| 완료 기록 | `complete_habit(habit_id, notes)` | 습관 완료 체크 |
| 연속 기록 | `get_streak(habit_id)` | 현재/최장 연속일 |
| 오늘 할 일 | `get_today_habits()` | 오늘 해야 할 습관 목록 |
| 통계 | `get_habit_stats(habit_id)` | 7일/30일 완료율, 요일별 분석 |
| 주간 요약 | `get_weekly_summary()` | 전체 완료율, 최고/주의 습관 |
| 메시지 | `get_motivation_message(habit_id)` | 동기부여 메시지 |

## 사용법

```python
from modules.habit import HabitTracker, HabitAnalytics, HabitSummary, HabitFrequency

# 초기화
tracker = HabitTracker()
analytics = HabitAnalytics(tracker)
summary = HabitSummary(tracker)

# 습관 추가
habit_id = tracker.add_habit("독서", "매일 30분", HabitFrequency.DAILY)

# 완료 기록
tracker.complete_habit(habit_id, notes="30분 소설 읽기")

# 연속 기록 확인
streak = tracker.get_streak(habit_id)
print(f"현재 {streak.current}일, 최장 {streak.longest}일")

# 통계
stats = analytics.get_habit_stats(habit_id)
print(f"7일 완료율: {stats.completion_rate_7d}%")

# 동기부여 메시지
msg = summary.get_motivation_message(habit_id)
print(msg)
```

## 파일 구조

```
habit/
├── __init__.py          # 모듈 export
├── models.py            # 데이터 모델 (82줄)
├── db_schema.py         # DB 스키마 (43줄)
├── db_queries.py        # DB CRUD (90줄)
├── tracker.py           # 추적 로직 (92줄)
├── analytics_core.py    # 통계 분석 (93줄)
├── analytics_summary.py # 요약/메시지 (79줄)
├── test_habit_tracker.py # 통합 테스트 (87줄)
└── demo.py              # 데모 스크립트 (80줄)
```

## 테스트

```bash
# 통합 테스트
python3 modules/habit/test_habit_tracker.py

# 데모 실행
python3 modules/habit/demo.py
```

## DB 테이블

### habits
- `id`: PK
- `name`: 습관명
- `description`: 설명
- `frequency`: DAILY/WEEKLY/WEEKDAYS/CUSTOM
- `target_days`: 요일 (0=월, 6=일)
- `active`: 활성 여부

### habit_logs
- `id`: PK
- `habit_id`: FK → habits
- `completed_at`: 완료 시각
- `notes`: 메모
