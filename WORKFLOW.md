---
name: claude-codex-workflow
version: "1.0.0"
description: Claude-Codex collaboration protocol
triggers:
  - /workflow
  - "codex 협업"
  - "claude-codex"
---

# Claude-Codex Collaboration Workflow

> Claude = Chief Tech Lead | Codex = Specialist Executor | 80/20 Split

---

## 1. Role Definitions

| Aspect | Claude (지휘자) | Codex (실행자) |
|--------|----------------|----------------|
| Role | Chief Tech Lead | Specialist Executor |
| Strengths | 아키텍처, 설계, 리뷰, 오케스트레이션 | 논리 구현, 최적화, 디버깅, 반복 코딩 |
| Output | plan.md, TASKS.md, 리뷰 코멘트 | 완성된 코드, 테스트, 최적화 결과 |
| Scope | 전체 프로젝트, 다중 파일 | 단일 모듈/기능 단위 |
| Decision | 아키텍처, 기술 선택, 트레이드오프 | 구현 세부사항, 알고리즘 선택 |

### Handoff Triggers

| Direction | Condition |
|-----------|-----------|
| Claude → Codex | 설계 완료 후 구현 진입 / 반복 코딩 / 성능 최적화 |
| Codex → Claude | 아키텍처 결정 (3+ 파일) / 에러 루프 3회 / 요구사항 불명확 |

---

## 2. Workflow Phases

| Phase | Owner | Actions |
|-------|-------|---------|
| 1. PLAN | Claude | 요구사항 분석 → 아키텍처 설계 → `.workflow/plan.md` 작성 |
| 2. DELEGATE | Claude | TASKS.md 작성 (1 Task = 1 Module) → Codex 프롬프트 생성 |
| 3. EXECUTE | Codex | TASKS.md 소비 → 구현 → 테스트 → context.md 업데이트 |
| 4. REVIEW | Claude | W-R Loop 실행 → Quality Gate 판정 (ACCEPT/REVISE/REJECT) |
| 5. INTEGRATE | Claude | 통합 테스트 → 폴리시 → 커밋/PR/배포 |

---

## 3. Context Preservation (3-File System)

프로젝트 루트 `.workflow/` 디렉토리에 배치.

| File | Owner | Purpose |
|------|-------|---------|
| `plan.md` | Claude 작성 | 아키텍처, 기술 결정, 모듈 구조, 리스크 |
| `context.md` | 양쪽 업데이트 | 현재 상태, 완료/진행/블로커, 최근 변경 |
| `TASKS.md` | Claude 작성, Codex 소비 | 구체적 실행 태스크 + Acceptance Criteria |

### plan.md Template

```markdown
# Project Plan
## Architecture: [요약]
## Tech Stack: [스택]
## Modules: [모듈 목록 + 설명]
## Decisions: [결정사항 + 근거]
## Risks: [리스크 + 완화 전략]
```

### context.md Template

```markdown
# Current Context
## Status: [PLANNING | EXECUTING | REVIEWING | INTEGRATING]
## Completed: [완료]
## In Progress: [진행]
## Blocked: [블로커]
## Recent Changes: [변경사항]
```

### TASKS.md Template

```markdown
# Tasks
## Task N: [제목]
- Status: [PENDING | IN_PROGRESS | DONE | BLOCKED]
- Module: [대상]
- Acceptance Criteria: [체크리스트]
- Constraints: [제약]
- Dependencies: [의존성]
```

### Memory Reset Protocol

컨텍스트 소진 시: `context.md` 저장 → 새 세션에서 3파일 로드 → 재개.

---

## 4. Task Delegation Protocol

### Pre-delegation Checklist

| # | Check |
|---|-------|
| 1 | 태스크가 단일 모듈 범위인가? |
| 2 | Acceptance Criteria가 측정 가능한가? |
| 3 | 입출력 인터페이스가 명확한가? |
| 4 | 의존 모듈이 이미 완료되었는가? |
| 5 | 필요한 타입/스키마가 정의되어 있는가? |
| 6 | 테스트 전략이 명시되어 있는가? |
| 7 | 에러 처리 방침이 포함되어 있는가? |
| 8 | 성능 요구사항이 명시되어 있는가? |

### Delegation Rules

