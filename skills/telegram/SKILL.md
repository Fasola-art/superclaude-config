---
name: telegram
description: Telegram group message monitoring and AI summarization. Watch chats, collect messages, generate summaries.
license: MIT
---

Telegram group message monitoring and summarization.

## Available Commands

### Run Bot
```bash
cd /Users/reim/.claude/modules/telegram
python3 monitor.py
```

### Message Summary
```bash
cd /Users/reim/.claude/modules/telegram

# List chat rooms
python3 summarizer.py list

# Full summary (24 hours)
python3 summarizer.py summary

# Full summary (48 hours)
python3 summarizer.py summary 48

# Specific chat room summary
python3 summarizer.py chat <CHAT_ID>
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

- Monitor: `/Users/reim/.claude/modules/telegram/monitor.py`
- Summarizer: `/Users/reim/.claude/modules/telegram/summarizer.py`
- Messages: `/Users/reim/.claude/modules/telegram/data/messages.json`
- Summaries: `/Users/reim/.claude/modules/telegram/data/summaries/`
