# Plan Mode - SuperClaude v4.1

> Strategic Planning System - Strategic planning workflow

---

## Plan Mode Use Cases

| Case                       | Input               | Focus                        | Analysis Depth |
|----------------------------|---------------------|------------------------------|----------------|
| **PRD Creation**           | Idea/Concept        | Business + Technical analysis | --think-hard   |
| **Project Planning**       | PRD document        | What & Why                   | --think-hard   |
| **Feature Implementation** | Feature description | How                          | --think        |
| **Problem Solving**        | Error/Bug/Incident  | Why & How to fix             | --think        |
| **Research**               | Problem/Topic/Need  | What if & Why not            | --think-hard   |

---

## Entry Conditions

| Condition                 | Action                            |
|---------------------------|-----------------------------------|
| PRD document received     | Auto-enter plan mode              |
| "create project" request  | Enter plan mode                   |
| 3+ core features          | Enter plan mode                   |
| Quick/qk keyword          | Execute /project-plan immediately |

---

## Case 1: PRD Creation (Idea → PRD Document)

### Skill Invocation
- **Command**: `/prd-create`
- **Skill Guide**: `~/.claude/skills/prd-create/SKILL.md`

### Entry Conditions
Enter **PRD Creation case** if any:
- "create", "write spec" keywords
- "project planning", "service planning" request
- `/prd-create` skill invocation

### Core Principles

| Principle          | Description                               |
|--------------------|-------------------------------------------|
| **Business First** | Business viability before tech/features   |
| **No-Go**          | Early exit if business viability lacking  |
| **Deep Research**  | Fast investigation via CLI orchestration  |
| **Dev Connection** | Propose Project Planning after completion |

### Command Options

| Command                  | Description          |
|--------------------------|----------------------|
| `/prd-create`            | Start PRD generation |
| `/prd-create thorough`   | Deep analysis mode   |
| `/prd-create enterprise` | Enterprise mode      |

### Phase Workflow

#### Phase 1: Idea Reception + Clarification
```yaml
actions:
  - Receive idea/concept
  - Core questions (What, Why, Who)
  - Collect answers
output: Clarified idea
```

#### Phase 2: Business Viability Review [Go/No-Go]
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

#### Phase 3: Technical/Design Research
```yaml
parallel_research:
  - Task(TechStack): Recommended tech stack
  - Task(GitHub): Open source/libraries
  - Task(APIDocs): External API investigation
  - Task(Design): Reference collection
  - Task(TechReview): Technical feasibility

output: AI feature/improvement suggestions
```

#### Phase 4: PRD Document Generation
```yaml
parallel_generation:
  - Task(Overview): Project overview
  - Task(Features): Feature specification
  - Task(Technical): Technical specifications
  - Task(Scope): Scope and priorities

output: Integrated PRD document
```

#### Phase 5: Confirmation + Next Steps
```yaml
actions:
  - Present PRD document
  - Apply modification requests
  - "Start development now?" → Connect to Project Planning
```

---

## Case 2: Project Planning (Long-Running Automated Work)

### Reference Document
`~/.claude/docs/PROJECT-PLANNING.md`

### Entry Conditions
**Auto-enter plan mode** if any:
- PRD document received (file or text)
- "create project", "develop service" project creation request
- Complex request with 3+ features

**(Immediate execution):**
- `quick` / `qk` keyword included → Execute immediately via `/project-plan` skill

### Step Workflow

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
│ Phase 2: Blueprint + Execution Plan + Approval [★ Only Approval Point] │
│  - 📄 BLUEPRINT.md (screens, journey, data, sections)       │
│  - 🔥 Parallel groups + Execution summary                    │
│  - 💬 "Building this way. Proceed?"                          │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Deep Analysis + Questions + Ideas
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

### Step 2: Blueprint + Approval [★ Only Approval Point]
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

### Step 3: Adaptive Parallel Auto Development
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

## Case 3: Ideation (/ideation)

### Invocation
- `/ideation` command or "idea" keyword

### Input
- Discussion format (sequential / debate / brainstorm)
- Analysis depth (quick / standard / deep / full)
- Execute → Review results

### Discussion Modes

| Mode           | Description                        | Best For             |
|----------------|------------------------------------|--------------------- |
| **sequential** | Sequential discussion (round-based) | Deep analysis needed |
| **debate**     | Pro/con debate (team opposition)   | Go/No-Go decision    |
| **brainstorm** | Brainstorming (parallel ideas)     | Diverse ideas        |

### Scale Options

| Scale      | Persona Count | Use Case            |
|------------|---------------|---------------------|
| **3**      | 3             | Quick review        |
| **5-10**   | 5-10          | General ideation    |
| **10-15+** | 15+           | Important decisions |
| **All**    | All           | Strategic decisions |

### Topic Presets

| Topic                  | Trigger Keywords                       |
|------------------------|----------------------------------------|
| **business_strategy**  | revenue, sales, business, strategy     |
| **product_innovation** | innovation, new, feature, product      |
| **marketing_campaign** | marketing, campaign, brand             |
| **tech_decision**      | tech, architecture, stack              |
| **ux_improvement**     | UX, usability, experience              |
| **pricing_model**      | revenue model, pricing, business model |

### Persona Categories (27)

| Category     | Personas                                            |
|--------------|-----------------------------------------------------|
| Business     | ceo, cfo, coo, sales, bd, legal                     |
| Marketing    | marketing, growth, content, community, pr           |
| Innovation   | innovator, futurist, visionary, disruptor, inventor |
| Design       | designer, ux, user_advocate                         |
| Analysis     | critic, realist, devil_advocate, risk_analyst       |
| Research     | researcher, ethnographer, competitor                |
| Facilitation | moderator                                           |

### Advocate/Critic Perspective

**Advocate:**
- "Why can this plan succeed?"
- [strengths, opportunities, feasibility, value]

**Critic:**
- "How can this plan fail?"
- [weaknesses, risks, attack vectors, omissions]

### Result Actions

| Condition       | Action                                        |
|-----------------|-----------------------------------------------|
| **Proceed**     | No serious risk → Implement immediately       |
| **Conditional** | Specific risk exists → Mitigate then proceed  |
| **Redesign**    | Serious issues found → Return to design phase |

---

## Case 4: Problem Solving (5 Whys)

### Phase 1: Quick Diagnosis (Parallel)
```yaml
parallel:
  - LSP: getDiagnostics, goToDefinition, findReferences
  - Error KB: Search ~/.claude/error-kb/
  - Browser: read_console_messages, read_network_requests
```

### Phase 2: Cause Estimation
```yaml
actions:
  - Git: git log, git diff (when did it occur?)
  - Task(Explore): Codebase exploration
  - Browser: browser_evaluate
```

### Phase 3: Solution Search
```yaml
actions:
  - WebSearch: Error message search
  - Context7: Library documentation reference
```

### Phase 4: Verification
```yaml
actions:
  - Browser: navigate, read_console_messages
  - Code fix + Test execution
```

---

## Safety Guards

```yaml
safety_guards:
  max_iterations: 10
  consecutive_failures_limit: 5
  checkpoint_every: "on round completion"

hard_stop:  # Auto halt
  - DB schema changes
  - Auth logic changes
  - Payment related
  - Data deletion
```

---

## Plan Mode Output Template

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
2. ...

---

## 📄 BLUEPRINT

### 🖥️ Screen Layout
[ASCII or Mermaid diagram]

### 🗺️ User Journey
[Main scenarios]

### 🏗️ Execution Plan
| Section | Milestone | Tasks |
|---------|-----------|-------|

---

**"Building this way. Proceed?"**
```
