# Ownership & Borrowing Rules

## Core Principles

| Concept | Rule |
|---------|------|
| Ownership | Each value has one owner |
| Borrowing | References don't take ownership |
| Lifetimes | References must be valid |

## Borrowing Patterns

```rust
// GOOD: Borrow instead of move
fn process(data: &str) -> usize {
    data.len()
}

// GOOD: Mutable borrow
fn append(data: &mut Vec<i32>, value: i32) {
    data.push(value);
}

// GOOD: Return owned value
fn create() -> String {
    String::from("hello")
}
```

## Lifetimes

```rust
// Explicit lifetime
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with lifetime
struct Parser<'a> {
    input: &'a str,
}
```

## Anti-patterns

```rust
// BAD: Unnecessary clone
let data = input.clone();
process(&data);

// GOOD: Just borrow
process(&input);

// BAD: Moving when borrowing works
fn process(data: String) { ... }

// GOOD: Borrow when you don't need ownership
fn process(data: &str) { ... }
```

## Clone vs Copy

```rust
// Copy: Simple types (i32, f64, bool)
let x = 5;
let y = x;  // Copy, both valid

// Clone: Explicit deep copy
let s1 = String::from("hello");
let s2 = s1.clone();  // Explicit clone
```
