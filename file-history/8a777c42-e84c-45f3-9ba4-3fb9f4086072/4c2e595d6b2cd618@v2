# Go 언어 프로필

> **버전**: 1.0.0
> **적용 대상**: Go 1.21+
> **자동 감지**: `go.mod` 존재 시

---

## 🎯 목표

**Primary Outcome**: 관용적(idiomatic)이고 효율적인 Go 코드 생성

**Success Criteria**:
- [ ] `go vet` 경고 0개
- [ ] `golangci-lint` 통과
- [ ] 모든 에러 명시적 처리
- [ ] 불필요한 goroutine 누수 0개

**Failure Cases**:
- 🔴 에러 무시 (`_ = err`) → 명시적 처리
- 🔴 data race 발생 → `go test -race` 통과 필수

---

## 🚀 빠른 참조

### Go 철학

| 원칙 | 설명 | 예시 |
|------|------|------|
| **Simplicity** | 단순함 추구 | 제네릭보다 인터페이스 |
| **Explicitness** | 명시적 표현 | 에러 명시적 반환 |
| **Composition** | 상속 대신 합성 | 임베딩 활용 |
| **Concurrency** | CSP 모델 | 채널로 통신 |

### 필수 명령어

```bash
# 빌드 전 필수 검사
go fmt ./...                    # 포맷팅
go vet ./...                    # 정적 분석
golangci-lint run              # 린트
go test -race ./...            # 레이스 검사
```

---

## 📋 섹션 1: 에러 처리 규칙

### 📊 에러 처리 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| `if err != nil` | 모든 에러 체크 | 즉시 반환 |
| `errors.Is()` | 에러 비교 | sentinel 에러 |
| `errors.As()` | 에러 타입 추출 | 커스텀 에러 |
| `fmt.Errorf("%w")` | 에러 래핑 | 컨텍스트 추가 |

### ✅ 에러 처리 패턴

```go
// ✅ GOOD: 에러 즉시 처리
func LoadConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("설정 파일 읽기 실패: %w", err)
    }

    var config Config
    if err := json.Unmarshal(data, &config); err != nil {
        return nil, fmt.Errorf("JSON 파싱 실패: %w", err)
    }

    return &config, nil
}

// ✅ GOOD: 커스텀 에러 타입
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}

// ✅ GOOD: sentinel 에러
var (
    ErrNotFound = errors.New("not found")
    ErrInvalid  = errors.New("invalid input")
)

// ✅ GOOD: 에러 체인 확인
func handleError(err error) {
    if errors.Is(err, ErrNotFound) {
        // 404 처리
    }

    var notFound *NotFoundError
    if errors.As(err, &notFound) {
        log.Printf("Resource: %s, ID: %s", notFound.Resource, notFound.ID)
    }
}
```

### ❌ 에러 처리 안티패턴

```go
// ❌ BAD: 에러 무시
data, _ := os.ReadFile("config.json")

// ❌ BAD: panic 남용
if err != nil {
    panic(err)  // 복구 불가
}

// ❌ BAD: 에러 래핑 없이 반환
if err != nil {
    return err  // 컨텍스트 손실
}

// ❌ BAD: 문자열 비교
if err.Error() == "not found" {  // fragile
    ...
}
```

### ⚠️ 예외 처리

| 상황 | 허용되는 패턴 |
|------|--------------|
| main 함수 | `log.Fatal(err)` |
| 테스트 코드 | `t.Fatal(err)` |
| 초기화 실패 | `panic()` (프로그램 시작 불가) |
| 불변 조건 위반 | `panic()` (버그) |

---

## 📋 섹션 2: 구조체와 인터페이스 규칙

### 📊 구조체 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| **Functional Options** | 선택적 설정 | `WithTimeout()` |
| **Embedding** | 합성 | `type Server struct { *http.Server }` |
| **Constructor** | 초기화 | `NewXXX()` 함수 |

### ✅ 구조체 패턴

```go
// ✅ GOOD: Functional Options 패턴
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
        timeout: 30 * time.Second,  // 기본값
        logger:  slog.Default(),
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// 사용
server := NewServer(":8080",
    WithTimeout(10*time.Second),
    WithLogger(customLogger),
)

// ✅ GOOD: 임베딩으로 합성
type LoggedServer struct {
    *Server
    accessLog *AccessLog
}
```

