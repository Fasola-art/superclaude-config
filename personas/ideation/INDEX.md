# Ideation Persona Index

> **Total**: 27 expert personas
> **Activation**: Auto-triggered by keywords/phrases
> **Purpose**: Multi-perspective idea discussion and validation

---

## Persona Groups

### Business (Executives) - 6

| ID               | Name                | Core Role                    | Priority | Keywords                                        |
|------------------|---------------------|------------------------------|----------|-------------------------------------------------|
| `ceo`            | CEO                 | Strategic decision-making    | 82       | CEO, strategy, decision-making, business model  |
| `cfo`            | CFO                 | Financial analysis / ROI     | 81       | finance, ROI, cost, monetization, budget        |
| `coo`            | COO                 | Operations / Process         | 80       | operations, process, resources, efficiency      |
| `legal`          | Legal Counsel       | Legal review / Compliance    | 79       | legal, regulation, contract, IP, compliance     |
| `sales`          | Sales Lead          | Customer value / Revenue     | 78       | sales, pricing strategy, B2B, B2C               |
| `bd`             | Business Dev        | Partnership / Expansion      | 77       | partnership, alliance, new business, MOU        |

### Marketing - 5

| ID               | Name                | Core Role                    | Priority | Keywords                                        |
|------------------|---------------------|------------------------------|----------|-------------------------------------------------|
| `marketing`      | Marketing Strategist| Branding / Positioning       | 76       | marketing, branding, positioning, targeting     |
| `growth`         | Growth Hacker       | Growth hacking / Experiments | 75       | growth, AARRR, A/B test, funnel                 |
| `content`        | Content Strategist  | Storytelling / Channels      | 74       | content, storytelling, social media             |
| `community`      | Community Manager   | Engagement / Loyalty         | 73       | community, fandom, engagement, loyalty          |
| `pr`             | PR Specialist       | Public relations / Media     | 72       | PR, publicity, media, press release             |

### Innovation - 5

| ID               | Name                | Core Role                    | Priority | Keywords                                        |
|------------------|---------------------|------------------------------|----------|-------------------------------------------------|
| `innovator`      | Innovator           | New tech / Trends            | 71       | innovation, new tech, trends                    |
| `futurist`       | Futurist            | Long-term outlook / Scenario | 70       | future, forecast, prediction, megatrend         |
| `visionary`      | Visionary           | Vision / Big picture         | 69       | vision, mission, goals, inspiration             |
| `disruptor`      | Disruptor           | Disruptive innovation        | 68       | disruption, disruptive innovation, contrarian   |
| `inventor`       | Inventor            | Novel solutions              | 67       | invention, patent, tech combination, originality|

### Design (Design/UX) - 3

| ID               | Name                | Core Role                    | Priority | Keywords                                        |
|------------------|---------------------|------------------------------|----------|-------------------------------------------------|
| `designer`       | Designer            | Visual design / Aesthetics   | 66       | design, visual design, brand                    |
| `ux`             | UX Designer         | User experience / Flow       | 65       | UX, user experience, usability, flow            |
| `user_advocate`  | User Advocate       | Accessibility / Needs        | 64       | user, accessibility, needs, pain points         |

### Validation - 4

| ID               | Name                | Core Role                    | Priority | Keywords                                        |
|------------------|---------------------|------------------------------|----------|-------------------------------------------------|
| `critic`         | Critic              | Critical analysis / Weakness | 63       | critique, criticism, weakness, improvement      |
| `realist`        | Realist             | Feasibility                  | 62       | realism, feasibility, resources                 |
| `devil_advocate` | Devil's Advocate    | Counter-argument / Alts      | 61       | counter-argument, rebuttal, alternative         |
| `risk_analyst`   | Risk Analyst        | Risk factors / Mitigation    | 60       | risk, danger, mitigation, scenario              |

### Research - 3

| ID               | Name                | Core Role                    | Priority | Keywords                                        |
|------------------|---------------------|------------------------------|----------|-------------------------------------------------|
| `researcher`     | Researcher          | Market research / Data       | 59       | research, survey, data, market analysis         |
| `ethnographer`   | Ethnographer        | User observation / Behavior  | 58       | ethnography, observation, behavior analysis     |
| `competitor`     | Competitive Analyst | Benchmarking / Differentiation| 57      | competitive analysis, benchmarking, differentiation|

