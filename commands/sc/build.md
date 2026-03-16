---
description: "프로젝트 빌드 | Build project"
argument-hint: "[options]"
---

# Build

Build the project.

## Usage

```
/sc:build              # Default build
/sc:build --prod       # Production build
/sc:build --watch      # Watch mode
```

## Behavior

1. Detect project type (Next.js, Vite, etc.)
2. Execute appropriate build command
3. Analyze and report build results
