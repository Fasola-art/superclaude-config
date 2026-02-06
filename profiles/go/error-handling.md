# Error Handling Rules

## Patterns

| Pattern | Example |
|---------|---------|
| Immediate handling | `if err != nil { return err }` |
| Wrap with context | `fmt.Errorf("fetch user: %w", err)` |
| Sentinel errors | `var ErrNotFound = errors.New()` |
| Custom error types | `type NotFoundError struct{}` |

## Good Patterns

```go
// Wrap errors with context
if err != nil {
    return fmt.Errorf("failed to fetch user %s: %w", userID, err)
}

// Sentinel errors
var (
    ErrNotFound = errors.New("not found")
    ErrInvalid  = errors.New("invalid input")
)

// Usage
if errors.Is(err, ErrNotFound) {
    return http.StatusNotFound
}

// Custom error type
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found: %s", e.Resource, e.ID)
}

// Check custom error
var notFound *NotFoundError
if errors.As(err, &notFound) {
    log.Printf("Resource: %s, ID: %s", notFound.Resource, notFound.ID)
}
```

## Anti-patterns

```go
// BAD: Ignoring error
data, _ := os.ReadFile("config.json")

// BAD: No context
if err != nil {
    return err
}

// BAD: Using panic
if err != nil {
    panic(err)
}

// GOOD: defer for cleanup
f, err := os.Open(path)
if err != nil {
    return nil, err
}
defer f.Close()
```
