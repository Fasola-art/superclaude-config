# Go Coding Rules (38 Rules)

> **Version**: 2026.01
> **Target**: Go 1.21+
> **Goal**: Idiomatic and efficient Go code

---

## Priority Summary

| Priority | Category | Rules | Key Effect             |
|----------|----------|-------|------------------------|
| CRITICAL | ERROR    | 6     | Robust error handling  |
| CRITICAL | CONCUR   | 6     | Safe concurrency       |
| HIGH     | STRUCT   | 5     | Struct design          |
| HIGH     | IFACE    | 5     | Interface design       |
| MEDIUM   | FUNC     | 5     | Function design        |
| MEDIUM   | PKG      | 5     | Package structure      |
| LOW      | PERF     | 3     | Performance optimization |
| LOW      | TEST     | 3     | Test patterns          |

---

## CRITICAL: ERROR (Error Handling)

### ERROR-001: Handle Errors Immediately

```go
// BAD: Ignoring error
data, _ := os.ReadFile("config.json")

// GOOD: Handle error
data, err := os.ReadFile("config.json")
if err != nil {
    return nil, fmt.Errorf("failed to read config file: %w", err)
}
```

### ERROR-002: Wrap Errors with Context

```go
// BAD: No context
if err != nil {
    return err
}

// GOOD: Add context
if err != nil {
    return fmt.Errorf("failed to fetch user %s: %w", userID, err)
}
```

### ERROR-003: Use Sentinel Errors

```go
var (
    ErrNotFound = errors.New("not found")
    ErrInvalid  = errors.New("invalid input")
)

// Usage
if errors.Is(err, ErrNotFound) {
    return http.StatusNotFound
}
```

### ERROR-004: Custom Error Types

```go
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}

// Usage
var notFound *NotFoundError
if errors.As(err, &notFound) {
    log.Printf("Resource: %s, ID: %s", notFound.Resource, notFound.ID)
}
```

### ERROR-005: Never Use panic

```go
// BAD: Using panic
if err != nil {
    panic(err)
}

// GOOD: Return error
if err != nil {
    return nil, err
}
```

### ERROR-006: Use defer for Resource Cleanup

```go
func ReadFile(path string) ([]byte, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer f.Close()  // Always executes

    return io.ReadAll(f)
}
```

---

## CRITICAL: CONCUR (Concurrency)

### CONCUR-001: Use errgroup

```go
g, ctx := errgroup.WithContext(ctx)

for _, url := range urls {
    url := url  // Capture
    g.Go(func() error {
        return fetch(ctx, url)
    })
}

if err := g.Wait(); err != nil {
    return err
}
```

### CONCUR-002: Propagate Context

```go
func Fetch(ctx context.Context, url string) (*Response, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }
    return http.DefaultClient.Do(req)
}
```

### CONCUR-003: Set Timeouts

```go
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()

result, err := Fetch(ctx, url)
```

### CONCUR-004: Communicate via Channels

```go
// BAD: Shared memory
var counter int
go func() { counter++ }()

// GOOD: Channel
results := make(chan int)
go func() { results <- compute() }()
result := <-results
```

### CONCUR-005: Prevent Goroutine Leaks

```go
// BAD: Potential leak
go func() {
    for {
        process()
    }
}()

// GOOD: Exit via context
go func() {
    for {
        select {
        case <-ctx.Done():
            return
        default:
            process()
        }
    }
}()
```

### CONCUR-006: Only Sender Closes Channel

```go
func producer(ch chan<- int) {
    defer close(ch)  // Sender closes
    for i := 0; i < 10; i++ {
        ch <- i
    }
}

func consumer(ch <-chan int) {
    for v := range ch {
        process(v)
    }
}
```

---

## HIGH: STRUCT (Structs)

### STRUCT-001: Constructor Functions

```go
type Server struct {
    addr    string
    timeout time.Duration
}

func NewServer(addr string) *Server {
    return &Server{
        addr:    addr,
        timeout: 30 * time.Second,
    }
}
```

