# SNS Automation Module

> **Version**: 1.0.0
> **Purpose**: SNS automation system for influencers/creators

---

## 🚀 Quickstart

```bash
# 1. Set environment variables
cp .env.example .env
# Edit .env file to add API keys

# 2. Import n8n workflows
# Access n8n → Workflows → Import from File
# Select JSON files from n8n-workflows/ folder

# 3. Test run
# Click "Test Workflow" in the workflow
```

---

## 📁 Folder Structure

```
sns-automation/
├── n8n-workflows/           # n8n workflow JSON files
│   ├── 01-content-distributor.json
│   ├── 02-engagement-automation.json
│   ├── 03-trend-analyzer.json
│   ├── 04-weekly-report.json
│   └── README.md
├── .env.example             # Environment variable template
└── README.md                # This file

# Related skill: ~/.claude/skills/sns-automation/SKILL.md
```

---

## 📋 Workflow List

| # | Name | Trigger | Function |
|---|------|---------|----------|
| 1 | Content Distributor | Webhook | Multi-platform auto upload |
| 2 | Engagement Automation | 15min schedule | Auto-reply to comments/DMs |
| 3 | Trend Analyzer | Daily 06:00 | Trend analysis + idea generation |
| 4 | Weekly Report | Sunday 21:00 | Weekly performance analysis |

---

## 🔗 Related Documents

| Document | Description |
|----------|-------------|
| `~/.claude/docs/N8N-PYTHON-UPLOAD.md` | n8n setup guide |
| `~/.claude/skills/sns-automation/SKILL.md` | Skill detailed documentation |
| `~/.claude/docs/INSTRUCTION-FILE-CHECKLIST.md` | Instruction quality checklist |

---

## 📊 Expected Results

| Item | Before | After | Savings |
|------|--------|-------|---------|
| Platform upload | 2 hours | 5 min | 95% |
| Comment response | 2 hours | 30 min | 75% |
| Trend analysis | 1 hour | Auto | 100% |
| **Weekly total** | **7 hours** | **35 min** | **92%** |

---

**META**
- Created: 2026-01-30
- Category: Automation
- Command: /sns
