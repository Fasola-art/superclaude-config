---
name: music-lesson
description: Music lesson recording pipeline - STT transcription, AI summarization, and Notion upload.
version: "1.0.0"
triggers:
  - /music-lesson
  - process music lesson
  - lesson recording conversion
---

# Music Lesson Auto-Documentation

> Convert recording files to text via CLOVA STT, summarize with Claude, and upload to Notion

---

## Usage

### Single File Processing
```bash
python ~/.claude/modules/music-lesson/pipeline.py /path/to/lesson.mp3
python ~/.claude/modules/music-lesson/pipeline.py /path/to/lesson.mp3 2026-02-01
```

### Folder Watch (Auto-processing)
```bash
python ~/.claude/modules/music-lesson/watcher.py
```

### Direct Python Usage
```python
import sys
sys.path.insert(0, str(Path.home() / ".claude" / "modules" / "music-lesson"))
from pipeline import process_lesson

result = process_lesson("/path/to/lesson.mp3")
print(result.notion_url)
```

---

## Execution Instructions

1. **On recording file processing request**:
   - Execute `~/.claude/modules/music-lesson/pipeline.py`
   - Return result URL

2. **On folder watch request**:
   - Run `~/.claude/modules/music-lesson/watcher.py` in background
   - Clova Note folder: `~/Library/CloudStorage/GoogleDrive-.../My Drive/ClovaNote`

3. **On settings change**:
   - Modify `~/.claude/modules/music-lesson/config.json`

---

## Reference

- **Supported formats**: mp3, m4a, wav, flac, aac, ogg
- **APIs**: CLOVA Speech (STT), Claude Haiku (summary), Notion (upload)
- **API Keys**: `~/.claude/credentials/api-keys.json`
- **Notion Page ID**: `2f8ecc9a6ef580018794f0ba232ece99`

---

## Output Example

Content created on Notion page:
- Date, Student info
- Key points
- Core concepts
- Homework/practice tasks (checklist)
- Next lesson preparation
