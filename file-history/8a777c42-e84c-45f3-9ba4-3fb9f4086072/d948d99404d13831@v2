# IDE 폴더

> **목적**: IDE(VS Code, Cursor 등) 연동 관련 설정 및 플러그인 데이터
> **갱신일**: 2026-01-30

---

## 📁 폴더 구조

```
ide/
├── README.md           # 이 파일
├── vscode/             # VS Code 설정
│   ├── settings.json   # 워크스페이스 설정
│   ├── keybindings.json
│   └── snippets/       # 코드 스니펫
├── cursor/             # Cursor AI 설정
│   └── settings.json
├── extensions/         # 추천 확장 목록
│   └── recommended.json
└── workspace/          # 워크스페이스 템플릿
    └── {template-name}.code-workspace
```

---

## 🎯 지원 IDE

| IDE | 연동 상태 | 기능 |
|-----|----------|------|
| **VS Code** | ✅ 지원 | Claude Code 확장 |
| **Cursor** | ✅ 지원 | 네이티브 통합 |
| **JetBrains** | 🔄 계획 | 플러그인 개발 중 |
| **Neovim** | 🔄 계획 | LSP 연동 |

---

## ⚙️ VS Code 통합

### 추천 확장 프로그램
```json
// extensions/recommended.json
{
  "recommendations": [
    "anthropics.claude-code",
    "ms-python.python",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "dbaeumer.vscode-eslint"
  ]
}
```

### Claude Code 설정
```json
// vscode/settings.json
{
  "claude-code.autoStart": true,
  "claude-code.configPath": "~/.claude/CLAUDE.md",
  "claude-code.terminal.integrated": true
}
```

---

## 🔧 워크스페이스 템플릿

### Next.js 프로젝트
```json
// workspace/nextjs.code-workspace
{
  "folders": [
    { "path": "." }
  ],
  "settings": {
    "typescript.tsdk": "node_modules/typescript/lib",
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### Python 프로젝트
```json
// workspace/python.code-workspace
{
  "folders": [
    { "path": "." }
  ],
  "settings": {
    "python.linting.enabled": true,
    "python.linting.mypyEnabled": true
  }
}
```

---

## 📋 스니펫

### TypeScript 스니펫
```json
// vscode/snippets/typescript.json
{
  "React Function Component": {
    "prefix": "rfc",
    "body": [
      "export function ${1:ComponentName}() {",
      "  return (",
      "    <div>",
      "      $0",
      "    </div>",
      "  );",
      "}"
    ]
  }
}
```

---

## ⚠️ 주의사항

- IDE 설정은 프로젝트별로 오버라이드 가능
- Claude Code 확장은 VS Code 1.80+ 필요
- 워크스페이스 템플릿은 `.vscode/` 폴더와 병합됨

---

**META**
- Category: ide
- Last Updated: 2026-01-30
- Version: 1.0.0
