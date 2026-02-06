# Case 1: PRD Creation

> Idea → PRD Document

## Skill Invocation

- **Command**: `/prd-create`
- **Skill Guide**: `~/.claude/skills/prd-create/SKILL.md`

## Entry Conditions

Enter PRD Creation case if any:
- "create", "write spec" keywords
- "project planning", "service planning" request
- `/prd-create` skill invocation

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Business First** | Business viability before tech/features |
| **No-Go** | Early exit if business viability lacking |
| **Deep Research** | Fast investigation via CLI orchestration |
| **Dev Connection** | Propose Project Planning after completion |

## Command Options

| Command | Description |
|---------|-------------|
| `/prd-create` | Start PRD generation |
| `/prd-create thorough` | Deep analysis mode |
| `/prd-create enterprise` | Enterprise mode |

## Phase Workflow

### Phase 1: Idea Reception + Clarification
```yaml
actions:
  - Receive idea/concept
  - Core questions (What, Why, Who)
  - Collect answers
output: Clarified idea
```

### Phase 2: Business Viability Review [Go/No-Go]
```yaml
parallel_research:
  - Task(MarketSize): TAM/SAM/SOM, growth rate
  - Task(CompetitorAnalysis): Competitors, differentiation, barriers
  - Task(Profitability): Revenue model, ARPU, break-even

judgment:
  - 🟢 Go: Proceed to Phase 3
  - 🟡 Pivot: Suggest direction change → Re-review
  - 🔴 No-Go: Explain reason + Exit
```

### Phase 3: Technical/Design Research
```yaml
parallel_research:
  - Task(TechStack): Recommended tech stack
  - Task(GitHub): Open source/libraries
  - Task(APIDocs): External API investigation
  - Task(Design): Reference collection
  - Task(TechReview): Technical feasibility

output: AI feature/improvement suggestions
```

### Phase 4: PRD Document Generation
```yaml
parallel_generation:
  - Task(Overview): Project overview
  - Task(Features): Feature specification
  - Task(Technical): Technical specifications
  - Task(Scope): Scope and priorities

output: Integrated PRD document
```

### Phase 5: Confirmation + Next Steps
```yaml
actions:
  - Present PRD document
  - Apply modification requests
  - "Start development now?" → Connect to Project Planning
```

---

**Related**: [project-planning.md](project-planning.md)
