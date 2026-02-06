# Client Work Tracker

클라이언트별 작업 시간 및 청구 관리

## 사용법

```python
from modules.client import ClientTracker

tracker = ClientTracker()

# 클라이언트 추가
client_id = tracker.add_client("Acme Corp", "Website Redesign")

# 작업 기록
tracker.log_work(client_id, 5.5, "프론트엔드 개발", hourly_rate=100.0)
tracker.log_work(client_id, 3.0, "백엔드 개발", hourly_rate=120.0)

# 작업 요약
summary = tracker.get_summary(client_id)
print(f"총 시간: {summary['total_hours']}h")
print(f"총 금액: ${summary['total_amount']}")

# 월별 인보이스 데이터
logs = tracker.get_invoice_data(client_id, "2026-02")
for log in logs:
    print(f"{log.date}: {log.hours}h - {log.description}")
```

## 파일 구조

- `types.py`: Client, WorkLog 데이터 타입
- `db.py`: SQLite DB 관리
- `tracker.py`: 메인 트래커 클래스
- `test_client_tracker.py`: 테스트
