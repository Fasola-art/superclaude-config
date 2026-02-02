# Dynamic Context Pruning (DCP) Rules

> SuperClaude v4.1 - Automatic Context Management System

---

## Overview

DCP (Dynamic Context Pruning) efficiently manages the Claude Code session context window.
Automatically cleans unnecessary information based on context usage to ensure session continuity.

---

## Thresholds (Optimized for Mac Studio Ultra M2)

| Level | Threshold | Action | Alert |
|-------|-----------|--------|-------|
| Normal | < 75% | Monitor only | None |
| Warning | 75% | Show warning | `Warning: Context 75%` |
| Critical | 90% | Suggest auto DCP | `Critical: Context 90% - Compression recommended` |
| Emergency | 95% | Force compression | `Emergency: Context 95% - Force compression` |

---

## DCP Strategies

### 1. Deduplication

```yaml
deduplication:
  file_reads:
    rule: "Same file repeated reads -> Keep only latest result"
    action: "Remove previous Read results"
  bash_outputs:
    rule: "Same command repeated -> Keep only last result"
    action: "Remove previous Bash outputs"
  grep_results:
    rule: "Same pattern search -> Keep only latest result"
    action: "Remove previous Grep results"
```

### 2. Error Cleanup

```yaml
error_cleanup:
  resolved_errors:
    rule: "Resolved error messages -> Delete"
    condition: "When same command succeeds"
  duplicate_errors:
    rule: "Same error repeated -> Keep first + count only"
    format: "[Error message] (occurred N times)"
  stack_traces:
    rule: "Stack traces repeated 3+ times -> Replace with summary"
    action: "Keep only key lines"
```

### 3. File Summarization

```yaml
file_summarize:
  large_files:
    threshold: 2000  # lines
    rule: "2000+ line files -> Keep only relevant sections"
    action: "Preserve only requested sections"
  log_outputs:
    threshold: 50  # lines
    rule: "Log outputs -> Keep only last 50 lines"
    action: "Remove previous logs"
  config_files:
    rule: "Config files -> Keep only changed parts"
    action: "Compress to diff format"
```

---

## Preserved Items (Never Delete)

```yaml
preserve_always:
  - "Current task context"
  - "Active TodoWrite items"
  - "Recently modified file list"
  - "CLAUDE.md core rules"
  - "Current errors and fix attempts"
  - "User explicit request content"
```

---

## Auto-Execution Conditions

### 90% Auto DCP

```yaml
auto_dcp_at_90:
  trigger: "Context usage >= 90%"
  actions:
    1: "Execute deduplication strategy"
    2: "Execute error cleanup strategy"
    3: "Execute file summarization strategy"
  report:
    format: "DCP executed: [X] tokens freed. Current usage: [Y]%"
```

### 95% Emergency Compression

```yaml
emergency_at_95:
  trigger: "Context usage >= 95%"
  actions:
    1: "Force execute all DCP strategies"
    2: "Remove old file contents"
    3: "Create session archive"
  warning: "Session continuity at risk - Immediate cleanup required"
```
