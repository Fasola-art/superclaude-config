# Python Language Profile

> **Version**: 1.0.0
> **Target**: Python 3.10+
> **Auto-detect**: `pyproject.toml`, `requirements.txt`, `setup.py`

---

## Goal

**Primary Outcome**: Type-safe and maintainable Python code

**Success Criteria**:
- [ ] Type hints on all functions
- [ ] `mypy --strict` passes
- [ ] Zero `ruff` lint warnings
- [ ] Test coverage 80%+

---

## Quick Reference

### Required Rules

| Rule | Description | Example |
|------|-------------|---------|
| **Type hints** | All function signatures | `def fn(x: int) -> str:` |
| **f-string** | String formatting | `f"Hello, {name}"` |
| **pathlib** | Path handling | `Path("file.txt")` |
| **dataclass** | Data classes | `@dataclass` |

### Tools

| Tool | Purpose |
|------|---------|
| `ruff` | Lint + Format |
| `mypy` | Type check |
| `pytest` | Testing |
| `uv` | Package management |

---

## Files

| File | Content |
|------|---------|
| [type-hints.md](type-hints.md) | Type hint patterns |
| [error-handling.md](error-handling.md) | Exception handling |
| [class-design.md](class-design.md) | dataclass, Protocol |
| [async.md](async.md) | Async programming |
| [testing.md](testing.md) | pytest patterns |

---

## Self-Diagnosis

### Critical
- [ ] Type hints on all functions
- [ ] No bare `except:`
- [ ] No `Any` overuse

### Important
- [ ] `mypy --strict` passes
- [ ] `ruff check .` clean
- [ ] Tests with fixtures

---

## References

| Document | Link |
|----------|------|
| Python Docs | https://docs.python.org/3/ |
| mypy Docs | https://mypy.readthedocs.io/ |
| Ruff Docs | https://docs.astral.sh/ruff/ |
| Rules | `~/.claude/rules/python/` |
