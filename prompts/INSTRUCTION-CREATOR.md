# Instruction File Generator (for Claude Code)

> **Purpose**: Provide this file to Claude Code to auto-generate high-quality instruction files.

---

## How to Use

```bash
# Request in Claude Code like this:
"Based on this instruction-creator.md file, create an instruction file for [topic]"

# Examples:
"Based on this file, create an 'API Design Guide' instruction file"
"Based on this file, create 'React Component Writing Rules' instructions"
```

---

## Generation Principles (Rules for Claude to Follow)

### Phase 1: Strategy Development

#### Goal Definition Template
```markdown
# [Instruction Title]

## Goal
**Primary Outcome**: Following this instruction produces [specific deliverable].
- Example: "Production-deployable API documentation"
- Example: "PRD document for investor submission"

**Success Criteria**:
- [ ] [Measurable criterion 1] (e.g., 12+ of 15 sections completed)
- [ ] [Measurable criterion 2] (e.g., Test coverage 80%+)
- [ ] [Measurable criterion 3]

**Failure Cases** (Stop signals):
- If [situation 1] → Stop work and review
- If [situation 2] → [Provide alternative]
```

#### User Definition Template
```markdown
## Target Users
**Primary User**: [Specific role] (e.g., Senior backend developer, Startup PM)

**Usage Context**:
- Situation: [When to use]
- Purpose: [Why to use]
- Environment: [Where to use]

**Constraints**:
- Technical: [Limitations]
- Time: [Expected duration]
- Resources: [Required tools/knowledge]
```

---

### Phase 2: Structure Design (Most Important!)

#### Required Structure Rules

**1. Section Independence Principle**
```markdown
## [Section Number]. [Section Title]

### Section Overview
- **Goal**: Result from this section
- **Input**: Required prior information ("None" if none)
- **Output**: What you get on completion
- **Duration**: Approx. XX minutes

### Writing Guide
[Specific writing method]

### Completion Checklist
- [ ] [Required item 1]
- [ ] [Required item 2]

### Exception Handling
- **[If no data]**: → [Alternative]
- **[If too many options]**: → [Criteria]
```

**2. Table-Centric Design Rules**

Use tables for 60%+ instead of prose:

```markdown
# BAD Example (prose)
Competitor A has a strong brand, but the price is high...

# GOOD Example (table)
| Competitor | Strengths | Weaknesses | Priority |
|------------|-----------|------------|----------|
| A | Strong brand | High price | P0 |
| B | Low price strategy | Low quality | P1 |
```

**3. Unified Metadata Rules**

Use only these evaluation standards:

```markdown
# Standard Evaluation System
- Impact: H (High) / M (Medium) / L (Low)
- Priority: P0 (Critical) / P1 (Important) / P2 (Nice-to-have)
- Status: Complete / In Progress / Not Started / On Hold
- Grade: Excellent / Good / Needs Improvement
```

**4. Hierarchy Rules**

```markdown
# Top level (file title) - only 1
## Main sections (2 #) - recommend 5-9
### Sub-topics (3 #) - 3-7 per section
#### Detail items (4 #) - maximum depth

**Note**: ##### (5) is forbidden (too deep)
```

---

### Phase 3: Interface Design

#### Required Visual Elements

**1. Emoji System (use consistently)**
```markdown
Target/Purpose
List/Overview
Data/Analysis
Tip/Insight
Warning/Caution
Important/Urgent
Required item
Optional item
Time
Action/Execute
```

**2. Separator Usage Rules**
```markdown
# Clear separation between sections
---

## New section starts
```

---

### Phase 4: Quality Assurance

#### Required Inclusions

**1. Exception Handling Section (in all main sections)**
```markdown
### Exception Handling

#### If No Data
→ Mark as "[Research needed]" and proceed to next step

#### If Too Many Options
→ Select top 3 using [criteria]

#### If Conflicting Requirements
→ Use [priority matrix] to decide
```

**2. Good/Bad Examples (in key sections)**
```markdown
### Writing Examples

#### BAD Example
[Specific bad example]
**Problem**: [Why it's bad]

#### GOOD Example
[Specific good example]
**Benefit**: [Why it's good]
```

