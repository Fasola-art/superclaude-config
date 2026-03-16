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
├── index.md            # This file (module overview)
├── features.md         # Features and capabilities
├── usage.md            # Configuration and usage
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

## Documentation

| File | Content | Lines |
|------|---------|-------|
| [features.md](features.md) | News sources, filtering, analysis | ~90 |
| [usage.md](usage.md) | Skills, config, examples | ~70 |

---

**Related**: [features.md](features.md) | [usage.md](usage.md)
