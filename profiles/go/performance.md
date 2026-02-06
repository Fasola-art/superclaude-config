# Performance Rules

## Patterns

| Pattern | Effect |
|---------|--------|
| Preallocate slices | Avoid reallocations |
| strings.Builder | Efficient string concat |
| sync.Pool | Reuse objects |

## Preallocate

```go
// GOOD: Known capacity
items := make([]Item, 0, expectedSize)
```

## strings.Builder

```go
var sb strings.Builder
sb.Grow(100)
sb.WriteString("Hello, ")
sb.WriteString("World!")
result := sb.String()
```

## sync.Pool

```go
var bufPool = sync.Pool{
    New: func() any {
        return new(bytes.Buffer)
    },
}

func Process(data []byte) {
    buf := bufPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufPool.Put(buf)
    }()
    buf.Write(data)
}
```

## Benchmarking

```go
func BenchmarkProcess(b *testing.B) {
    data := generateTestData()
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Process(data)
    }
}
```

```bash
go test -bench=. -benchmem
```
