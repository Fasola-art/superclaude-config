# Rust Language Profile

> **Version**: 1.0.0
> **Target**: Rust 2021 Edition+
> **Auto-detect**: Presence of `Cargo.toml`

---

## Goal

**Primary Outcome**: Generate memory-safe and performance-optimized Rust code

**Success Criteria**:
- [ ] Zero `panic!` possible code (Never Panics)
- [ ] All errors handled with `Result<T, E>`
- [ ] Zero `clippy` warnings
- [ ] Zero unnecessary `clone()`

**Failure Cases**:
- `unwrap()` in production code → Replace with `?` operator
- `unsafe` block → Must review safe alternatives

---

## Quick Reference

### Never Panics Principle

| Prohibited Pattern | Alternative | Reason |
|--------------------|-------------|--------|
| `.unwrap()` | `.ok()`, `?`, `unwrap_or()` | Runtime panic |
| `.expect()` | `?` + context | Runtime panic |
| `panic!()` | `Result::Err()` | Unrecoverable |
| `array[index]` | `.get(index)` | Out of bounds panic |
| `slice[..]` | `.get(..)` | Out of bounds panic |

### Required Commands

```bash
# Pre-build required checks
cargo clippy -- -D warnings     # Warnings = Errors
cargo fmt --check               # Format check
cargo test                      # Run tests
cargo miri test                 # UB check (nightly)
```

---

## Section 1: Error Handling Rules

### Error Handling Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `Result<T, E>` | All fallible operations | File I/O, parsing, API |
| `Option<T>` | Value may be absent | Search results, config |
| `?` operator | Error propagation | `file.read()?` |
| `anyhow` | Application errors | CLI, web servers |
| `thiserror` | Library errors | Custom error types |

### Error Handling Patterns

```rust
// GOOD: Custom error with thiserror
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("File not found: {0}")]
    FileNotFound(String),

    #[error("Parse failed: {0}")]
    ParseError(#[from] serde_json::Error),

    #[error("Network error: {0}")]
    NetworkError(#[from] reqwest::Error),
}

// GOOD: Return Result
pub fn load_config(path: &str) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)
        .map_err(|_| AppError::FileNotFound(path.to_string()))?;

    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}

// GOOD: Option handling
fn find_user(id: u64) -> Option<User> {
    users.iter().find(|u| u.id == id).cloned()
}

// Usage
let user = find_user(42).ok_or(AppError::UserNotFound)?;
```

### Error Handling Anti-patterns

```rust
// BAD: unwrap() usage
let config = load_config("config.json").unwrap();

// BAD: expect() in production
let file = File::open("data.txt").expect("Failed to open file");

// BAD: panic! usage
if value < 0 {
    panic!("Negative values not allowed");
}

// BAD: Direct index access
let first = items[0];  // Panics on empty vec
```

### Exception Handling

| Situation | Allowed Pattern |
|-----------|-----------------|
| Test code | `unwrap()`, `expect()` allowed |
| Initialization (main start) | `expect()` + clear message |
| Invariant | `debug_assert!()` |
| Example/prototype | `unwrap()` allowed, comment required |

---

## Section 2: Ownership and Borrowing Rules

### Ownership Patterns

| Situation | Pattern | Example |
|-----------|---------|---------|
| Ownership transfer needed | `T` (value) | `fn consume(s: String)` |
| Read only needed | `&T` (immutable ref) | `fn read(s: &str)` |
| Modification needed | `&mut T` (mutable ref) | `fn modify(v: &mut Vec<i32>)` |
| Optional ownership | `Cow<'a, T>` | Minimize copies |

### Ownership Patterns

```rust
// GOOD: Use immutable reference (prevent copy)
fn calculate_length(s: &str) -> usize {
    s.len()
}

// GOOD: Explicit mutable reference
fn push_item(items: &mut Vec<i32>, item: i32) {
    items.push(item);
}

// GOOD: Cow to prevent unnecessary copies
use std::borrow::Cow;

fn process_name(name: &str) -> Cow<'_, str> {
    if name.is_empty() {
        Cow::Borrowed("Unknown")
    } else if name.contains("@") {
        Cow::Owned(name.replace("@", "_"))
    } else {
        Cow::Borrowed(name)
    }
}

// GOOD: Builder pattern for ownership transfer
struct Config {
    name: String,
    value: i32,
}

impl Config {
    fn builder() -> ConfigBuilder {
        ConfigBuilder::default()
    }
}

struct ConfigBuilder {
    name: Option<String>,
    value: Option<i32>,
}

impl ConfigBuilder {
    fn name(mut self, name: impl Into<String>) -> Self {
        self.name = Some(name.into());
        self
    }

    fn build(self) -> Result<Config, &'static str> {
        Ok(Config {
            name: self.name.ok_or("name is required")?,
            value: self.value.unwrap_or(0),
        })
    }
}
```

