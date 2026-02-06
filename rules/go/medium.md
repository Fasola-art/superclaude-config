# Go Medium Priority Rules (FUNC + PKG)

## FUNC: 함수 설계

### FUNC-001: 명시적 반환
```go
// BAD: Naked return
func divide(a, b int) (result int, err error) {
    if b == 0 { err = errors.New("division by zero"); return }
    result = a / b; return
}

// GOOD: Explicit return
func divide(a, b int) (int, error) {
    if b == 0 { return 0, errors.New("division by zero") }
    return a / b, nil
}
```

### FUNC-002: Early Return
```go
func process(data *Data) error {
    if data == nil { return ErrNilData }
    if !data.Valid() { return ErrInvalidData }
    // Main logic
    return nil
}
```

### FUNC-003: Variadic Parameters
```go
func Sum(nums ...int) int {
    total := 0
    for _, n := range nums { total += n }
    return total
}
```

### FUNC-004: Closure Capture 주의
```go
// BAD: Variable capture issue
for _, v := range values {
    go func() { process(v) }()  // Always last value
}

// GOOD: Explicit capture
for _, v := range values {
    v := v  // Local copy
    go func() { process(v) }()
}
```

### FUNC-005: defer 순서 (LIFO)
```go
func process() {
    defer fmt.Println("first")   // Executes last
    defer fmt.Println("second")  // Executes second
    defer fmt.Println("third")   // Executes first
}
// Output: third, second, first
```

---

## PKG: 패키지 구조

### PKG-001: 패키지 명명
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

### PKG-002: Internal 패키지
```
project/
├── cmd/
├── internal/    # Not accessible externally
│   ├── config/
│   └── db/
└── pkg/         # Publicly accessible
```

### PKG-003: 순환 의존성 금지
```go
// BAD: A → B → A
// GOOD: Separate with interfaces
```

### PKG-004: init() 최소화
```go
// Prefer explicit initialization
func Setup() error { return nil }
```

### PKG-005: 문서화 주석
```go
// Package user provides user management functionality.
package user

// User represents a system user.
type User struct { ID, Name string }

// NewUser creates a new user with the given name.
func NewUser(name string) *User { return &User{Name: name} }
```
