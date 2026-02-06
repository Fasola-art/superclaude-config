# Python Rules (42 Rules)

> Python 3.10+ | Type-safe & Maintainable

## File Structure

| File | Content | Rules |
|------|---------|-------|
| [critical.md](critical.md) | TYPE + ERROR | 11 |
| [high.md](high.md) | ASYNC + CLASS | 10 |
| [medium.md](medium.md) | FUNC + IMPORT | 11 |
| [low.md](low.md) | PERF + TEST | 10 |
| [QUICK-REFERENCE.md](QUICK-REFERENCE.md) | Quick ref | - |

## Validation

```bash
mypy --strict . && ruff check . && pytest -v
```
