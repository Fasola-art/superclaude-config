---
name: project-scaffold
description: Project generation with Starter/Dynamic/Enterprise levels.
version: "2.0.0"
triggers:
  - /scaffold
  - /new-project
  - create project
author: reim
tags:
  - typescript
  - project
  - scaffold
  - level
---

# Project Scaffold Skill

> Multi-level project generation

---

## Usage

```bash
/scaffold <project-name> [--level starter|dynamic|enterprise] [--ai]
```

### Levels

| Level | Stack | DB | Auth | Deploy | Time |
|-------|-------|----|------|--------|------|
| starter | HTML/CSS/JS | None | None | GitHub Pages | ~3min |
| dynamic | Next.js + TS + Supabase | Supabase | Supabase Auth | Vercel | ~10min |
| enterprise | Docker + K8s + Terraform | PostgreSQL + Redis | OAuth2 + JWT | AWS/GCP | ~20min |

### Examples

```bash
/scaffold my-blog --level starter
/scaffold saas-app --level dynamic --ai
/scaffold platform --level enterprise
```

---

## Execution Instructions

<command-name>project-scaffold</command-name>

### 1. Collect Input

If level not specified, use AskUserQuestion:
- Project name (required)
- Level: Starter / Dynamic / Enterprise
- AI integration: Claude / OpenAI / None
- Output path

### 2. Level-specific Generation

| Level | Reference |
|-------|-----------|
| starter | [references/starter.md](references/starter.md) |
| dynamic | [references/dynamic.md](references/dynamic.md) |
| enterprise | [references/enterprise.md](references/enterprise.md) |

### 3. Post-creation

1. Install dependencies (if applicable)
2. Initialize git repository
3. Create .env.example
4. Display getting-started instructions

---

## Reference

### Common Options

- `--ai`: Include AI integration (Claude API)
- `--notion`: Notion API integration
- `--supabase`: Supabase integration (dynamic level default)

### Level Detection Heuristic

If level not specified, infer from project name keywords:
- "blog", "landing", "portfolio" → starter
- "app", "saas", "dashboard" → dynamic
- "platform", "service", "api" → enterprise

---

**META**
- Version: 2.0.0
- Updated: 2026-02-07
