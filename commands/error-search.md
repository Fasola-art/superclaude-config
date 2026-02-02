---
description: "Search similar errors in Error KB"
argument-hint: "[error_message]"
---

# Error KB Search

Analyze error messages and search for similar resolved cases in Error KB.

## Behavior

1. Analyze the error message from arguments or recent errors
2. Search `~/.claude/error-kb/resolved/` using Jaccard similarity (threshold: 70%)
3. Match Quick Fix patterns from `~/.claude/patterns/error-success-map.json`
4. Present solution if similar resolved case exists
5. Suggest registering as new error if not found

## Usage Examples

```
/error-search "Cannot find module 'react'"
/error-search "TS2304: Cannot find name 'useState'"
```

## Output Format

```
🔍 Error KB Search Results

Error: [Error message summary]
Type: [module_not_found | typescript_error | ...]

📌 Similar Resolved Case Found (similarity: 85%)
- Cause: [Cause description]
- Solution: [Solution method]
- Command: [Successful command]

💡 Quick Fix: [Immediately executable fix]
```