- **1 Task = 1 Module** (단일 파일 또는 밀접 관련 파일 그룹)
- **Max 3 files** per task
- **Self-contained**: 태스크 단독 테스트 가능
- **Clear boundary**: 다른 모듈 내부 수정 금지

---

## 5. Codex Command Templates

> 모든 템플릿에 Agent Rules 5대 규칙 내장 (Section 7 참조)

### Template 1: Feature Implementation

```
[CONTEXT]
프로젝트: {project_name} | 모듈: {module_path}
관련 파일: {file_list}
기존 인터페이스: {interface_definition}

[TASK]
{feature_description}을 구현하라.

[ACCEPTANCE CRITERIA]
- [ ] {criterion_1}
- [ ] {criterion_2}
- [ ] 모든 테스트 통과, 타입 에러 없음

[CONSTRAINTS]
1. 파일: 50~120줄 (초과 시 분할)
2. 타입 힌트 필수, No stub/placeholder
3. 기존 패턴/네이밍 컨벤션 준수
4. 에러는 컨텍스트와 함께 래핑
```

### Template 2: Bug Fix

```
[CONTEXT]
버그 위치: {file_path}:{line_number}
에러: {error_message}
재현: {steps} | 예상: {expected} | 실제: {actual}

[TASK]
위 버그를 수정하라.

[ACCEPTANCE CRITERIA]
- [ ] 에러 미발생, 기존 테스트 통과
- [ ] 수정에 대한 회귀 테스트 추가
- [ ] 근본 원인 주석 기록

[CONSTRAINTS]
1. 최소 변경 원칙 - 필요한 부분만 수정
2. 관련 없는 리팩토링 금지
3. 사이드 이펙트 확인
```

### Template 3: Optimization

```
[CONTEXT]
대상: {file_path}
현재: {current_metrics} | 목표: {target_metrics}
프로파일링: {profiling_data}

[TASK]
{optimization_target}을 최적화하라.

[ACCEPTANCE CRITERIA]
- [ ] {target_metric} 달성
- [ ] 기존 테스트 통과, 벤치마크 포함
- [ ] 최적화 근거 주석 기록

[CONSTRAINTS]
1. 가독성 유지, 기존 API 변경 금지
2. 메모리 vs 속도 트레이드오프 명시
```

### Template 4: Test Writing

```
[CONTEXT]
대상: {target_module} | 프레임워크: {framework}
기존 테스트: {existing_tests}
커버리지 목표: {coverage_target}%

[TASK]
{target_module} 테스트를 작성하라.

[ACCEPTANCE CRITERIA]
- [ ] Happy/Error/Boundary path 포함
- [ ] 커버리지 {coverage_target}% 이상
- [ ] 모든 테스트 독립 실행 가능

[CONSTRAINTS]
1. Table-driven / parametrize 패턴
2. 외부 의존성 mock 처리
3. AAA 패턴 (Arrange-Act-Assert) 준수
```

### Template 5: Refactoring

```
[CONTEXT]
대상: {file_path} | 문제: {code_smell}
목표 구조: {target_structure}
관련 테스트: {test_files}

[TASK]
{refactoring_description}을 수행하라.

[ACCEPTANCE CRITERIA]
- [ ] 기존 테스트 전부 통과 (동작 무변경)
- [ ] 라인 수 제한 준수, 네이밍 통일

[CONSTRAINTS]
1. 동작 변경 금지 - 리팩토링만
2. 한 번에 하나의 기법만 적용
3. 각 단계마다 테스트 실행
```

---

## 6. Cross-debugging Protocol

### Claude → Codex Handoff

| Condition | 전달 내용 |
|-----------|----------|
| 에러 루프 3회 | 디버깅 컨텍스트 + 시도한 해결책 |
| 로직 난제 | 문제 정의 + 입출력 예시 + 제약조건 |
| 성능 병목 | 프로파일링 데이터 + 핫스팟 위치 |

### Codex → Claude Escalation

| Condition | Action |
|-----------|--------|
| 아키텍처 결정 | 옵션 + 트레이드오프 정리 후 에스컬레이션 |
| 3+ 파일 변경 | 영향 범위 분석 후 승인 요청 |
| 요구사항 모호 | 구체적 질문 목록 작성 |