### Special - 1

| ID               | Name                | Core Role                    | Priority | Keywords                                        |
|------------------|---------------------|------------------------------|----------|-------------------------------------------------|
| `moderator`      | Moderator           | Discussion facilitation      | 56       | summarize, consensus, conclusion, synthesis     |

---

## Persona Activation Rules

### Priority Levels

| Level    | Value | Description                                |
|----------|-------|--------------------------------------------|
| Highest  | 80+   | Executives (CEO, CFO, COO, Legal)          |
| High     | 70-79 | Marketing, Sales, Business Development     |
| Medium   | 60-69 | Innovation, Design, Validation             |
| Low      | 56-59 | Research, Moderator                        |

### Keyword Matching Rules

1. **Exact keyword match takes precedence**
   - "ROI analysis" → `cfo` (exact match)
   - "A/B test design" → `growth` (exact match)

2. **Compound keyword handling**
   - Multiple persona keywords detected → higher priority persona takes precedence
   - Same priority → persona with more keyword matches wins

3. **Ambiguous cases**
   - Use `/ideation` command for multi-persona discussion
   - Example: "new service idea" → requires multiple perspectives

---

## Persona Delegation Rules

### Delegation Hierarchy

```
ceo (final decision-maker)
    ├── cfo (financial questions)
    ├── coo (operational questions)
    ├── legal (legal questions)
    ├── marketing (marketing questions)
    └── bd (partnership questions)

marketing (marketing lead)
    ├── growth (growth metrics)
    ├── content (content)
    ├── community (community)
    └── pr (public relations)

moderator (discussion facilitator)
    └── synthesizes all persona opinions
```

### Delegation Examples

| Question                      | Assigned Persona   | Reason                   |
|-------------------------------|--------------------|--------------------------|
| "Business strategy direction?"| `ceo`              | Strategic decision       |
| "Expected revenue?"           | `cfo`              | Financial analysis       |
| "Legal risks?"                | `legal`            | Legal review             |
| "Target customers?"           | `marketing`        | Marketing strategy       |
| "Competitor analysis?"        | `competitor`       | Competitive analysis     |
| "Is it feasible?"             | `realist`          | Feasibility check        |
| "Counter-arguments?"          | `devil_advocate`   | Critical review          |

---

## /ideation Multi-Persona Discussion

### Default Configuration

When `/ideation` command executes, the following persona combination engages:

| Role     | Persona           | Perspective              |
|----------|-------------------|--------------------------|
| Strategy | `ceo`             | Business strategy        |
| Finance  | `cfo`             | ROI, costs               |
| Ops      | `coo`             | Execution feasibility    |
| Customer | `user_advocate`   | User needs               |
| Critic   | `devil_advocate`  | Counter-arguments        |
| Facilitator | `moderator`    | Opinion synthesis        |

### Discussion Flow

```
1. ceo: Present strategic perspective
2. cfo: Evaluate financial viability
3. coo: Assess operational feasibility
4. user_advocate: Provide user perspective feedback
5. devil_advocate: Critical review
6. moderator: Synthesize opinions and conclude
```

---

## Activation Examples

```
"Create new product launch strategy"
→ ceo, marketing, cfo activated (strategy, marketing, finance)

"Brand renewal ideas"
→ marketing, designer, content activated

"Startup fundraising prep"
→ ceo, cfo, bd activated

"New technology adoption review"
→ innovator, cto, risk_analyst activated

"Need market research"
→ researcher, competitor activated
```

---

## Group Synergies

| Combination         | Personas                             | Synergy                           |
|---------------------|--------------------------------------|-----------------------------------|
| Strategy Planning   | ceo + cfo + coo                      | Strategy-Finance-Execution        |
| Marketing Campaign  | marketing + content + growth         | Strategy-Content-Growth           |
| Product Development | ux + designer + user_advocate        | Design-Experience-Needs           |
| Risk Review         | legal + risk_analyst + realist       | Legal-Risk-Feasibility            |
| Innovation Exploration | innovator + futurist + disruptor  | Tech-Future-Disruption            |

---

**META**
- Created: 2026-01-30
- Updated: 2026-01-30
- Count: 27 personas
- Groups: 7 (Business, Marketing, Innovation, Design, Validation, Research, Special)
- Version: 2.0 (individual file separation complete)
