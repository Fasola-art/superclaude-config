---
name: pdca
description: Plan-Do-Check-Act iterative development workflow.
version: "1.0.0"
triggers:
  - /pdca
  - PDCA workflow
  - iterative development
author: reim
tags:
  - workflow
  - methodology
  - quality
---

# PDCA Workflow Skill

> Plan → Do → Check → Act 반복 개발 사이클

---

## Usage

```bash
/pdca plan <feature>     # Plan 단계: 계획 수립
/pdca do                 # Do 단계: 태스크 실행
/pdca check              # Check 단계: 검증 실행
/pdca act                # Act 단계: 개선점 분석
/pdca iterate            # 다음 iteration으로 이동
/pdca status             # 현재 상태 표시
/pdca report             # 완료 보고서 생성
```

---

## Execution Instructions

<command-name>pdca</command-name>

### Subcommands

#### `plan <feature>`
1. Create `.pdca/` directory in project root
2. Generate `state.json` with initial state
3. Generate `plan.md` using this template:
   ```markdown
   # Plan: {feature}
   ## 목표
   ## 성공 기준
   ## 태스크 목록
   ## 리스크
   ```
4. Create TaskCreate items from plan tasks
5. Set state → `plan: completed`

#### `do`
1. Read `.pdca/state.json`, verify stage = plan completed
2. Execute pending tasks (use TaskList/TaskUpdate)
3. Log progress to `.pdca/do-log.md`
4. Auto-Retry Loop integration (Feature 1):
   - Each code change triggers quality gates
   - Failed gates → auto-feedback → retry
5. Set state → `do: completed`

#### `check`
1. Run all quality gates on changed files
2. Run tests (if configured)
3. Generate `.pdca/check-results.md`:
   ```markdown
   # Check Results - Iteration {n}
   ## Quality Gate 점수: {score}%
   ## 테스트 결과
   ## 발견된 이슈
   ```
4. Set state → `check: completed, score: {n}`

#### `act`
1. Analyze check results
2. Generate `.pdca/act-actions.md`:
   ```markdown
   # Act: 개선 액션
   ## 이번 iteration 성과
   ## 개선 필요 항목
   ## 다음 iteration 목표
   ```
3. Set state → `act: completed`

#### `iterate`
1. Save current iteration to `.pdca/history/iteration-{n}.json`
2. Increment iteration number
3. Reset stages to pending
4. If score ≥ pass_threshold → suggest completion
5. If iteration = max_iterations → force report

#### `status`
Display current PDCA state:
```
PDCA: {feature} | Iteration {n}/{max}
  Plan: ✅ | Do: 🔄 | Check: ⏳ | Act: ⏳
  Last Score: {score}%
```

#### `report`
Generate final report from all iteration history.

---

## State Schema

See [references/templates.md](references/templates.md) for state.json format.

## Stage Details

See [references/stages.md](references/stages.md) for detailed guidance.

---

**META**
- Version: 1.0.0
- Created: 2026-02-07