### STRUCT-002: Functional Options

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

### STRUCT-003: Embedding

```go
type LoggedServer struct {
    *Server
    logger *slog.Logger
}
```

### STRUCT-004: Pointer vs Value Receivers

```go
// Value receiver: Small structs, immutable
func (p Point) String() string {
    return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

// Pointer receiver: Large structs, needs mutation
func (s *Server) Start() error {
    s.running = true
    return nil
}
```

### STRUCT-005: Useful Zero Values

```go
// Zero value is valid state
type Buffer struct {
    data []byte
}

var buf Buffer  // Ready to use
buf.Write([]byte("hello"))
```

---

## HIGH: IFACE (Interfaces)

### IFACE-001: Keep Interfaces Small

```go
// GOOD: Small interface
type Reader interface {
    Read(p []byte) (n int, err error)
}

// BAD: Too large interface
type Repository interface {
    Get, Save, Delete, Update, List, Count, Search...
}
```

### IFACE-002: Define at Consumer Side

```go
// Define interface where needed
type UserGetter interface {
    GetByID(ctx context.Context, id string) (*User, error)
}

func NewHandler(ug UserGetter) *Handler {
    return &Handler{users: ug}
}
```

### IFACE-003: Compose Interfaces

```go
type ReadWriter interface {
    Reader
    Writer
}
```

### IFACE-004: Verify Interface Compliance

```go
var _ UserRepository = (*PostgresRepo)(nil)
```

### IFACE-005: Minimize Empty Interface

```go
// BAD
func Process(data any) any { ... }

// GOOD
func Process[T any](data T) T { ... }
```

---

## MEDIUM: FUNC (Functions)

### FUNC-001: Explicit Returns

```go
// BAD: Naked return
func divide(a, b int) (result int, err error) {
    if b == 0 {
        err = errors.New("division by zero")
        return
    }
    result = a / b
    return
}

// GOOD: Explicit return
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}
```

### FUNC-002: Early Return

```go
func process(data *Data) error {
    if data == nil {
        return ErrNilData
    }
    if !data.Valid() {
        return ErrInvalidData
    }
    // Main logic
    return nil
}
```

### FUNC-003: Variadic Parameters

```go
func Sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}
```

### FUNC-004: Closure Capture Caution

```go
// BAD: Variable capture issue
for _, v := range values {
    go func() {
        process(v)  // Always last value
    }()
}

// GOOD: Explicit capture
for _, v := range values {
    v := v  // Local copy
    go func() {
        process(v)
    }()
}
```

### FUNC-005: defer Order

```go
func process() {
    defer fmt.Println("first")   // Executes last
    defer fmt.Println("second")  // Executes second
    defer fmt.Println("third")   // Executes first
}
// Output: third, second, first (LIFO)
```

---

## MEDIUM: PKG (Packages)

### PKG-001: Package Naming

```go
// GOOD
package user
package http
package json

// BAD
package userService  // No camelCase
package utils        // Too generic
package common       // Meaningless
```

### PKG-002: Internal Packages

```
project/
├── cmd/
├── internal/    # Not accessible externally
│   ├── config/
│   └── db/
└── pkg/         # Publicly accessible
```

### PKG-003: No Circular Dependencies

```go
// BAD: A → B → A
// GOOD: Separate with interfaces
```

### PKG-004: Minimize init()

```go
// Use only when necessary
func init() {
    // Registry registration, etc.
}

// Prefer explicit initialization
func Setup() error {
    return nil
}
```

### PKG-005: Documentation Comments

```go
// Package user provides user management functionality.
package user

// User represents a system user.
type User struct {
    ID   string
    Name string
}

// NewUser creates a new user with the given name.
func NewUser(name string) *User {
    return &User{Name: name}
}
```

---

## LOW: PERF (Performance)

### PERF-001: Preallocate Slices

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

---

## LOW: TEST (Testing)

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

---

**META**
- Version: 2026.01
- Last Updated: 2026-01-30
