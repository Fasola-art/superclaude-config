# SNS Automation Workflow Skill

> **Version**: 1.2.0
> **Created**: 2026-01-30
> **Last Updated**: 2026-01-30
> **Purpose**: Design and implement SNS automation system for influencers/content creators
> **Module Path**: `~/.claude/modules/sns-automation/`
> **Command**: `/sns`

---

## Overview

This skill designs workflows to automate SNS content creation, distribution, engagement management, and analytics.

---

## Quick Start

```bash
# 1. Run n8n (Docker)
docker run -d --name n8n -p 5678:5678 n8nio/n8n

# 2. Import Workflows
# n8n UI (localhost:5678) → Workflows → Import from File
# ~/.claude/modules/sns-automation/n8n-workflows/*.json

# 3. Configure Credentials
# Settings → Credentials → Enter API keys for each service
```

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| 01-content-distributor | Webhook | Multi-platform content distribution |
| 02-engagement-automation | 15min schedule | Auto-reply to comments/DMs |
| 03-trend-analyzer | Daily 06:00 | Trend analysis + ideas |
| 04-weekly-report | Sunday 21:00 | Weekly performance report |

---

## System Architecture (TO-BE)

```
┌─────────────────────────────────────────────────────────────┐
│                    SNS Automation System                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Content Hub  │───▶│ AI Processor │───▶│ Distribution │  │
│  │ (Storage)    │    │ (Transform)  │    │   Engine     │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │          │
│         ▼                   ▼                   ▼          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Analytics   │◀───│ Engagement   │◀───│ Multi-platform│  │
│  │  Dashboard   │    │  Auto-reply  │    │ (IG/TT/YT)   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Workflow Details

### Workflow 1: Content Creation → Multi-platform Distribution

```
[Trigger] Original content upload (Google Drive / Dropbox)
    │
    ▼
┌─────────────────────────────────────────────┐
│ [AI Processor] Content Analysis              │
│ • Detect video length, topic, mood           │
│ • Auto-extract optimal thumbnail             │
│ • Auto-generate subtitles (Whisper API)      │
└─────────────────────────────────────────────┘
    │
    ├──────────────┬──────────────┐
    ▼              ▼              ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│ Instagram  │ │  TikTok    │ │  YouTube   │
│ Transform  │ │  Transform │ │  Transform │
│ • 1:1/4:5  │ │ • 9:16     │ │ • Shorts   │
│   resize   │ │   vertical │ │   60sec    │
│ • Caption  │ │ • Trending │ │ • Chapter  │
│   optimize │ │   music    │ │   markers  │
│ • Hashtag  │ │ • Hook     │ │ • SEO tags │
│   suggest  │ │   text     │ │            │
└────────────┘ └────────────┘ └────────────┘
    │              │              │
    ▼              ▼              ▼
┌─────────────────────────────────────────────┐
│ [Scheduler] Optimal time scheduling          │
│ • Instagram: 12:00, 18:00, 21:00            │
│ • TikTok: 07:00, 12:00, 19:00               │
│ • YouTube: 17:00, 20:00                     │
└─────────────────────────────────────────────┘
    │
    ▼
[Execute] Auto-upload + cross-posting
```

### Workflow 2: Engagement Automation

```
[Trigger] New comment/DM received
    │
    ▼
┌─────────────────────────────────────────────┐
│ [AI] Message Type Classification             │
│ • Fan comment → Auto-reply                   │
│ • Sponsorship inquiry → Separate queue + alert│
│ • Negative comment → Monitoring flag         │
│ • Question → FAQ match or manual request     │
└─────────────────────────────────────────────┘
    │
    ├─────────────┬─────────────┐
    ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Auto-reply│ │ Sponsor  │ │ Crisis   │
│          │ │ Mgmt     │ │ Response │
│ "Thank   │ │• Notion  │ │• Instant │
│  you!    │ │  DB save │ │  alert   │
│  💕"     │ │• Template│ │• Hide    │
│ "Have a  │ │  reply   │ │  action  │
│  great   │ │• Calendar│ │• Escalate│
│  day!"   │ │  sync    │ │          │
│ (persona │ │          │ │          │
│  maintain)│ │          │ │          │
└──────────┘ └──────────┘ └──────────┘
```

### Workflow 3: Content Planning Automation

```
[Trigger] Daily 6am / Weekly Monday
    │
    ▼
┌─────────────────────────────────────────────┐
│ [Trend Collection]                           │
│ • TikTok trending hashtags                   │
│ • Instagram explore tab popular content      │
│ • Google Trends rising keywords              │
│ • Competitor influencer recent posts         │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ [AI Analysis]                                │
│ • Filter trends matching my content style    │
│ • Calculate expected performance score       │
│ • Generate 3 content ideas                   │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ [Output] Auto-update content calendar        │
│ • Notion / Google Calendar sync              │
│ • Slack/Telegram notification                │
└─────────────────────────────────────────────┘
```

### Workflow 4: Analytics and Reporting

```
[Trigger] Every Sunday 21:00
    │
    ▼
