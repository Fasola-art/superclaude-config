# Plan Mode - SuperClaude v4.1

> Strategic Planning System - 전략적 계획 수립 워크플로우

---

## Plan Mode Use Cases

| Case | Input | Focus | Analysis Depth |
|------|-------|-------|----------------|
| **PRD Creation** | 아이디어/컨셉 | 사업성 + 기술 분석 | --think-hard |
| **Project Planning** | PRD document | What & Why | --think-hard |
| **Feature Implementation** | Feature description | How | --think |
| **Problem Solving** | Error/Bug/Incident | Why & How to fix | --think |
| **Research** | Problem/Topic/Need | What if & Why not | --think-hard |

---

## 진입 조건

| 조건 | 동작 |
|------|------|
| PRD 문서 수신 | 플랜 모드 자동 진입 |
| "프로젝트 만들어줘" 요청 | 플랜 모드 진입 |
| 핵심 기능 3개 이상 | 플랜 모드 진입 |
| 빠르게/qk 키워드 | /project-plan 즉시 실행 |

---

## Case 1: PRD Creation (아이디어 → PRD 문서)

### 스킬 호출
- **명령어**: `/prd-create`
- **스킬 가이드**: `~/.claude/skills/prd-create/SKILL.md`

### 진입 조건
하나에 해당하면 **PRD Creation 케이스 진입**:
- "만들어줘", "기획서 작성" 등 키워드
- "프로젝트 기획", "서비스 기획" 요청
- `/prd-create` 스킬 호출

### 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **사업성 우선** | 기술/기능 전에 사업성 검토 먼저 |
| **No-Go** | 사업성 부족하면 조기 종료 |
| **딥리서치** | CLI 오케스트레이션으로 빠른 조사 |
| **개발 연결** | 완성 후 Project Planning 제안 |

### 명령어 옵션

| 명령어 | 설명 |
|--------|------|
| `/prd-create` | PRD 생성 시작 |
| `/prd-create thorough` | 심층 분석 모드 |
| `/prd-create enterprise` | 엔터프라이즈 모드 |

### Phase 워크플로우

#### Phase 1: 아이디어 수신 + 구체화
```yaml
actions:
  - 아이디어/컨셉 수신
  - 핵심 질문 (What, Why, Who)
  - 답변 수집
output: 구체화된 아이디어
```

#### Phase 2: 사업성 검토 [Go/No-Go]
```yaml
parallel_research:
  - Task(시장규모): TAM/SAM/SOM, 성장률
  - Task(경쟁분석): 경쟁사, 차별화, 진입장벽
  - Task(수익성): 수익모델, ARPU, 손익분기점

judgment:
  - 🟢 Go: Phase 3 진행
  - 🟡 Pivot: 방향 수정 제안 → 재검토
  - 🔴 No-Go: 이유 설명 + 종료
```

#### Phase 3: 기술/디자인 리서치
```yaml
parallel_research:
  - Task(기술스택): 추천 기술 스택
  - Task(GitHub): 오픈소스/라이브러리
  - Task(API문서): 외부 API 조사
  - Task(디자인): 레퍼런스 수집
  - Task(기술검토): 기술적 실현 가능성

output: AI 기능/개선 아이디어 제안
```

#### Phase 4: PRD 문서 생성
```yaml
parallel_generation:
  - Task(개요): 프로젝트 개요
  - Task(기능): 기능 명세
  - Task(기술): 기술 사양
  - Task(범위): 범위 및 우선순위

output: 통합 PRD 문서
```

#### Phase 5: 확인 + 다음 단계
```yaml
actions:
  - PRD 문서 제시
  - 수정 요청 반영
  - "바로 개발할까요?" → Project Planning 연결
```

---

## Case 2: Project Planning (장시간 자동 작업)

### 참조 문서
`~/.claude/docs/PROJECT-PLANNING.md`

