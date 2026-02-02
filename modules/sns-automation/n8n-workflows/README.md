# n8n Workflows

> n8n workflow JSON files for SNS automation

---

## 📁 File List

| File | Trigger | Function |
|------|---------|----------|
| `01-content-distributor.json` | Webhook | Multi-platform content distribution |
| `02-engagement-automation.json` | 15min schedule | Auto-reply to comments/DMs |
| `03-trend-analyzer.json` | Daily 06:00 | Trend analysis + ideas |
| `04-weekly-report.json` | Sunday 21:00 | Weekly performance report |

---

## 🚀 Import Method

1. Access n8n (`http://localhost:5678`)
2. **Workflows** → **Import from File**
3. Select JSON file
4. Connect **Credentials** (see below)

---

## 🔐 Required Credentials

### Common for All Workflows

| Credential | n8n Type | Required Info |
|------------|----------|---------------|
| OpenAI | OpenAI API | API Key |
| Telegram | Telegram Bot | Bot Token |
| Google Sheets | Google Sheets OAuth2 | OAuth connection |

### Platform-specific (Optional)

| Credential | Workflow | Required Info |
|------------|----------|---------------|
| Instagram | 01, 02 | Access Token, Business ID |
| TikTok | 01 | Access Token |
| Twitter | 01 | Bearer Token |

---

## ⚙️ Environment Variable Setup

Set in n8n Settings → Environment Variables:

```bash
# Required
OPENAI_API_KEY=sk-xxx
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
GOOGLE_SHEET_ID=xxx

# Instagram
INSTAGRAM_ACCESS_TOKEN=xxx
INSTAGRAM_BUSINESS_ID=xxx

# TikTok
TIKTOK_ACCESS_TOKEN=xxx

# Twitter
TWITTER_BEARER_TOKEN=xxx
```

---

## 🧪 Testing Methods

### 01. Content Distributor

```bash
curl -X POST http://localhost:5678/webhook/content \
  -H "Content-Type: application/json" \
  -d '{
    "media_url": "https://example.com/image.jpg",
    "caption": "Test caption",
    "platforms": ["instagram"]
  }'
```

### 02. Engagement Automation

- Click **Execute Workflow** in n8n
- Or wait 15 minutes

### 03. Trend Analyzer

- Click **Execute Workflow** in n8n
- Or wait until next 06:00

### 04. Weekly Report

- Click **Execute Workflow** in n8n
- Or wait until next Sunday 21:00

---

## ⚠️ Post-Import Modifications Required

1. **Replace Credential IDs**: Change `OPENAI_CREDENTIAL_ID`, `TELEGRAM_CREDENTIAL_ID`, etc. to actual IDs
2. **Verify Environment Variables**: Ensure all `$env.XXX` are configured
3. **Test Execution**: Run Execute Node for each node

---

## 📊 Workflow Details

### 01. Content Distributor

```
Webhook → Parse Input → AI Caption → Prepare Posts
    ↓
    ├── Instagram → Post
    └── TikTok → Post
    ↓
Aggregate → Telegram Notify → Respond
```

### 02. Engagement Automation

```
Schedule (15min) → Fetch Comments → Parse → AI Classify
    ↓
    ├── Fan Comment → Auto Reply
    └── Collab → Telegram Notify
    ↓
Log to Sheet
```

### 03. Trend Analyzer

```
Schedule (6AM) → Google Trends ─┐
                Instagram Trends ┴→ Merge → AI Analysis
    ↓
Format Briefing
    ├── Telegram
    └── Google Sheets
```

### 04. Weekly Report

```
Schedule (Sun 21:00) → IG Insights ─┐
                       IG Posts ────┴→ Aggregate → AI Analysis
    ↓
Format Report
    ├── Telegram
    └── Google Sheets
```

---

**META**
- Created: 2026-01-30
- Version: 1.0.0
