# Claude 스킬 사용 가이드

> SuperClaude v2.0.9 스킬 시스템

---

## 스킬 개요

스킬은 특정 작업을 수행하는 미리 정의된 워크플로우입니다.
`/` 명령어로 호출하며, 자동화된 멀티 스텝 작업을 실행합니다.

---

## 핵심 스킬 목록

### PRD 생성

| 명령어 | 설명 |
|--------|------|
| `/prd-create` | 아이디어 → 사업성 검토 → PRD 생성 |

**워크플로우**
1. 아이디어/컨셉 수신 + 구체화
2. 사업성 검토 (Go/No-Go)
3. 기술/디자인 리서치
4. PRD 문서 생성
5. 확인 + 다음 단계 연결

**모드 옵션**
| 모드 | 에이전트 | 섹션 수 |
|------|----------|--------|
| quick | 없음 | 1-10 |
| standard | PRD 생성팀 (4개) | 1-10 |
| thorough | 전체 (사업성+기술+PRD) | 1-10 |
| enterprise | 전체 + 법률/비용/리스크 | 1-26 |

---

### 프로젝트 관리

| 명령어 | 설명 |
|--------|------|
| `/project-plan` | PRD로 프로젝트 시작 |
| `/project-status` | 현재 진행 상황 확인 |
| `/project-continue` | 이전 작업 계속 |

**Project Plan 워크플로우**
```
Step 1: 깊은 분석 + 질문 + 아이디어
├── 5 Layer 분석 (Business/Functional/Technical/UX/Risk)
├── 질문 (🔴반드시/🟡확인/⚪나중에)
└── AI 아이디어 제안

Step 2: 청사진 + 승인 [★ 유일한 승인 시점]
├── BLUEPRINT.md (화면, 여정, 데이터, 섹션)
└── "이렇게 만들겠습니다. 진행할까요?"

Step 3: 적응형 병렬 자동 개발
├── Steel Thread 구현
├── 적응형 병렬 (10개 시작)
└── 완료 보고서
```

---

### 아이디어 토론

| 명령어 | 설명 |
|--------|------|
| `/ideation` | 다중 페르소나 아이디어 토론 |

**모드 선택**
| 모드 | 설명 |
|------|------|
| sequential | 순차 토론 (라운드별 발언) - 깊은 분석 |
| debate | 찬반 토론 (팀 대립) - Go/No-Go 결정 |
| brainstorm | 브레인스토밍 (병렬 아이디어) - 다양한 아이디어 |

**깊이 선택**
| 깊이 | 페르소나 수 | 용도 |
|------|------------|------|
| quick | 5명 | 빠른 검토 |
| standard | 10명 | 일반 아이디어 |
| deep | 15명+ | 중요한 의사결정 |
| full | 27명 | 전략적 결정 |

---

### 리서치

| 명령어 | 설명 |
|--------|------|
| `/research` | 범용 딥리서치 |

**기능**
- 웹 검색 통합
- 문서 크롤링
- 요약 및 분석
- 출처 정리

---

### 에러 처리

| 명령어 | 설명 |
|--------|------|
| `/error-search` | Error KB 검색 |

**사용법**
```bash
/error-search "Cannot find module"
/error-search --type typescript
/error-search --pending
/error-search --stats
```

---

### 복구

| 명령어 | 설명 |
|--------|------|
| `/recover` | 세션 복구 |

**옵션**
```bash
/recover           # 마지막 스냅샷 복구
/recover --list    # 스냅샷 목록
/recover --id X    # 특정 스냅샷 복구
```

---

## 스킬 확장

### 커스텀 스킬 생성

```yaml
# ~/.claude/skills/my-skill.yaml
name: my-skill
description: "내 커스텀 스킬"
trigger: "/my-skill"
steps:
  - action: read_files
    pattern: "src/**/*.ts"
  - action: analyze
    type: "dependencies"
  - action: generate_report
    format: "markdown"
```

### 스킬 설치

```bash
# 마켓플레이스에서 설치
claude skill install <skill-name>

# 로컬 파일에서 설치
claude skill install ./my-skill.yaml
```
