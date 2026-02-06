# Plan Mode - SuperClaude

> 전략적 계획 워크플로우

## Use Cases

| Case | Input | Focus | Analysis Depth |
|------|-------|-------|----------------|
| **PRD Creation** | Idea/Concept | Business + Technical | --think-hard |
| **Project Planning** | PRD document | What & Why | --think-hard |
| **Feature Implementation** | Feature description | How | --think |
| **Problem Solving** | Error/Bug/Incident | Why & How to fix | --think |
| **Research** | Problem/Topic/Need | What if & Why not | --think-hard |

## Entry Conditions

| Condition | Action |
|-----------|--------|
| PRD document received | Auto-enter plan mode |
| "create project" request | Enter plan mode |
| 3+ core features | Enter plan mode |
| Quick/qk keyword | Execute /project-plan immediately |

## 파일 구조

| 파일 | 내용 |
|------|------|
| [prd-creation.md](prd-creation.md) | Case 1: Idea → PRD |
| [project-planning.md](project-planning.md) | Case 2: PRD → Project |
| [ideation.md](ideation.md) | Case 3: /ideation |
| [problem-solving.md](problem-solving.md) | Case 4: 5 Whys + Safety |

## Output Template

```markdown
## 📊 Analysis Results
### 🔍 5 Layer Analysis
- **Business**: ...
- **Functional**: ...
- **Technical**: ...
- **UX**: ...
- **Risk**: ...

### ❓ Questions
- 🔴 [Must confirm]
- 🟡 [Should confirm]
- ⚪ [Decide later]

### 💡 AI Idea Suggestions
1. ...

---
**"Building this way. Proceed?"**
```

---

**META**
- Version: 4.1
- Refactored: 2026-02-04
