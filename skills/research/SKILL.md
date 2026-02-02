# /research - General Deep Research Skill

> **Version**: 1.0.0
> **Alias**: /ds, deepsearch
> **Persona**: explorer

---

## Overview

General deep research skill. Performs various research tasks from codebase analysis to web research.

## Triggers

- `/research [topic]`
- `/ds [topic]`
- `ds quick [topic]` - Quick mode (skip questions)
- `deepsearch [topic]`

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    /RESEARCH WORKFLOW                            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: Input Analysis                                          │
├─────────────────────────────────────────────────────────────────┤
│  User Input                                                      │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                             │
│  │ Trigger Detection│                                            │
│  │ - /research      │                                            │
│  │ - ds / ds quick  │                                            │
│  │ - deepsearch     │                                            │
│  └─────────────────┘                                             │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐     ┌────────────────────────────────────┐  │
│  │ Auto-detect     │────▶│ 10 Preset Matching                 │  │
│  │ Preset          │     │ market_research / competitor_analysis│ │
│  └─────────────────┘     │ tech_research / academic_research   │  │
│                          │ decision_support / general_inquiry  │  │
│                          │ product_review / how_to             │  │
│                          │ news_analysis / troubleshooting     │  │
│                          └────────────────────────────────────┘  │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                             │
│  │ Set Defaults    │                                             │
│  │ - depth: preset │                                             │
│  │ - format: preset│                                             │
│  │ - breadth: auto │                                             │
│  └─────────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: Pre-questions (with AI Ideas)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│     ┌──────────────────────┐                                     │
│     │ Using "ds quick"?    │                                     │
│     └──────────────────────┘                                     │
│          │           │                                           │
│        YES          NO                                           │
│          │           │                                           │
│          ▼           ▼                                           │
│     ┌────────┐  ┌──────────────────────────────┐                 │
│     │  Skip  │  │ Present AI Ideas             │                 │
│     │ Go to  │  │                              │                 │
│     │ Phase 3│  │ "[AI Analysis] Research from:│                 │
│     └────────┘  │  1. [Perspective 1] - reason │                 │
│                 │  2. [Perspective 2] - reason │                 │
│                 │  3. [Perspective 3] - reason │                 │
│                 │                              │                 │
│                 │  Any additional requests?"   │                 │
│                 └──────────────────────────────┘                 │
│                           │                                      │
│                           ▼                                      │
│                 ┌──────────────────────────────┐                 │
│                 │ Collect User Feedback        │                 │
│                 │ - Additional perspectives    │                 │
│                 │ - Length/format changes      │                 │
│                 │ - Scope adjustments          │                 │
│                 └──────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: Research Execution                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                 ┌──────────────────────────────┐                 │
│                 │    Parallel Search Execution │                 │
│                 └──────────────────────────────┘                 │
│                           │                                      │
│     ┌─────────────────────┼─────────────────────┐                │
│     │                     │                     │                │
│     ▼                     ▼                     ▼                │
│ ┌───────────┐       ┌───────────┐       ┌───────────┐           │
│ │ WebSearch │       │ WebSearch │       │ WebSearch │    ...    │
│ │  Query 1  │       │  Query 2  │       │  Query 3  │           │
│ │           │       │           │       │           │           │
│ │ [topic]   │       │ [topic]   │       │ [topic]   │           │
│ │ market    │       │ trends    │       │ key       │           │
│ │ size      │       │ 2026      │       │ players   │           │
│ └───────────┘       └───────────┘       └───────────┘           │
│     │                     │                     │                │
│     └─────────────────────┼─────────────────────┘                │
│                           ▼                                      │
│                 ┌──────────────────────────────┐                 │
│                 │ Aggregate Results            │                 │
│                 │ (breadth × queries)          │                 │
│                 └──────────────────────────────┘                 │
│                           │                                      │
│                           ▼                                      │
│                 ┌──────────────────────────────┐                 │
│                 │        Fetch Pages           │                 │
│                 └──────────────────────────────┘                 │
│                           │                                      │
│     ┌─────────────────────┼─────────────────────┐                │
│     │                     │                     │                │
│     ▼                     ▼                     ▼                │
│ ┌───────────┐       ┌───────────┐       ┌───────────┐           │
│ │ WebFetch  │       │ WebFetch  │       │ WebFetch  │    ...    │
│ │ Source 1  │       │ Source 2  │       │ Source 3  │           │
│ │ Official  │       │ News      │       │ Research  │           │
│ │ Docs      │       │ Article   │       │ Report    │           │
│ └───────────┘       └───────────┘       └───────────┘           │
│     │                     │                     │                │
│     └─────────────────────┼─────────────────────┘                │
│                           ▼                                      │
│                 ┌──────────────────────────────┐                 │
│                 │ depth >= deep?               │                 │
│                 └──────────────────────────────┘                 │
│                     │               │                            │
│                   YES              NO                            │
│                     │               │                            │
│                     ▼               ▼                            │
│           ┌─────────────────┐  ┌────────┐                        │
│           │ Cross-validation│  │  Skip  │                        │
│           └─────────────────┘  └────────┘                        │
│                     │                                            │
│                     ▼                                            │
│           ┌─────────────────────────────────┐                    │
│           │ Cross-validation (3 sources)    │                    │
│           │                                 │                    │
│           │ Fact 1: ✅A ✅B ✅C → Verified   │                    │
│           │ Fact 2: ✅A ✅B ❌C → Mostly OK  │                    │
│           │ Fact 3: ✅A ❌B ❌C → Mismatch   │                    │
│           └─────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Phase 4: Result Generation                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                 ┌──────────────────────────────┐                 │
│                 │      Reliability Rating      │                 │
│                 │                              │                 │
│                 │ ⭐⭐⭐⭐⭐ (5): Official docs, academic papers│   │
│                 │ ⭐⭐⭐⭐ (4): Trusted news (Reuters, NYT)    │   │
│                 │ ⭐⭐⭐ (3): General news, industry blogs    │   │
│                 │ ⭐⭐ (2): Personal blogs, outdated sources  │   │
│                 │ ⭐ (1): Unknown sources, hard to verify     │   │
│                 └──────────────────────────────┘                 │
│                           │                                      │
│                           ▼                                      │
│     ┌─────────────────────┬─────────────────────┐                │
│     │                     │                     │                │
│     ▼                     ▼                     ▼                │
│ ┌───────────┐       ┌───────────┐       ┌─────────────┐         │
│ │  Report   │       │  Summary  │       │  Comparison │         │
│ │  5-10p    │       │   1-2p    │       │    2-5p     │         │
│ │           │       │           │       │             │         │
│ │ Structure:│       │ Structure:│       │ Structure:  │         │
│ │ -Summary  │       │ -Summary  │       │ -Comp table │         │
│ │ -Background│      │ -Points   │       │ -Details    │         │
│ │ -Analysis │       │ -Table    │       │ -Pros/cons  │         │
│ │ -Forecast │       │ -Sources  │       │ -Recommend  │         │
│ │ -Conclusion│      └───────────┘       └─────────────┘         │
│ │ -References│                                                   │
│ └───────────┘                                                    │
│                           │                                      │
│                           ▼                                      │
│                 ┌──────────────────────────────┐                 │
│                 │         Final Output         │                 │
│                 │                              │                 │
│                 │ ■ Metadata                   │                 │
│                 │  - Depth: [level]            │                 │
│                 │  - Sources: [N]              │                 │
│                 │  - Reliability: ⭐⭐⭐⭐      │                 │
│                 │  - Cross-validated: ✅/❌    │                 │
│                 │                              │                 │
│                 │ Content                      │                 │
│                 │ [Selected format content]    │                 │
│                 │                              │                 │
│                 │ References                   │                 │
│                 │ [Sorted by reliability]      │                 │
│                 │                              │                 │
│                 │ Further Research Suggestions │                 │
│                 │ [Related topic recommendations]│               │
│                 └──────────────────────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Sequence Diagram

