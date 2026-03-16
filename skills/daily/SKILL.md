---
name: daily
description: Quick reference for frequently used paths. Economic outlook, trading module, personas, API keys, and other key folder paths.
license: MIT
---

Quick reference for frequently used paths.

## Key Paths

| Purpose | Path |
|---------|------|
| **Economic Outlook** | `C:/Users/MSI/.claude/modules/trading/reports/daily/` |
| **Trading Module** | `C:/Users/MSI/.claude/modules/trading/` |
| **News Module** | `C:/Users/MSI/.claude/modules/news-collector/` |
| **Telegram Module** | `C:/Users/MSI/.claude/modules/telegram/` |
| **Personas** | `C:/Users/MSI/.claude/personas/` |
| **Skills** | `C:/Users/MSI/.claude/skills/` |
| **API Keys** | `C:/Users/MSI/.claude/credentials/api-keys.json` |
| **Settings** | `C:/Users/MSI/.claude/settings.json` |

## Quick Open

```bash
# Economic outlook folder
explorer C:/Users/MSI/.claude/modules/trading/reports/daily/

# Trading module
explorer C:/Users/MSI/.claude/modules/trading/

# Personas folder
explorer C:/Users/MSI/.claude/personas/

# Skills folder
explorer C:/Users/MSI/.claude/skills/

# API keys file
explorer C:/Users/MSI/.claude/credentials/api-keys.json
```

## Today's Outlook File

```powershell
# Today's outlook
type C:/Users/MSI/.claude/modules/trading/reports/daily/outlook_$(Get-Date -Format yyyy-MM-dd).json

# Latest outlook
Get-ChildItem C:/Users/MSI/.claude/modules/trading/reports/daily/outlook_*.json | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```