### Ownership Anti-patterns

```rust
// BAD: Unnecessary clone
fn process(items: Vec<String>) {
    for item in items.clone() {  // clone unnecessary
        println!("{}", item);
    }
}

// BAD: String when &str sufficient
fn greet(name: String) {  // &str sufficient
    println!("Hello, {}", name);
}

// BAD: Excessive Box usage
fn small_value() -> Box<i32> {  // Just return i32
    Box::new(42)
}
```

---

## Section 3: Struct and Trait Rules

### Struct Design Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Newtype** | Strengthen type safety | `struct UserId(u64)` |
| **Builder** | Complex construction | `Config::builder().build()` |
| **TypeState** | State machine | `Connection<Connected>` |
| **Wrapper** | Extend existing type | `struct Wrapper<T>(T)` |

### Struct Patterns

```rust
// GOOD: Newtype pattern
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(u64);

impl UserId {
    pub fn new(id: u64) -> Self {
        Self(id)
    }

    pub fn as_u64(&self) -> u64 {
        self.0
    }
}

// GOOD: TypeState pattern
pub struct Connection<S> {
    addr: String,
    state: std::marker::PhantomData<S>,
}

pub struct Disconnected;
pub struct Connected;

impl Connection<Disconnected> {
    pub fn new(addr: impl Into<String>) -> Self {
        Self {
            addr: addr.into(),
            state: std::marker::PhantomData,
        }
    }

    pub fn connect(self) -> Result<Connection<Connected>, Error> {
        // Connection logic...
        Ok(Connection {
            addr: self.addr,
            state: std::marker::PhantomData,
        })
    }
}

impl Connection<Connected> {
    pub fn send(&self, data: &[u8]) -> Result<(), Error> {
        // Only available in Connected state
        Ok(())
    }
}
```

### Trait Implementation Priority

| Trait | Required | Purpose |
|-------|----------|---------|
| `Debug` | Required | Debug output |
| `Clone` | Recommended | Value copy |
| `PartialEq`, `Eq` | Recommended | Comparison |
| `Hash` | Conditional | When used as HashMap key |
| `Default` | Recommended | Default value creation |
| `Display` | Conditional | User output |
| `Serialize`, `Deserialize` | Conditional | When serialization needed |

### derive Macro Order

```rust
// GOOD: Consistent derive order
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
#[derive(Serialize, Deserialize)]  // serde on separate line
pub struct Point {
    pub x: i32,
    pub y: i32,
}
```

---

## Section 4: Async Programming Rules

### Async Runtime Selection

| Runtime | When to Use | Features |
|---------|-------------|----------|
| **tokio** | Web servers, high performance | Multi-threaded, rich ecosystem |
| **async-std** | Simple async | std-like API |
| **smol** | Embedded, lightweight | Minimal dependencies |

### Async Patterns

```rust
// GOOD: Parallel execution
use tokio::try_join;

async fn fetch_all() -> Result<(User, Posts, Stats), Error> {
    let (user, posts, stats) = try_join!(
        fetch_user(),
        fetch_posts(),
        fetch_stats()
    )?;
    Ok((user, posts, stats))
}

// GOOD: Stream processing
use futures::stream::{self, StreamExt};

async fn process_items(items: Vec<Item>) -> Vec<Result<Processed, Error>> {
    stream::iter(items)
        .map(|item| async move { process(item).await })
        .buffer_unordered(10)  // 10 concurrent
        .collect()
        .await
}

// GOOD: Timeout handling
use tokio::time::{timeout, Duration};

async fn fetch_with_timeout() -> Result<Data, Error> {
    timeout(Duration::from_secs(30), fetch_data())
        .await
        .map_err(|_| Error::Timeout)?
}
```

### Async Anti-patterns

