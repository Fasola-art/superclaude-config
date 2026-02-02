# PRD Workflow

> Product Requirements Document creation and management workflow

---

## Overview

PRD (Product Requirements Document) is a core document defining project requirements, goals, and scope.

---

## PRD Creation Process

### Step 1: Idea Collection
```
/prd-create [idea]
```

- Business viability review
- Market analysis
- Technical feasibility evaluation

### Step 2: Requirements Definition

```markdown
## Requirements

### Functional Requirements
- FR-001: [Feature description]
- FR-002: [Feature description]

### Non-Functional Requirements
- NFR-001: Performance - [Requirement]
- NFR-002: Security - [Requirement]
```

### Step 3: Scope Setting

```yaml
in_scope:
  - Core feature A
  - Core feature B

out_of_scope:
  - Future development features
  - Excluded items
```

### Step 4: Milestone Definition

```markdown
## Milestones

| Phase | Goal | Deliverables      |
|-------|------|-------------------|
| M1    | MVP  | Core features     |
| M2    | Beta | Extended features |
| M3    | GA   | Complete product  |
```

---

## PRD Template

```markdown
# [Project Name] PRD

## 1. Overview
### 1.1 Purpose
### 1.2 Background
### 1.3 Goals

## 2. Users
### 2.1 Target Users
### 2.2 User Stories

## 3. Requirements
### 3.1 Functional Requirements
### 3.2 Non-Functional Requirements

## 4. Design
### 4.1 System Architecture
### 4.2 Data Model

## 5. Milestones
### 5.1 Schedule
### 5.2 Deliverables

## 6. Risks
### 6.1 Technical Risks
### 6.2 Mitigation Strategies
```

---

## Related Commands

| Command           | Description      |
|-------------------|------------------|
| `/prd-create`     | Create PRD       |
| `/project-plan`   | Project planning |
| `/project-status` | Check progress   |
