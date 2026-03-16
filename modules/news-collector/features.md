# News Collector Features

> Core capabilities of the news collection module

---

## 1. News Sources

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

---

## 2. Filtering

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

---

## 3. Sentiment Analysis

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

---

## 4. Summarization

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

---

## 5. Alerts

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

**Related**: [index.md](index.md) | [usage.md](usage.md)
