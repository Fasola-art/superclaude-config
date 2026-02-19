# Claude-Codex Collaboration Workflow 지침 생성

## Context

사용자가 Claude(지휘자)와 Codex(실행자)의 협업 워크플로우를 정리한 리서치를 제공함.
기존 SuperClaude v2.0.9 시스템(hooks, personas, skills, rules)과 통합하여,
**양쪽 CLI 모두 읽을 수 있는 단일 워크플로우 지침 파일**을 만드는 것이 목표.

핵심 원칙:
- Claude = Chief Tech Lead (전략, 설계, 리뷰, 오케스트레이션)
- Codex = Specialist Executor (논리 구현, 최적화, 디버깅)
- 80/20 분할: Codex 80% 코딩 → Claude 20% 폴리시/리뷰

---

## Step 1: `~/.claude/WORKFLOW.md` 생성 (신규, ~270줄)

라인 제한 해제 (Codex가 단일 파일 통째로 읽는 것이 최적).

### 파일 구조

```
WORKFLOW.md
├── Frontmatter (YAML)
├── 1. Role Definitions (~25줄)
│   ├── Claude vs Codex 역할/강점/경계 테이블
│   └── Handoff 트리거 조건
├── 2. Workflow Phases (~35줄)
│   ├── Phase 1: PLAN (Claude) - 아키텍처, plan.md 생성
│   ├── Phase 2: DELEGATE (Claude→Codex) - TASKS.md 작성
│   ├── Phase 3: EXECUTE (Codex) - 구현
│   ├── Phase 4: REVIEW (Claude) - W-R Loop, Quality Gate
│   └── Phase 5: INTEGRATE (Claude) - 병합, 테스트, 배포
├── 3. Context Preservation - 3-File System (~35줄)
│   ├── plan.md / context.md / TASKS.md 역할 정의
│   ├── 각 파일 템플릿
│   └── 컴팩트/메모리 리셋 프로토콜
├── 4. Task Delegation Protocol (~25줄)
│   ├── Pre-delegation 체크리스트 (8항목)
│   └── 위임 단위 규칙 (1 Task = 1 Module)
├── 5. Codex Command Templates (~70줄)
│   ├── Template 1: Feature Implementation
│   ├── Template 2: Bug Fix / Debug
│   ├── Template 3: Optimization
│   ├── Template 4: Test Writing
│   └── Template 5: Refactoring
├── 6. Cross-debugging Protocol (~25줄)
│   ├── Claude→Codex 핸드오프 조건 (에러 루프 3회, 로직 난제)
│   ├── Codex→Claude 에스컬레이션 (아키텍처 결정, 3+파일 변경)
│   └── 핸드오프 템플릿
├── 7. SuperClaude Integration (~25줄)
│   ├── 기존 hook/persona/skill 연동 포인트 테이블
│   └── 기존 agent-rules 주입 방법
├── 8. Quality Gates (~25줄)
│   ├── Post-Codex 리뷰 체크리스트 (10항목)
│   └── ACCEPT / REVISE / REJECT 판정 기준
└── META
```

### 주요 콘텐츠

**Codex Command Templates** (핵심 섹션):
- 실제 Codex CLI에 복사-붙여넣기 가능한 프롬프트 5종
- 각 템플릿: `[CONTEXT]` → `[TASK]` → `[ACCEPTANCE CRITERIA]` → `[CONSTRAINTS]` 구조
- 기존 `rules/_shared/agent-rules.md`의 5대 필수 규칙을 모든 템플릿에 내장

**3-File System**:
- 프로젝트 루트에 `.workflow/` 디렉토리 생성
- `plan.md`: Claude가 작성, 아키텍처/결정 기록
- `context.md`: 양쪽 모두 업데이트, 현재 상태
- `TASKS.md`: Claude가 작성, Codex가 소비하는 구체적 태스크 목록

---

## Step 2: `~/.claude/CLAUDE.md` 수정 (2곳)

### 2-1. Slash Commands 테이블에 1행 추가 (line 219 부근)

```markdown
| /workflow         | Claude-Codex collaboration       |
```

### 2-2. Documentation Reference 테이블에 1행 추가 (line 284 부근)

```markdown
| Claude-Codex Workflow | `WORKFLOW.md`                     |
```

---

## Step 3: `~/.claude/INSTALLED_SKILLS.md` 수정 (1곳)

Core Skills 테이블에 1행 추가 (line 18 부근):

```markdown
| workflow | 1.0.0 | Active | Claude-Codex collaboration workflow |
```

---

## 수정 대상 파일 요약

| 파일 | 작업 | 변경량 |
|------|------|--------|
| `~/.claude/WORKFLOW.md` | **신규 생성** | ~270줄 |
| `~/.claude/CLAUDE.md` | 2행 추가 | +2줄 |
| `~/.claude/INSTALLED_SKILLS.md` | 1행 추가 | +1줄 |

---

## 검증 방법

1. `wc -l ~/.claude/WORKFLOW.md` → 250-300줄 범위 확인
2. WORKFLOW.md의 Codex 템플릿을 실제 Codex CLI에 복사하여 구문 오류 없이 읽히는지 확인
3. `/workflow` 명령어가 keyword-detector에서 감지되는지 확인
4. `.workflow/` 디렉토리 생성 후 plan.md, context.md, TASKS.md 템플릿이 유효한지 확인
