# Go 규칙 퀵 레퍼런스

## 🔴 CRITICAL (반드시 적용)

### 에러 처리
```go
// ✅ 에러 래핑
if err != nil {
    return fmt.Errorf("context: %w", err)
}
```

### 에러 무시 금지
```go
// ❌ data, _ := os.ReadFile(...)
// ✅ data, err := os.ReadFile(...)
```

### context 전파
```go
func Fetch(ctx context.Context, url string) error {
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    ...
}
```

---

## 🟠 HIGH (강력 권장)

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

### 작은 인터페이스
```go
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

---

## 🟡 MEDIUM (권장)

### 조기 반환
```go
if err != nil {
    return err
}
// 정상 로직
```

### 테이블 테스트
```go
tests := []struct{ name string; input, expected int }{...}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {...})
}
```

### 슬라이스 사전 할당
```go
items := make([]Item, 0, cap)
```

---

## 🟢 LOW (선택)

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

## 검사 명령어

```bash
# 필수 검사
go fmt ./...
go vet ./...
golangci-lint run
go test -race ./...

# 벤치마크
go test -bench=. -benchmem
```
