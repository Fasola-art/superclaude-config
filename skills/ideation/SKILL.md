# Ideation Skill

> 다중 페르소나 아이디어 토론 스킬 - 27개 전문가 관점에서 아이디어 검토

---

## 개요

`/ideation` 명령어는 아이디어를 여러 전문가 페르소나 관점에서 다각도로 검토합니다. 각 페르소나가 자신의 전문 영역에서 질문하고, 의견을 제시하며, 최종적으로 모더레이터가 종합합니다.

---

## 사용법

```
/ideation [아이디어 또는 주제]
```

**예시**:
```
/ideation AI 기반 반려동물 건강 관리 앱
/ideation 크리에이터 이코노미 플랫폼 아이디어
/ideation 새로운 SaaS 비즈니스 모델
```

---

## 토론 구성

### 기본 패널 (6인)

| 역할 | 페르소나 | 관점 |
|------|----------|------|
| 전략 | `ceo` | 비즈니스 전략, 비전 |
| 재무 | `cfo` | ROI, 비용 효율성 |
| 운영 | `coo` | 실행 가능성, 리소스 |
| 고객 | `user_advocate` | 사용자 니즈, 접근성 |
| 비판 | `devil_advocate` | 반대 의견, 대안 |
| 진행 | `moderator` | 의견 종합, 결론 |

### 확장 패널 (옵션)

```
/ideation --panel marketing  → 마케팅 중심 패널
/ideation --panel tech       → 기술 중심 패널
/ideation --panel full       → 전체 27인 패널
```

| 패널 | 페르소나들 |
|------|-----------|
| marketing | marketing, growth, content, community, pr |
| tech | innovator, futurist, inventor, designer, ux |
| validation | critic, realist, risk_analyst, devil_advocate |
| research | researcher, ethnographer, competitor |
| full | 모든 27개 페르소나 |

---

## 토론 워크플로우

### Phase 1: 아이디어 발표

```
[사용자] 아이디어 제시
    ↓
[CEO] 전략적 관점에서 첫 인상 및 핵심 질문
```

### Phase 2: 다각도 검토 (병렬)

```
[CFO] 재무적 타당성
    - 예상 ROI는?
    - 초기 투자 비용은?
    - 수익화 시점은?

[COO] 운영 가능성
    - 필요 인력은?
    - 운영 프로세스는?
    - 확장 가능한가?

[User Advocate] 사용자 관점
    - 실제 니즈가 있는가?
    - 사용자 경험은?
    - 접근성은?

[Devil's Advocate] 비판적 검토
    - 왜 실패할 수 있는가?
    - 경쟁사는 왜 안 했는가?
    - 대안은 없는가?
```

### Phase 3: 심층 토론 (선택적)

```
[Marketing] 시장 진입 전략
[Growth] 성장 지표 및 레버
[Legal] 법적 리스크
[Risk Analyst] 리스크 완화 방안
```

### Phase 4: 종합 및 결론

```
[Moderator] 의견 종합
    ├── 핵심 합의점
    ├── 미해결 논점
    ├── 추천 방향
    └── 다음 단계 (Action Items)
```

---

## 출력 형식

```markdown
# 💡 Ideation Session: [아이디어 제목]

## 📋 Executive Summary
[한 문단 요약]

---

## 🎭 페르소나별 의견

### CEO (전략)
**관점**: [전략적 평가]
**질문**: [핵심 질문]
**제안**: [추천 사항]

### CFO (재무)
**관점**: [재무적 평가]
**우려**: [비용/수익 이슈]
**제안**: [재무 전략]

### COO (운영)
**관점**: [운영 평가]
**우려**: [실행 이슈]
**제안**: [운영 계획]

### User Advocate (사용자)
**관점**: [사용자 관점]
**우려**: [UX 이슈]
**제안**: [사용자 중심 개선]

### Devil's Advocate (비판)
**관점**: [비판적 분석]
**우려**: [핵심 약점]
**대안**: [대안 제시]

---

## ⚖️ 종합 평가

### ✅ 강점
- [강점 1]
- [강점 2]

### ⚠️ 우려사항
- [우려 1]
- [우려 2]

### 🎯 핵심 논점
- [해결해야 할 질문들]

---

## 📌 Action Items

1. [다음 단계 1]
2. [다음 단계 2]
3. [다음 단계 3]

---

## 🔗 추천 다음 스킬

- `/prd-create` - PRD 문서 작성
- `/research` - 심층 리서치
- `/project-plan` - 프로젝트 계획
```

---

## 페르소나 참조

### 전체 페르소나 (27개)

| 그룹 | 페르소나들 |
|------|-----------|
| Business | ceo, cfo, coo, legal, sales, bd |
| Marketing | marketing, growth, content, community, pr |
| Innovation | innovator, futurist, visionary, disruptor, inventor |
| Design | designer, ux, user_advocate |
| Validation | critic, realist, devil_advocate, risk_analyst |
| Research | researcher, ethnographer, competitor |
| Special | moderator |

### 페르소나 상세

경로: `~/.claude/personas/ideation/`

---

## 설정 옵션

```yaml
# ~/.claude/superclaude-config.json
ideation:
  default_panel: "basic"       # basic/marketing/tech/validation/full
  parallel_opinions: true      # 병렬 의견 수집
  include_questions: true      # 각 페르소나 질문 포함
  summary_style: "detailed"    # brief/detailed
  auto_action_items: true      # Action Items 자동 생성
```

---

## 트리거

- `/ideation` 명령어 직접 호출
- "아이디어 토론해줘" 요청 시 자동 활성화
- "다양한 관점에서 검토해줘" 요청 시 활성화
- "페르소나 토론" 요청 시 활성화

---

## 관련 스킬

| 스킬 | 용도 |
|------|------|
| `/prd-create` | 아이디어 → PRD 문서 |
| `/research` | 시장/기술 리서치 |
| `/project-plan` | 프로젝트 계획 수립 |

---

## 관련 문서

- `~/.claude/personas/ideation/INDEX.md` - 페르소나 인덱스
- `~/.claude/docs/PERSONAS.md` - 페르소나 시스템 문서
