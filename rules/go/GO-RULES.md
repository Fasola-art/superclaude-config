# Go 코딩 규칙 (38개 규칙)

> **버전**: 2026.01
> **적용 대상**: Go 1.21+
> **목표**: 관용적(idiomatic)이고 효율적인 Go 코드

---

## 우선순위 요약

| 우선순위 | 카테고리 | 규칙 수 | 핵심 효과 |
|---------|---------|--------|----------|
| 🔴 CRITICAL | ERROR | 6 | 안정적 에러 처리 |
| 🔴 CRITICAL | CONCUR | 6 | 안전한 동시성 |
| 🟠 HIGH | STRUCT | 5 | 구조체 설계 |
| 🟠 HIGH | IFACE | 5 | 인터페이스 설계 |
| 🟡 MEDIUM | FUNC | 5 | 함수 설계 |
| 🟡 MEDIUM | PKG | 5 | 패키지 구조 |
| 🟢 LOW | PERF | 3 | 성능 최적화 |
| 🟢 LOW | TEST | 3 | 테스트 패턴 |

---

## 🔴 CRITICAL: ERROR (에러 처리)

### ERROR-001: 에러 즉시 처리

```go
// ❌ BAD: 에러 무시
data, _ := os.ReadFile("config.json")

// ✅ GOOD: 에러 처리
data, err := os.ReadFile("config.json")
if err != nil {
    return nil, fmt.Errorf("설정 파일 읽기 실패: %w", err)
}
```

### ERROR-002: 에러 래핑

```go
// ❌ BAD: 컨텍스트 없음
if err != nil {
    return err
}

// ✅ GOOD: 컨텍스트 추가
if err != nil {
    return fmt.Errorf("사용자 %s 조회 실패: %w", userID, err)
}
```

### ERROR-003: sentinel 에러

```go
var (
    ErrNotFound = errors.New("not found")
    ErrInvalid  = errors.New("invalid input")
)

// 사용
if errors.Is(err, ErrNotFound) {
    return http.StatusNotFound
}
```

### ERROR-004: 커스텀 에러 타입

```go
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}

// 사용
var notFound *NotFoundError
if errors.As(err, &notFound) {
    log.Printf("리소스: %s, ID: %s", notFound.Resource, notFound.ID)
}
```

### ERROR-005: panic 금지

```go
// ❌ BAD: panic 사용
if err != nil {
    panic(err)
}

// ✅ GOOD: 에러 반환
if err != nil {
    return nil, err
}
```

### ERROR-006: defer로 리소스 정리

```go
func ReadFile(path string) ([]byte, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer f.Close()  // 항상 실행

    return io.ReadAll(f)
}
```

---

## 🔴 CRITICAL: CONCUR (동시성)

### CONCUR-001: errgroup 사용

```go
g, ctx := errgroup.WithContext(ctx)

for _, url := range urls {
    url := url  // 캡처
    g.Go(func() error {
        return fetch(ctx, url)
    })
}

if err := g.Wait(); err != nil {
    return err
}
```

### CONCUR-002: context 전파

```go
func Fetch(ctx context.Context, url string) (*Response, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }
    return http.DefaultClient.Do(req)
}
```

### CONCUR-003: 타임아웃 설정

```go
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()

result, err := Fetch(ctx, url)
```

### CONCUR-004: 채널로 통신

```go
// ❌ BAD: 공유 메모리
var counter int
go func() { counter++ }()

// ✅ GOOD: 채널
results := make(chan int)
go func() { results <- compute() }()
result := <-results
```

### CONCUR-005: goroutine 누수 방지

