# Concurrency Rules

## Patterns

| Pattern | When to Use |
|---------|-------------|
| `errgroup` | Parallel execution with errors |
| Context | Cancellation, timeouts |
| Channels | Communication |
| `sync.WaitGroup` | Wait for goroutines |

## errgroup

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

## Context Propagation

```go
func Fetch(ctx context.Context, url string) (*Response, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }
    return http.DefaultClient.Do(req)
}

// With timeout
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()
```

## Channels

```go
// Only sender closes channel
func producer(ch chan<- int) {
    defer close(ch)
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

## Anti-patterns

```go
// BAD: Goroutine leak
go func() {
    for {
        process()  // Never exits
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
