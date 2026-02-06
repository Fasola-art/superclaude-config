# Error Handling Rules

## Patterns

| Pattern | When to Use |
|---------|-------------|
| `Result<T, E>` | Recoverable errors |
| `Option<T>` | Optional values |
| `?` operator | Propagate errors |
| `thiserror` | Custom error types |
| `anyhow` | Application errors |

## Custom Error with thiserror

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("User not found: {0}")]
    UserNotFound(String),

    #[error("Invalid input: {0}")]
    ValidationError(String),

    #[error("Database error")]
    DatabaseError(#[from] sqlx::Error),

    #[error("IO error")]
    IoError(#[from] std::io::Error),
}

fn find_user(id: &str) -> Result<User, AppError> {
    let user = db.find(id)
        .ok_or_else(|| AppError::UserNotFound(id.to_string()))?;
    Ok(user)
}
```

## anyhow for Applications

```rust
use anyhow::{Context, Result};

fn process_file(path: &str) -> Result<String> {
    let content = std::fs::read_to_string(path)
        .context("Failed to read file")?;
    Ok(content)
}
```

## Anti-patterns

```rust
// BAD: unwrap in production
let user = get_user().unwrap();

// BAD: Ignore errors
let _ = save_data();

// GOOD: Handle errors
let user = get_user()?;

// GOOD: Match for specific handling
match get_user() {
    Ok(user) => process(user),
    Err(AppError::UserNotFound(id)) => create_user(id),
    Err(e) => return Err(e),
}
```