```
┌──────────┐  ┌─────────────┐  ┌────────────────┐  ┌───────────┐  ┌───────────┐
│   User   │  │Skill Router │  │Preset Detector │  │ WebSearch │  │ WebFetch  │
└────┬─────┘  └──────┬──────┘  └───────┬────────┘  └─────┬─────┘  └─────┬─────┘
     │               │                 │                 │               │
     │ "ds AI market"│                 │                 │               │
     │──────────────▶│                 │                 │               │
     │               │                 │                 │               │
     │               │ detect_preset() │                 │               │
     │               │────────────────▶│                 │               │
     │               │                 │                 │               │
     │               │ market_research │                 │               │
     │               │◀────────────────│                 │               │
     │               │                 │                 │               │
     │ AI ideas      │                 │                 │               │
     │◀──────────────│                 │                 │               │
     │               │                 │                 │               │
     │ "proceed"     │                 │                 │               │
     │──────────────▶│                 │                 │               │
     │               │                 │                 │               │
     │               │ search_queries (parallel)        │               │
     │               │────────────────────────────────▶│               │
     │               │                 │                 │               │
     │               │                 │     results[]   │               │
     │               │◀────────────────────────────────│               │
     │               │                 │                 │               │
     │               │ fetch_pages (parallel)           │               │
     │               │─────────────────────────────────────────────────▶│
     │               │                 │                 │               │
     │               │                 │                 │   content[]   │
     │               │◀─────────────────────────────────────────────────│
     │               │                 │                 │               │
     │ Final report  │                 │                 │               │
     │◀──────────────│                 │                 │               │
     │               │                 │                 │               │
```