### 진입 조건
하나에 해당하면 **자동으로 플랜 모드 진입**:
- PRD 문서 수신 (파일 또는 텍스트)
- "프로젝트 만들어줘", "서비스 개발해줘" 등 프로젝트 생성 요청
- 기능 3개 이상의 복잡한 요청

**(즉시 실행):**
- `빠르게` / `qk` 키워드 포함 → `/project-plan` 스킬로 즉시 실행

### Step 워크플로우

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: 깊은 분석 + 질문 + 아이디어                         │
│  - 🔍 5 Layer 분석 (Business/Functional/Technical/UX/Risk)  │
│  - ❓ 질문 (🔴반드시 / 🟡확인 / 🔵나중에)                    │
│  - 💡 AI 아이디어 제안                                       │
│  - 📋 확인: 질문 답변 + 아이디어 채택 여부                   │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: 청사진 + 실행 계획 + 승인 [★ 유일한 승인 시점]      │
│  - 📄 BLUEPRINT.md (화면, 여정, 데이터, 섹션)               │
│  - 🔥 병렬 그룹 + 실행 요약                                  │
│  - 💬 "이렇게 만들겠습니다. 진행할까요?"                     │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: 깊은 분석 + 질문 + 아이디어
```yaml
5_layer_analysis:
  - Business: 목적, 타겟, 경쟁사, 수익모델
  - Functional: 기능, 의존성, 우선순위, 숨겨진 요구사항
  - Technical: 스택, 아키텍처, 확장성, 외부 의존성
  - UX: 플로우, 화면, 인터랙션
  - Risk: 기술/일정/누락 리스크

questions:
  - 🔴 반드시 확인 (진행 불가)
  - 🟡 확인 필요 (가정 가능)
  - ⚪ 나중에 결정 가능

output: AI 아이디어 제안 (선택사항)
```

### Step 2: 청사진 + 승인 [★ 유일한 승인 시점]
```yaml
blueprint_md:
  part1_what:
    - 🖥️ 화면 구성도 (ASCII or Mermaid)
    - 🗺️ 사용자 여정 (주요 시나리오 2-3개)
    - 🗄️ 데이터 구조 (핵심 엔티티, 관계)

  part2_how:
    - 🏗️ 섹션 분할 (Section → Milestone → Task)
    - ⚡ 병렬 그룹 [P1], [P2], ...
    - 📊 실행 요약

approval:
  prompt: "이렇게 만들겠습니다. 진행할까요?"
  yes: ["진행해", "OK", "ㅇㅇ"] → Step 3
  no: "수정할 부분 말씀" → 수정 후 재승인
```

### Step 3: 적응형 병렬 자동 개발
```yaml
steel_thread:
  purpose: "아키텍처 검증"
  action: "핵심 경로 하나를 먼저 완성"

adaptive_parallel:
  initial: 10  # M2 Ultra 최적화
  scale_up: +5  # 연속 3성공
  scale_down: -3  # 1실패
  maximum: 24  # CPU 코어 수

auto_progress:
  - T01 ✅ → goals.json 업데이트 → T01 의존 태스크 대기열 추가
  - T02 ✅ → goals.json 업데이트 → 자동으로 다음 태스크
  - (완료까지 자동 반복 - 사용자 개입 불필요)

completion_report:
  - 실행 요약 (총 섹션, 총 태스크, 최대 동시 실행)
  - 결과물 (섹션별 상태, 완료율, 주요 파일)
  - ⚠️ 미완료 항목 (있는 경우)
  - 실행 방법 (npm install, npm run dev)
  - 테스트 방법
```

---

## Case 3: Ideation (/ideation)

### 호출 방법
- `/ideation` 호출 또는 "아이디어" 키워드 사용

### 입력
- 토론 형태 (sequential / debate / brainstorm)
- 분석 깊이 (quick / standard / deep / full)
- 실행 → 결과 확인

### 토론 모드

| 모드 | 설명 | 적합한 상황 |
|------|------|-------------|
| **sequential** | 순차 토론 (라운드별 발언) | 깊은 분석 필요 |
| **debate** | 찬반 토론 (팀 대립) | Go/No-Go 결정 |
| **brainstorm** | 브레인스토밍 (병렬 아이디어) | 다양한 아이디어 |

