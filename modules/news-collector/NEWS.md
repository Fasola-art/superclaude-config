# News Collector Module

> SuperClaude news collection and analysis module

---

## Overview

News collector module automatically gathers news from various sources,
performs filtering, summarization, and sentiment analysis.

---

## Folder Structure

```
~/.claude/modules/news-collector/
├── NEWS.md             # This file (module guide)
├── config.json         # Module configuration
├── sources/            # News source definitions
│   ├── rss.json
│   ├── api.json
│   └── custom/
├── filters/            # Filtering rules
│   ├── keywords.json
│   ├── categories.json
│   └── exclude.json
├── alerts/             # Alert settings
│   └── rules.json
└── archive/            # Archive
    ├── 2026/
    │   ├── 01/
    │   └── ...
    └── index.json
```

---

## Features

### 1. News Sources

```yaml
sources:
  rss_feeds:
    - name: "Bloomberg"
      url: "https://www.bloomberg.com/feed"
      category: "finance"

    - name: "TechCrunch"
      url: "https://techcrunch.com/feed"
      category: "tech"

    - name: "Reuters"
      url: "https://www.reuters.com/rssFeed"
      category: "general"

  api_sources:
    - name: "NewsAPI"
      type: "api"
      endpoint: "https://newsapi.org/v2"
      requires_key: true

    - name: "Google News"
      type: "scraper"
      url: "https://news.google.com"

  custom_sources:
    - name: "Company Blog"
      type: "rss"
      url: "custom_url"
```

### 2. Filtering

```yaml
filters:
  keywords:
    include:
      - "AI"
      - "Machine Learning"
      - "Trading"
      - "Cryptocurrency"
    exclude:
      - "Advertisement"
      - "Spam"

  categories:
    - tech
    - finance
    - crypto

  language:
    - ko
    - en

  time_range:
    max_age_hours: 24

  deduplication:
    enabled: true
    similarity_threshold: 0.8
```

### 3. Sentiment Analysis

```yaml
sentiment:
  enabled: true
  model: "local"  # or "api"

  output:
    - score: -1.0 ~ 1.0
    - label: "positive" | "neutral" | "negative"
    - confidence: 0.0 ~ 1.0

  aggregation:
    - by_source
    - by_category
    - by_keyword
    - by_time
```

### 4. Summarization

```yaml
summarization:
  enabled: true
  max_length: 200  # characters
  language: "ko"

  output:
    - title: "Original title"
    - summary: "AI-generated summary"
    - key_points: ["Key point 1", "Key point 2"]
    - entities: ["Company name", "Person name"]
```

### 5. Alerts

```yaml
alerts:
  channels:
    - Desktop Notification
    - Telegram
    - Slack
    - Email

  triggers:
    keyword_mention:
      keywords: ["Urgent", "Breaking"]
      priority: high

    sentiment_spike:
      threshold: 0.5  # Sudden change
      direction: "negative"

    volume_spike:
      threshold: 200  # % increase
      timeframe: "1h"
```

---

## Skill Commands

| Command | Description |
|---------|-------------|
| /news-fetch | Fetch latest news |
| /news-filter [keyword] | Filter by keyword |
| /news-summary [URL] | Summarize news article |
| /news-sentiment [topic] | Analyze sentiment |
| /news-alert [condition] | Set up alerts |

---

## Configuration (config.json)

```json
{
  "fetchInterval": 3600,
  "maxArticlesPerSource": 50,
  "archiveRetentionDays": 90,
  "sentiment": {
    "enabled": true,
    "model": "local"
  },
  "summarization": {
    "enabled": true,
    "maxLength": 200
  },
  "alerts": {
    "enabled": true,
    "channels": ["desktop"]
  }
}
```

---

## Usage Examples

```bash
# Fetch latest news
/news-fetch

# Filter AI-related news only
/news-filter "AI"

# Summarize specific article
/news-summary https://example.com/article

# Analyze cryptocurrency sentiment
/news-sentiment "Bitcoin"

# Set negative news alert
/news-alert "sentiment < -0.5" --keyword "my portfolio"
```

---

## Scheduling

```yaml
schedule:
  fetch:
    interval: "1h"  # Hourly
    sources: "all"

  archive:
    interval: "1d"  # Daily
    cleanup: true

  report:
    interval: "1d"
    time: "09:00"
    format: "daily_digest"
```

---

## Roadmap

- [ ] Real-time streaming collection
- [ ] Multi-language translation
- [ ] Image/chart analysis
- [ ] Trading module integration
