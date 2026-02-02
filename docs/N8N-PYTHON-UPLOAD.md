# n8n Python Upload Guide

> **Version**: 1.1.0
> **Last Modified**: 2026-01-30
> **Purpose**: n8n workflow setup and usage for SNS automation

---

## 5-Minute Quickstart

### Step 1: Access n8n
```bash
# If running with Docker
docker start n8n

# Access in browser
open http://localhost:5678
```

### Step 2: Import Workflow
1. Workflows → Click **Import from File**
2. Select JSON from `~/.claude/modules/sns-automation/n8n-workflows/`
3. Connect Credentials (see checklist below)

### Step 3: Test Run
1. Open workflow → Click **Test Workflow**
2. Verify results → Toggle **Active** ON

---

## Workflow Summary

| #   | Workflow             | Trigger     | Python Code Function                            | Status |
|-----|----------------------|-------------|-------------------------------------------------|--------|
| 1   | Content Distribution | Webhook     | Platform config, AI caption parsing, API calls  | ✅     |
| 2   | Engagement           | Every 15min | Comment collection, classification, auto-response | ✅     |
| 3   | Trend Analysis       | Daily 06:00 | Trend collection, briefing, ideas               | ✅     |

> ✅ = Workflow JSON created (`~/.claude/modules/sns-automation/n8n-workflows/`)

---

## Credentials Setup Checklist

### Required

| Credential         | Setup Method                      | Check |
|--------------------|-----------------------------------|-------|
| **OpenAI API**     | Settings → Credentials → OpenAI   | ☐     |
| **Telegram Bot**   | Get token from @BotFather         | ☐     |
| **Google Sheets**  | OAuth2 or Service Account         | ☐     |

### Optional

| Credential    | Setup Method                   | Check |
|---------------|--------------------------------|-------|
| **Instagram** | Get from Meta Business Suite   | ☐     |
| **TikTok**    | Get from TikTok for Developers | ☐     |
| **Twitter**   | Twitter Developer Portal       | ☐     |
| **YouTube**   | Google Cloud Console           | ☐     |

---

## Environment Variables Setup

### Set in n8n Settings

```bash
# Required
OPENAI_API_KEY=sk-xxx

# Instagram (Optional)
INSTAGRAM_ACCESS_TOKEN=xxx
INSTAGRAM_BUSINESS_ID=xxx

# Telegram (Required)
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx

# Google Sheets (Required)
GOOGLE_SHEET_ID=xxx

# TikTok (Optional)
TIKTOK_ACCESS_TOKEN=xxx

# Twitter (Optional)
TWITTER_BEARER_TOKEN=xxx
```

### .env File Template

```bash
# Path: ~/.claude/modules/sns-automation/.env
cp ~/.claude/modules/sns-automation/.env.example ~/.claude/modules/sns-automation/.env
```

---

## Python Code Node Patterns

### Basic Structure

```python
# Access input data
data = _input.first().json

# Access environment variables
token = _env.get('INSTAGRAM_ACCESS_TOKEN', '')

# API call
import requests
response = requests.post(url, headers=headers, json=payload)

# Error handling
if response.status_code != 200:
    return {"json": {"error": response.text, "status": "failed"}}

# Success return
return {
    "json": {
        "status": "success",
        "data": response.json()
    }
}
```

### Error Handling Pattern

```python
try:
    result = api_call()
    return {"json": {"status": "success", "data": result}}
except requests.exceptions.Timeout:
    return {"json": {"status": "timeout", "error": "API timeout"}}
except requests.exceptions.RequestException as e:
    return {"json": {"status": "error", "error": str(e)}}
except Exception as e:
    return {"json": {"status": "failed", "error": str(e)}}
```

---

## File Structure

```
~/.claude/modules/sns-automation/
├── n8n-workflows/
│   ├── 01-content-distributor.json    # Content distribution
│   ├── 02-engagement-automation.json  # Engagement
│   ├── 03-trend-analyzer.json         # Trend analysis
│   └── README.md                      # Workflow description
├── .env.example                       # Environment variable template
├── SKILL.md                           # Skill document
└── README.md                          # Module overview
```

---

## Workflow Details

### 01. Content Distribution (content-distributor)

| Item           | Content                                                    |
|----------------|------------------------------------------------------------|
| **Trigger**    | Webhook (POST)                                             |
| **Input**      | `{media_url, caption, platforms[]}`                        |
| **Processing** | AI caption optimization → Platform conversion → API call   |
| **Output**     | Upload results for each platform                           |

**Test Method**:
```bash
curl -X POST http://localhost:5678/webhook/content \
  -H "Content-Type: application/json" \
  -d '{"media_url": "https://...", "caption": "Test", "platforms": ["instagram"]}'
```

### 02. Engagement Automation (engagement-automation)

| Item           | Content                                              |
|----------------|------------------------------------------------------|
| **Trigger**    | Schedule (15min)                                     |
| **Input**      | None (auto-collect)                                  |
| **Processing** | Collect comments → AI classification → Auto-response |
| **Output**     | Processed comment count, response history            |

### 03. Trend Analysis (trend-analyzer)

| Item           | Content                                      |
|----------------|----------------------------------------------|
| **Trigger**    | Schedule (Daily 06:00)                       |
| **Input**      | None (auto-collect)                          |
| **Processing** | Collect trends → Integrate → AI briefing     |
| **Output**     | Telegram notification + Google Sheets record |

---

## Troubleshooting

### Common Errors

| Error                   | Cause                   | Solution                  |
|-------------------------|-------------------------|---------------------------|
| `401 Unauthorized`      | API key expired/invalid | Re-configure Credentials  |
| `429 Too Many Requests` | Rate Limit exceeded     | Increase call interval    |
| `500 Internal Error`    | Platform server error   | Add retry logic           |
| `Timeout`               | Network delay           | Increase timeout value    |

### Debugging Methods

1. **Check n8n logs**: `docker logs n8n`
2. **Execute node by node**: Step-by-step verification with Execute Node
3. **Webhook test**: Use Postman or curl

---

## Related Documents

| Document              | Path                                         | Description                |
|-----------------------|----------------------------------------------|----------------------------|
| SNS Automation Skill  | `~/.claude/skills/sns-automation/SKILL.md`   | Full architecture          |
| Instruction Checklist | `~/.claude/docs/INSTRUCTION-FILE-CHECKLIST.md` | Document quality standards |
| n8n Official Docs     | https://docs.n8n.io                          | n8n reference              |

---

## Self-Diagnostic Checklist

### Setup Completion Check

- [ ] n8n running normally
- [ ] Required Credentials configured (OpenAI, Telegram, Google Sheets)
- [ ] Environment variables configured
- [ ] Workflow Import completed
- [ ] Test run successful

### Operations Check

- [ ] Workflow in Active state
- [ ] Telegram notification reception confirmed
- [ ] Error log monitoring configured

---

## Changelog

| Version | Date       | Changes                                      |
|---------|------------|----------------------------------------------|
| 1.1.0   | 2026-01-30 | Added quickstart, checklist, troubleshooting |
| 1.0.0   | 2026-01-30 | Initial version                              |

---

**META**
- Created: 2026-01-30
- Category: Automation / n8n
- Related: sns-automation, workflow
