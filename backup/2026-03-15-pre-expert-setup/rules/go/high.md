# Go High Priority Rules (STRUCT + IFACE)

## STRUCT: 구조체 설계

### STRUCT-001: 생성자 함수
```go
func NewServer(addr string) *Server {
    return &Server{addr: addr, timeout: 30 * time.Second}
}
```

### STRUCT-002: Functional Options
```go
type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{addr: addr, timeout: 30 * time.Second}
    for _, opt := range opts { opt(s) }
    return s
}
```

### STRUCT-003: 임베딩
```go
type LoggedServer struct {
    *Server
    logger *slog.Logger
}
```

### STRUCT-004: Receiver 선택
```go
// Value: 작은 구조체, 불변
func (p Point) String() string { return fmt.Sprintf("(%d,%d)", p.X, p.Y) }

// Pointer: 큰 구조체, 변경 필요
func (s *Server) Start() error { s.running = true; return nil }
```

### STRUCT-005: 유용한 Zero Value
```go
type Buffer struct { data []byte }
var buf Buffer  // 바로 사용 가능
```

---

## IFACE: 인터페이스 설계

### IFACE-001: 작은 인터페이스
```go
// GOOD
type Reader interface { Read(p []byte) (n int, err error) }

// BAD: Get, Save, Delete, Update, List...
```

### IFACE-002: 소비자 측에서 정의
```go
type UserGetter interface {
    GetByID(ctx context.Context, id string) (*User, error)
}
func NewHandler(ug UserGetter) *Handler { return &Handler{users: ug} }
```

### IFACE-003: 인터페이스 합성
```go
type ReadWriter interface { Reader; Writer }
```

### IFACE-004: 컴파일 타임 검증
```go
var _ UserRepository = (*PostgresRepo)(nil)
```

### IFACE-005: any 최소화
```go
// BAD: func Process(data any) any
// GOOD: func Process[T any](data T) T
```
