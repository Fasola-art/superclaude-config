# Go Language Profile

> **Version**: 1.0.0
> **Target**: Go 1.21+
> **Auto-detect**: Presence of `go.mod`

---

## Goal

**Primary Outcome**: Generate idiomatic and efficient Go code

**Success Criteria**:
- [ ] Zero `go vet` warnings
- [ ] `golangci-lint` passes
- [ ] All errors explicitly handled
- [ ] Zero unnecessary goroutine leaks

**Failure Cases**:
- Ignored error (`_ = err`) → Explicit handling required
- Data race detected → `go test -race` must pass

---

## Quick Reference

### Go Philosophy

| Principle | Description | Example |
|-----------|-------------|---------|
| **Simplicity** | Pursue simplicity | Interface over generics |
| **Explicitness** | Explicit expression | Explicit error return |
| **Composition** | Composition over inheritance | Use embedding |
| **Concurrency** | CSP model | Communicate via channels |

### Required Commands

```bash
# Pre-build required checks
go fmt ./...                    # Formatting
go vet ./...                    # Static analysis
golangci-lint run              # Lint
go test -race ./...            # Race detection
```

---

## Section 1: Error Handling Rules

### Error Handling Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `if err != nil` | All error checks | Immediate return |
| `errors.Is()` | Error comparison | Sentinel errors |
| `errors.As()` | Error type extraction | Custom errors |
| `fmt.Errorf("%w")` | Error wrapping | Add context |

### Error Handling Patterns

```go
// GOOD: Immediate error handling
func LoadConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("failed to read config file: %w", err)
    }

    var config Config
    if err := json.Unmarshal(data, &config); err != nil {
        return nil, fmt.Errorf("JSON parse failed: %w", err)
    }

    return &config, nil
}

// GOOD: Custom error type
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}

// GOOD: Sentinel errors
var (
    ErrNotFound = errors.New("not found")
    ErrInvalid  = errors.New("invalid input")
)

// GOOD: Error chain verification
func handleError(err error) {
    if errors.Is(err, ErrNotFound) {
        // Handle 404
    }

    var notFound *NotFoundError
    if errors.As(err, &notFound) {
        log.Printf("Resource: %s, ID: %s", notFound.Resource, notFound.ID)
    }
}
```

### Error Handling Anti-patterns

```go
// BAD: Ignore error
data, _ := os.ReadFile("config.json")

// BAD: panic overuse
if err != nil {
    panic(err)  // Unrecoverable
}

// BAD: Return error without wrapping
if err != nil {
    return err  // Context lost
}

// BAD: String comparison
if err.Error() == "not found" {  // Fragile
    ...
}
```

### Exception Handling

| Situation | Allowed Pattern |
|-----------|-----------------|
| main function | `log.Fatal(err)` |
| Test code | `t.Fatal(err)` |
| Initialization failure | `panic()` (program cannot start) |
| Invariant violation | `panic()` (bug) |

---

## Section 2: Struct and Interface Rules

### Struct Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Functional Options** | Optional settings | `WithTimeout()` |
| **Embedding** | Composition | `type Server struct { *http.Server }` |
| **Constructor** | Initialization | `NewXXX()` function |

### Struct Patterns

```go
// GOOD: Functional Options pattern
type Server struct {
    addr    string
    timeout time.Duration
    logger  *slog.Logger
}

type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) {
        s.timeout = d
    }
}

func WithLogger(l *slog.Logger) Option {
    return func(s *Server) {
        s.logger = l
    }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{
        addr:    addr,
        timeout: 30 * time.Second,  // Default
        logger:  slog.Default(),
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
server := NewServer(":8080",
    WithTimeout(10*time.Second),
    WithLogger(customLogger),
)

// GOOD: Composition via embedding
type LoggedServer struct {
    *Server
    accessLog *AccessLog
}
```

### Interface Patterns

| Principle | Description | Example |
|-----------|-------------|---------|
| **Small interfaces** | 1-3 methods | `io.Reader`, `io.Writer` |
| **Consumer-defined** | Define on consumer side | Dependency inversion |
| **Implicit implementation** | No implements keyword | Duck typing |

