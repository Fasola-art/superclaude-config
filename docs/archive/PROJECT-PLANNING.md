# Project Planning Guide

> 3-Step Workflow Details

---

## Task Decomposition Structure

```
Section                   # Independent feature area
└── Milestone             # 1-2 hour work unit
    └── Task              # 15-30 minute work unit
        └── Step          # Single action
```

---

## Parallel Classification Rules (SSOT)

### ✅ Parallelizable
- Different file modifications (LoginForm vs SignupForm)
- Same component, different features

### ❌ Sequential Required
- types.ts → Code using that type (dependency)
- Same file simultaneous modification (conflict)

---

## Step 1: Deep Analysis

### 5 Layer Analysis

```yaml
business:
  - Purpose: Why this project?
  - Target: Who is it for?
  - Competitors: Existing alternatives?
  - Revenue model: How to monetize?

functional:
  - Features: What to build?
  - Dependencies: What must come first?
  - Priorities: P0/P1/P2 classification
  - Hidden requirements: Implicit needs

technical:
  - Stack: What technologies?
  - Architecture: System structure?
  - Scalability: How to handle growth?
  - External dependencies: External services/APIs?

ux:
  - Flow: User journey?
  - Screens: What screens needed?
  - Interaction: How do users interact?

risk:
  - Technical risk: Technical difficulties?
  - Schedule risk: Delay possibilities?
  - Omission risk: Missing anything?
```

### Question Priority

| Priority         | Indicator | Description                    |
|------------------|-----------|--------------------------------|
| 🔴 Must confirm  | High      | Cannot proceed without answer  |
| 🟡 Should confirm | Medium    | Can proceed with assumption    |
| ⚪ Decide later   | Low       | Decide during implementation   |

---

## Step 2: Blueprint (BLUEPRINT.md)

### Part 1: What to Build

```markdown
## 🖥️ Screen Layout

┌─────────────────────────────────────┐
│           Header                    │
├─────────────────────────────────────┤
│  Sidebar  │        Main Content     │
│           │                         │
│  - Menu1  │   [Component Area]     │
│  - Menu2  │                         │
│  - Menu3  │                         │
└───────────┴─────────────────────────┘

## 🗺️ User Journey

1. Signup → Email verification → Onboarding
2. Login → Dashboard → Feature use
3. Settings → Profile edit → Save

## 🗄️ Data Structure

User
├── id: string (PK)
├── email: string (unique)
├── name: string
└── createdAt: timestamp

Post
├── id: string (PK)
├── userId: string (FK → User)
├── title: string
├── content: text
└── publishedAt: timestamp
```

### Part 2: How to Build

```markdown
## 🏗️ Section Breakdown

### Section 1: Auth System [P1]
- Milestone 1.1: Signup
  - Task 1.1.1: Signup form UI
  - Task 1.1.2: Email duplicate check API
  - Task 1.1.3: Signup logic
- Milestone 1.2: Login
  - Task 1.2.1: Login form UI
  - Task 1.2.2: JWT token generation

### Section 2: Dashboard [P1]
- Milestone 2.1: Layout
  - Task 2.1.1: Header component
  - Task 2.1.2: Sidebar component [P1]
  - Task 2.1.3: Main layout [P1]

## ⚡ Parallel Groups

[P1] Task 2.1.2, Task 2.1.3 (can run simultaneously)

## 📊 Execution Summary

| Item                     | Count |
|--------------------------|-------|
| Total sections           | 5     |
| Total milestones         | 15    |
| Total tasks              | 45    |
| Expected parallel groups | 12    |
```

---

## Step 3: Adaptive Parallel Execution

### Execution Algorithm

```python
concurrent = 10  # Initial (M2 Ultra)
success_streak = 0

while tasks_remaining:
    # Parallel execution
    results = execute_parallel(next_tasks[:concurrent])

    for result in results:
        if result.success:
            success_streak += 1
            if success_streak >= 3:
                concurrent = min(concurrent + 5, 24)
                success_streak = 0
        else:
            concurrent = max(concurrent - 3, 3)
            success_streak = 0

    update_goals_json()
    add_unblocked_tasks_to_queue()
```

### Execution Log Example

```
[10:00] Start: 10 concurrent
[10:05] T01-T10 complete (10/10 success)
[10:05] Scale up: 10 → 15
[10:10] T11-T25 complete (14/15 success, 1 failure)
[10:10] Scale down: 15 → 12
[10:15] T26-T37 complete (12/12 success)
[10:15] Scale up: 12 → 17
...
[11:30] Complete: Total 45 tasks
```

---

## Completion Report Format

```markdown
# Project Completion Report

## 📊 Execution Summary
- Total sections: 5
- Total tasks: 45
- Max concurrent: 20
- Total time: 90 minutes

## ✅ Results
| Section   | Status      | Completion | Main Files       |
|-----------|-------------|------------|------------------|
| Auth      | ✅ Complete | 100%       | src/auth/*       |
| Dashboard | ✅ Complete | 100%       | src/dashboard/*  |
| API       | ✅ Complete | 100%       | src/api/*        |

## ⚠️ Incomplete Items
- None

## 🚀 Run Instructions
\`\`\`bash
npm install
npm run dev
\`\`\`

## 🧪 Test Instructions
\`\`\`bash
npm run test
npm run test:e2e
\`\`\`
```
