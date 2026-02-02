# Research Orchestrator

Conduct systematic research on complex topics and generate comprehensive reports.

## Usage
```
/orchestrator <research topic>
/orchestrator Impact of AI on encryption
/orchestrator 2026 Korean real estate market outlook
```

## Workflow

```
1. Query Analysis    → Clarify question
2. Research Brief    → Structure research questions
3. Strategy          → Establish research strategy
4. Parallel Research → Execute parallel research
5. Synthesis         → Consolidate results
6. Report            → Generate final report
```

## Agents Used

| Agent | Role |
|-------|------|
| `research-orchestrator` | Overall coordination |
| `academic-researcher` | Academic research |
| `technical-researcher` | Technical investigation |
| `data-analyst` | Data analysis |
| `fact-checker` | Fact verification |
| `research-synthesizer` | Result consolidation |
| `report-generator` | Report generation |

---

**Execution Instructions:**

When this command is invoked:

1. Invoke `research-orchestrator` agent using Task tool
2. Pass user's research topic
3. Orchestrator automatically coordinates required agents sequentially/in parallel
4. Return final report to user

**Example invocation:**
```
Task tool usage:
- subagent_type: research-orchestrator (or general-purpose if unavailable)
- prompt: "Conduct comprehensive research using Open Deep Research methodology on the following topic: [topic]"
```
