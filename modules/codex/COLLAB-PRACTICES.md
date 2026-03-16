# Claude x Codex Collaboration Practices (Persistent Notes)

## Goal
- Keep `Claude` as planner/reviewer and `Codex` as implementation executor.
- Optimize for reliability, speed, and low context loss across sessions.

## Role Split
- Claude: architecture, task decomposition, quality gates, final review.
- Codex: deterministic implementation, refactor, debugging, test execution.

## Operating Workflow
1. Write spec first (task-template 10 sections).
2. Split work into small executable tasks.
3. Run Codex for first-pass implementation.
4. Run validation (`typecheck`, `lint`, `test`, `build`).
5. Return to Claude for review and final integration decisions.

## Context Retention (3-file system)
- `plan.md`: what to build and milestone sequence.
- `context.md`: key decisions and constraints.
- `TASKS.md`: status/checklist/next action.
- Update after each meaningful task unit.

## Execution Defaults
- Prefer WSL2 workspace for heavy coding workloads.
- Use explicit constraints in prompts (scope, files, forbidden edits, success criteria).
- Require no placeholders/stubs in implementation output.

## Safety/Automation
- Fast mode flags can reduce friction (`codex --yolo`, `claude --dangerously-skip-permissions`) but increase risk.
- Keep destructive/system-level operations explicit and auditable.
- Resolve port conflicts quickly with force-kill by PID when needed.

## Verification Standard
- Minimum completion gate:
  - Type errors: 0
  - Lint errors: 0
  - Tests: pass
  - Build: success

## Prompting Style for Codex
- Give exact file targets and line-of-responsibility.
- State prohibited actions clearly (no scope expansion, no dependency drift unless requested).
- Ask for concise completion report:
  - changed files
  - validation commands run
  - unresolved items

## Notes
- Treat model marketing claims and version superiority claims as non-binding.
- Prefer measurable behavior and reproducible validation over anecdotal rankings.
