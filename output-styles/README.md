# Output Styles 폴더

> **목적**: 결과물 생성을 위한 마크다운/PDF/HTML 스타일 템플릿
> **갱신일**: 2026-01-30

---

## 📁 폴더 구조

```
output-styles/
├── README.md           # 이 파일
├── markdown/           # 마크다운 스타일
│   ├── default.md      # 기본 스타일
│   ├── technical.md    # 기술 문서용
│   └── report.md       # 보고서용
├── html/               # HTML 템플릿
│   ├── default.html
│   └── presentation.html
├── pdf/                # PDF 설정
│   └── config.json
└── themes/             # 테마 설정
    ├── light.json
    └── dark.json
```

---

## 🎯 스타일 유형

| 스타일 | 용도 | 형식 |
|--------|------|------|
| **default** | 일반 문서 | MD/HTML |
| **technical** | 기술 문서, API 문서 | MD |
| **report** | 분석 보고서, PRD | MD/PDF |
| **presentation** | 발표 자료 | HTML |
| **code** | 코드 문서화 | MD |

---

## 📋 마크다운 스타일

### 기본 스타일 (default.md)
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

## 목차
1. [개요](#개요)
2. [상세](#상세)
3. [결론](#결론)

---
```

### 기술 문서 스타일 (technical.md)
```markdown
---
title: "{title}"
type: "technical"
api_version: "{version}"
---

# {title}

## 개요
{overview}

## 사용법
\`\`\`{language}
{code_example}
\`\`\`

## API 레퍼런스
| 메서드 | 설명 | 반환값 |
|--------|------|--------|
| ... | ... | ... |
```

---

## 🎨 테마 설정

### 라이트 테마
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

### 다크 테마
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

## 📄 PDF 설정

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

## 🔧 사용 방법

### 스타일 적용
```bash
# 기술 문서 스타일로 생성
/sc:document --style technical

# PDF로 내보내기
/sc:document --format pdf --theme light
```

### 커스텀 스타일 추가
1. `output-styles/{format}/` 폴더에 새 템플릿 추가
2. 템플릿 파일명이 스타일 이름이 됨
3. `{placeholder}` 형식으로 변수 사용

---

**META**
- Category: output-styles
- Last Updated: 2026-01-30
- Version: 1.0.0
