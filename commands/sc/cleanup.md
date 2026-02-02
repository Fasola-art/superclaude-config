---
description: "Cleanup code"
argument-hint: "[target]"
---

# Cleanup

Clean up code and remove unnecessary elements.

## Usage

```
/sc:cleanup            # Full project
/sc:cleanup src/       # Specific directory
/sc:cleanup --imports  # Unused imports only
/sc:cleanup --logs     # console.log only
```

## Cleanup Items

- Remove unused imports
- Remove console.log/debug statements
- Warn about unused variables
- Format cleanup