```rust
// BAD: Sequential execution (unnecessary wait)
let user = fetch_user().await?;
let posts = fetch_posts().await?;  // Can parallelize

// BAD: Blocking call in async block
async fn bad_example() {
    std::thread::sleep(Duration::from_secs(1));  // Blocking!
    // Use tokio::time::sleep().await
}

// BAD: Infinite loop without spawn
async fn bad_loop() {
    loop {
        process().await;  // Problem if no yield point
    }
}
```

---

## Section 5: Testing Rules

### Test Strategy

| Test Type | Location | Coverage Target |
|-----------|----------|-----------------|
| Unit test | `mod tests` inside | 80% |
| Integration test | `tests/` directory | 100% critical paths |
| Doc test | `///` comments | 100% public API |
| Property test | `proptest` | Edge cases |

### Test Patterns

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // GOOD: Clear test name
    #[test]
    fn parse_valid_json_returns_config() {
        let json = r#"{"name": "test", "value": 42}"#;
        let result = parse_config(json);
        assert!(result.is_ok());
        assert_eq!(result.unwrap().name, "test");
    }

    // GOOD: Error case test
    #[test]
    fn parse_invalid_json_returns_error() {
        let json = "not valid json";
        let result = parse_config(json);
        assert!(result.is_err());
    }

    // GOOD: Property test with proptest
    use proptest::prelude::*;

    proptest! {
        #[test]
        fn parse_roundtrip(value: i32) {
            let s = value.to_string();
            let parsed: i32 = s.parse().unwrap();
            prop_assert_eq!(parsed, value);
        }
    }
}

// GOOD: Doc test
/// Adds two numbers.
///
/// # Examples
///
/// ```
/// use mylib::add;
/// assert_eq!(add(2, 3), 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

---

## Section 6: Performance Optimization Rules

### Optimization Checklist

| Item | Tool | Target |
|------|------|--------|
| Unnecessary allocations | `cargo clippy` | Zero |
| Minimize clone | Code review | Only when necessary |
| Inline | `#[inline]` | Hot paths only |
| SIMD | `packed_simd` | Performance critical sections |

### Optimization Patterns

```rust
// GOOD: Pre-allocation
let mut items = Vec::with_capacity(1000);

// GOOD: Iterator chaining (lazy evaluation)
let sum: i32 = items
    .iter()
    .filter(|x| **x > 0)
    .map(|x| x * 2)
    .sum();

// GOOD: Conditional copy with Cow
use std::borrow::Cow;

fn normalize(s: &str) -> Cow<'_, str> {
    if s.is_ascii() {
        Cow::Borrowed(s)
    } else {
        Cow::Owned(s.to_lowercase())
    }
}

// GOOD: Fixed size with Box<[T]>
let fixed: Box<[i32]> = vec![1, 2, 3].into_boxed_slice();
```

---

## Section 7: Clippy Rules

### Required Clippy Lints

```toml
# Cargo.toml or clippy.toml
[lints.clippy]
# Required (deny)
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
todo = "deny"
unimplemented = "deny"

# Warning (warn)
clone_on_ref_ptr = "warn"
inefficient_to_string = "warn"
large_types_passed_by_value = "warn"
needless_pass_by_value = "warn"
```

### CI Configuration

```yaml
# .github/workflows/rust.yml
name: Rust CI

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt

      - name: Format check
        run: cargo fmt --check

      - name: Clippy
        run: cargo clippy -- -D warnings

      - name: Test
        run: cargo test

      - name: Miri (optional)
        run: |
          rustup +nightly component add miri
          cargo +nightly miri test
```

---

## Self-Diagnosis Checklist

### Critical (Must Complete)
- [ ] Zero `unwrap()` / `expect()` in production code
- [ ] Zero `panic!()` usage
- [ ] `clippy -- -D warnings` passes
- [ ] All errors return `Result<T, E>`

### Important (80%+)
- [ ] Removed unnecessary `clone()`
- [ ] Appropriate `&str` vs `String` selection
- [ ] Written doc tests
- [ ] Meaningful error messages

### Nice-to-have
- [ ] Property-based tests
- [ ] UB check with Miri
- [ ] Written benchmarks

**Pass Criteria**: Critical 100% + Important 80%+

---

## References

| Document | Link |
|----------|------|
| The Rust Book | https://doc.rust-lang.org/book/ |
| Rust API Guidelines | https://rust-lang.github.io/api-guidelines/ |
| Clippy Lints | https://rust-lang.github.io/rust-clippy/ |
| Rustonomicon | https://doc.rust-lang.org/nomicon/ |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Auto-detect: `Cargo.toml`