### Interface Patterns

```go
// GOOD: Small interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// GOOD: Composed interface
type ReadWriter interface {
    Reader
    Writer
}

// GOOD: Consumer-side definition
// repository.go (interface definition)
type UserRepository interface {
    GetByID(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

// postgres_repo.go (implementation)
type PostgresUserRepo struct {
    db *sql.DB
}

func (r *PostgresUserRepo) GetByID(ctx context.Context, id string) (*User, error) {
    // Implementation
}

// GOOD: Interface verification
var _ UserRepository = (*PostgresUserRepo)(nil)
```

### Interface Anti-patterns

```go
// BAD: Too large interface
type Repository interface {
    GetByID(id string) (*Model, error)
    GetAll() ([]*Model, error)
    Create(m *Model) error
    Update(m *Model) error
    Delete(id string) error
    Count() (int, error)
    Search(query string) ([]*Model, error)
    // ... 10+ methods
}

// BAD: Provider-side interface definition
// impl.go
type MyService interface {  // Provider defines
    DoSomething() error
}

type myServiceImpl struct{}  // Implements own interface
```

---

## Section 3: Concurrency Rules

### Concurrency Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **goroutine + channel** | Communication | `ch <- data` |
| **sync.WaitGroup** | Wait for completion | `wg.Wait()` |
| **context.Context** | Cancellation/Timeout | `ctx.Done()` |
| **errgroup** | Parallel with errors | `g.Go(func() error)` |

### Concurrency Patterns

```go
// GOOD: Parallel processing with errgroup
func FetchAll(ctx context.Context, urls []string) ([]Response, error) {
    g, ctx := errgroup.WithContext(ctx)
    responses := make([]Response, len(urls))

    for i, url := range urls {
        i, url := i, url  // Capture
        g.Go(func() error {
            resp, err := fetch(ctx, url)
            if err != nil {
                return err
            }
            responses[i] = resp
            return nil
        })
    }

    if err := g.Wait(); err != nil {
        return nil, err
    }
    return responses, nil
}

// GOOD: Worker pool
func WorkerPool(ctx context.Context, jobs <-chan Job, results chan<- Result) {
    var wg sync.WaitGroup
    numWorkers := runtime.GOMAXPROCS(0)

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for {
                select {
                case job, ok := <-jobs:
                    if !ok {
                        return
                    }
                    results <- process(job)
                case <-ctx.Done():
                    return
                }
            }
        }()
    }

    wg.Wait()
    close(results)
}

// GOOD: Timeout with context
func FetchWithTimeout(url string) (*Response, error) {
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }

    return http.DefaultClient.Do(req)
}
```

### Concurrency Anti-patterns

```go
// BAD: Goroutine leak
func leakyGoroutine() {
    ch := make(chan int)
    go func() {
        val := <-ch  // Blocks forever (no sender)
        fmt.Println(val)
    }()
    // Function exits, goroutine waits forever
}

// BAD: Goroutine without context
go func() {
    for {
        process()  // Cannot cancel
    }
}()

// BAD: Communicate via shared memory
var counter int
go func() { counter++ }()  // Data race
go func() { counter++ }()

// GOOD: Communicate via channels
results := make(chan int)
go func() { results <- compute() }()
```

### Exception Handling

| Situation | Note |
|-----------|------|
| panic in goroutine | `recover()` required |
| Channel close | Only sender closes |
| select default | Beware busy waiting |

---

## Section 4: Testing Rules

### Test Strategy

| Test Type | Filename | Coverage Target |
|-----------|----------|-----------------|
| Unit test | `*_test.go` | 80% |
| Table test | Multiple cases | Core functions |
| Benchmark | `Benchmark*` | Performance critical |
| Integration test | `// +build integration` | Critical paths |

### Test Patterns

