# Go Testing

## Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
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
            t.Error("expected name to be Alice")
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
func TestWithDB(t *testing.T) {
    db := setupTestDB(t)

    user := &User{Name: "Alice"}
    if err := db.Create(user); err != nil {
        t.Fatalf("failed to create user: %v", err)
    }
}

func setupTestDB(t *testing.T) *DB {
    t.Helper()
    db, err := NewTestDB()
    if err != nil {
        t.Fatalf("failed to create test db: %v", err)
    }
    t.Cleanup(func() { db.Close() })
    return db
}
```

## Parallel Tests

```go
func TestParallel(t *testing.T) {
    t.Parallel()
    // Runs in parallel with other parallel tests
}
```

---

## Commands

```bash
go test ./...         # Run all
go test -v ./...      # Verbose
go test -cover ./...  # Coverage
go test -race ./...   # Race detection
```
