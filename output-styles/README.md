# Output Styles Folder

> **Purpose**: Markdown/PDF/HTML style templates for output generation
> **Updated**: 2026-01-30

---

## Folder Structure

```
output-styles/
├── README.md           # This file
├── markdown/           # Markdown styles
│   ├── default.md      # Default style
│   ├── technical.md    # Technical documentation
│   └── report.md       # Report style
├── html/               # HTML templates
│   ├── default.html
│   └── presentation.html
├── pdf/                # PDF settings
│   └── config.json
└── themes/             # Theme settings
    ├── light.json
    └── dark.json
```

---

## Style Types

| Style | Purpose | Format |
|-------|---------|--------|
| **default** | General documents | MD/HTML |
| **technical** | Technical docs, API docs | MD |
| **report** | Analysis reports, PRD | MD/PDF |
| **presentation** | Presentation materials | HTML |
| **code** | Code documentation | MD |

---

## Markdown Styles

### Default Style (default.md)
```markdown
---
title: "{title}"
date: "{date}"
author: "Claude Code"
version: "{version}"
---

# {title}

> {summary}

---

## Table of Contents
1. [Overview](#overview)
2. [Details](#details)
3. [Conclusion](#conclusion)

---
```

### Technical Documentation Style (technical.md)
```markdown
---
title: "{title}"
type: "technical"
api_version: "{version}"
---

# {title}

## Overview
{overview}

## Usage
\`\`\`{language}
{code_example}
\`\`\`

## API Reference
| Method | Description | Return |
|--------|-------------|--------|
| ... | ... | ... |
```

---

## Theme Settings

### Light Theme
```json
// themes/light.json
{
  "name": "light",
  "colors": {
    "background": "#ffffff",
    "text": "#333333",
    "heading": "#1a1a1a",
    "code_bg": "#f5f5f5",
    "link": "#0066cc"
  },
  "fonts": {
    "body": "Inter, sans-serif",
    "code": "JetBrains Mono, monospace"
  }
}
```

### Dark Theme
```json
// themes/dark.json
{
  "name": "dark",
  "colors": {
    "background": "#1e1e1e",
    "text": "#d4d4d4",
    "heading": "#ffffff",
    "code_bg": "#2d2d2d",
    "link": "#4fc1ff"
  }
}
```

---

## PDF Settings

```json
// pdf/config.json
{
  "page_size": "A4",
  "margins": {
    "top": "2cm",
    "bottom": "2cm",
    "left": "2.5cm",
    "right": "2.5cm"
  },
  "header": {
    "enabled": true,
    "content": "{title} | {date}"
  },
  "footer": {
    "enabled": true,
    "content": "Page {page} of {pages}"
  }
}
```

---

## Usage

### Applying Styles
```bash
# Generate with technical documentation style
/sc:document --style technical

# Export as PDF
/sc:document --format pdf --theme light
```

### Adding Custom Styles
1. Add new template to `output-styles/{format}/` folder
2. Template filename becomes style name
3. Use `{placeholder}` format for variables

---

**META**
- Category: output-styles
- Last Updated: 2026-01-30
- Version: 1.0.0
