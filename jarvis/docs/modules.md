# JARVIS 모듈 상세

> 각 모듈의 구현 세부사항

---

## MemoryManager

**역할**: 작업 연속성 관리

**데이터:**
- 작업 기록 (timestamp, task, file_path, progress)
- 일정 (schedule)
- 태스크 (tasks with priority)

**주요 메서드:**
```typescript
async getRecentWork(days: number): Promise<WorkLog[]>
async saveWorkLog(task: string, filePath: string): Promise<void>
async getNextTask(): Promise<Task | null>
```

---

## HabitTracker

**역할**: 습관 형성 지원

**데이터:**
- 습관 목록 (name, frequency, target)
- 체크 기록 (date, completed)
- 스트릭 (연속 달성 일수)

**주요 메서드:**
```typescript
async addHabit(name: string, frequency: string): Promise<void>
async checkHabit(habitId: number): Promise<void>
async getStreak(habitId: number): Promise<number>
```

---

## PTCoach

**역할**: 운동 프로그램 관리

**데이터:**
- 운동 프로그램 (exercises with sets/reps)
- 완료 기록 (date, exercises, completed)
- 진행률 (weekly/monthly stats)

**주요 메서드:**
```typescript
async getTodayWorkout(): Promise<Workout>
async logWorkout(exercises: Exercise[]): Promise<void>
async getProgress(): Promise<Stats>
```

---

## DietCoach

**역할**: 식단 및 영양 관리

**데이터:**
- 식단 계획 (meals with nutrition)
- 섭취 기록 (food, calories, macros)
- 수분 섭취 (water intake)

**주요 메서드:**
```typescript
async getDailyPlan(): Promise<MealPlan>
async logMeal(food: string, calories: number): Promise<void>
async logWater(ml: number): Promise<void>
```

---

## ProjectMonitor

**역할**: 프로젝트 빌드/테스트 모니터링

**데이터:**
- 프로젝트 목록 (name, path, type)
- 빌드 상태 (status, timestamp, logs)
- 테스트 결과 (passed, failed, skipped)

**주요 메서드:**
```typescript
async getProjectStatus(name: string): Promise<Status>
async runTests(projectPath: string): Promise<TestResult>
async watchProjects(): Promise<void>
```

---

## ClientWorkTracker

**역할**: 클라이언트 프로젝트 관리

**동작:**
1. 키워드 감지 (외부인 문서 분석 요청)
2. 프로젝트 폴더 생성 (`~/projects/client-{name}/`)
3. 6개 문서 병렬 생성:
   - research-insights.md
   - competitive-analysis.md
   - user-personas.md
   - feature-requirements.md
   - technical-architecture.md
   - implementation-roadmap.md

**주요 메서드:**
```typescript
async detectClientRequest(text: string): Promise<boolean>
async createProjectStructure(clientName: string): Promise<void>
async generateDocuments(context: string): Promise<void>
```

---

## GitHubMonitor

**역할**: GitHub 활동 모니터링

**데이터:**
- PR 목록 (open, closed, merged)
- 이슈 목록 (assigned, mentioned)
- 리뷰 요청 (pending, approved, changes_requested)
- CI 상태 (success, failure, pending)

**주요 메서드:**
```typescript
async getPullRequests(): Promise<PR[]>
async getIssues(): Promise<Issue[]>
async getReviewRequests(): Promise<Review[]>
async monitorCI(): Promise<void>
```

---

## WeatherMonitor

**역할**: 날씨 정보 제공

**데이터:**
- 현재 날씨 (temp, feels_like, description)
- 예보 (hourly, daily)
- 옷차림 추천 (based on temp/weather)

**주요 메서드:**
```typescript
async getCurrentWeather(): Promise<Weather>
async getForecast(hours: number): Promise<Forecast[]>
async getClothingAdvice(): Promise<string>
```

---

**META**
- Version: 2026.02
- Category: Module Reference