```go
// ❌ BAD: 누수 가능
go func() {
    for {
        process()
    }
}()

// ✅ GOOD: context로 종료
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

### CONCUR-006: 송신자만 close

```go
func producer(ch chan<- int) {
    defer close(ch)  // 송신자가 close
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

## 🟠 HIGH: STRUCT (구조체)

### STRUCT-001: 생성자 함수

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

### STRUCT-003: 임베딩

```go
type LoggedServer struct {
    *Server
    logger *slog.Logger
}
```

### STRUCT-004: 포인터 vs 값 수신자

```go
// 값 수신자: 작은 구조체, 불변
func (p Point) String() string {
    return fmt.Sprintf("(%d, %d)", p.X, p.Y)
}

// 포인터 수신자: 큰 구조체, 수정 필요
func (s *Server) Start() error {
    s.running = true
    return nil
}
```

### STRUCT-005: 제로값 유용하게

```go
// ✅ 제로값이 유효한 상태
type Buffer struct {
    data []byte
}

var buf Buffer  // 바로 사용 가능
buf.Write([]byte("hello"))
```

---

## 🟠 HIGH: IFACE (인터페이스)

### IFACE-001: 작은 인터페이스

```go
// ✅ GOOD: 작은 인터페이스
type Reader interface {
    Read(p []byte) (n int, err error)
}

// ❌ BAD: 너무 큰 인터페이스
type Repository interface {
    Get, Save, Delete, Update, List, Count, Search...
}
```

### IFACE-002: 소비자 정의

```go
// 소비자 쪽에서 필요한 인터페이스 정의
type UserGetter interface {
    GetByID(ctx context.Context, id string) (*User, error)
}

func NewHandler(ug UserGetter) *Handler {
    return &Handler{users: ug}
}
```

### IFACE-003: 인터페이스 합성

```go
type ReadWriter interface {
    Reader
    Writer
}
```

### IFACE-004: 인터페이스 검증

```go
var _ UserRepository = (*PostgresRepo)(nil)
```

### IFACE-005: 빈 인터페이스 최소화

```go
// ❌ BAD
func Process(data any) any { ... }

// ✅ GOOD
func Process[T any](data T) T { ... }
```

---

## 🟡 MEDIUM: FUNC (함수)

### FUNC-001: 명확한 반환

```go
// ❌ BAD: naked return
func divide(a, b int) (result int, err error) {
    if b == 0 {
        err = errors.New("division by zero")
        return
    }
    result = a / b
    return
}

// ✅ GOOD: 명시적 반환
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}
```

### FUNC-002: 조기 반환

```go
func process(data *Data) error {
    if data == nil {
        return ErrNilData
    }
    if !data.Valid() {
        return ErrInvalidData
    }
    // 정상 로직
    return nil
}
```

### FUNC-003: 가변 인자

```go
func Sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}
```

### FUNC-004: 클로저 주의

```go
// ❌ BAD: 변수 캡처 문제
for _, v := range values {
    go func() {
        process(v)  // 항상 마지막 값
    }()
}

// ✅ GOOD: 명시적 전달
for _, v := range values {
    v := v  // 로컬 복사
    go func() {
        process(v)
    }()
}
```

### FUNC-005: defer 순서

```go
func process() {
    defer fmt.Println("first")   // 마지막 실행
    defer fmt.Println("second")  // 두 번째 실행
    defer fmt.Println("third")   // 첫 번째 실행
}
// 출력: third, second, first (LIFO)
```

---

## 🟡 MEDIUM: PKG (패키지)

### PKG-001: 패키지 명명

```go
// ✅ GOOD
package user
package http
package json

// ❌ BAD
package userService  // camelCase 금지
package utils        // 너무 일반적
package common       // 무의미
```

### PKG-002: 내부 패키지

```
project/
├── cmd/
├── internal/    # 외부 접근 불가
│   ├── config/
│   └── db/
└── pkg/         # 외부 공개 가능
```

### PKG-003: 순환 의존성 금지

```go
// ❌ BAD: A → B → A
// ✅ GOOD: 인터페이스로 분리
```

### PKG-004: init() 최소화

```go
// ⚠️ 필요한 경우만 사용
func init() {
    // 레지스트리 등록 등
}

// ✅ 명시적 초기화 선호
func Setup() error {
    return nil
}
```

### PKG-005: 문서 주석

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

## 🟢 LOW: PERF (성능)

### PERF-001: 슬라이스 사전 할당

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

## 🟢 LOW: TEST (테스트)

### TEST-001: 테이블 기반 테스트

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

### TEST-002: 병렬 테스트

```go
func TestParallel(t *testing.T) {
    tests := []struct{ name string }{...}

    for _, tt := range tests {
        tt := tt
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            // 테스트
        })
    }
}
```

### TEST-003: 벤치마크

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

## 📊 체크리스트

### 빌드 전
```bash
go fmt ./...
go vet ./...
golangci-lint run
go test -race ./...
```

### 코드 리뷰 시
- [ ] 모든 에러 처리됨
- [ ] 에러 래핑 적절함
- [ ] goroutine 누수 없음
- [ ] context 전파됨

---

**META**
- Version: 2026.01
- Last Updated: 2026-01-30