┌─────────────────────────────────────────────┐
│ [Data Collection]                            │
│ • Instagram Insights API                     │
│ • TikTok Analytics                           │
│ • YouTube Studio API                         │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ [Analysis]                                   │
│ • Top 5 content (reach/engagement)           │
│ • Follower growth trends                     │
│ • Recalculate optimal upload times           │
│ • Hashtag performance analysis               │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│ [Report Generation]                          │
│ • Auto-generate PDF weekly report            │
│ • Email (for sponsor sharing)                │
│ • Dashboard update                           │
└─────────────────────────────────────────────┘
```

---

## Tech Stack Recommendations

| Layer | Tool | Purpose |
|-------|------|---------|
| Workflow Engine | n8n (self-hosted) | Full automation orchestration |
| AI | OpenAI GPT-4 / Claude | Caption generation, comment classification, ideas |
| Media Processing | FFmpeg / Cloudinary | Resizing, format conversion |
| Voice | Whisper API | Auto-subtitle generation |
| Scheduling | Buffer / Later API | Multi-platform scheduling |
| Database | Notion API / Supabase | Content/sponsor management |
| Notifications | Telegram Bot / Slack | Real-time alerts |
| Dashboard | Metabase / Google Sheets | Analytics dashboard |

---

## Expected Results After Automation

| Task | Before | After | Savings |
|------|--------|-------|---------|
| Platform upload | 2 hours | 5 min | **95%** |
| Comment/DM response | 2 hours | 30 min | **75%** |
| Hashtag research | 1 hour | Auto | **100%** |
| Trend analysis | 1 hour | Auto | **100%** |
| Reporting | 1 hour | Auto | **100%** |
| Weekly total | 7 hours | 35 min | **92%** |

---

## Implementation Phases

### Phase 1: Environment Setup
1. Install n8n (Docker / self-hosted)
2. Configure `.env` environment variables
3. Enter API keys

### Phase 2: Workflow Import
1. Import workflows in n8n
2. `Workflows → Import from File → Select JSON`
3. Connect Credentials
   - OpenAI, Instagram, YouTube, TikTok, Telegram, Notion, Google Sheets

### Phase 3: Test Execution
1. Verify with manual workflow execution

---

## Platform API Notes

| Platform | Notes |
|----------|-------|
| Instagram | Business/Creator account required, Meta app review needed |
| TikTok | Content Posting API requires separate approval (1-2 weeks) |
| Twitter | v2 API + OAuth 2.0 required |
| YouTube | OAuth consent screen setup required |

---

## Implementation Options

### Option A: n8n Workflow Build
- Build automation pipeline with self-hosting (free)

### Option B: SaaS Combination
- Connect existing services like Zapier + Buffer + Notion

### Option C: Custom App Development
- Develop dedicated dashboard with Next.js + API

### Option D: Planning First
- Write specification first, then develop

---

## Related Commands

```bash
# Call /sns skill
/sns

# Request specific workflow
"Design SNS automation workflow"
"Create automation using influencer persona"
```

---

## References

- https://kissflow.com/workflow/bpm/bpm-vs-workflow/
- https://www.boc-group.com/en/blog/bpm/business-process-management-bpm/
- https://www.techtarget.com/searchcio/tip/6-trends-shaping-the-future-of-BPM
- https://www.digidop.com/blog/n8n-vs-make-vs-zapier
- https://n8n.io/

---

## Self-diagnostic Checklist

### Environment Setup
- [ ] n8n installed and running (`localhost:5678` accessible)
- [ ] `.env` file created with API keys
- [ ] All 4 workflow JSONs imported

### API Connections
- [ ] OpenAI API key validated
- [ ] Instagram Graph API connected (business account required)
- [ ] Telegram Bot Token configured
- [ ] Google Sheets service account connected

### Testing
- [ ] 01-content-distributor: Test with webhook URL
- [ ] 02-engagement: Manual run → verify comment fetch
- [ ] 03-trend-analyzer: Manual run → verify AI analysis
- [ ] 04-weekly-report: Manual run → verify report generation

---

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Instagram API 401 | Token expired | Reissue token in Meta Business Suite |
| n8n Webhook 404 | Workflow inactive | Toggle workflow → Active ON |
| OpenAI rate limit | Excessive API calls | Add retry settings to HTTP Request node |
| Telegram no messages | Chat ID error | `/start` → Verify Chat ID from bot |
| Google Sheets permission | Service account not shared | Share spreadsheet with service account email |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-30 | Initial version: Workflows 1-3 |
| 1.1.0 | 2026-01-30 | Added Workflow 4 (Analytics and Reporting) |
| 1.2.0 | 2026-01-30 | Added Quick Start, Checklist, Troubleshooting |

---

**META**
- Generated: 2026-01-30
- Tool: Claude Code (SuperClaude v2.0.9)