```go
// GOOD: Table-based test
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
                t.Errorf("Add(%d, %d) = %d, want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

// GOOD: Using testify
func TestUser(t *testing.T) {
    user := NewUser("test")

    assert.NotNil(t, user)
    assert.Equal(t, "test", user.Name)
    assert.NoError(t, user.Validate())
}

// GOOD: Benchmark
func BenchmarkProcess(b *testing.B) {
    data := generateTestData()

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Process(data)
    }
}

// GOOD: Parallel test
func TestParallel(t *testing.T) {
    tests := []struct{ name string }{...}

    for _, tt := range tests {
        tt := tt  // Capture
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            // Test logic
        })
    }
}
```

---

## Section 5: Project Structure Rules

### Standard Layout

```
project/
├── go.mod
├── go.sum
├── main.go              # Or cmd/app/main.go
├── cmd/
│   └── app/
│       └── main.go      # Entry point
├── internal/            # Private packages
│   ├── config/
│   ├── handler/
│   ├── service/
│   └── repository/
├── pkg/                 # Public packages (optional)
├── api/                 # API definitions (OpenAPI, proto)
├── web/                 # Web assets
├── scripts/             # Build/deploy scripts
├── testdata/            # Test data
└── docs/
```

### Package Naming Rules

| Rule | Example | Anti-pattern |
|------|---------|--------------|
| Lowercase, single word | `user`, `http` | `userService`, `HTTP` |
| Noun form | `config` | `configure` |
| Avoid plurals | `user` | `users` |
| Avoid util/common | Specific name | `util`, `helpers` |

---

## Section 6: Performance Optimization Rules

### Optimization Checklist

| Item | Tool | Target |
|------|------|--------|
| Minimize allocations | `pprof` | Zero alloc on hot paths |
| Escape analysis | `go build -gcflags=-m` | Minimize heap allocations |
| Slice pre-allocation | `make([]T, 0, cap)` | Prevent reallocations |
| sync.Pool | Object reuse | Reduce GC pressure |

### Optimization Patterns

```go
// GOOD: Slice pre-allocation
items := make([]Item, 0, expectedSize)

// GOOD: strings.Builder
var sb strings.Builder
sb.Grow(100)  // Expected size
sb.WriteString("Hello, ")
sb.WriteString("World!")
result := sb.String()

// GOOD: sync.Pool
var bufferPool = sync.Pool{
    New: func() any {
        return new(bytes.Buffer)
    },
}

func Process(data []byte) {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufferPool.Put(buf)
    }()

    buf.Write(data)
    // Process
}

// GOOD: Pointer receiver (large structs)
func (s *LargeStruct) Method() {
    // Prevents copy
}
```

---

## Section 7: Logging Rules (slog)

### Structured Logging

```go
import "log/slog"

// GOOD: Structured logging
logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

logger.Info("User created",
    slog.String("user_id", user.ID),
    slog.String("email", user.Email),
    slog.Duration("duration", elapsed),
)

// GOOD: Error logging
logger.Error("Database connection failed",
    slog.String("host", dbHost),
    slog.Any("error", err),
)

// GOOD: Context propagation
ctx = context.WithValue(ctx, "request_id", requestID)
logger.InfoContext(ctx, "Request processing started")
```

---

## Self-Diagnosis Checklist

### Critical (Must Complete)
- [ ] Zero `go vet ./...` warnings
- [ ] `go test -race ./...` passes
- [ ] All errors explicitly handled (no ignoring)
- [ ] No goroutine leaks

### Important (80%+)
- [ ] `golangci-lint` passes
- [ ] Error wrapping provides context
- [ ] context.Context propagation
- [ ] Test coverage 80%+

### Nice-to-have
- [ ] Written benchmarks
- [ ] pprof profiling
- [ ] Documentation comments

**Pass Criteria**: Critical 100% + Important 80%+

---

## References

| Document | Link |
|----------|------|
| Effective Go | https://go.dev/doc/effective_go |
| Go Code Review | https://go.dev/wiki/CodeReviewComments |
| Go Proverbs | https://go-proverbs.github.io/ |
| Uber Style Guide | https://github.com/uber-go/guide |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Auto-detect: `go.mod`
