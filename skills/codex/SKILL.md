---
name: codex-workflow
description: 작업 분석 후 코덱스/에이전트에 위임하는 4단계 워크플로우
version: "1.0.0"
triggers:
  - /codex
  - 코덱스 위임
  - codex delegate
  - 코덱스로 넘겨
  - 코덱스한테 맡겨
  - codex로 넘겨
---

# Codex Workflow Skill

> 작업을 분석하고 코덱스/에이전트에 최적화된 명세서를 생성하여 위임하는 워크플로우

---

## 작업 분류 매트릭스

| 작업 유형 | 클로드 전담 | 코덱스 위임 |
|-----------|------------|------------|
| 요구사항 분석 | ✅ | - |
| 아키텍처 설계 | ✅ | - |
| 단순 CRUD 구현 | - | ✅ |
| 반복 패턴 코드 | - | ✅ |
| 성능 최적화 | - | ✅ |
| 리팩토링 (대규모) | - | ✅ |
| 보일러플레이트 | - | ✅ |
| 테스트 대량 생성 | - | ✅ |
| 버그 수정 | - | ✅ |
| 보안 감사/설계 | ✅ | - |
| 컨텍스트 의존 판단 | ✅ | - |

### 코덱스 위임 판단 기준
- 변경 파일 수 > 5개
- 반복적 패턴 (CRUD, 미들웨어, 훅)
- 컨텍스트 독립적 작업
- 명확한 입출력 정의 가능

---

## Phase 1: 작업 분석 + 적합성 판단

**실행 내용:**
1. 사용자 요청에서 작업 유형 식별
2. 위 매트릭스 기준으로 코덱스 적합성 평가
3. 적합 → Phase 2 진행 / 부적합 → 클로드 직접 처리

**코덱스 부적합 패턴:**
- "어떻게 설계해야 해?" (설계 결정 필요)
- "이 코드 이해하고 리팩토링" (컨텍스트 심층 이해 필요)
- "사용자 요구사항 정리해줘" (요구사항 분석)
- "아키텍처 선택해줘" (전략적 판단)

---

## Phase 2: 명세서 자동 생성

**`~/.claude/modules/codex/task-template.md` 기반으로 10섹션 명세서 작성:**

```
섹션 1: 작업 목표 (단일 문장)
섹션 2: 환경 정보 (WSL2 경로 + 모델 선택)
섹션 3: 기술 스택 및 패턴
섹션 4: 입력 파일 (읽기 전용 목록)
섹션 5: 출력 파일 (생성/수정/보호 파일)
섹션 6: 세부 요구사항 (FR/NFR)
섹션 7: 인터페이스 명세
섹션 8: 금지 사항 (PROHIBITED)
섹션 9: 검증 방법 (실행 명령어)
섹션 10: 성공 기준 + 클로드 검증 체크포인트
```

**모델 선택 가이드 (CLAUDE.md Cost Strategy):**

| 작업 유형 | 모델 |
|-----------|------|
| 복잡 로직/알고리즘/아키텍처 | `opus` |
| 표준 구현/리팩토링/기능 개발 | `sonnet` (기본값) |
| 단순 수정/포맷/타입 정의 | `haiku` |

---

## Phase 3: WSL2 실행 명령 생성

**핸드오프 전 필수 체크:**
```bash
# 1. 컨텍스트 손실 방지
/compact  # 실행 권장

# 2. TASKS.md 업데이트
## Status: CODEX_DELEGATED
## Done: [완료된 작업]
## Next: [코덱스 완료 후 클로드 검증]
## Blockers: [없음]
```

**생성되는 실행 명령:**
```bash
# WSL2 내에서 실행 (~/project 경로 사용)
# Windows 경로(/mnt/c/) 절대 사용 금지

# Codex CLI
codex --model {model} "$(cat ~/project/.planning/codex-task.md)"

# 또는 파일 기반
codex --model {model} --file ~/project/.planning/codex-task.md

# 대안: Claude Subagent (WSL2 불필요)
# → Claude Code의 Task tool로 위임 (현재 세션에서 직접 실행)
```

**3-파일 시스템:**
- `~/project/.planning/plan.md` - 아키텍처/설계 (클로드 작성)
- `~/project/.planning/context.md` - 현재 컨텍스트 (자동 업데이트)
- `~/project/TASKS.md` - 진행 상태 (실시간 업데이트)

---

## Phase 4: 클로드 검증 + TASKS.md 업데이트

**에이전트 완료 후 클로드 검증 순서:**

```
1. 완료 보고 수신
2. 생성 파일 목록 확인
3. 5개 품질 게이트 적용:
   [ ] 기능 완성도: 명세서 요구사항 100% 충족
   [ ] 코드 품질: 줄 제한 준수 + 린트 통과
   [ ] 타입 안전성: 타입 힌트/정의 완성
   [ ] 테스트 존재: 핵심 로직 테스트 포함
   [ ] 의존성 정합성: import/require 실제 존재
4. TASKS.md → ## Status: COMPLETED 업데이트
5. 미흡 사항 → 재위임 또는 클로드 직접 보완
```

---

## 에이전트 역할 지침 전달

코덱스/에이전트에 명세서와 함께 전달:
```
~/.claude/modules/codex/roles/agent-role.md
```
이 파일은 **모델 독립적**으로 설계되어 Codex, Aider, GPT-Engineer, Claude Subagent 등 모든 AI 코딩 에이전트에 동일하게 적용됩니다.

---

## 사용 예시

```
User: 사용자 인증 미들웨어 구현을 코덱스한테 맡겨줘

Claude: /codex 워크플로우 실행

[Phase 1] 작업 분석
→ JWT 미들웨어: 명확한 입출력, 반복 패턴 → 코덱스 적합 ✅

[Phase 2] 명세서 생성
→ 10섹션 명세서 작성 중...
→ 모델: sonnet (표준 구현)
→ 저장: ~/project/.planning/codex-task.md

[Phase 3] 실행 명령
codex --model sonnet --file ~/project/.planning/codex-task.md

[Phase 4] 검증 대기
→ 완료 후 5개 품질 게이트 적용 예정
```

---

## 관련 파일

| 파일 | 역할 |
|------|------|
| `~/.claude/modules/codex/task-template.md` | 명세서 템플릿 |
| `~/.claude/modules/codex/roles/agent-role.md` | 에이전트 역할 지침 |
| `~/.claude/modules/codex/roles/claude-role.md` | 클로드 역할 지침 |
| `~/.claude/modules/codex/roles/RACI.md` | RACI 매트릭스 |
| `~/.claude/docs/CODEX-WORKFLOW.md` | 참조 가이드 |
