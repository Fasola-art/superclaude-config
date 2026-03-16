# Vibe Workflow Guide

> Keyword-based behavior control system

---

## Overview

The Vibe system controls Claude's behavior via natural language keywords.
Provides 13 Vibe Keywords and 4 Mode Keywords.

---

## Vibe Keywords Workflow

### 1. fast (qk)

```
User: "fast create a login form"
         │
         ▼
┌─────────────────────────────┐
│ Keyword detected: "fast"    │
├─────────────────────────────┤
│ Actions:                    │
│ ├── Writer-Reviewer: 3 max  │
│ ├── Validation: skip        │
│ └── Immediate code gen      │
└─────────────────────────────┘
         │
         ▼
   [Output result directly]
```

### 2. experiment (exp)

```
User: "experiment mode apply new algorithm"
         │
         ▼
┌─────────────────────────────┐
│ 1. Create current snapshot  │
├─────────────────────────────┤
│ 2. Apply experimental code  │
├─────────────────────────────┤
│ 3. Check result             │
│    ├── Success: "Keep it?"  │
│    └── Failure: "Rollback?" │
└─────────────────────────────┘
```

### 3. parallel (para)

```
User: "parallel create 3 APIs"
         │
         ▼
┌─────────────────────────────┐
│ 1. Task decomposition       │
│    ├── API 1: /users        │
│    ├── API 2: /posts        │
│    └── API 3: /comments     │
├─────────────────────────────┤
│ 2. Dependency analysis      │
│    └── Independent → parallel│
├─────────────────────────────┤
│ 3. Adaptive parallel exec   │
│    └── Start 10 concurrent  │
└─────────────────────────────┘
```

### 4. fix

```
User: "fix this error"
         │
         ▼
┌─────────────────────────────┐
│ 1. Search Error KB          │
│    └── Jaccard 70%+ similar │
├─────────────────────────────┤
│ 2. Similar error found?     │
│    ├── Yes: Apply prev fix  │
│    └── No: New analysis     │
├─────────────────────────────┤
│ 3. Ralph Loop (max 10)      │
│    └── Auto fix attempts    │
├─────────────────────────────┤
│ 4. On success: KB learns    │
└─────────────────────────────┘
```

### 5. undo

```
User: "undo recent changes"
         │
         ▼
┌─────────────────────────────┐
│ 1. Query snapshot list      │
├─────────────────────────────┤
│ 2. Select last snapshot     │
├─────────────────────────────┤
│ 3. Execute rollback         │
│    └── Restore files        │
├─────────────────────────────┤
│ 4. "Restoration complete"   │
└─────────────────────────────┘
```

### 6. continue (cont)

```
User: "continue yesterday's work"
         │
         ▼
┌─────────────────────────────┐
│ 1. Load STATE.md            │
├─────────────────────────────┤
│ 2. Restore TodoWrite items  │
├─────────────────────────────┤
│ 3. Load context summary     │
├─────────────────────────────┤
│ 4. Confirm resume point     │
│    └── "Continuing here"    │
└─────────────────────────────┘
```

---

## Mode Keywords Workflow

### ultrawork (ulw)

```
User: "ultrawork mode full refactoring"
         │
         ▼
┌─────────────────────────────┐
│ Personas activated:         │
│ ├── explorer: code explore  │
│ ├── librarian: doc reference│
│ └── analyzer: analysis      │
├─────────────────────────────┤
│ Actions:                    │
│ ├── Maximize parallel       │
│ ├── All analysis tools on   │
│ └── Deep search mode        │
└─────────────────────────────┘
```

### deepsearch (ds)

```
User: "deepsearch React 19 new features"
         │
         ▼
┌─────────────────────────────┐
│ /research skill activated   │
├─────────────────────────────┤
│ 1. Execute web search       │
├─────────────────────────────┤
│ 2. Crawl documentation      │
├─────────────────────────────┤
│ 3. Summarize and analyze    │
├─────────────────────────────┤
│ 4. Organize sources         │
└─────────────────────────────┘
```

### strategic (str)

```
User: "strategic mode review architecture"
         │
         ▼
┌─────────────────────────────┐
│ architect persona activated │
├─────────────────────────────┤
│ Analysis:                   │
│ ├── Tradeoff analysis       │
│ ├── Long-term impact        │
│ └── Red/Blue Team analysis  │
├─────────────────────────────┤
│ Output:                     │
│ ├── 🔵 Blue Team (strengths)│
│ └── 🔴 Red Team (weaknesses)│
└─────────────────────────────┘
```

### visual (vis)

```
User: "visual mode analyze this screenshot"
         │
         ▼
┌─────────────────────────────┐
│ Personas activated:         │
│ ├── multimodal: visual      │
│ └── frontend: UI expert     │
├─────────────────────────────┤
│ Analysis:                   │
│ ├── Image recognition       │
│ ├── UI element detection    │
│ └── Improvement suggestions │
└─────────────────────────────┘
```

---

## Keyword Combination Examples

```yaml
# Fast parallel execution
"fast parallel create 3 components"
→ Writer-Reviewer minimal + parallel execution

# Strategic analysis then fix
"strategic mode analyze then fix"
→ Tradeoff analysis + Error KB auto-fix

# Experiment then test
"experiment mode apply and test"
→ Snapshot create + apply code + run tests
```
