# Case 2: Project Planning

> PRD → Long-Running Automated Work

## Reference Document

`~/.claude/docs/PROJECT-PLANNING.md`

## Entry Conditions

**Auto-enter plan mode** if any:
- PRD document received (file or text)
- "create project", "develop service" project creation request
- Complex request with 3+ features

**(Immediate execution):**
- `quick` / `qk` keyword included → Execute immediately via `/project-plan` skill

## Step Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Deep Analysis + Questions + Ideas                   │
│  - 🔍 5 Layer Analysis (Business/Functional/Technical/UX/Risk)│
│  - ❓ Questions (🔴Must / 🟡Confirm / 🔵Later)               │
│  - 💡 AI idea suggestions                                    │
│  - 📋 Confirm: Question answers + Idea adoption              │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Blueprint + Execution Plan + Approval              │
│  [★ Only Approval Point]                                    │
│  - 📄 BLUEPRINT.md (screens, journey, data, sections)       │
│  - 🔥 Parallel groups + Execution summary                    │
│  - 💬 "Building this way. Proceed?"                          │
└─────────────────────────────────────────────────────────────┘
```

## Step 1: Deep Analysis + Questions + Ideas

```yaml
5_layer_analysis:
  - Business: Purpose, target, competitors, revenue model
  - Functional: Features, dependencies, priorities, hidden requirements
  - Technical: Stack, architecture, scalability, external dependencies
  - UX: Flow, screens, interactions
  - Risk: Technical/schedule/omission risks

questions:
  - 🔴 Must confirm (cannot proceed)
  - 🟡 Should confirm (can assume)
  - ⚪ Decide later (during implementation)

output: AI idea suggestions (optional)
```

## Step 2: Blueprint + Approval [★ Only Approval Point]

```yaml
blueprint_md:
  part1_what:
    - 🖥️ Screen layout (ASCII or Mermaid)
    - 🗺️ User journey (2-3 main scenarios)
    - 🗄️ Data structure (core entities, relationships)

  part2_how:
    - 🏗️ Section breakdown (Section → Milestone → Task)
    - ⚡ Parallel groups [P1], [P2], ...
    - 📊 Execution summary

approval:
  prompt: "Building this way. Proceed?"
  yes: ["proceed", "OK", "yes"] → Step 3
  no: "Tell me what to modify" → Modify and re-approve
```

## Step 3: Adaptive Parallel Auto Development

```yaml
steel_thread:
  purpose: "Architecture validation"
  action: "Complete one critical path first"

adaptive_parallel:
  initial: 10  # M2 Ultra optimized
  scale_up: +5  # 3 consecutive successes
  scale_down: -3  # 1 failure
  maximum: 24  # CPU core count

auto_progress:
  - T01 ✅ → Update goals.json → Add T01 dependent tasks to queue
  - T02 ✅ → Update goals.json → Auto next task
  - (Auto repeat until complete - no user intervention needed)

completion_report:
  - Execution summary (total sections, tasks, max concurrent)
  - Results (section status, completion rate, main files)
  - ⚠️ Incomplete items (if any)
  - Run instructions (npm install, npm run dev)
  - Test instructions
```

---

**Related**: [prd-creation.md](prd-creation.md), [ideation.md](ideation.md)
