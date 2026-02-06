# Structs & Interfaces Rules

## Struct Patterns

### Constructor Functions

```go
func NewServer(addr string) *Server {
    return &Server{
        addr:    addr,
        timeout: 30 * time.Second,
    }
}
```

### Functional Options

```go
type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) {
        s.timeout = d
    }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{addr: addr, timeout: 30 * time.Second}
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

### Embedding

```go
type LoggedServer struct {
    *Server
    logger *slog.Logger
}
```

### Receiver Selection

```go
// Value: Small structs, immutable
func (p Point) String() string {
    return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

// Pointer: Large structs, needs mutation
func (s *Server) Start() error {
    s.running = true
    return nil
}
```

---

## Interface Rules

### Keep Small

```go
// GOOD
type Reader interface {
    Read(p []byte) (n int, err error)
}

// BAD: Too large
type Repository interface {
    Get, Save, Delete, Update, List, Count...
}
```

### Define at Consumer

```go
type UserGetter interface {
    GetByID(ctx context.Context, id string) (*User, error)
}

func NewHandler(ug UserGetter) *Handler {
    return &Handler{users: ug}
}
```

### Compile-time Check

```go
var _ UserRepository = (*PostgresRepo)(nil)
```
