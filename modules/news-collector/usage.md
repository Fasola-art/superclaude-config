# News Collector Usage

> Configuration and usage guide

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
- [ ] Podcast/audio transcript support
- [ ] Custom ML model training

---

**Related**: [index.md](index.md) | [features.md](features.md)