### 📊 인터페이스 패턴

| 원칙 | 설명 | 예시 |
|------|------|------|
| **작은 인터페이스** | 1-3개 메서드 | `io.Reader`, `io.Writer` |
| **소비자 정의** | 사용하는 쪽에서 정의 | 의존성 역전 |
| **암묵적 구현** | implements 키워드 없음 | 덕 타이핑 |

### ✅ 인터페이스 패턴

```go
// ✅ GOOD: 작은 인터페이스
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// ✅ GOOD: 합성된 인터페이스
type ReadWriter interface {
    Reader
    Writer
}

// ✅ GOOD: 소비자 쪽에서 정의
// repository.go (인터페이스 정의)
type UserRepository interface {
    GetByID(ctx context.Context, id string) (*User, error)
    Save(ctx context.Context, user *User) error
}

// postgres_repo.go (구현)
type PostgresUserRepo struct {
    db *sql.DB
}

func (r *PostgresUserRepo) GetByID(ctx context.Context, id string) (*User, error) {
    // 구현
}

// ✅ GOOD: 인터페이스 검증
var _ UserRepository = (*PostgresUserRepo)(nil)
```

### ❌ 인터페이스 안티패턴

```go
// ❌ BAD: 너무 큰 인터페이스
type Repository interface {
    GetByID(id string) (*Model, error)
    GetAll() ([]*Model, error)
    Create(m *Model) error
    Update(m *Model) error
    Delete(id string) error
    Count() (int, error)
    Search(query string) ([]*Model, error)
    // ... 10개 이상 메서드
}

// ❌ BAD: 제공자 쪽에서 인터페이스 정의
// impl.go
type MyService interface {  // 제공자가 정의
    DoSomething() error
}

type myServiceImpl struct{}  // 자기 인터페이스 구현
```

---

## 📋 섹션 3: 동시성 규칙

### 📊 동시성 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| **goroutine + channel** | 통신 | `ch <- data` |
| **sync.WaitGroup** | 완료 대기 | `wg.Wait()` |
| **context.Context** | 취소/타임아웃 | `ctx.Done()` |
| **errgroup** | 에러 있는 병렬 | `g.Go(func() error)` |

### ✅ 동시성 패턴

```go
// ✅ GOOD: errgroup으로 병렬 처리
func FetchAll(ctx context.Context, urls []string) ([]Response, error) {
    g, ctx := errgroup.WithContext(ctx)
    responses := make([]Response, len(urls))

    for i, url := range urls {
        i, url := i, url  // 캡처
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

// ✅ GOOD: worker pool
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

// ✅ GOOD: context로 타임아웃
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

### ❌ 동시성 안티패턴

```go
// ❌ BAD: goroutine 누수
func leakyGoroutine() {
    ch := make(chan int)
    go func() {
        val := <-ch  // 영원히 블록 (송신자 없음)
        fmt.Println(val)
    }()
    // 함수 종료, goroutine은 영원히 대기
}

// ❌ BAD: context 없는 goroutine
go func() {
    for {
        process()  // 취소 불가
    }
}()

// ❌ BAD: 공유 메모리로 통신
var counter int
go func() { counter++ }()  // data race
go func() { counter++ }()

// ✅ GOOD: 채널로 통신
results := make(chan int)
go func() { results <- compute() }()
```

### ⚠️ 예외 처리

| 상황 | 주의사항 |
|------|----------|
| goroutine 내 panic | `recover()` 필수 |
| 채널 close | 송신자만 close |
| select default | 바쁜 대기 주의 |

---

## 📋 섹션 4: 테스트 규칙

### 📊 테스트 전략

| 테스트 유형 | 파일명 | 커버리지 목표 |
|------------|--------|--------------|
| 단위 테스트 | `*_test.go` | 80% |
| 테이블 테스트 | 여러 케이스 | 핵심 함수 |
| 벤치마크 | `Benchmark*` | 성능 핵심부 |
| 통합 테스트 | `// +build integration` | 핵심 경로 |

### ✅ 테스트 패턴

