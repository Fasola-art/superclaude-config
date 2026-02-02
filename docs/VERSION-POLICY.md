# Version Management Policy

> SuperClaude versioning and release policy

---

## Version Scheme

### Semantic Versioning
```
MAJOR.MINOR.PATCH
  │     │     └── Bug fixes, minor improvements
  │     └──────── New features, backward compatible
  └────────────── Major changes, breaking compatibility
```

### Current Version
```
SuperClaude v2.0.9
```

---

## Version Files

### VERSION File
```
~/.claude/VERSION
```

Content: `2.0.9`

### Metadata
```json
// ~/.claude/superclaude-metadata.json
{
  "version": "2.0.9",
  "installed": "2026-01-29",
  "lastUpdated": "2026-01-30"
}
```

---

## Update Policy

### Auto Updates
- Patch version: Auto-apply
- Minor version: Apply after notification
- Major version: Manual approval required

### Update Check
```
# Auto-checked via hook
~/.claude/hooks/UserPromptSubmit/auto-update-checker.js
```

---

## Release Notes

### Format
```markdown
## v2.0.9 (2026-01-30)

### New Features
- Feature A added
- Feature B improved

### Bug Fixes
- Issue #123 fixed
- Issue #456 fixed

### Changes
- Setting X changed
- Behavior Y improved
```

---

## Compatibility

### Plugin Compatibility
| SuperClaude | Plugin Min Version |
|-------------|---------------------|
| 2.0.x       | 1.0.0               |
| 2.1.x       | 1.1.0               |

### Claude Code Compatibility
| SuperClaude | Claude Code |
|-------------|-------------|
| 2.0.x       | 1.0.x       |
