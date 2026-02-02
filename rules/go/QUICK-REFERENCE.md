# Go Rules Quick Reference

## CRITICAL (Must Apply)

### Error Handling
```go
// Wrap errors with context
if err != nil {
    return fmt.Errorf("context: %w", err)
}
```

### Never Ignore Errors
```go
// BAD: data, _ := os.ReadFile(...)
// GOOD: data, err := os.ReadFile(...)
```

### Propagate Context
```go
func Fetch(ctx context.Context, url string) error {
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    ...
}
```

---

## HIGH (Strongly Recommended)

### errgroup
```go
g, ctx := errgroup.WithContext(ctx)
for _, url := range urls {
    url := url
    g.Go(func() error { return fetch(ctx, url) })
}
return g.Wait()
```

### Functional Options
```go
func NewServer(addr string, opts ...Option) *Server
```

### Small Interfaces
```go
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

---

## MEDIUM (Recommended)

### Early Return
```go
if err != nil {
    return err
}
// Main logic
```

### Table-Driven Tests
```go
tests := []struct{ name string; input, expected int }{...}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {...})
}
```

### Preallocate Slices
```go
items := make([]Item, 0, cap)
```

---

## LOW (Optional)

### sync.Pool
```go
var pool = sync.Pool{New: func() any { return new(Buffer) }}
```

### strings.Builder
```go
var sb strings.Builder
sb.WriteString("...")
```

---

## Validation Commands

```bash
# Required checks
go fmt ./...
go vet ./...
golangci-lint run
go test -race ./...

# Benchmark
go test -bench=. -benchmem
```
