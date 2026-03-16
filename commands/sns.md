---
description: "SNS 자동화 워크플로우 | SNS automation workflow design and management"
argument-hint: "[workflow_name or action]"
---

# SNS Automation

Design and manage SNS content distribution, engagement, and trend analysis automation workflows.

## Behavior

1. Analyze request (workflow design / n8n setup / modify existing workflow)
2. Check tech stack (n8n, API, AI)
3. Design or modify workflow
4. Provide implementation guide

## Available Actions

| Action | Description |
|--------|-------------|
| `design` | Design new workflow |
| `setup` | n8n environment setup guide |
| `check` | Audit existing workflows |
| `improve` | Workflow improvement suggestions |

## Usage Examples

```bash
/sns                          # Full SNS automation guide
/sns design content           # Design content distribution workflow
/sns setup                    # n8n setup guide
/sns check                    # Audit existing workflows
```

## Workflow Types

| # | Workflow | Trigger | Function |
|---|----------|---------|----------|
| 1 | Content Distribution | Webhook | Multi-platform auto upload |
| 2 | Engagement | 15min schedule | Auto-respond to comments/DMs |
| 3 | Trend Analysis | Daily 06:00 | Trend collection + ideas |
| 4 | Analytics Report | Weekly Sunday | Weekly performance report |

## Related Documentation

- Skill details: `~/.claude/skills/sns-automation/SKILL.md`
- n8n guide: `~/.claude/docs/N8N-PYTHON-UPLOAD.md`
- Module folder: `~/.claude/modules/sns-automation/`

## Tech Stack

| Layer | Tool |
|-------|------|
| Workflow | n8n (self-hosted) |
| AI | OpenAI / Claude |
| Media | FFmpeg / Cloudinary |
| Notifications | Telegram / Slack |
