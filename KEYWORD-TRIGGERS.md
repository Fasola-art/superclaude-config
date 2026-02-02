# SuperClaude Keyword Trigger System

> Vibe Keywords (13) + Mode Keywords (4) Detailed Definitions

---

## Vibe Keywords (13)

### 1. quick (qk)
```yaml
trigger: ["quick", "qk", "fast", "urgent", "immediately"]
action:
  - Skip verification steps
  - Writer-Reviewer minimal mode (3 iterations)
  - Execute immediately
use_case: "quick build login form"
```

### 2. experiment (exp)
```yaml
trigger: ["experiment", "exp", "test", "try"]
action:
  - Create current state snapshot
  - Execute experimental code
  - Provide rollback option
use_case: "experiment with new algorithm"
```

### 3. parallel (para)
```yaml
trigger: ["parallel", "para", "concurrent", "simultaneously"]
action:
  - Activate adaptive parallel execution
  - Process independent tasks concurrently
  - Auto-detect dependencies
use_case: "parallel create 3 components"
```

### 4. fix
```yaml
trigger: ["fix", "repair", "debug", "bug"]
action:
  - Search Error KB (Jaccard 70%+)
  - Activate Ralph Loop (max 10 attempts)
  - Auto-fix attempt
use_case: "fix this error"
```

### 5. undo
```yaml
trigger: ["undo", "rollback", "revert", "cancel"]
action:
  - Retrieve last snapshot
  - Execute rollback
  - Preserve changes option
use_case: "undo recent changes"
```

### 6. continue (cont)
```yaml
trigger: ["continue", "cont", "resume", "proceed"]
action:
  - Restore STATE.md
  - Load previous context
  - Resume from breakpoint
use_case: "continue yesterday's work"
```

### 7. check (chk)
```yaml
trigger: ["check", "chk", "verify", "validate"]
action:
  - TypeScript type check
  - ESLint check
  - Build check
  - Bundle size analysis
use_case: "check all code"
```

### 8. test (tst)
```yaml
trigger: ["test", "tst", "run tests"]
action:
  - Find related test files
  - Execute tests
  - Coverage report
use_case: "test auth module"
```

### 9. deploy (dep)
```yaml
trigger: ["deploy", "dep", "release"]
action:
  - Run deployment checklist
  - Performance check
  - Update ROADMAP.md
use_case: "deploy to staging"
```

### 10. cleanup (clean)
```yaml
trigger: ["cleanup", "clean", "tidy"]
action:
  - Remove unused imports
  - Remove console.log
  - Remove dead code
  - Formatting
use_case: "cleanup this file"
```

### 11. performance (perf)
```yaml
trigger: ["performance", "perf", "optimize"]
action:
  - Full project performance analysis
  - Identify bottlenecks
  - Auto-fix suggestions
use_case: "performance analysis"
```

### 12. plan
```yaml
trigger: ["plan", "design", "architect"]
action:
  - Create .planning/ directory
  - Generate PROJECT.md
  - Generate ROADMAP.md
  - Generate STATE.md
use_case: "plan the project"
```

### 13. analyze (map)
```yaml
trigger: ["analyze", "map", "mapping", "structure"]
action:
  - Full codebase analysis
  - Auto-generate 7 documents
  - Dependency graph
use_case: "analyze this project"
```

---

## Mode Keywords (4)

### 1. ultrawork (ulw)
```yaml
trigger: ["ultrawork", "ulw", "maximum performance"]
activated_personas: [explorer, librarian, analyzer]
behavior:
  - Maximize parallel execution
  - Activate all analysis tools
  - Deep search mode
use_case: "ultrawork mode for full refactoring"
```

### 2. deepsearch (ds)
```yaml
trigger: ["deepsearch", "ds", "deep search"]
activated_personas: [explorer]
behavior:
  - Activate /research skill
  - Include web search
  - Document crawling
use_case: "deepsearch latest React patterns"
```

### 3. strategic (str)
```yaml
trigger: ["strategic", "str", "strategy"]
activated_personas: [architect]
behavior:
  - Trade-off analysis
  - Long-term impact consideration
  - Red Team / Blue Team analysis
use_case: "strategic architecture review"
```

### 4. visual (vis)
```yaml
trigger: ["visual", "vis", "image"]
activated_personas: [multimodal, frontend]
behavior:
  - Screenshot analysis
  - Image processing
  - UI visual review
use_case: "visual analyze this screenshot"
```

---

## Keyword Detection Priority

1. Mode Keywords (global mode change)
2. Vibe Keywords (work style change)
3. Security keywords (force persona activation)
4. General keywords (default processing)

---

## Combination Examples

```bash
# parallel + quick
"parallel quick create 3 APIs"

# strategic + analyze
"strategic mode analyze current architecture"

# experiment + test
"experiment new algorithm and test"
```
