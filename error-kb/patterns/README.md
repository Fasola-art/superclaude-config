# Error KB - Patterns Folder

> **Purpose**: Common error patterns and Quick Fix solution mapping
> **Updated**: 2026-01-30

---

## 📁 File Structure

```
patterns/
├── README.md              # This file
└── error-success-map.json # Error pattern → solution mapping
```

---

## 🎯 How It Works

1. **Error occurs** → Extract error message
2. **Pattern matching** → Compare with regex in `error-success-map.json`
3. **Quick Fix suggestion** → Suggest `fix` command from matched pattern
4. **Auto-apply** (optional) → Execute `fix` after user approval

---

## 📋 Pattern Types

| Type | Description | Example |
|------|-------------|---------|
| **quick_fixes** | Regex-based instant resolution | `npm install $1` |
| **error_classifications** | Category-based general solutions | `typescript_error` |

---

## 🔧 Adding Patterns

### Add Quick Fix
```json
{
  "id": "qf_xxx",
  "regex": "Error message pattern (use capture groups)",
  "fix": "Resolution command ($1, $2 reference capture groups)",
  "description": "Description",
  "category": "Classification category"
}
```

### Add Error Classification
```json
{
  "type": "new_error_type",
  "patterns": ["pattern1", "pattern2"],
  "solutions": ["solution1", "solution2"]
}
```

---

## 📊 Related Files

- `~/.claude/error-kb/categories/` - Category-specific detailed docs
- `~/.claude/error-kb/pending/` - Unresolved errors
- `~/.claude/error-kb/resolved/` - Resolved errors

---

**META**
- Category: error-kb/patterns
- Last Updated: 2026-01-30
