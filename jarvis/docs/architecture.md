# JARVIS 아키텍처

> 시스템 설계 및 모듈 구조

---

## 시스템 레이어

```
┌─────────────────────────────────────┐
│ UI Layer (자연어 입력)               │
├─────────────────────────────────────┤
│ NLU (의도 파악)                      │
├─────────────────────────────────────┤
│ Orchestrator (작업 분배)             │
├─────────────────────────────────────┤
│ Modules (기능 실행)                  │
├─────────────────────────────────────┤
│ Memory (SQLite)                      │
└─────────────────────────────────────┘
```

---

## 모듈 목록

| 모듈 | 데이터 | 용도 |
|------|--------|------|
| MemoryManager | 작업 기록, 일정, 태스크 | 작업 연속성 |
| HabitTracker | 습관, 스트릭 | 습관 추적 |
| PTCoach | 운동 기록, 프로그램 | 운동 코칭 |
| DietCoach | 식단, 수분 섭취 | 식단 관리 |
| ProjectMonitor | 빌드/테스트 상태 | CI/CD 모니터링 |
| ClientWorkTracker | 클라이언트 작업 | 외주 프로젝트 관리 |
| GitHubMonitor | PR, 이슈, 리뷰 | GitHub 연동 |
| WeatherMonitor | 날씨 캐시 | 날씨 정보 |

자세한 내용은 [modules.md](modules.md) 참고.

---

## 병렬 처리 전략

**원칙:**
- 독립 작업 → 동시 실행
- 의존 작업 → 순차 실행
- 실패 격리 → 부분 성공 허용

**예시:**
```typescript
// 브리핑 시 병렬 fetch
const [weather, schedule, habits, projects] = await Promise.allSettled([
  fetchWeather(),
  fetchSchedule(),
  fetchHabits(),
  fetchProjects()
]);
```

---

## 데이터베이스 스키마

```sql
-- 작업 기록
CREATE TABLE work_log (
  id INTEGER PRIMARY KEY,
  timestamp DATETIME,
  task TEXT,
  file_path TEXT,
  progress TEXT
);

-- 습관 추적
CREATE TABLE habits (
  id INTEGER PRIMARY KEY,
  name TEXT,
  frequency TEXT,
  streak INTEGER
);

-- 운동 기록
CREATE TABLE workouts (
  id INTEGER PRIMARY KEY,
  date DATE,
  exercises JSONB,
  completed BOOLEAN
);
```

---

## 브라우저 자동화

**Chrome Extension 연동:**
1. 확장 프로그램 설치
2. WebSocket 통신
3. Puppeteer 스크립트 실행

**Use Cases:**
- 레스토랑 예약
- 영화 티켓 구매
- 웹 데이터 스크래핑

---

## 학습 메커니즘

**패턴 분석:**
- 자주 사용하는 명령 패턴
- 선호 시간대/장소
- 성공/실패 피드백

**적용:**
- 제안 우선순위 조정
- 기본값 학습
- 단축 명령 생성

---

**META**
- Version: 2026.02
- Category: Architecture
