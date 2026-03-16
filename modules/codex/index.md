# Codex Module Index

> 코덱스(또는 외부 AI 에이전트) 협업 워크플로우

## 파일 구조

| 파일 | 역할 |
|------|------|
| [task-template.md](task-template.md) | 작업 명세서 템플릿 (10섹션) |
| [roles/agent-role.md](roles/agent-role.md) | 코덱스 역할 지침 (모델 독립적) |
| [roles/claude-role.md](roles/claude-role.md) | 클로드 역할 지침 |
| [roles/RACI.md](roles/RACI.md) | RACI 매트릭스 |

## 사용 방법

1. `/codex` 스킬 실행 → 작업 분석
2. `task-template.md` 기반 명세서 자동 생성
3. 코덱스에 명세서 전달 (WSL2 filesystem)
4. 완료 후 클로드 검증

## 관련 파일

- `~/.claude/skills/codex-workflow/SKILL.md` - 스킬 진입점
- `~/.claude/docs/CODEX-WORKFLOW.md` - 참조 가이드
