# Go Low Priority Rules (PERF + TEST)

## PERF: 성능 최적화

### PERF-001: Slice 사전 할당
```go
items := make([]Item, 0, expectedSize)
```

### PERF-002: strings.Builder
```go
var sb strings.Builder
sb.Grow(100)
sb.WriteString("Hello, ")
sb.WriteString("World!")
result := sb.String()
```

### PERF-003: sync.Pool
```go
var bufPool = sync.Pool{
    New: func() any { return new(bytes.Buffer) },
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

---

## TEST: 테스트 패턴

### TEST-001: Table-Driven Tests
```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("got %d, want %d", result, tt.expected)
            }
        })
    }
}
```

### TEST-002: Parallel Tests
```go
func TestParallel(t *testing.T) {
    tests := []struct{ name string }{...}

    for _, tt := range tests {
        tt := tt
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            // Test
        })
    }
}
```

### TEST-003: Benchmarks
```go
func BenchmarkProcess(b *testing.B) {
    data := generateTestData()
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Process(data)
    }
}
```

---

## Checklist

### Before Build
```bash
go fmt ./...
go vet ./...
golangci-lint run
go test -race ./...
```

### Code Review
- [ ] All errors handled
- [ ] Errors wrapped appropriately
- [ ] No goroutine leaks
- [ ] Context propagated
