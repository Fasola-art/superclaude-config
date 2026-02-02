# Vibe Keywords Cheatsheet

> **Version**: 1.0.0
> **Updated**: 2026-01-30

---

## Quick Reference

### Most Used Keywords

| Keyword | Alias | Action | Usage Example |
|---------|-------|--------|---------------|
| **quick** | qk | Skip verification, execute immediately | "quick build this function" |
| **fix** | - | Error KB + auto recovery | "fix this error" |
| **check** | chk | Type + Lint + Build verification | "check this code" |
| **parallel** | para | Parallel agent execution | "parallel do these 3 tasks" |

---

## Keywords by Category

### Execution Control

| Keyword | Alias | Action | Details |
|---------|-------|--------|---------|
| **quick** | `qk` | Skip verification, execute immediately | Skip Writer-Reviewer |
| **experiment** | `exp` | Snapshot → Execute → Rollback option | Safe experimentation |
| **parallel** | `para` | Parallel agent execution | Max 24 (M2 Ultra) |

#### Usage Examples

```
"quick add console.log"
→ Immediately modify code without verification

"experiment with new algorithm"
→ Create snapshot, execute, rollback on failure

"parallel analyze these 5 files"
→ Process concurrently with parallel agents
```

---

### Fix/Recovery

| Keyword | Alias | Action | Details |
|---------|-------|--------|---------|
| **fix** | - | Error KB + Self-Healing | Max 10 auto attempts |
| **undo** | - | Rollback to last snapshot | git stash pop |
| **continue** | `cont` | Continue previous work | Restore STATE.md |

#### Usage Examples

```
"fix this TypeError"
→ Search Error KB + auto-fix attempt (max 10)

"undo"
→ Rollback recent changes

"continue"
→ Resume work interrupted from previous session
```

---

### Verification

| Keyword | Alias | Action | Checks |
|---------|-------|--------|--------|
| **check** | `chk` | Full verification | Type + Lint + Build + Bundle |
| **test** | `tst` | Run tests | Auto-identify related tests |

#### Usage Examples

```
"check this component"
→ TypeScript + ESLint + Build + Bundle size check

"test"
→ Auto-run tests related to changed code
```

---

### Deploy/Cleanup

| Keyword | Alias | Action | Details |
|---------|-------|--------|---------|
| **deploy** | `dep` | Deployment checklist | Performance + ROADMAP update |
| **cleanup** | `clean` | Code cleanup | Remove unused imports, console.log |

#### Usage Examples

```
"deploy"
→ Run pre-deploy checklist + performance check

"cleanup this file"
→ Remove unused code, console.log, comments
```

---

### Analysis/Planning

| Keyword | Alias | Action | Output |
|---------|-------|--------|--------|
| **performance** | `perf` | Performance analysis | Auto-fix suggestions |
| **plan** | - | Generate documents | PROJECT, ROADMAP, STATE |
| **analyze** | `map` | Codebase analysis | Generate 7 documents |

#### Usage Examples

```
"performance analysis"
→ Full project performance analysis + optimization suggestions

"plan the project"
→ Generate project documents in .planning/ folder

"analyze this codebase"
→ Generate structure, dependencies, complexity docs (7 total)
```

---

## Mode Keywords

| Keyword | Alias | Action | Activated Personas |
|---------|-------|--------|-------------------|
| **ultrawork** | `ulw` | Maximum performance agents | explorer, librarian, analyzer |
| **deepsearch** | `ds` | Deep research mode | explorer |
| **strategic** | `str` | Strategic analysis | architect |
| **visual** | `vis` | Image/screenshot analysis | multimodal, frontend |

#### Usage Examples

```
"ultrawork analyze this codebase"
→ Activate 3 personas in parallel, maximum performance

"deepsearch this library"
→ Web search + document analysis + summary

"strategic review architecture"
→ Trade-off analysis + decision support

"visual analyze this screenshot"
→ UI/UX analysis + improvement suggestions
```

---

## Keyword Combinations

### Frequently Used Combinations

| Combination | Action |
|-------------|--------|
| `quick fix` | Skip verification and fix error immediately |
| `parallel analyze` | Analyze codebase in parallel |
| `experiment performance` | Safely attempt performance optimization |
| `check test` | Verify then run tests |

### Usage Examples

```
"quick fix this null error"
→ Skip Writer-Reviewer + immediate fix

"parallel analyze these 3 modules"
→ Analyze concurrently with parallel agents

"experiment with performance optimization"
→ Snapshot then attempt optimization, rollback on failure
```

---

## Keyword Action Details

### quick (qk)

```yaml
Action:
  - Skip Writer-Reviewer loop
  - Minimize Quality Gate
  - Immediately modify code

When to Use:
  - Simple modifications
  - Urgent hotfixes
  - Prototyping

Caution:
  - Quality verification skipped
  - Not recommended for production code
```

### fix

```yaml
Action:
  1. Search Error KB for similar errors
  2. Attempt to apply solution
  3. Verify build/test
  4. Try different solution on failure (max 10)

Self-Healing:
  - Max 10 auto recovery attempts
  - Different approach each attempt
  - Learn to Error KB on success

Output:
  - Applied solution
  - Modified files list
  - Verification results
```

### parallel (para)

```yaml
Action:
  - Parallel agent execution
  - Auto-adjust concurrent count

Settings (superclaude-config.json):
  initial: 10        # Starting concurrent count
  scale_up: +5       # Increase on 3 consecutive successes
  scale_down: -3     # Decrease on 1 failure
  maximum: 24        # Maximum (M2 Ultra core count)
  minimum: 3         # Minimum

Adaptive:
  - Auto-adjust based on success rate
  - Decrease immediately on failure, increase gradually on success
```

---

## Cautions

| Keyword | Caution |
|---------|---------|
| `quick` | Quality verification skipped - not for production |
| `experiment` | Requires snapshot - check git status |
| `parallel` | CPU usage increases |
| `fix` | Max 10 attempts - may take time |
| `deploy` | Production impact - use carefully |

---

## References

| Document | Path |
|----------|------|
| Keyword Details | `~/.claude/KEYWORD-TRIGGERS.md` |
| Vibe Workflow | `~/.claude/docs/VIBE-WORKFLOW.md` |
| Settings Guide | `~/.claude/docs/SETTINGS-GUIDE.md` |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
