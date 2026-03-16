---
name: telegram
description: Telegram group message monitoring and AI summarization. Watch chats, collect messages, generate summaries.
license: MIT
---

Telegram group message monitoring and summarization.

## Available Commands

### Run Bot
```bash
cd C:/Users/MSI/.claude/modules/telegram
python monitor.py
```

### Message Summary
```bash
cd C:/Users/MSI/.claude/modules/telegram

# List chat rooms
python summarizer.py list

# Full summary (24 hours)
python summarizer.py summary

# Full summary (48 hours)
python summarizer.py summary 48

# Specific chat room summary
python summarizer.py chat <CHAT_ID>
```

## Bot Commands (In Telegram)

- `/summary` - Last 24 hours summary
- `/stats` - Message statistics
- `/chats` - Monitored chat rooms

## Configuration

Bot Info:
- Name: FINANCIAL NEWS-LI
- Username: @FASOLASI_bot

Add bot to group to automatically start message collection.

## File Locations

- Monitor: `C:/Users/MSI/.claude/modules/telegram/monitor.py`
- Summarizer: `C:/Users/MSI/.claude/modules/telegram/summarizer.py`
- Messages: `C:/Users/MSI/.claude/modules/telegram/data/messages.json`
- Summaries: `C:/Users/MSI/.claude/modules/telegram/data/summaries/`
