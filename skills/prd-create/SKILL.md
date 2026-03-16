---
name: prd-create
description: Transform ideas into structured PRD (Product Requirements Document)
version: "1.0.0"
triggers:
  - /prd-create
  - create prd
  - PRD 작성
  - idea to prd
---

# PRD Create Skill

> Transform ideas into structured PRD (Product Requirements Document)

---

## Overview

The `/prd-create` command takes user ideas through business validation, technical/design research to generate comprehensive PRD documents.

---

## 5 Phase Workflow

### Phase 1: Idea Intake + Clarification Questions

**Goal**: Understand idea essence and define scope

1. Receive idea
2. 5 Layer analysis (Business/Functional/Technical/UX/Risk)
3. Prioritize clarification questions (Red: Required / Yellow: Confirm / White: Later)
4. AI idea suggestions

**Question Framework**:
- **Business**: Target users, revenue model, competitive differentiation
- **Functional**: Core features, MVP scope, priorities
- **Technical**: Tech stack, scalability requirements
- **UX**: User journey, key interactions
- **Risk**: Technical risks, legal/regulatory issues

---

### Phase 2: Business Validation (Go/No-Go Decision)

**Goal**: Determine project continuation

**Evaluation Criteria**:
| Item | Weight | Evaluation |
|------|--------|------------|
| Market Opportunity | 25% | TAM/SAM/SOM, growth rate |
| Technical Feasibility | 25% | Tech stack, development complexity |
| Business Model | 20% | Profitability, scalability |
| Competitive Advantage | 15% | Differentiation points |
| Resource Requirements | 15% | Budget, team, timeline |

**Decision Results**:
- **Go**: Proceed to Phase 3
- **No-Go**: Provide feedback, end or suggest pivot
- **Conditional Go**: Conditional approval (risk mitigation required)

> **Note**: Only proceed to Phase 3+ on Go decision

---

### Phase 3: Technical/Design Research

**Goal**: Technical investigation and design direction for PRD

**Technical Research**:
- Similar service analysis
- Tech stack recommendations
- Architecture pattern suggestions
- Third-party service research

**Design Research**:
- Competitor UI/UX analysis
- Design reference collection
- User flow drafts
- Wireframe direction

---

### Phase 4: PRD Document Generation

**Goal**: Create comprehensive PRD document

**PRD Template Structure**:
```markdown
# [Project Name] PRD

## 1. Executive Summary
- Project overview
- Core value proposition
- Success metrics (KPIs)

## 2. Problem Statement
- Problem to solve
- Current solution limitations
- Target users

## 3. Solution Overview
- Proposed solution
- Core feature list
- Differentiation points

## 4. Functional Requirements
### 4.1 MVP Features (P0)
### 4.2 Phase 2 Features (P1)
### 4.3 Future Features (P2)

## 5. Non-Functional Requirements
- Performance requirements
- Security requirements
- Scalability requirements

## 6. Technical Architecture
- System architecture
- Tech stack
- Data model

## 7. User Experience
- User personas
- User journey
- Key screen descriptions

## 8. Success Metrics
- Quantitative metrics
- Qualitative metrics
- Measurement methods

## 9. Timeline & Milestones
- Phase 1: MVP (key milestones)
- Phase 2: Expansion
- Phase 3: Maturity

## 10. Risks & Mitigations
- Technical risks
- Business risks
- Mitigation strategies

## 11. Appendix
- Glossary
- References
- Wireframes
```

---

### Phase 5: Next Steps Selection

**Goal**: Determine next action after PRD completion

**Options**:
1. **Start Development**: Connect to `/project-plan` → Begin project planning
2. **Revise**: Incorporate PRD feedback and revise
3. **Save**: Save PRD document to `.planning/` folder

---

## Usage Example

```
User: I have an idea for a pet health management app

Claude: Executing /prd-create skill.

[Phase 1: Idea Analysis]
Great idea! I have some clarification questions:

Required:
1. Who is your target user? (dogs/cats/all pets)
2. What is the most important feature for MVP?

Confirm:
3. What revenue model are you planning?
4. What differentiates this from existing apps?

AI Suggestions:
- Consider adding remote vet consultation
- Pet community feature for engagement
- AI-based symptom checker

...continues
```

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `/project-plan` | PRD → Project plan |
| `/project-status` | Check progress |
| `/ideation` | Multi-persona idea discussion |
| `/research` | General deep research |

---

## Output Location

Generated PRD is saved to:
- `.planning/PRD-[ProjectName].md`
- `.planning/BLUEPRINT.md` (screen structure, user journey, data structure)

---

## Configuration Options

```yaml
# ~/.claude/superclaude-config.json
prd_create:
  auto_research: true      # Auto-execute Phase 3
  go_nogo_required: true   # Phase 2 required
  template: "standard"     # PRD template (standard/lean/enterprise)
  output_dir: ".planning"  # Output directory
```

---

## Triggers

- Direct `/prd-create` command
- Auto-activates on "create PRD" request
- Runs Phase 1-2 only on "review idea" request

---

## Related Documents

- `~/.claude/docs/PRD-WORKFLOW.md` - Detailed workflow
- `~/.claude/docs/PROJECT-PLANNING.md` - Project planning system
- `~/.claude/docs/PLAN-MODE.md` - Plan mode rules
