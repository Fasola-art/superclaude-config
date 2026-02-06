# Starter Level Template

> HTML/CSS/JS 정적 사이트

## Structure

```
<project>/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── main.js
├── assets/
│   └── images/
├── .gitignore
└── README.md
```

## index.html Template

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project-name}</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header><h1>{project-name}</h1></header>
  <main id="app"></main>
  <script src="js/main.js"></script>
</body>
</html>
```

## style.css Template

```css
:root {
  --primary: #2563eb;
  --bg: #ffffff;
  --text: #1f2937;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; color: var(--text); background: var(--bg); }
header { padding: 2rem; text-align: center; }
main { max-width: 800px; margin: 0 auto; padding: 1rem; }
```

## Deploy

```bash
# GitHub Pages
git init && git add . && git commit -m "init"
# Settings > Pages > Source: main branch
```
