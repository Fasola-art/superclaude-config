# Async Programming Rules

## tokio Runtime

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let result = fetch_data().await?;
    println!("{}", result);
    Ok(())
}
```

## Async Patterns

### Parallel Execution

```rust
use tokio::join;

let (user, posts) = join!(
    fetch_user(id),
    fetch_posts(id)
);
```

### Concurrent Tasks

```rust
use tokio::spawn;

let handles: Vec<_> = urls.iter()
    .map(|url| spawn(fetch(url.clone())))
    .collect();

let results: Vec<_> = futures::future::join_all(handles)
    .await
    .into_iter()
    .filter_map(|r| r.ok())
    .collect();
```

### Timeouts

```rust
use tokio::time::{timeout, Duration};

match timeout(Duration::from_secs(30), fetch_data()).await {
    Ok(result) => handle(result?),
    Err(_) => return Err(anyhow!("Timeout")),
}
```

## Anti-patterns

```rust
// BAD: Blocking in async
async fn bad() {
    std::thread::sleep(Duration::from_secs(1));  // Blocks!
}

// GOOD: Async sleep
async fn good() {
    tokio::time::sleep(Duration::from_secs(1)).await;
}
```
