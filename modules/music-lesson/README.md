# Music Lesson Auto-Recording System

> Audio file → CLOVA STT → Claude summary → Notion auto-upload

---

## Installation

```bash
cd C:\Users\MSI\.claude\modules\music-lesson
pip install anthropic requests watchdog
```

---

## Usage

### 1. Single File Processing

```bash
python pipeline.py /path/to/lesson.mp3
python pipeline.py /path/to/lesson.mp3 2026-02-01  # Specify date
```

### 2. Folder Watch (Auto-processing)

```bash
python watcher.py                           # Default CLOVA Note folder
python watcher.py /path/to/watch/folder     # Specified folder
```

### 3. Use in Python

```python
from pipeline import process_lesson

result = process_lesson("/path/to/lesson.mp3")
print(result.notion_url)  # Notion page URL
print(result.summary.main_points)  # Main points
```

---

## File Structure

| File | Description |
|------|-------------|
| `clova_stt.py` | CLOVA Speech STT module |
| `summarizer.py` | Claude Haiku summarization module |
| `notion_uploader.py` | Notion page creation module |
| `pipeline.py` | Full pipeline integration |
| `watcher.py` | Folder watch (auto-process new files) |
| `config.json` | Configuration file |

---

## Configuration (`config.json`)

```json
{
  "language": "ko-KR",           // STT language
  "notion_parent_page_id": null, // Notion parent page (null uses api-keys.json)
  "auto_upload": true,           // Auto Notion upload
  "save_transcript": true,       // Save transcript
  "transcript_dir": "C:/Users/MSI/.claude/modules/music-lesson/transcripts",
  "watch_path": "G:/내 드라이브/클로바노트",
  "processed_dir": null,         // Move processed files here (null = don't move)
  "recursive": false             // Include subfolders
}
```

---

## API Key Setup

Required keys in `C:\Users\MSI\.claude\credentials\api-keys.json`:

```json
{
  "clova_speech": {
    "secret_key": "...",
    "invoke_url": "https://clovaspeech-gw.ncloud.com/recog/v1/stt"
  },
  "anthropic": {
    "api_key": "sk-ant-..."
  },
  "notion": {
    "internal_secret": "ntn_...",
    "page_id": "..."
  }
}
```

---

## Supported Audio Formats

- MP3 (`.mp3`)
- M4A (`.m4a`)
- WAV (`.wav`)
- FLAC (`.flac`)
- AAC (`.aac`)
- OGG (`.ogg`)

---

## Summary Format

The following content is auto-generated in Notion page:

- 📌 **Main Points**: Key lesson content
- 🎵 **Core Concepts**: Music concepts/techniques learned
- 📝 **Homework/Practice**: Checklist format
- 📅 **Next Lesson Prep**: Preparation items

---

## Troubleshooting

### CLOVA API Error
- Verify Secret Key
- Check network connection
- Verify audio file format

### Notion Upload Failed
- Verify Internal Secret
- Check Page ID (Integration must be connected to page)

### Summary Not Working Properly
- Check audio quality (noisy audio degrades STT quality)
- Recommend splitting long recordings (over 30 minutes)

---

**META**
- Version: 1.0.0
- Created: 2026-02-01
