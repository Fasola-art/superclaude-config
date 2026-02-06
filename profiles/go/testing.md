# Testing Rules

## Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -2, -3, -5},
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

## Subtests

```go
func TestUser(t *testing.T) {
    t.Run("Create", func(t *testing.T) {
        user := NewUser("Alice")
        if user.Name != "Alice" {
            t.Error("expected Alice")
        }
    })

    t.Run("Validate", func(t *testing.T) {
        user := NewUser("")
        if err := user.Validate(); err == nil {
            t.Error("expected validation error")
        }
    })
}
```

## Test Helpers

```go
func setupTestDB(t *testing.T) *DB {
    t.Helper()
    db, err := NewTestDB()
    if err != nil {
        t.Fatalf("failed to create db: %v", err)
    }
    t.Cleanup(func() { db.Close() })
    return db
}
```

## Parallel Tests

```go
func TestParallel(t *testing.T) {
    t.Parallel()
    // Runs in parallel
}
```

## Commands

```bash
go test ./...
go test -v ./...
go test -cover ./...
go test -race ./...
```
