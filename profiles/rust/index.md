# Rust Language Profile

> **Version**: 1.0.0
> **Target**: Rust 1.75+
> **Auto-detect**: `Cargo.toml`

---

## Goal

**Primary Outcome**: Safe, concurrent, and performant Rust code

**Success Criteria**:
- [ ] `cargo clippy` passes
- [ ] No `unwrap()` in production
- [ ] Proper error handling with `Result`
- [ ] Tests pass

---

## Quick Reference

### Required Rules

| Rule | Description | Example |
|------|-------------|---------|
| **Result** | Error handling | `Result<T, E>` |
| **?** operator | Error propagation | `file.read()?` |
| **No unwrap** | Safe access | Use `?` or `match` |
| **Ownership** | Memory safety | Borrow when possible |

### Tools

| Tool | Purpose |
|------|---------|
| `cargo fmt` | Format |
| `cargo clippy` | Lint |
| `cargo test` | Test |
| `cargo build --release` | Optimized build |

---

## Files

| File | Content |
|------|---------|
| [error-handling.md](error-handling.md) | Result, thiserror, anyhow |
| [ownership.md](ownership.md) | Ownership, borrowing, lifetimes |
| [structs-traits.md](structs-traits.md) | Struct, impl, traits |
| [async.md](async.md) | tokio, async/await |
| [testing.md](testing.md) | Tests, mocking |

---

## Self-Diagnosis

### Critical
- [ ] No `unwrap()` in production
- [ ] `cargo clippy` clean
- [ ] Proper `Result` handling

### Important
- [ ] Custom error types
- [ ] Minimal `.clone()`
- [ ] Tests included

---

## Commands

```bash
cargo fmt
cargo clippy
cargo test
cargo build --release
```
