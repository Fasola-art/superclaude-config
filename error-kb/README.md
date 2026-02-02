# Error Knowledge Base (Error KB)

> **Version**: 1.0.0
> **Purpose**: Error pattern learning and auto-resolution support

---

## 🎯 Goal

**Primary Outcome**: Auto-recognize recurring errors and suggest solutions

**Workflow**:
1. Error occurs → Record in `pending/`
2. Resolved → Move to `resolved/` + save solution
3. Similar error occurs → Match via Jaccard similarity (threshold: 0.70)
4. Match found → Auto-apply previous solution

---

## 📁 Directory Structure

```
error-kb/
├── README.md              # This file (index)
├── pending/               # Unresolved errors
│   └── {hash}.json
├── resolved/              # Resolved errors
│   └── {hash}.json
├── categories/            # Category-specific patterns
│   ├── typescript.md
│   ├── react.md
│   ├── nextjs.md
│   ├── mcp.md
│   └── git.md
├── patterns/              # Quick Fix pattern mapping
│   ├── README.md
│   └── error-success-map.json
└── templates/             # Registration templates
    └── error-entry.json
```

---

## 📊 Current Status

### Statistics

| Item | Count |
|------|-------|
| Resolved errors | 8 |
| Unresolved errors | 4 |
| Categories | 5 |

### Recently Resolved Errors

| ID | Type | Message | Solution |
|----|------|---------|----------|
| cd40c474953d | mcp-protocol | Server start failed: gdrive | Replace with @isaacphi/mcp-gdrive |
| 8153edd3e663 | mcp-protocol | - | - |

---

## 🔧 Usage

### Error Search

```bash
# Slash command
/error-search "error message"

# Or Vibe keyword
"fix this TypeError"
```

### Manual Registration

```bash
# Add new error to pending
cp templates/error-entry.json pending/{new-hash}.json
# Edit and save content
```

### Mark as Resolved

```bash
# Move to resolved
mv pending/{hash}.json resolved/{hash}.json
# Update resolution field
```

---

## 📋 JSON Schema

### Error Entry Structure

```json
{
  "id": "string (12-char hash)",
  "type": "string (error category)",
  "message": "string (error message)",
  "timestamp": "string (occurrence time)",
  "raw_log": "string (original log)",
  "created_at": "string (ISO 8601)",
  "resolved": "boolean",
  "resolution": "string | null (solution)",
  "context": "object (additional context)",
  "resolved_at": "string | null (resolution time)",
  "tags": ["string"] (optional),
  "related_files": ["string"] (optional),
  "prevention": "string (prevention measure, optional)"
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique hash (12 chars) |
| `type` | string | Error category |
| `message` | string | Error message |
| `resolved` | boolean | Resolution status |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `resolution` | string | Resolution method |
| `context` | object | Additional info |
| `tags` | string[] | Search tags |
| `prevention` | string | Prevention measure |

---

## 🏷️ Error Types (Categories)

| Type | Description | Examples |
|------|-------------|----------|
| `typescript` | TS compile errors | TS2304, TS2345 |
| `react` | React runtime errors | Hydration, Hook rules |
| `nextjs` | Next.js errors | Build, SSR, App Router |
| `mcp-protocol` | MCP server errors | Connection failed, timeout |
| `git` | Git errors | Conflicts, permissions, remote |
| `npm` | Package errors | Install, version conflicts |
| `build` | Build errors | Webpack, Vite |
| `runtime` | Runtime errors | TypeError, ReferenceError |

---

## 🔍 Similarity Matching

### Jaccard Similarity

```python
def jaccard_similarity(a: str, b: str) -> float:
    tokens_a = set(tokenize(a))
    tokens_b = set(tokenize(b))
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)
```

### Matching Settings

```yaml
threshold: 0.70          # Match if 70%+ similar
max_suggestions: 3       # Max 3 suggestions
boost_same_type: 0.1     # Bonus for same type
```

---

## 📚 Category Documents

### Quick Links

| Category | Document | Key Patterns |
|----------|----------|--------------|
| TypeScript | [typescript.md](categories/typescript.md) | TS2304, TS2345, strict mode |
| React | [react.md](categories/react.md) | Hydration, Hook rules |
| Next.js | [nextjs.md](categories/nextjs.md) | App Router, SSR |
| MCP | [mcp.md](categories/mcp.md) | Connection, timeout |
| Git | [git.md](categories/git.md) | Conflicts, remote |

---

## 🔄 Auto-Learning

### Self-Healing Flow

```
1. Error occurs
2. Search Error KB (similarity 0.70+)
3. If matched:
   - Auto-apply previous solution
   - Verify build/test
   - Complete if success
   - Try next solution if failed (max 10 attempts)
4. If not matched:
   - Record in pending
   - Notify user
```

### Learning Triggers

| Event | Action |
|-------|--------|
| Manual resolution | Update resolution field |
| Pattern recognition | Group similar errors |
| Frequent occurrence | Increase priority |

---

## ⚠️ Cautions

1. **Exclude PII**: Never include API keys, passwords in error logs
2. **Minimize context**: Store only necessary information
3. **Regular cleanup**: Review old pending items
4. **Adjust similarity**: Increase threshold if too many false positives

---

## 📊 Statistics Commands

```bash
# Total stats
ls -la ~/.claude/error-kb/{pending,resolved}/ | wc -l

# Stats by type
grep -l '"type": "typescript"' ~/.claude/error-kb/**/*.json | wc -l

# Recently resolved errors
ls -lt ~/.claude/error-kb/resolved/ | head -5
```

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Similarity Threshold: 0.70
- Max Ralph Retries: 10
