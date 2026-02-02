# 목표별 페르소나 & 에이전트 최적 구성

> 3가지 목표: 트레이딩, 음악/작곡, 개발
> 총 79개 에이전트 + 41개 페르소나 기반 구성

---

## 목차

1. [트레이딩 (부업 → 본업)](#-목표-1-트레이딩-부업--본업)
2. [음악 선생님 + 작곡가 (본업)](#-목표-2-음악-선생님--작곡가-본업)
3. [개발자 (Claude Code)](#-목표-3-개발자-claude-code)
4. [통합 워크플로우](#-통합-워크플로우-권장)
5. [빠른 명령어 요약](#-빠른-명령어-요약)

---

## 🎯 목표 1: 트레이딩 (부업 → 본업)

### 필수 에이전트

| 에이전트 | 역할 |
|----------|------|
| `quant-analyst` | 퀀트 전략 분석, 백테스팅 설계 |
| `data-analyst` | 시장 데이터 분석, 시각화 |
| `data-scientist` | ML 모델 (FinBERT, YOLO) 설계 |
| `data-engineer` | 데이터 파이프라인 구축 |
| `performance-profiler` | 시스템 성능 최적화 |

### 추천 페르소나

| 페르소나 | 활용 |
|----------|------|
| `analyzer` | 시장 패턴 분석, 근본 원인 추적 |
| `architect` | 트레이딩 시스템 아키텍처 설계 |
| `performance` | 실행 속도 최적화, 지연 시간 감소 |
| `risk_analyst` | 리스크 관리 전략 수립 |
| `cfo` | 자금 관리, ROI 분석 |

### 즉시 활용 예시

```bash
# 퀀트 분석 시작
> "str para 트레이딩 파이프라인 설계해줘.
   Jetson(FinBERT) + RPi5(YOLO) + 4090(메인) 통합"

# 백테스팅 최적화
> "perf 백테스팅 성능 분석해줘.
   현재 5년치 데이터 처리에 너무 오래 걸림"

# 데이터 파이프라인
> "data-engineer 에이전트로 실시간 뉴스 → 감정분석 파이프라인 구축"
```

### 트레이딩 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                     24시간 자동화 파이프라인                      │
└─────────────────────────────────────────────────────────────────┘

     뉴스 API          거래소 API         차트 스크린샷
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Jetson Orin    │ │  4090 노트북     │ │  라즈베리파이    │
│  ────────────── │ │  ────────────── │ │  ────────────── │
│  FinBERT 분석   │ │  실시간 가격     │ │  YOLO 패턴분석  │
│  감정점수 산출  │ │  주문 실행       │ │  캔들/패턴 인식 │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                   ┌─────────────────┐
                   │   통합 신호     │
                   │  (가중치 적용)  │
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
         텔레그램       자동 주문      대시보드
          알림           실행         (갤탭/폰)
```

---

## 🎵 목표 2: 음악 선생님 + 작곡가 (본업)

### 추천 에이전트

| 에이전트 | 역할 |
|----------|------|
| `content-marketer` | 레슨 콘텐츠 마케팅 |
| `social-media-copywriter` | SNS 홍보 문구 작성 |
| `technical-writer` | 교재/커리큘럼 문서화 |
| `video-editor` | 레슨 영상 편집 조언 |
| `seo-analyzer` | 온라인 레슨 홍보 최적화 |

### 추천 페르소나

| 페르소나 | 활용 |
|----------|------|
| `mentor` | 교육 콘텐츠 설계, 학습 단계 구성 |
| `creative` | 작곡 아이디어 브레인스토밍 (ideation 세션) |
| `content` | 레슨 자료 스토리텔링 |
| `marketing` | 레슨 브랜딩, 차별화 전략 |
| `user_advocate` | 학생 관점 고려 |

### 즉시 활용 예시

```bash
# 레슨 커리큘럼 설계
> "mentor 페르소나로 초보자용 피아노 커리큘럼 12주 과정 설계해줘"

# 아이디어 토론
> "/ideation 신곡 컨셉: 전자음악 + 국악 퓨전"

# 홍보 콘텐츠
> "content-marketer 에이전트로 인스타그램 레슨 홍보 시리즈 만들어줘"
```

### 음악 워크플로우

```
┌─────────────────────────────────────────────────────────────────┐
│                      음악 워크플로우                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │   Mac Studio     │         │  갤럭시탭 S8     │              │
│  │   M2 Ultra       │         │  Ultra           │              │
│  ├──────────────────┤         ├──────────────────┤              │
│  │ • Logic Pro X    │         │ • 악보 표시      │              │
│  │ • 플러그인 (VST) │    ───▶ │ • 레슨 교재      │              │
│  │ • 마스터링       │         │ • 필기 (S펜)     │              │
│  │ • AI 작곡 보조   │         │ • 학생 화상수업  │              │
│  └──────────────────┘         └──────────────────┘              │
│           │                                                      │
│           ▼                                                      │
│  ┌──────────────────┐                                           │
│  │    LG Gram       │                                           │
│  ├──────────────────┤                                           │
│  │ • 외부 레슨 시   │                                           │
│  │ • 가벼운 편집    │                                           │
│  │ • 자료 준비      │                                           │
│  └──────────────────┘                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💻 목표 3: 개발자 (Claude Code)

### 핵심 에이전트 (시스템 등록됨)

| 에이전트 | 역할 |
|----------|------|
| `code-architect` | 아키텍처 설계, 확장성 분석 |
| `code-reviewer` | 코드 품질 검토, 보안 검사 |
| `code-explorer` | 코드베이스 분석, 구조 파악 |
| `code-simplifier` | 복잡한 코드 단순화 |
| `fullstack-developer` | 풀스택 개발 지원 |
| `security-engineer` | 보안 취약점 분석 |
| `devops-engineer` | CI/CD, 배포 자동화 |
| `test-engineer` | 테스트 커버리지, 품질 보증 |

### 추천 페르소나 (자동 활성화)

| 페르소나 | 활용 |
|----------|------|
| `security` | 인증/결제 코드 시 자동 활성화 (90% 우선순위) |
| `architect` | 시스템 설계 시 활성화 |
| `backend` | API 개발 시 활성화 |
| `frontend` | UI 컴포넌트 개발 시 활성화 |
| `qa` | 테스트 코드 작성 시 활성화 |
| `devops` | 배포 설정 시 활성화 |

### 자동 활성화 키워드

```yaml
security (자동): auth, login, password, token, session, payment
architect (자동): architecture, design, structure, system
frontend (자동): component, ui, form, button, css
backend (자동): api, endpoint, database, server
qa (자동): test, e2e, coverage, bug, quality
devops (자동): deploy, ci, cd, docker, kubernetes
```

### 개발 환경

```
┌─────────────────────────────────────────────────────────────────┐
│                      개발 환경                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────┐               │
│  │              Mac Studio M2 Ultra              │               │
│  │                  (메인 개발기)                 │               │
│  ├──────────────────────────────────────────────┤               │
│  │ • Claude Code + SuperClaude v2.0.9           │               │
│  │ • Xcode (iOS/macOS 앱)                        │               │
│  │ • Docker, Kubernetes                          │               │
│  │ • 병렬 에이전트 24개 동시 실행                 │               │
│  └──────────────────────────────────────────────┘               │
│                          │                                       │
│           ┌──────────────┼──────────────┐                       │
│           ▼              ▼              ▼                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐               │
│  │ 라즈베리파이 │ │ Jetson      │ │ 사무용 PC   │               │
│  │ (테스트서버) │ │ (AI 테스트) │ │ (빌드서버)  │               │
│  └─────────────┘ └─────────────┘ └─────────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔥 통합 워크플로우 권장

### 트레이딩 시스템 개발 시

```bash
# 1단계: 아키텍처 설계
> "str 트레이딩 봇 아키텍처 설계.
   architect + analyzer + performance 페르소나 활성화"

# 2단계: 코드 구현
> "para data-engineer + quant-analyst 에이전트로
   FinBERT 뉴스 파이프라인 구현"

# 3단계: 품질 검증
> "code-reviewer + security-engineer + test-engineer
   병렬로 코드 검토"
```

### 일일 워크플로우

| 시간 | 작업 |
|------|------|
| 오전 | 개발 (Mac Studio) - architect, security 활성화 |
| 오후 | 음악 레슨 (Mac + 갤탭) - mentor 페르소나 |
| 저녁 | 트레이딩 (4090) - analyzer, performance 활성화 |
| 밤 | 작곡 (Mac) - creative 페르소나 + ideation |

---

## 📋 빠른 명령어 요약

| 목표 | 명령어 | 효과 |
|------|--------|------|
| 트레이딩 | `str para 파이프라인설계` | architect + analyzer + performance |
| 분석 | `perf 백테스팅최적화` | performance + data-analyst |
| 레슨 | `mentor 커리큘럼설계` | mentor + content |
| 작곡 | `/ideation 곡 컨셉` | 다중 creative 페르소나 토론 |
| 개발 | `str 시스템설계` | architect + security + backend |
| 리뷰 | `/review-pr` | code-reviewer 병렬 실행 |

---

## 📊 전체 에이전트 목록 (79개)

### 개발/코드

- `code-architect`, `code-explorer`, `code-reviewer`, `code-simplifier`
- `fullstack-developer`, `frontend-developer`, `backend-architect`
- `typescript-pro`, `python-pro`, `golang-pro`, `sql-pro`

### 보안/품질

- `security-engineer`, `security-auditor`, `api-security-audit`
- `test-engineer`, `feature-code-reviewer`, `silent-failure-hunter`

### 데이터/AI

- `data-analyst`, `data-scientist`, `data-engineer`
- `quant-analyst`, `ml-engineer`, `model-evaluator`

### 인프라/배포

- `devops-engineer`, `cloud-architect`, `database-architect`
- `vercel-deployment-specialist`, `performance-profiler`

### 리서치/분석

- `research-orchestrator`, `research-synthesizer`, `academic-researcher`
- `technical-researcher`, `fact-checker`, `competitive-intelligence-analyst`

### 콘텐츠/마케팅

- `content-marketer`, `social-media-copywriter`, `social-media-clip-creator`
- `seo-analyzer`, `video-editor`, `technical-writer`

### 특수/기타

- `business-analyst`, `product-strategist`, `prompt-engineer`
- `mcp-expert`, `ai-ethics-advisor`, `agent-creator`

---

## 📊 전체 페르소나 목록 (41개)

### 개발 (14개)

`security`, `architect`, `backend`, `performance`, `frontend`, `qa`,
`devops`, `analyzer`, `refactorer`, `explorer`, `librarian`, `mentor`,
`scribe`, `multimodal`

### 비즈니스 (6개)

`ceo`, `cfo`, `coo`, `sales`, `bd`, `legal`

### 마케팅 (5개)

`marketing`, `growth`, `content`, `community`, `pr`

### 혁신 (5개)

`innovator`, `futurist`, `visionary`, `disruptor`, `inventor`

### 디자인 (3개)

`designer`, `ux`, `user_advocate`

### 검증 (4개)

`critic`, `realist`, `devil_advocate`, `risk_analyst`

### 리서치 (3개)

`researcher`, `ethnographer`, `competitor`

### 특수 (1개)

`moderator`

---

**META**
- Generated: 2026-01-31
- Tool: Claude Code (SuperClaude v2.0.9)
- Total: 79 Agents + 41 Personas
