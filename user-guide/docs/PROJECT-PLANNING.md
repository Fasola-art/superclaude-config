# 프로젝트 플래닝 가이드

> 3-Step 워크플로우 상세

---

## 태스크 분해 구조

```
Section (섹션)          # 독립 기능 영역
└── Milestone (마일스톤)  # 1-2시간 작업
    └── Task (태스크)     # 15-30분 작업
        └── Step (스텝)   # 단일 동작
```

---

## 병렬 분류 규칙 (SSOT)

### ✅ 병렬 가능
- 다른 파일 수정 (LoginForm vs SignupForm)
- 같은 컴포넌트, 다른 기능

### ❌ 순차 필요
- types.ts → 해당 타입 사용 (의존성)
- 같은 파일 동시 수정 (충돌)

---

## Step 1: 깊은 분석

### 5 Layer 분석

```yaml
business:
  - 목적: 왜 이 프로젝트를 하는가?
  - 타겟: 누구를 위한 것인가?
  - 경쟁사: 기존 대안은?
  - 수익모델: 어떻게 수익을 낼 것인가?

functional:
  - 기능: 무엇을 만드는가?
  - 의존성: 어떤 기능이 선행되어야 하는가?
  - 우선순위: P0/P1/P2 분류
  - 숨겨진 요구사항: 암묵적으로 필요한 것

technical:
  - 스택: 어떤 기술을 사용할 것인가?
  - 아키텍처: 시스템 구조는?
  - 확장성: 성장에 어떻게 대응할 것인가?
  - 외부 의존성: 외부 서비스/API는?

ux:
  - 플로우: 사용자 여정은?
  - 화면: 어떤 화면이 필요한가?
  - 인터랙션: 어떻게 상호작용하는가?

risk:
  - 기술 리스크: 기술적 어려움은?
  - 일정 리스크: 지연 가능성은?
  - 누락 리스크: 놓친 것이 있는가?
```

### 질문 우선순위

| 우선순위 | 표시 | 설명 |
|---------|------|------|
| 🔴 반드시 확인 | High | 답변 없이 진행 불가 |
| 🟡 확인 필요 | Medium | 가정 후 진행 가능 |
| ⚪ 나중에 결정 | Low | 구현 중 결정 가능 |

---

## Step 2: 청사진 (BLUEPRINT.md)

### Part 1: 무엇을 만드는가

```markdown
## 🖥️ 화면 구성도

┌─────────────────────────────────────┐
│           Header                    │
├─────────────────────────────────────┤
│  Sidebar  │        Main Content     │
│           │                         │
│  - Menu1  │   [Component Area]     │
│  - Menu2  │                         │
│  - Menu3  │                         │
└───────────┴─────────────────────────┘

## 🗺️ 사용자 여정

1. 회원가입 → 이메일 인증 → 온보딩
2. 로그인 → 대시보드 → 기능 사용
3. 설정 → 프로필 수정 → 저장

## 🗄️ 데이터 구조

User
├── id: string (PK)
├── email: string (unique)
├── name: string
└── createdAt: timestamp

Post
├── id: string (PK)
├── userId: string (FK → User)
├── title: string
├── content: text
└── publishedAt: timestamp
```

### Part 2: 어떻게 만드는가

```markdown
## 🏗️ 섹션 분할

### Section 1: 인증 시스템 [P1]
- Milestone 1.1: 회원가입
  - Task 1.1.1: 회원가입 폼 UI
  - Task 1.1.2: 이메일 중복 검사 API
  - Task 1.1.3: 회원가입 로직
- Milestone 1.2: 로그인
  - Task 1.2.1: 로그인 폼 UI
  - Task 1.2.2: JWT 토큰 발급

### Section 2: 대시보드 [P1]
- Milestone 2.1: 레이아웃
  - Task 2.1.1: Header 컴포넌트
  - Task 2.1.2: Sidebar 컴포넌트 [P1]
  - Task 2.1.3: Main 레이아웃 [P1]

## ⚡ 병렬 그룹

[P1] Task 2.1.2, Task 2.1.3 (동시 실행 가능)

## 📊 실행 요약

| 항목 | 수량 |
|------|------|
| 총 섹션 | 5개 |
| 총 마일스톤 | 15개 |
| 총 태스크 | 45개 |
| 예상 병렬 그룹 | 12개 |
```

---

## Step 3: 적응형 병렬 실행

### 실행 알고리즘

```python
concurrent = 10  # 초기값 (M2 Ultra)
success_streak = 0

while tasks_remaining:
    # 병렬 실행
    results = execute_parallel(next_tasks[:concurrent])

    for result in results:
        if result.success:
            success_streak += 1
            if success_streak >= 3:
                concurrent = min(concurrent + 5, 24)
                success_streak = 0
        else:
            concurrent = max(concurrent - 3, 3)
            success_streak = 0

    update_goals_json()
    add_unblocked_tasks_to_queue()
```

### 실행 로그 예시

```
[10:00] 시작: 10개 동시 실행
[10:05] T01-T10 완료 (10/10 성공)
[10:05] 스케일업: 10 → 15개
[10:10] T11-T25 완료 (14/15 성공, 1 실패)
[10:10] 스케일다운: 15 → 12개
[10:15] T26-T37 완료 (12/12 성공)
[10:15] 스케일업: 12 → 17개
...
[11:30] 완료: 총 45개 태스크
```

---

## 완료 보고서 형식

```markdown
# 프로젝트 완료 보고서

## 📊 실행 요약
- 총 섹션: 5개
- 총 태스크: 45개
- 최대 동시 실행: 20개
- 총 소요 시간: 90분

## ✅ 결과물
| 섹션 | 상태 | 완료율 | 주요 파일 |
|------|------|--------|-----------|
| 인증 | ✅ 완료 | 100% | src/auth/* |
| 대시보드 | ✅ 완료 | 100% | src/dashboard/* |
| API | ✅ 완료 | 100% | src/api/* |

## ⚠️ 미완료 항목
- 없음

## 🚀 실행 방법
\`\`\`bash
npm install
npm run dev
\`\`\`

## 🧪 테스트 방법
\`\`\`bash
npm run test
npm run test:e2e
\`\`\`
```
