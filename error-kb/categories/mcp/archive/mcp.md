# MCP Error Patterns

> **Category**: mcp-protocol
> **Updated**: 2026-01-30

---

## 🔴 Critical Errors

### Server Start Failed

**Message**: `MCP server start failed [server-name]`

**Causes**:
1. Package not installed
2. Invalid configuration
3. Permission issue

**Solutions**:
```bash
# 1. Check package
npm list -g | grep mcp

# 2. Manual execution test
npx @server-name/mcp --debug

# 3. Check configuration
cat ~/.claude/mcp.json

# 4. Check logs
tail -f ~/.claude/logs/mcp.log
```

**Example fix**:
```json
// Problem: gdrive server failed
// Fix: Replace with @isaacphi/mcp-gdrive

// mcp-router/servers.json
{
  "gdrive": {
    "command": "npx",
    "args": ["@isaacphi/mcp-gdrive"]
  }
}
```

---

### Request Timeout

**Message**: `Request timeout: initialize`

**Causes**:
1. Network issue
2. Server overload
3. Invalid configuration

**Solutions**:
```bash
# 1. Check network
ping registry.npmjs.org

# 2. Restart server
# Restart Claude Code

# 3. Adjust timeout settings
# mcp-router/config.json
{
  "timeout": 60000,  # Increase to 60 seconds
  "retries": 3
}
```

---

### Connection Refused

**Message**: `Connection refused: ECONNREFUSED`

**Causes**:
1. Server not running
2. Port conflict
3. Firewall

**Solutions**:
```bash
# 1. Check process
ps aux | grep mcp

# 2. Check port
lsof -i :port_number

# 3. Check firewall (macOS)
sudo pfctl -s rules
```

---

## 🟠 Common Errors

### Tool Call Failed

**Message**: `Tool call failed: [tool-name]`

**Causes**:
1. Invalid parameters
2. Authentication expired
3. Server error

**Solutions**:
```typescript
// Check parameters
{
  "tool": "context7.get-library-docs",
  "params": {
    "libraryId": "valid-ID",  // Required
    "query": "search term"    // Optional
  }
}

// Refresh authentication
// Re-configure authentication token for the server
```

---

### Serialization Error

**Message**: `JSON serialization failed`

**Cause**: Response data parsing failed

**Solutions**:
```bash
# Check raw response
npx @server-name/mcp --debug

# Update server version
npm update -g @server-name/mcp
```

---

## 🟡 Configuration Errors

### mcp.json Parsing Error

**Cause**: JSON syntax error

**Solutions**:
```bash
# Syntax check
cat ~/.claude/mcp.json | jq .

# Correct format
{
  "mcpServers": {
    "mcp-router": {
      "command": "python",
      "args": ["~/.claude/mcp-router/server.py"]
    }
  }
}
```

---

### Duplicate Server Registration

**Cause**: Same server registered multiple times

**Solutions**:
```json
// ❌ Wrong configuration
{
  "mcpServers": {
    "context7": { ... },    // Direct registration
    "mcp-router": { ... }   // Router also includes context7
  }
}

// ✅ Correct configuration (router only)
{
  "mcpServers": {
    "mcp-router": {
      "command": "python",
      "args": ["~/.claude/mcp-router/server.py"]
    }
  }
}
```

---

## 📊 Error Frequency

| Error | Frequency | Severity |
|-------|-----------|----------|
| Server start failed | High | High |
| Timeout | Medium | Medium |
| Tool call failed | Medium | Medium |
| Config error | Low | Low |

---

## 🔧 Debugging

```bash
# Full logs
tail -f ~/.claude/logs/mcp.log

# Specific server status
cat ~/.claude/mcp-router/status.json

# Manual test
echo '{"method":"tools/list"}' | npx @server-name/mcp
```

---

## 🔄 Recovery Procedures

### Full MCP Reset

```bash
# 1. Clear cache
rm -rf ~/.claude/mcp-router/cache/*

# 2. Reset status
rm ~/.claude/mcp-router/status.json

# 3. Restart Claude Code
# Run claude again in terminal
```

### Individual Server Reset

```bash
# 1. Remove server
# Delete server entry from mcp-router/servers.json

# 2. Clear cache
rm ~/.claude/mcp-router/cache/server-name.*

# 3. Re-add
# Re-register in mcp-router/servers.json
```

---

**META**
- Category: mcp-protocol
- Last Updated: 2026-01-30
