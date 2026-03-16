---
description: "뉴스 수집 및 요약 | News collection and summary"
---

# /news Command

Collect and summarize news and market data.

## Execution

1. **Bloomberg News** - Market, economy, tech category breaking news
2. **Finviz News** - Stock market news and prices
3. **FRED Indicators** - Key economic indicator check

## Usage

```
/news           # Full news collection
/news market    # Market news only
/news breaking  # Breaking news only
```

## Execution Script

Execute the following command to collect news:

```bash
python3 ~/.claude/scripts/scheduled_collectors.py all
```

## Output Format

### Breaking News (if any)
- Breaking [Category] Headline

### Market Summary
- Major index movements
- Sector trends

### News Highlights
- Positive/Negative/Neutral classification
- Sorted by importance

## Data Storage Location
- Bloomberg: `~/.claude/modules/news-collector/archive/bloomberg/`
- Finviz: `~/.claude/modules/news-collector/archive/finviz/`
