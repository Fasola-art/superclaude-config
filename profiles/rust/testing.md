# Testing Rules

## Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_user_creation() {
        let user = User::new("1", "Alice");
        assert_eq!(user.name, "Alice");
    }

    #[test]
    #[should_panic(expected = "invalid")]
    fn test_panic() {
        validate("invalid");
    }
}
```

## Result Tests

```rust
#[test]
fn test_parse() -> Result<(), Box<dyn std::error::Error>> {
    let value = parse("123")?;
    assert_eq!(value, 123);
    Ok(())
}
```

## Async Tests

```rust
#[tokio::test]
async fn test_fetch() {
    let result = fetch_data().await.unwrap();
    assert!(!result.is_empty());
}
```

## Test Organization

```rust
// tests/integration_test.rs
use my_crate::*;

#[test]
fn integration_test() {
    let app = App::new();
    let result = app.process("input");
    assert!(result.is_ok());
}
```

## Commands

```bash
cargo test                    # Run all tests
cargo test test_name          # Run specific test
cargo test -- --nocapture     # Show println
cargo test -- --test-threads=1  # Sequential
```
