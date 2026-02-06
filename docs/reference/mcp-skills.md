# MCP Router & Skills

> MCP 서버 + 스킬 시스템

## MCP Router System

### Why MCP Router?

- **Direct Registration**: 모든 MCP 도구가 시스템 프롬프트에 → 컨텍스트 폭발
- **Router**: 단일 진입점, 동적 로딩 → 컨텍스트 절약

### Registered Servers (servers.json)

| Server | Purpose | Main Tools |
|--------|---------|------------|
| context7 | Library doc search | resolve-library-id, query-docs |
| mana | Code analysis | find_symbol, search_for_pattern, rename_symbol |
| playwright | Browser automation | browser_navigate, browser_click, browser_type |
| playwright-test | E2E testing | test_list, test_run, test_debug |

---

## Skill System

### Main Skills (34+)

| Category | Skills |
|----------|--------|
| Documents | pdf, docx, pptx, xlsx |
| Design | frontend-design, canvas-design, algorithmic-art |
| Dev | frontend-dev, mcp-builder, webapp-testing |
| Planning | prd-create, ideation, research, agent-team |
| Present | presentation-orchestrator, brand-guidelines |

### Key Skill Commands

| Command | Purpose |
|---------|---------|
| /prd-create | Idea → PRD 생성 |
| /project-plan | PRD → 프로젝트 계획 |
| /project-status | 진행 상황 확인 |
| /research | 일반 딥 리서치 |
| /ideation | 멀티 페르소나 토론 |
| /commit | Git 커밋 |
| /review-pr | PR 리뷰 |
| /tdd | TDD 워크플로우 |
| /e2e | E2E 테스트 생성 |

---

**Related**: [index.md](index.md)
