---
description: "세션 분위기 확인/설정 | Check and set session vibe"
argument-hint: "[vibe_name]"
---

# Vibe Settings

Check or change the current session's vibe (work mode/tone).

## Available Vibes

| Vibe | Description | Active Personas |
|------|-------------|-----------------|
| `default` | Default mode | - |
| `ultrawork` | Maximum performance | explorer, librarian, analyzer |
| `deepsearch` | Deep research | explorer |
| `strategic` | Strategic analysis | architect |
| `visual` | Visual analysis | multimodal, frontend |

## Usage Examples

```
/vibe              # Check current vibe
/vibe ultrawork    # Set ultrawork mode
/vibe strategic    # Set strategic mode
```

## Behavior

1. Run without arguments: Display current vibe state
2. Specify vibe name: Switch to that mode
3. Auto-activate related personas
4. Update session settings

## Output Format

```
🎨 Vibe Settings

Current Vibe: [vibe_name]
Active Personas: [persona_list]

Settings:
- Parallel execution: [enabled/disabled]
- Review level: [strict/normal/quick]
- Output style: [detailed/concise]

To change: /vibe [vibe_name]
```
