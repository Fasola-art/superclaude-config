# Structs & Traits Rules

## Struct Patterns

### Basic Struct

```rust
#[derive(Debug, Clone)]
pub struct User {
    pub id: String,
    pub name: String,
    pub email: Option<String>,
}

impl User {
    pub fn new(id: impl Into<String>, name: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            name: name.into(),
            email: None,
        }
    }

    pub fn with_email(mut self, email: impl Into<String>) -> Self {
        self.email = Some(email.into());
        self
    }
}

// Usage
let user = User::new("1", "Alice").with_email("alice@example.com");
```

### Newtype Pattern

```rust
#[derive(Debug, Clone, PartialEq)]
pub struct UserId(String);

impl UserId {
    pub fn new(id: impl Into<String>) -> Self {
        Self(id.into())
    }
}
```

---

## Trait Patterns

### Define Traits

```rust
pub trait Repository {
    type Error;

    fn find(&self, id: &str) -> Result<Option<User>, Self::Error>;
    fn save(&self, user: &User) -> Result<(), Self::Error>;
}
```

### Implement Traits

```rust
impl Repository for PostgresRepo {
    type Error = sqlx::Error;

    fn find(&self, id: &str) -> Result<Option<User>, Self::Error> {
        // Implementation
    }

    fn save(&self, user: &User) -> Result<(), Self::Error> {
        // Implementation
    }
}
```

### Common Derives

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash, Default)]
pub struct Config {
    pub name: String,
    pub value: i32,
}
```
