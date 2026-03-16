---
description: "에이전트 생성 | Spawn agent"
argument-hint: "[agent_type]"
---

# Spawn Agent

Create agents for specific tasks.

## Usage

```
/sc:spawn explorer         # Explorer agent
/sc:spawn analyzer         # Analyzer agent
/sc:spawn --parallel 3     # Parallel agents
```

## Agent Types

- explorer: Code exploration
- analyzer: Analysis
- reviewer: Review
- implementer: Implementation
