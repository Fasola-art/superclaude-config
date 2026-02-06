# Project Planning

> 8단계 프로젝트 계획 워크플로우

## 8-Step Workflow

| Phase | Step | Description |
|-------|------|-------------|
| 1 | Deep Analysis | 심층 분석 + 질문 + 아이디어 |
| 2 | 5 Layer Analysis | Business/Functional/Technical/UX/Risk |
| 3 | Question Priority | 🔴 Required / 🟡 Confirm / ⚪ Later |
| 4 | AI Ideas | AI 아이디어 제안 |
| 5 | Blueprint | ★ 유일한 승인 포인트 |
| 6 | BLUEPRINT.md | 화면, 유저 저니, 데이터 구조 |
| 7 | Execution Plan | Section → Milestone → Task |
| 8 | Auto-Development | Adaptive 병렬 자동 개발 |

## Deliverables

- BLUEPRINT.md (화면, 유저 저니, 데이터 구조)
- Execution plan (Section → Milestone → Task)
- 자동 생성 완료 리포트

## Execution Features

- **Steel Thread**: 아키텍처 검증을 위한 핵심 경로 우선 구현
- **Adaptive Scaling**: 5로 시작 → 성공률에 따라 조정 (최대 무제한)
- **병렬 자동 개발**: 독립적인 태스크 동시 실행

## Code Architecture Principles

| Principle | Description |
|-----------|-------------|
| UI/Hook Separation | 컴포넌트는 UI만, 로직은 use-*.ts에 |
| Extract Common | 2+ 반복 → shared 컴포넌트로 추출 |
| SSOT | 단일 소스, computed 값은 파생 |

---

**Related**: [settings.md](settings.md), [../orchestrator/orchestrator-workflow.md](../orchestrator/orchestrator-workflow.md)
