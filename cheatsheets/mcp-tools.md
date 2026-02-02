# MCP Tools Cheatsheet

> **Version**: 1.0.0
> **Updated**: 2026-01-30

---

## Quick Reference

### MCP Router Architecture

```
Claude Code
    ↓
mcp-router (single entry point)
    ↓
Dynamic loading of required servers only
    ├── context7
    ├── serena
    └── playwright
```

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Single entry point** | Only mcp-router registered in mcp.json |
| **Dynamic loading** | Run servers only when needed |
| **Context saving** | Minimize system prompts |

---

## Available MCP Servers

### Context7 - Library Documentation Search

| Tool | Description | Usage Example |
|------|-------------|---------------|
| `resolve` | Lookup library ID | Check Next.js docs ID |
| `get-library-docs` | Search documentation | Next.js routing docs |

#### Usage Examples

```
"Find Next.js App Router docs"
→ context7.resolve("next.js")
→ context7.get-library-docs(id, "app router")
```

#### Supported Libraries

| Library | Purpose |
|---------|---------|
| Next.js | React framework |
| React | UI library |
| Supabase | Backend service |
| Tailwind | CSS framework |
| Prisma | ORM |

---

### Serena - Code Analysis

| Tool | Description | Usage Example |
|------|-------------|---------------|
| `find-symbol` | Search symbol | Find function/class location |
| `get-definition` | Get definition | Check function implementation |
| `find-references` | Find references | Find usages |
| `analyze-file` | Analyze file | Understand structure |

#### Usage Examples

```
"Find UserService class definition"
→ serena.find-symbol("UserService")
→ serena.get-definition(location)

"Find where this function is used"
→ serena.find-references(symbol)
```

---

### Playwright - Browser Automation

| Tool | Description | Usage Example |
|------|-------------|---------------|
| `navigate` | Navigate page | Visit URL |
| `click` | Click | Button click |
| `fill` | Input | Form fill |
| `screenshot` | Screenshot | Screen capture |
| `evaluate` | Run JS | Custom script |

#### Usage Examples

```
"Take a screenshot of this page"
→ playwright.navigate(url)
→ playwright.screenshot()

"Test the login form"
→ playwright.fill("#email", "test@example.com")
→ playwright.fill("#password", "password")
→ playwright.click("button[type=submit]")
```

---

## MCP Router Configuration

### mcp.json Configuration (Correct Method)

```json
{
  "mcpServers": {
    "mcp-router": {
      "command": "python",
      "args": ["~/.claude/mcp-router/server.py"]
    }
  }
}
```

### Incorrect Configuration (Never Do This)

```json
{
  "mcpServers": {
    "context7": { ... },    // Direct registration forbidden
    "sequential": { ... },  // Context explosion
    "playwright": { ... }   // System prompt bloat
  }
}
```

---

## Server List (mcp-router/servers.json)

### Currently Registered Servers

| Server | Command | Purpose |
|--------|---------|---------|
| `context7` | `npx @context7/mcp` | Documentation search |
| `serena` | `npx @serena/mcp` | Code analysis |
| `playwright` | `npx @playwright/mcp` | Browser automation |

### Adding New Server

```json
// ~/.claude/mcp-router/servers.json
{
  "servers": {
    "new-server": {
      "command": "npx",
      "args": ["@new-server/mcp"],
      "description": "New server description"
    }
  }
}
```

---

## Usage Scenarios

### Documentation Search Flow

```
1. Identify library
   → context7.resolve("library-name")

2. Search documentation
   → context7.get-library-docs(id, "search term")

3. Use results
   → Apply to code generation
```

### Code Analysis Flow

```
1. Search symbol
   → serena.find-symbol("class/function name")

2. Check definition
   → serena.get-definition(location)

3. Find references
   → serena.find-references(symbol)

4. Impact analysis
   → Plan refactoring
```

### Browser Testing Flow

```
1. Navigate to page
   → playwright.navigate(url)

2. Interact
   → playwright.fill / click

3. Verify
   → playwright.screenshot / evaluate

4. Check results
   → Analyze test results
```

---

## Cautions

### Context Management

| Situation | Caution |
|-----------|---------|
| Multiple server calls | Call sequentially, no parallel |
| Large responses | Request only needed parts |
| Cache usage | Avoid repeated identical requests |

### Performance Considerations

| Server | Response Time | Resources |
|--------|---------------|-----------|
| context7 | Fast | Low |
| serena | Medium | Medium |
| playwright | Slow | High |

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No server response | Server not running | Restart mcp-router |
| Timeout | Network issue | Retry |
| Permission error | Auth issue | Check token |

### Debugging

```bash
# Check MCP logs
tail -f ~/.claude/logs/mcp.log

# Check server status
cat ~/.claude/mcp-router/status.json

# Run server manually
npx @context7/mcp --debug
```

---

## References

| Document | Path |
|----------|------|
| MCP Integration Guide | `~/.claude/skills/mcp-integration/` |
| MCP Router Config | `~/.claude/mcp-router/` |
| Settings Guide | `~/.claude/docs/SETTINGS-GUIDE.md` |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