### Handoff Template

```
[HANDOFF: {방향}]
Reason: {사유} | Context: {상태}
Attempted: {시도한 해결책}
Request: {요청} | Files: {파일 목록}
```

---

## 7. SuperClaude Integration

| Feature | Integration Point |
|---------|-------------------|
| Writer-Reviewer Loop | Phase 4 REVIEW: 4-agent 병렬 리뷰 |
| TodoWrite | Phase 2 DELEGATE: TASKS.md 자동 생성 |
| Personas | PLAN: architect/reviewer persona 활용 |
| Hooks | Codex 산출물 수령 시 자동 lint/format |
| Skills | `/workflow`로 워크플로우 시작 |
| Agent Rules | Codex 프롬프트에 5대 규칙 내장 |
| Quality Gates | Phase 4: `docs/QUALITY-GATES.md` 기준 |

### Agent Rules (모든 Codex 프롬프트에 내장)

```
1. 파일: 50~120줄 범위 유지 (초과 시 분할, 미달 시 병합)
2. Python: 타입 힌트 + docstring 필수
3. 기존 코드 먼저 확인
4. No stub/placeholder - 완전한 구현만
5. 에러는 컨텍스트와 함께 래핑
```

---

## 8. Quality Gates

### Post-Codex Review Checklist (10항목)

| # | Check |
|---|-------|
| 1 | 파일 라인 수 50~120줄 범위 |
| 2 | 모든 함수에 타입 힌트/시그니처 |
| 3 | 에러 처리 완전 (컨텍스트 래핑) |
| 4 | 테스트 존재 및 통과 |
| 5 | 기존 패턴/네이밍 일관성 |
| 6 | 불필요한 의존성 미추가 |
| 7 | stub/placeholder/TODO 없음 |
| 8 | 보안 취약점 없음 (하드코딩 시크릿 등) |
| 9 | 성능 요구사항 충족 |
| 10 | 문서화 (docstring, 주석) 적절 |

### Judgment Criteria

| Verdict | Condition | Action |
|---------|-----------|--------|
| ACCEPT | 10/10 통과 | 통합 진행 |
| REVISE | 7-9/10, 경미한 이슈 | 수정 지시 후 Codex 재위임 |
| REJECT | ≤6/10, 근본 문제 | Phase 2부터 재시작 |

---

## 9. Executor Compatibility (AI-Agnostic)

Codex 외 다른 AI도 Executor 역할 수행 가능.

| AI Tool | Executor 지침 로드 방법 |
|---------|------------------------|
| Codex CLI | 프로젝트 루트 `AGENTS.md` 자동 로드 |
| Claude Code | `executor` 페르소나 활성화 또는 `.workflow/AGENTS.md` 참조 |
| Cursor | `.cursorrules`에 AGENTS.md 내용 포함 |
| Gemini/GPT | 시스템 프롬프트에 AGENTS.md 내용 붙여넣기 |
| Windsurf | `.windsurfrules`에 AGENTS.md 내용 포함 |

### 프로젝트 적용 방법

```bash
# 1. 프로젝트 루트에 .workflow/ 복사
cp -r ~/.workflow/ <project-root>/.workflow/

# 2. Codex용: 프로젝트 루트에 AGENTS.md 심볼릭 링크
ln -s .workflow/AGENTS.md <project-root>/AGENTS.md

# 3. Claude executor 모드: 페르소나 키워드 "executor" 사용
```

### Template 파일 위치

| File | Path | Purpose |
|------|------|---------|
| AGENTS.md (master) | `~/.workflow/AGENTS.md` | AI-agnostic Executor 지침 |
| executor persona | `~/.claude/personas/dev/executor.json` | Claude Executor 모드 |
| plan.md template | `~/.workflow/plan.md` | 아키텍처 계획 템플릿 |
| context.md template | `~/.workflow/context.md` | 상태 추적 템플릿 |
| TASKS.md template | `~/.workflow/TASKS.md` | 태스크 목록 템플릿 |

---

**META**
- Version: 1.1.0
- Created: 2026-02-17
- Updated: 2026-02-17
- Compatibility: Claude Code, Codex CLI, Cursor, Gemini, GPT, Windsurf
