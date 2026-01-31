# PRD Create Skill

> 아이디어를 체계적인 PRD(Product Requirements Document)로 변환하는 스킬

---

## 개요

`/prd-create` 명령어는 사용자의 아이디어를 받아 사업성 검토, 기술/디자인 리서치를 거쳐 완성도 높은 PRD 문서를 생성합니다.

---

## 5 Phase 워크플로우

### Phase 1: 아이디어 수신 + 구체화 질문

**목표**: 아이디어의 본질 파악 및 범위 정의

1. 아이디어 수신
2. 5 Layer 분석 (Business/Functional/Technical/UX/Risk)
3. 구체화 질문 우선순위 (🔴 필수 / 🟡 확인 / ⚪ 나중에)
4. 💡 AI 아이디어 제안

**질문 프레임워크**:
- **Business**: 타겟 사용자, 수익 모델, 경쟁 차별화
- **Functional**: 핵심 기능, MVP 범위, 우선순위
- **Technical**: 기술 스택, 확장성 요구사항
- **UX**: 사용자 여정, 핵심 인터랙션
- **Risk**: 기술적 리스크, 법적/규제 이슈

---

### Phase 2: 사업성 검토 (Go/No-Go 판정) ★

**목표**: 프로젝트 진행 여부 결정

**평가 기준**:
| 항목 | 가중치 | 평가 내용 |
|------|--------|----------|
| 시장 기회 | 25% | TAM/SAM/SOM, 성장률 |
| 기술 실현성 | 25% | 기술 스택, 개발 복잡도 |
| 비즈니스 모델 | 20% | 수익성, 확장성 |
| 경쟁 우위 | 15% | 차별화 포인트 |
| 리소스 요구 | 15% | 예산, 팀, 시간 |

**판정 결과**:
- ✅ **Go**: Phase 3로 진행
- ❌ **No-Go**: 피드백 제공 후 종료 또는 피벗 제안
- 🟡 **Conditional Go**: 조건부 승인 (리스크 완화 필요)

> ⚠️ **Go 판정 시에만** Phase 3 이후 진행

---

### Phase 3: 기술/디자인 리서치

**목표**: PRD 작성을 위한 기술 조사 및 디자인 방향 수립

**기술 리서치**:
- 유사 서비스 분석
- 기술 스택 추천
- 아키텍처 패턴 제안
- 서드파티 서비스 조사

**디자인 리서치**:
- 경쟁사 UI/UX 분석
- 디자인 레퍼런스 수집
- 사용자 플로우 초안
- 와이어프레임 방향

---

### Phase 4: PRD 문서 생성

**목표**: 완성도 높은 PRD 문서 작성

**PRD 템플릿 구조**:
```markdown
# [프로젝트명] PRD

## 1. Executive Summary
- 프로젝트 개요
- 핵심 가치 제안
- 성공 지표 (KPIs)

## 2. Problem Statement
- 해결하려는 문제
- 현재 솔루션의 한계
- 타겟 사용자

## 3. Solution Overview
- 제안 솔루션
- 핵심 기능 목록
- 차별화 포인트

## 4. Functional Requirements
### 4.1 MVP Features (P0)
### 4.2 Phase 2 Features (P1)
### 4.3 Future Features (P2)

## 5. Non-Functional Requirements
- 성능 요구사항
- 보안 요구사항
- 확장성 요구사항

## 6. Technical Architecture
- 시스템 아키텍처
- 기술 스택
- 데이터 모델

## 7. User Experience
- 사용자 페르소나
- 사용자 여정
- 핵심 화면 설명

## 8. Success Metrics
- 정량적 지표
- 정성적 지표
- 측정 방법

## 9. Timeline & Milestones
- Phase 1: MVP (주요 마일스톤)
- Phase 2: 확장
- Phase 3: 성숙

## 10. Risks & Mitigations
- 기술 리스크
- 비즈니스 리스크
- 완화 전략

## 11. Appendix
- 용어 정의
- 참고 자료
- 와이어프레임
```

---

### Phase 5: 다음 단계 선택

**목표**: PRD 완료 후 다음 행동 결정

**선택지**:
1. **개발 시작**: `/project-plan`으로 연결 → 프로젝트 플래닝 시작
2. **수정**: PRD 피드백 반영 및 수정
3. **저장**: PRD 문서를 `.planning/` 폴더에 저장

---

## 사용 예시

```
사용자: 반려동물 건강 관리 앱 아이디어가 있어

Claude: /prd-create 스킬을 실행합니다.

[Phase 1: 아이디어 분석]
좋은 아이디어입니다! 몇 가지 구체화 질문이 있습니다:

🔴 필수:
1. 타겟 사용자는 누구인가요? (강아지/고양이/모든 반려동물)
2. MVP에서 가장 중요한 기능은 무엇인가요?

🟡 확인:
3. 수익 모델은 어떻게 계획하고 계신가요?
4. 기존 앱과의 차별점은 무엇인가요?

💡 AI 제안:
- 수의사 원격 상담 기능 추가 고려
- 반려동물 커뮤니티 기능으로 engagement 강화
- AI 기반 증상 체커 기능

...계속
```

---

## 연관 스킬

| 스킬 | 용도 |
|------|------|
| `/project-plan` | PRD → 프로젝트 플랜 |
| `/project-status` | 진행 상황 확인 |
| `/ideation` | 다중 페르소나 아이디어 토론 |
| `/research` | 범용 딥리서치 |

---

## 출력 위치

생성된 PRD는 다음 위치에 저장됩니다:
- `.planning/PRD-[프로젝트명].md`
- `.planning/BLUEPRINT.md` (화면 구조도, 사용자 여정, 데이터 구조)

---

## 설정 옵션

```yaml
# ~/.claude/superclaude-config.json
prd_create:
  auto_research: true      # Phase 3 자동 실행
  go_nogo_required: true   # Phase 2 필수 여부
  template: "standard"     # PRD 템플릿 (standard/lean/enterprise)
  output_dir: ".planning"  # 출력 디렉토리
```

---

## 트리거

- `/prd-create` 명령어 직접 호출
- "PRD 만들어줘" 요청 시 자동 활성화
- "아이디어 검토해줘" 요청 시 Phase 1-2만 실행

---

## 관련 문서

- `~/.claude/docs/PRD-WORKFLOW.md` - 상세 워크플로우
- `~/.claude/docs/PROJECT-PLANNING.md` - 프로젝트 플래닝 시스템
- `~/.claude/docs/PLAN-MODE.md` - 플랜 모드 규칙
