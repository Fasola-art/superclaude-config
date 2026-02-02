---
name: daily
description: Quick reference for frequently used paths. Economic outlook, trading module, personas, API keys, and other key folder paths.
license: MIT
---

Quick reference for frequently used paths.

## Key Paths

| Purpose | Path |
|---------|------|
| **Economic Outlook** | `/Users/reim/.claude/modules/trading/reports/daily/` |
| **Trading Module** | `/Users/reim/.claude/modules/trading/` |
| **News Module** | `/Users/reim/.claude/modules/news-collector/` |
| **Telegram Module** | `/Users/reim/.claude/modules/telegram/` |
| **Personas** | `/Users/reim/.claude/personas/` |
| **Skills** | `/Users/reim/.claude/skills/` |
| **API Keys** | `/Users/reim/.claude/credentials/api-keys.json` |
| **Settings** | `/Users/reim/.claude/settings.json` |

## Quick Open

```bash
# Economic outlook folder
open /Users/reim/.claude/modules/trading/reports/daily/

# Trading module
open /Users/reim/.claude/modules/trading/

# Personas folder
open /Users/reim/.claude/personas/

# Skills folder
open /Users/reim/.claude/skills/

# API keys file
open /Users/reim/.claude/credentials/api-keys.json
```

## Today's Outlook File

```bash
# Today's outlook
cat /Users/reim/.claude/modules/trading/reports/daily/outlook_$(date +%Y-%m-%d).json

# Latest outlook
ls -t /Users/reim/.claude/modules/trading/reports/daily/outlook_*.json | head -1
```