```go
// ✅ GOOD: 테이블 기반 테스트
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

// ✅ GOOD: testify 사용
func TestUser(t *testing.T) {
    user := NewUser("test")

    assert.NotNil(t, user)
    assert.Equal(t, "test", user.Name)
    assert.NoError(t, user.Validate())
}

// ✅ GOOD: 벤치마크
func BenchmarkProcess(b *testing.B) {
    data := generateTestData()

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Process(data)
    }
}

// ✅ GOOD: 병렬 테스트
func TestParallel(t *testing.T) {
    tests := []struct{ name string }{...}

    for _, tt := range tests {
        tt := tt  // 캡처
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            // 테스트 로직
        })
    }
}
```

---

## 📋 섹션 5: 프로젝트 구조 규칙

### 📊 표준 레이아웃

```
project/
├── go.mod
├── go.sum
├── main.go              # 또는 cmd/app/main.go
├── cmd/
│   └── app/
│       └── main.go      # 진입점
├── internal/            # 비공개 패키지
│   ├── config/
│   ├── handler/
│   ├── service/
│   └── repository/
├── pkg/                 # 공개 패키지 (선택)
├── api/                 # API 정의 (OpenAPI, proto)
├── web/                 # 웹 자산
├── scripts/             # 빌드/배포 스크립트
├── testdata/            # 테스트 데이터
└── docs/
```

### 📊 패키지 명명 규칙

| 규칙 | 예시 | 안티패턴 |
|------|------|----------|
| 소문자, 단일 단어 | `user`, `http` | `userService`, `HTTP` |
| 명사형 | `config` | `configure` |
| 복수형 피하기 | `user` | `users` |
| util/common 피하기 | 구체적 이름 | `util`, `helpers` |

---

## 📋 섹션 6: 성능 최적화 규칙

### 📊 최적화 체크리스트

| 항목 | 도구 | 목표 |
|------|------|------|
| 할당 최소화 | `pprof` | 핫 경로 0 alloc |
| escape 분석 | `go build -gcflags=-m` | 힙 할당 최소화 |
| 슬라이스 사전 할당 | `make([]T, 0, cap)` | 재할당 방지 |
| sync.Pool | 객체 재사용 | GC 부하 감소 |

### ✅ 최적화 패턴

```go
// ✅ GOOD: 슬라이스 사전 할당
items := make([]Item, 0, expectedSize)

// ✅ GOOD: strings.Builder
var sb strings.Builder
sb.Grow(100)  // 예상 크기
sb.WriteString("Hello, ")
sb.WriteString("World!")
result := sb.String()

// ✅ GOOD: sync.Pool
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
    // 처리
}

// ✅ GOOD: 포인터 수신자 (큰 구조체)
func (s *LargeStruct) Method() {
    // 복사 방지
}
```

---

## 📋 섹션 7: 로깅 규칙 (slog)

### ✅ 구조화된 로깅

```go
import "log/slog"

// ✅ GOOD: 구조화된 로깅
logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

logger.Info("사용자 생성",
    slog.String("user_id", user.ID),
    slog.String("email", user.Email),
    slog.Duration("duration", elapsed),
)

// ✅ GOOD: 에러 로깅
logger.Error("데이터베이스 연결 실패",
    slog.String("host", dbHost),
    slog.Any("error", err),
)

// ✅ GOOD: 컨텍스트 전파
ctx = context.WithValue(ctx, "request_id", requestID)
logger.InfoContext(ctx, "요청 처리 시작")
```

---

## ✅ 자가 진단 체크리스트

### 🔴 Critical (반드시 완료)
- [ ] `go vet ./...` 경고 0개
- [ ] `go test -race ./...` 통과
- [ ] 모든 에러 명시적 처리 (무시 금지)
- [ ] goroutine 누수 없음

### 🟡 Important (80% 이상)
- [ ] `golangci-lint` 통과
- [ ] 에러 래핑으로 컨텍스트 제공
- [ ] context.Context 전파
- [ ] 테스트 커버리지 80%+

### 🟢 Nice-to-have
- [ ] 벤치마크 작성
- [ ] pprof 프로파일링
- [ ] 문서 주석 작성

**합격 기준**: Critical 100% + Important 80% 이상

---

## 📚 참조

| 문서 | 링크 |
|------|------|
| Effective Go | https://go.dev/doc/effective_go |
| Go Code Review | https://go.dev/wiki/CodeReviewComments |
| Go Proverbs | https://go-proverbs.github.io/ |
| Uber Style Guide | https://github.com/uber-go/guide |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Auto-detect: `go.mod`