---

## Presets

| Preset | Description | Default Depth | Default Format |
|--------|-------------|---------------|----------------|
| market_research | Market size, trends, competitors | deep | report |
| competitor_analysis | A vs B comparison | deep | comparison |
| tech_research | Tech stack, frameworks | medium | report |
| academic_research | Academic research, papers | deep | report |
| decision_support | Decision support | medium | comparison |
| general_inquiry | General questions | quick | summary |
| product_review | Product reviews | medium | comparison |
| how_to | Methods, tutorials | quick | summary |
| news_analysis | News, current affairs | medium | report |
| troubleshooting | Problem solving, debugging | quick | summary |

Detailed preset definitions: [references/presets.md](references/presets.md)

---

## Depth Levels

| Level | Queries | Sources | Cross-validation | Description |
|-------|---------|---------|------------------|-------------|
| quick | 3 | 5 | No | Quick overview |
| medium | 5 | 10 | No | Balanced analysis |
| deep | 8 | 20 | Yes | In-depth research |
| exhaustive | 12 | 30+ | Yes | Comprehensive investigation |

---

## Output Formats

| Format | Length | Structure |
|--------|--------|-----------|
| summary | 1-2p | Summary, points, table, sources |
| report | 5-10p | Summary, background, analysis, forecast, conclusion, references |
| comparison | 2-5p | Comparison table, detailed comparison, pros/cons, recommendation |

Detailed format definitions: [references/formats.md](references/formats.md)

---

## Usage Examples

### Basic Usage
```
/research AI agent market trends
```

### Quick Mode (Skip Questions)
```
ds quick WebSocket vs SSE
```
→ Execute comparison analysis immediately (no pre-questions)

### Comparison Analysis (Auto-detect → competitor_analysis)
```
ds Compare Notion vs Obsidian
```
→ Output in Comparison format
- Comparison table
- Detailed comparison (sync, plugins, pricing, etc.)
- Pros/cons
- Recommendation

---

## Keyword Trigger Connection

`/research` / `ds` keywords detected in `~/.claude/scripts/hooks/keyword-detector.ts`:

```typescript
research: {
  description: 'General deep research (codebase + general)',
  personas: ['explorer'],
  triggers: ['ds', 'deepsearch', 'research'],
  skill: '/research'
}
```

---

## References

- [Preset Details](references/presets.md)
- [Output Format Details](references/formats.md)