### 규모 옵션

| 규모 | 페르소나 수 | 용도 |
|------|-------------|------|
| **3명** | 3명 | 빠른 검토 |
| **5~10명** | 5-10명 | 일반적인 아이디어 |
| **10~15명+** | 15명+ | 중요한 의사결정 |
| **전체** | 전체 | 전략적 결정 |

### 주제 프리셋

| 주제 | 트리거 키워드 |
|------|---------------|
| **business_strategy** | 수익, 매출, 사업, 전략 |
| **product_innovation** | 혁신, 새로운, 기능, 제품 |
| **marketing_campaign** | 마케팅, 캠페인, 브랜드 |
| **tech_decision** | 기술, 아키텍처, 스택 |
| **ux_improvement** | UX, 사용성, 경험 |
| **pricing_model** | 수익모델, 가격, 비즈니스모델 |

### 페르소나 카테고리 (27개)

| 카테고리 | 페르소나 |
|----------|----------|
| 비즈니스 | ceo, cfo, coo, sales, bd, legal |
| 마케팅 | marketing, growth, content, community, pr |
| 혁신 | innovator, futurist, visionary, disruptor, inventor |
| 디자인 | designer, ux, user_advocate |
| 분석 | critic, realist, devil_advocate, risk_analyst |
| 리서치 | researcher, ethnographer, competitor |
| 진행 | moderator |

### Advocate/Critic Perspective

**Advocate (옹호자):**
- "Why can this plan succeed?"
- [strengths, opportunities, feasibility, value]

**Critic (비평가):**
- "How can this plan fail?"
- [weaknesses, risks, attack vectors, omissions]

### 결과 액션

| 조건 | 액션 |
|------|------|
| **진행** | 심각한 위험 없음 → 즉시 구현 |
| **조건부** | 특정 위험 존재 → 위험 완화 후 진행 |
| **재설계** | 심각한 문제 발견 → 설계 단계로 복귀 |

---

## Case 4: Problem Solving (5 Whys)

### Phase 1: 빠른 진단 (병렬)
```yaml
parallel:
  - LSP: getDiagnostics, goToDefinition, findReferences
  - Error KB: ~/.claude/error-kb/ 검색
  - Browser: read_console_messages, read_network_requests
```

### Phase 2: 원인 추정
```yaml
actions:
  - Git: git log, git diff (언제 발생?)
  - Task(Explore): 코드베이스 탐색
  - Browser: browser_evaluate
```

### Phase 3: 해결책 검색
```yaml
actions:
  - WebSearch: 에러 메시지 검색
  - Context7: 라이브러리 문서 참조
```

### Phase 4: 검증
```yaml
actions:
  - Browser: navigate, read_console_messages
  - 코드 수정 + 테스트 실행
```

---

## 안전장치

```yaml
safety_guards:
  max_iterations: 10
  consecutive_failures_limit: 5
  checkpoint_every: "라운드 완료 시"

hard_stop:  # 자동 중단
  - DB 스키마 변경
  - 인증 로직 변경
  - 결제 관련
  - 데이터 삭제
```

---

## Plan Mode Output Template

```markdown
## 📊 분석 결과

### 🔍 5 Layer 분석
- **Business**: ...
- **Functional**: ...
- **Technical**: ...
- **UX**: ...
- **Risk**: ...

### ❓ 질문
- 🔴 [반드시 확인 필요]
- 🟡 [확인 권장]
- ⚪ [나중에 결정 가능]

### 💡 AI 아이디어 제안
1. ...
2. ...

---

## 📄 BLUEPRINT

### 🖥️ 화면 구성도
[ASCII or Mermaid diagram]

### 🗺️ 사용자 여정
[주요 시나리오]

### 🏗️ 실행 계획
| Section | Milestone | Tasks |
|---------|-----------|-------|

---

**"이렇게 만들겠습니다. 진행할까요?"**
```
