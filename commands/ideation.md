---
description: "Multi-persona ideation discussion"
argument-hint: "[idea or topic]"
---

# Ideation Session

Review ideas from multiple expert persona perspectives.

## Behavior

1. Receive idea
2. Analyze from default panel of 6 perspectives (CEO, CFO, COO, User Advocate, Devil's Advocate, Moderator)
3. Present opinions and questions from each persona
4. Moderator synthesizes and concludes
5. Derive action items

## Persona Panel

### Default Panel (6 personas)
- **CEO**: Strategic perspective
- **CFO**: Financial viability
- **COO**: Operational feasibility
- **User Advocate**: User perspective
- **Devil's Advocate**: Critical review
- **Moderator**: Opinion synthesis

### Extended Options
- `--panel marketing`: Marketing focus (marketing, growth, content, community, pr)
- `--panel tech`: Technical focus (innovator, futurist, inventor, designer, ux)
- `--panel validation`: Validation focus (critic, realist, risk_analyst, devil_advocate)
- `--panel full`: Full 27-persona panel

## Usage Examples

```
/ideation AI pet health management app
/ideation Creator economy platform
/ideation --panel marketing New product launch strategy
```

## Output Format

```markdown
# 💡 Ideation Session: [Idea]

## 📋 Executive Summary
[Summary]

## 🎭 Persona Opinions
### CEO (Strategy)
### CFO (Finance)
### COO (Operations)
### User Advocate (User)
### Devil's Advocate (Critical)

## ⚖️ Synthesis
### ✅ Strengths
### ⚠️ Concerns
### 🎯 Key Points

## 📌 Action Items
```

## Persona Reference

- Full list: `~/.claude/personas/ideation/INDEX.md`
- Detailed skill: `~/.claude/skills/ideation/SKILL.md`

## Related Commands

- `/prd-create`: Generate PRD document
- `/research`: Deep research
- `/project-plan`: Project planning
