# JARVIS Advanced Features

ML 예측, GitHub 모니터링, 습관 추적 고급 기능

## ML 예측

작업 패턴 학습 및 예측

```python
import sys
sys.path.insert(0, "C:/Users/MSI/.claude/jarvis")

from memory.ml_predictor import get_predictor

predictor = get_predictor()

# 현재 시간 기반 예측
prediction = predictor.predict_work_type()
# {'predicted_work_type': 'code_editing', 'confidence': 75.3, ...}

# 피크 시간대
peaks = predictor.get_peak_hours(work_type='code_editing')
# [14, 15, 16]  # 오후 2-4시

# 주간 패턴
weekly = predictor.get_weekly_pattern()
# {'Monday': {'code_editing': 0.7, 'meeting': 0.3}, ...}
```

### 예측 타입

| work_type | 설명 |
|----------|------|
| code_editing | 코드 작성/수정 |
| code_review | 코드 리뷰 |
| documentation | 문서 작성 |
| meeting | 회의 |
| research | 조사/학습 |

### 출력 예시

```
🤖 ML 예측

📊 현재 예상 작업: code_editing (신뢰도: 78%)

⏰ 피크 시간대 (code_editing)
  • 14:00-16:00 (85% 확률)
  • 10:00-12:00 (72% 확률)

📅 주간 패턴
  월: code_editing (65%), meeting (20%)
  화: code_review (55%), documentation (25%)
  수: code_editing (70%), research (15%)
```

## GitHub 모니터링

PR, Issue, 리뷰 요청 추적

```python
from modules.github import GitHubClient, GitHubMonitor

# 단일 저장소
client = GitHubClient("owner/repo")

# PR 조회
prs = client.get_pull_requests(state="open")
# [{'number': 123, 'title': '...', 'author': '...'}]

# 리뷰 요청
review_requests = client.get_review_requests()
# [{'pr': 123, 'title': '...', 'requested_at': '...'}]

# 여러 저장소 모니터링
monitor = GitHubMonitor(repos=[
    "owner/repo1",
    "owner/repo2"
])

# 알림 확인
notifications = monitor.check_for_updates()
# [{'type': 'review_request', 'repo': '...', 'pr': 123}]

# 내 작업 항목
action_items = monitor.get_my_action_items()
# [{'type': 'pr_review', 'priority': 'high', 'pr': 123}]
```

### 출력 예시

```
🔔 GitHub 알림 (3개)

📝 리뷰 요청 (2개)
  • PR #123: Add authentication (owner/repo1)
  • PR #456: Fix bug (owner/repo2)

🐛 할당된 이슈 (1개)
  • Issue #789: Update docs (owner/repo1)

⚡ 우선순위 작업
  1. PR #123 리뷰 (2일 전 요청)
  2. Issue #789 처리 (마감: 내일)
```

## 습관 추적

일일 습관 관리 및 스트릭 추적

```python
from modules.habit import HabitTracker, HabitAnalytics, HabitFrequency

tracker = HabitTracker()

# 습관 생성
habit_id = tracker.create_habit(
    name="운동",
    frequency=HabitFrequency.DAILY,
    goal_count=1
)

# 완료 기록
tracker.log_completion(habit_id)

# 스트릭 확인
streak = tracker.get_current_streak(habit_id)
# {'current': 7, 'longest': 14}

# 통계
analytics = HabitAnalytics(tracker)
summary = analytics.get_weekly_summary()
# {'completed': 5, 'total': 7, 'rate': 71.4}
```

### Frequency 타입

| 타입 | 설명 |
|------|------|
| DAILY | 매일 |
| WEEKLY | 주 N회 |
| CUSTOM | 사용자 정의 |

### 출력 예시

```
🎯 습관 추적

📊 오늘 (3/5 완료)
  ✅ 운동 (스트릭: 7일)
  ✅ 독서 (스트릭: 3일)
  ✅ 코드 리뷰 (스트릭: 12일)
  ⬜ 블로그 작성
  ⬜ 영어 공부

🔥 최장 스트릭
  • 코드 리뷰: 25일
  • 운동: 14일

📈 주간 완료율: 71% (20/28)
```

## 통합 예시

모든 기능 조합

```python
# 1. 브리핑
tasks = TaskManager.get_today_tasks()
events = CalendarManager.get_today_events()

# 2. ML 예측
predictor = get_predictor()
prediction = predictor.predict_work_type()

# 3. GitHub 확인
monitor = GitHubMonitor(repos=["owner/repo"])
notifications = monitor.check_for_updates()

# 4. 습관 체크
tracker = HabitTracker()
today_habits = tracker.get_today_habits()

# 통합 출력
print(f"""
🌅 JARVIS 브리핑

📋 작업: {len(tasks)}개
📅 일정: {len(events)}개
🤖 예측: {prediction['work_type']} ({prediction['confidence']}%)
🔔 GitHub: {len(notifications)}개 알림
🎯 습관: {len([h for h in today_habits if h['completed']])}/{len(today_habits)} 완료
""")
```

## 자동화 워크플로우

여러 기능 조합한 스마트 워크플로우

### 아침 루틴

```python
# 1. 브리핑
tasks = TaskManager.get_today_tasks()
events = CalendarManager.get_today_events()
habits = HabitTracker().get_today_habits()

# 2. ML 예측
predictor = get_predictor()
prediction = predictor.predict_work_type()

# 3. GitHub 확인
monitor = GitHubMonitor()
notifications = monitor.check_for_updates()

# 4. 날씨
weather = get_weather()

print(f"""
🌅 JARVIS 모닝 브리핑

📋 작업: {len(tasks)}개
📅 일정: {len(events)}개
🎯 습관: {len([h for h in habits if h['completed']])}/{len(habits)}
🤖 예측: {prediction['work_type']} ({prediction['confidence']}%)
🔔 GitHub: {len(notifications)}개
🌤️  날씨: {weather['temp']}°C, {weather['condition']}
""")
```

### 작업 시작 전

```python
# 1. 컨텍스트 복원
context = recall_context()

# 2. 프로젝트 상태
monitor = ProjectMonitor(context['project_path'])
status = monitor.get_status()

# 3. 작업 시간 기록 시작
tracker = TimeTracker()
tracker.start_work(project=context['summary'])

print(f"""
🚀 작업 재개

📝 {context['summary']}
📁 {context['project_path']}
📊 진행률: {status['progress']}%
⏱️  작업 시간 기록 시작
""")
```

### 작업 종료 시

```python
# 1. 컨텍스트 저장
remember_context(
    summary="프로젝트 X 개발",
    project_path=current_path,
    last_file="main.py"
)

# 2. 작업 시간 종료
tracker.stop_work()

# 3. 습관 완료 기록
tracker = HabitTracker()
tracker.log_completion(habit_id)

# 4. 내일 작업 예측
predictor = get_predictor()
tomorrow = predictor.predict_tomorrow_tasks()

print(f"""
✅ 작업 종료

💾 컨텍스트 저장 완료
⏱️  작업 시간: {tracker.get_today_total()}시간
🎯 습관 완료: 3/5
🔮 내일 예측: {tomorrow}
""")
```

---

## Dependencies

```bash
# 필수
pip install scikit-learn watchdog

# GitHub (선택)
pip install PyGithub

# 웹 자동화 (선택)
pip install playwright
playwright install
```

---

## Reference

- 메인: [j.md](j.md)
- 액션: [j-actions.md](j-actions.md)
- 소스: `C:/Users/MSI/.claude/jarvis/modules/`
