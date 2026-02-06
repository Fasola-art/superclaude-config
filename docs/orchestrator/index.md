# Orchestrator/Agent/Skill/Hook Guide

> SuperClaude v2.0.9 구현 가이드

## 파일 구조

| 파일 | 내용 | 줄 |
|------|------|-----|
| [system-architecture.md](system-architecture.md) | 시스템 아키텍처 | 70 |
| [hook-system.md](hook-system.md) | 훅 시스템 상세 | 100 |
| [parallel-agents.md](parallel-agents.md) | 병렬 에이전트 실행 | 70 |
| [vibe-mode-keywords.md](vibe-mode-keywords.md) | Vibe/Mode 키워드 | 55 |
| [writer-reviewer.md](writer-reviewer.md) | Writer-Reviewer 루프 | 95 |
| [orchestrator-workflow.md](orchestrator-workflow.md) | Orchestrator 워크플로우 | 85 |
| [scenarios-basic.md](scenarios-basic.md) | 기본 시나리오 (1-3) | 75 |
| [scenarios-advanced.md](scenarios-advanced.md) | 고급 시나리오 (4-6) | 90 |
| [quick-reference.md](quick-reference.md) | 빠른 참조 + 트러블슈팅 | 80 |

## 핵심 컴포넌트

```
User Prompt
    ↓
UserPromptSubmit Hook (7)
    ↓
Claude Code Processing + PreToolUse Hook
    ↓
Tool Execution
    ↓
PostToolUse Hook (12)
```

## 주요 사용법

- **빠른 수정**: `qk change button color`
- **병렬 작업**: `para analyze and document`
- **딥 서치**: `ds find memory leak`
- **리서치**: `/orchestrator AI encryption impact`

---

**META**
- Version: 2.0.9
- Refactored: 2026-02-04