**3. Self-Diagnosis Checklist (at the end)**
```markdown
## Completion Self-Diagnosis

### Critical (Must Complete)
- [ ] [Required item 1]
- [ ] [Required item 2]

### Important (80%+ recommended)
- [ ] [Important item 1]
- [ ] [Important item 2]

### Nice-to-have (Optional)
- [ ] [Optional item 1]

**Pass Criteria**: Critical 100% + Important 80%+
```

---

### Phase 5: Execution Optimization

#### Required: Quick Start Guide (at file beginning)

```markdown
# Quick Start Guide

## Core Only (30-minute version)
1. **Section [X]**: Write [core item]
2. **Section [Y]**: Write [required item]
3. **Section [Z]**: Verify [deliverable]

→ This alone produces [minimum deliverable]!

## Full Version (2-4 hours)
- Core sections above + [additional sections]
- Include [detailed analysis]
- Complete [verification steps]

---
```

---

## Claude Code Generation Prompt Template

Request in Claude Code like this:

```
Create a "[topic]" instruction file with these criteria:

1. Filename: `[topic-english].md`

2. Required sections:
   - Goal definition (Phase 1 template)
   - Quick start guide (Phase 5 template)
   - 5-9 main sections (Phase 2 structure rules)
   - Exception handling per section (Phase 4)
   - Self-diagnosis checklist (Phase 4)
   - Usage guide (Phase 6)

3. Required rules:
   - Table/list ratio 60%+
   - Unified metadata (H/M/L, P0/P1/P2)
   - Emoji system
   - Maximum 4-level hierarchy (#### max)

4. Style:
   - Each section independently understandable
   - Rich examples (Good/Bad)
   - Clear placeholders ([XX], $XX)

Reference instruction-creator.md file.
```

---

## Generation Checklist (for Claude)

Claude Code, verify these when generating instruction files:

### Required Sections
- [ ] Goal definition (Primary Outcome, Success Criteria)
- [ ] Quick start guide (30-minute version)
- [ ] Usage guide (Pre-start check, Writing order)
- [ ] 5-9 main sections
- [ ] "Section Overview" in each section
- [ ] "Exception Handling" in each main section
- [ ] Self-diagnosis checklist
- [ ] Good/Bad examples (minimum 3)

### Style Compliance
- [ ] Tables/lists 60%+
- [ ] Consistent emoji usage
- [ ] Unified metadata (H/M/L, P0/P1/P2)
- [ ] Clear placeholders ([XX], $XX)
- [ ] Hierarchy within 4 levels (#### max)
- [ ] Section separators (---)

### Quality Criteria
- [ ] Each section independently understandable
- [ ] Measurable success criteria specified
- [ ] Actionable instructions (no abstract concepts)
- [ ] Exception handling methods provided

---

## Core Principles (What Claude Must Remember)

### 1. Modularity = Independence
```
Each section must work without other sections
→ Specify "Input/Output/Goal" per section
```

### 2. Consistency = Pattern Repetition
```
Apply same structure to all sections
→ "Overview → Writing Guide → Examples → Checklist"
```

### 3. Actionability = Specificity
```
"Modularize" (X) → "Create each section in ## format..." (O)
"See good examples" (X) → "Write as follows: [specific example]" (O)
```

### 4. Table-Centric = Scannability
```
3+ sentences of prose → Consider converting to table
3+ items → Always use table
```

### 5. Exception Handling = Prevent Blockage
```
Add "Exception Handling" to all main sections
Prepare for "No data?", "Too many options?"
```

---

## Final Instructions for Claude Code

**Claude Code, when creating instruction files:**

1. **Use all templates from this file as-is**
   - Copy-paste sections marked "template"
   - Only fill in content for the topic

2. **Follow required 5-step order**
   ```
   Step 1: Goal definition → Use Phase 1 template
   Step 2: Quick start guide → Use Phase 5 template
   Step 3: 5-9 main sections → Apply Phase 2 structure rules
   Step 4: Exception handling + Examples → Use Phase 4 templates
   Step 5: Usage guide + Checklist → Use Phase 6 templates
   ```

3. **Write table-centric**
   - 3+ items = Always table
   - Comparison/evaluation = Always table
   - Explanation only = Prose allowed

4. **Rich examples**
   - Examples for all placeholders
   - Good/Bad comparison examples
   - Actual usage scenario examples

5. **Verify before completion**
   - Check "Generation Checklist" above
   - Submit after all [ ] checked

**Following these rules produces 85%+ quality instruction files!**
