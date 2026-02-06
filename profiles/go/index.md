# Go Language Profile

> **Version**: 1.0.0
> **Target**: Go 1.21+
> **Auto-detect**: `go.mod`, `go.sum`

---

## Goal

**Primary Outcome**: Idiomatic and efficient Go code

**Success Criteria**:
- [ ] All errors handled
- [ ] No goroutine leaks
- [ ] Context propagated
- [ ] Tests pass with `-race`

---

## Quick Reference

### Required Rules

| Rule | Description | Example |
|------|-------------|---------|
| **Error handling** | Always check errors | `if err != nil` |
| **Error wrapping** | Add context | `fmt.Errorf("x: %w", err)` |
| **Context** | Propagate context | `ctx context.Context` |
| **defer** | Resource cleanup | `defer f.Close()` |

### Tools

| Tool | Purpose |
|------|---------|
| `go fmt` | Format |
| `go vet` | Static analysis |
| `golangci-lint` | Comprehensive lint |
| `go test -race` | Race detection |

---

## Files

| File | Content |
|------|---------|
| [error-handling.md](error-handling.md) | Error patterns |
| [concurrency.md](concurrency.md) | Goroutines, channels |
| [structs-interfaces.md](structs-interfaces.md) | Design patterns |
| [testing.md](testing.md) | Table-driven tests |
| [performance.md](performance.md) | Optimization |

---

## Self-Diagnosis

### Critical
- [ ] All errors handled
- [ ] No bare `panic()`
- [ ] Context propagated

### Important
- [ ] Errors wrapped with context
- [ ] No goroutine leaks
- [ ] Tests with `-race`

---

## Commands

```bash
go fmt ./...
go vet ./...
golangci-lint run
go test -race ./...
```
