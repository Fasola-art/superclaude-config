# Go Critical Rules (ERROR + CONCUR)

## ERROR: 에러 처리

### ERROR-001: 에러 즉시 처리
```go
// BAD
data, _ := os.ReadFile("config.json")

// GOOD
data, err := os.ReadFile("config.json")
if err != nil {
    return nil, fmt.Errorf("config read failed: %w", err)
}
```

### ERROR-002: 컨텍스트와 함께 래핑
```go
if err != nil {
    return fmt.Errorf("fetch user %s: %w", userID, err)
}
```

### ERROR-003: Sentinel Errors
```go
var ErrNotFound = errors.New("not found")

if errors.Is(err, ErrNotFound) { return http.StatusNotFound }
```

### ERROR-004: Custom Error Types
```go
type NotFoundError struct { Resource, ID string }
func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}
// errors.As(err, &notFound)
```

### ERROR-005: panic 금지 → return error

### ERROR-006: defer로 리소스 정리
```go
f, err := os.Open(path)
if err != nil { return nil, err }
defer f.Close()
```

---

## CONCUR: 동시성

### CONCUR-001: errgroup 사용
```go
g, ctx := errgroup.WithContext(ctx)
for _, url := range urls {
    url := url
    g.Go(func() error { return fetch(ctx, url) })
}
return g.Wait()
```

### CONCUR-002: Context 전파
```go
req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
```

### CONCUR-003: 타임아웃 설정
```go
ctx, cancel := context.WithTimeout(ctx, 10*time.Second)
defer cancel()
```

### CONCUR-004: 채널로 통신
```go
// BAD: var counter int; go func() { counter++ }()
// GOOD
ch := make(chan int)
go func() { ch <- compute() }()
result := <-ch
```

### CONCUR-005: Goroutine Leak 방지
```go
for {
    select {
    case <-ctx.Done(): return
    default: process()
    }
}
```

### CONCUR-006: 채널은 송신자만 close
```go
func producer(ch chan<- int) {
    defer close(ch)
    for i := 0; i < 10; i++ { ch <- i }
}
```
