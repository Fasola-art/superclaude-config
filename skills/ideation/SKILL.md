---
name: ideation
description: Multi-persona idea discussion skill - Review ideas from 27 expert perspectives
version: "1.0.0"
triggers:
  - /ideation
  - idea discussion
  - multi-persona review
  - 아이디어 토론
  - persona discussion
---

# Ideation Skill

> Multi-persona idea discussion skill - Review ideas from 27 expert perspectives

---

## Overview

The `/ideation` command reviews ideas from multiple expert persona perspectives. Each persona asks questions and provides opinions from their area of expertise, with a moderator synthesizing the final conclusions.

---

## Usage

```
/ideation [idea or topic]
```

**Examples**:
```
/ideation AI-based pet health management app
/ideation Creator economy platform idea
/ideation New SaaS business model
```

---

## Discussion Structure

### Base Panel (6 members)

| Role | Persona | Perspective |
|------|---------|-------------|
| Strategy | `ceo` | Business strategy, vision |
| Finance | `cfo` | ROI, cost efficiency |
| Operations | `coo` | Feasibility, resources |
| Customer | `user_advocate` | User needs, accessibility |
| Critic | `devil_advocate` | Opposing views, alternatives |
| Facilitator | `moderator` | Synthesize opinions, conclusions |

### Extended Panels (Optional)

```
/ideation --panel marketing  → Marketing-focused panel
/ideation --panel tech       → Technology-focused panel
/ideation --panel full       → All 27 personas
```

| Panel | Personas |
|-------|----------|
| marketing | marketing, growth, content, community, pr |
| tech | innovator, futurist, inventor, designer, ux |
| validation | critic, realist, risk_analyst, devil_advocate |
| research | researcher, ethnographer, competitor |
| full | All 27 personas |

---

## Discussion Workflow

### Phase 1: Idea Presentation

```
[User] Presents idea
    ↓
[CEO] Strategic perspective - first impression and key questions
```

### Phase 2: Multi-angle Review (Parallel)

```
[CFO] Financial viability
    - Expected ROI?
    - Initial investment cost?
    - Time to monetization?

[COO] Operational feasibility
    - Required personnel?
    - Operational processes?
    - Is it scalable?

[User Advocate] User perspective
    - Is there real need?
    - User experience?
    - Accessibility?

[Devil's Advocate] Critical review
    - Why might it fail?
    - Why haven't competitors done this?
    - Are there alternatives?
```

### Phase 3: Deep Discussion (Optional)

```
[Marketing] Market entry strategy
[Growth] Growth metrics and levers
[Legal] Legal risks
[Risk Analyst] Risk mitigation strategies
```

### Phase 4: Synthesis and Conclusion

```
[Moderator] Opinion synthesis
    ├── Key consensus points
    ├── Unresolved issues
    ├── Recommended direction
    └── Next steps (Action Items)
```

---

## Output Format

```markdown
# Ideation Session: [Idea Title]

## Executive Summary
[One paragraph summary]

---

## Persona Opinions

### CEO (Strategy)
**Perspective**: [Strategic assessment]
**Questions**: [Key questions]
**Suggestions**: [Recommendations]

### CFO (Finance)
**Perspective**: [Financial assessment]
**Concerns**: [Cost/revenue issues]
**Suggestions**: [Financial strategy]

### COO (Operations)
**Perspective**: [Operational assessment]
**Concerns**: [Execution issues]
**Suggestions**: [Operational plan]

### User Advocate (Customer)
**Perspective**: [User viewpoint]
**Concerns**: [UX issues]
**Suggestions**: [User-centric improvements]

### Devil's Advocate (Critic)
**Perspective**: [Critical analysis]
**Concerns**: [Key weaknesses]
**Alternatives**: [Alternative proposals]

---

## Overall Assessment

### Strengths
- [Strength 1]
- [Strength 2]

### Concerns
- [Concern 1]
- [Concern 2]

### Key Issues
- [Questions to resolve]

---

## Action Items

1. [Next step 1]
2. [Next step 2]
3. [Next step 3]

---

## Recommended Next Skills

- `/prd-create` - Create PRD document
- `/research` - Deep research
- `/project-plan` - Project planning
```

---

## Persona Reference

### All Personas (27)

| Group | Personas |
|-------|----------|
| Business | ceo, cfo, coo, legal, sales, bd |
| Marketing | marketing, growth, content, community, pr |
| Innovation | innovator, futurist, visionary, disruptor, inventor |
| Design | designer, ux, user_advocate |
| Validation | critic, realist, devil_advocate, risk_analyst |
| Research | researcher, ethnographer, competitor |
| Special | moderator |

### Persona Details

Path: `~/.claude/personas/ideation/`

---

## Configuration Options

```yaml
# ~/.claude/superclaude-config.json
ideation:
  default_panel: "basic"       # basic/marketing/tech/validation/full
  parallel_opinions: true      # Collect opinions in parallel
  include_questions: true      # Include questions from each persona
  summary_style: "detailed"    # brief/detailed
  auto_action_items: true      # Auto-generate action items
```

---

## Triggers

- Direct `/ideation` command
- Auto-activates on "discuss this idea" request
- Activates on "review from different perspectives" request
- Activates on "persona discussion" request

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `/prd-create` | Idea → PRD document |
| `/research` | Market/technology research |
| `/project-plan` | Project planning |

---

## Related Documents

- `~/.claude/personas/ideation/INDEX.md` - Persona index
- `~/.claude/docs/PERSONAS.md` - Persona system documentation
