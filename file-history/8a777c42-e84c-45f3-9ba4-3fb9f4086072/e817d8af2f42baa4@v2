# Rust 언어 프로필

> **버전**: 1.0.0
> **적용 대상**: Rust 2021 Edition+
> **자동 감지**: `Cargo.toml` 존재 시

---

## 🎯 목표

**Primary Outcome**: 메모리 안전하고 성능 최적화된 Rust 코드 생성

**Success Criteria**:
- [ ] `panic!` 발생 가능 코드 0개 (Never Panics)
- [ ] 모든 에러는 `Result<T, E>`로 처리
- [ ] `clippy` 경고 0개
- [ ] 불필요한 `clone()` 0개

**Failure Cases**:
- 🔴 `unwrap()` 프로덕션 코드에 사용 → `?` 연산자로 교체
- 🔴 `unsafe` 블록 → 안전한 대안 검토 필수

---

## 🚀 빠른 참조

### Never Panics 원칙

| 금지 패턴 | 대안 | 이유 |
|----------|------|------|
| `.unwrap()` | `.ok()`, `?`, `unwrap_or()` | 런타임 panic |
| `.expect()` | `?` + context | 런타임 panic |
| `panic!()` | `Result::Err()` | 복구 불가 |
| `array[index]` | `.get(index)` | 범위 초과 panic |
| `slice[..]` | `.get(..)` | 범위 초과 panic |

### 필수 명령어

```bash
# 빌드 전 필수 검사
cargo clippy -- -D warnings     # 경고 = 에러 처리
cargo fmt --check               # 포맷팅 검사
cargo test                      # 테스트 실행
cargo miri test                 # UB 검사 (nightly)
```

---

## 📋 섹션 1: 에러 처리 규칙

### 📊 에러 처리 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| `Result<T, E>` | 모든 실패 가능 연산 | 파일 I/O, 파싱, API |
| `Option<T>` | 값이 없을 수 있음 | 검색 결과, 설정값 |
| `?` 연산자 | 에러 전파 | `file.read()?` |
| `anyhow` | 애플리케이션 에러 | CLI, 웹 서버 |
| `thiserror` | 라이브러리 에러 | 커스텀 에러 타입 |

### ✅ 에러 처리 패턴

```rust
// ✅ GOOD: thiserror로 커스텀 에러
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("파일을 찾을 수 없습니다: {0}")]
    FileNotFound(String),

    #[error("파싱 실패: {0}")]
    ParseError(#[from] serde_json::Error),

    #[error("네트워크 에러: {0}")]
    NetworkError(#[from] reqwest::Error),
}

// ✅ GOOD: Result 반환
pub fn load_config(path: &str) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)
        .map_err(|_| AppError::FileNotFound(path.to_string()))?;

    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}

// ✅ GOOD: Option 처리
fn find_user(id: u64) -> Option<User> {
    users.iter().find(|u| u.id == id).cloned()
}

// 사용부
let user = find_user(42).ok_or(AppError::UserNotFound)?;
```

### ❌ 에러 처리 안티패턴

```rust
// ❌ BAD: unwrap() 사용
let config = load_config("config.json").unwrap();

// ❌ BAD: expect() 프로덕션 사용
let file = File::open("data.txt").expect("파일 열기 실패");

// ❌ BAD: panic! 사용
if value < 0 {
    panic!("음수는 허용되지 않습니다");
}

// ❌ BAD: 인덱스 직접 접근
let first = items[0];  // 빈 벡터면 panic
```

### ⚠️ 예외 처리

| 상황 | 허용되는 패턴 |
|------|--------------|
| 테스트 코드 | `unwrap()`, `expect()` 허용 |
| 초기화 (main 시작) | `expect()` + 명확한 메시지 |
| 불변 조건 (invariant) | `debug_assert!()` |
| 예제/프로토타입 | `unwrap()` 허용, 주석 필수 |

---

## 📋 섹션 2: 소유권과 빌림 규칙

### 📊 소유권 패턴

| 상황 | 사용 패턴 | 예시 |
|------|----------|------|
| 소유권 이전 필요 | `T` (값) | `fn consume(s: String)` |
| 읽기만 필요 | `&T` (불변 참조) | `fn read(s: &str)` |
| 수정 필요 | `&mut T` (가변 참조) | `fn modify(v: &mut Vec<i32>)` |
| 선택적 소유권 | `Cow<'a, T>` | 복사 최소화 |

### ✅ 소유권 패턴

```rust
// ✅ GOOD: 불변 참조 사용 (복사 방지)
fn calculate_length(s: &str) -> usize {
    s.len()
}

// ✅ GOOD: 가변 참조 명시
fn push_item(items: &mut Vec<i32>, item: i32) {
    items.push(item);
}

// ✅ GOOD: Cow로 불필요한 복사 방지
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

// ✅ GOOD: 빌더 패턴으로 소유권 이전
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

### ❌ 소유권 안티패턴

```rust
// ❌ BAD: 불필요한 clone
fn process(items: Vec<String>) {
    for item in items.clone() {  // clone 불필요
        println!("{}", item);
    }
}

// ❌ BAD: String 대신 &str 사용 가능
fn greet(name: String) {  // &str로 충분
    println!("Hello, {}", name);
}

// ❌ BAD: 과도한 Box 사용
fn small_value() -> Box<i32> {  // 그냥 i32 반환
    Box::new(42)
}
```

---

## 📋 섹션 3: 구조체와 트레잇 규칙

### 📊 구조체 설계 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| **Newtype** | 타입 안전성 강화 | `struct UserId(u64)` |
| **Builder** | 복잡한 생성 | `Config::builder().build()` |
| **TypeState** | 상태 기계 | `Connection<Connected>` |
| **Wrapper** | 기존 타입 확장 | `struct Wrapper<T>(T)` |

### ✅ 구조체 패턴

```rust
// ✅ GOOD: Newtype 패턴
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

// ✅ GOOD: TypeState 패턴
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
        // 연결 로직...
        Ok(Connection {
            addr: self.addr,
            state: std::marker::PhantomData,
        })
    }
}

impl Connection<Connected> {
    pub fn send(&self, data: &[u8]) -> Result<(), Error> {
        // Connected 상태에서만 send 가능
        Ok(())
    }
}
```

### 📊 트레잇 구현 우선순위

| 트레잇 | 필수 여부 | 용도 |
|--------|----------|------|
| `Debug` | 필수 | 디버깅 출력 |
| `Clone` | 권장 | 값 복사 |
| `PartialEq`, `Eq` | 권장 | 비교 연산 |
| `Hash` | 조건부 | HashMap 키 사용 시 |
| `Default` | 권장 | 기본값 생성 |
| `Display` | 조건부 | 사용자 출력 |
| `Serialize`, `Deserialize` | 조건부 | 직렬화 필요 시 |

### ✅ derive 매크로 순서

```rust
// ✅ GOOD: 일관된 derive 순서
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Default)]
#[derive(Serialize, Deserialize)]  // serde는 별도 줄
pub struct Point {
    pub x: i32,
    pub y: i32,
}
```

---

## 📋 섹션 4: 비동기 프로그래밍 규칙

### 📊 비동기 런타임 선택

| 런타임 | 사용 시점 | 특징 |
|--------|----------|------|
| **tokio** | 웹 서버, 고성능 | 멀티스레드, 풍부한 생태계 |
| **async-std** | 간단한 비동기 | std 유사 API |
| **smol** | 임베디드, 경량 | 최소 의존성 |

### ✅ 비동기 패턴

```rust
// ✅ GOOD: 병렬 실행
use tokio::try_join;

async fn fetch_all() -> Result<(User, Posts, Stats), Error> {
    let (user, posts, stats) = try_join!(
        fetch_user(),
        fetch_posts(),
        fetch_stats()
    )?;
    Ok((user, posts, stats))
}

// ✅ GOOD: 스트림 처리
use futures::stream::{self, StreamExt};

async fn process_items(items: Vec<Item>) -> Vec<Result<Processed, Error>> {
    stream::iter(items)
        .map(|item| async move { process(item).await })
        .buffer_unordered(10)  // 동시 실행 10개
        .collect()
        .await
}

// ✅ GOOD: 타임아웃 처리
use tokio::time::{timeout, Duration};

async fn fetch_with_timeout() -> Result<Data, Error> {
    timeout(Duration::from_secs(30), fetch_data())
        .await
        .map_err(|_| Error::Timeout)?
}
```

### ❌ 비동기 안티패턴

```rust
// ❌ BAD: 순차 실행 (불필요한 대기)
let user = fetch_user().await?;
let posts = fetch_posts().await?;  // 병렬 가능

// ❌ BAD: async 블록 내 블로킹 호출
async fn bad_example() {
    std::thread::sleep(Duration::from_secs(1));  // 블로킹!
    // tokio::time::sleep().await 사용
}

// ❌ BAD: spawn 없이 무한 루프
async fn bad_loop() {
    loop {
        process().await;  // yield point 없으면 문제
    }
}
```

---

## 📋 섹션 5: 테스트 규칙

### 📊 테스트 전략

| 테스트 유형 | 위치 | 커버리지 목표 |
|------------|------|--------------|
| 단위 테스트 | `mod tests` 내부 | 80% |
| 통합 테스트 | `tests/` 디렉토리 | 핵심 경로 100% |
| 문서 테스트 | `///` 주석 | 공개 API 100% |
| Property 테스트 | `proptest` | 엣지 케이스 |

### ✅ 테스트 패턴

```rust
#[cfg(test)]
mod tests {
    use super::*;

    // ✅ GOOD: 명확한 테스트명
    #[test]
    fn parse_valid_json_returns_config() {
        let json = r#"{"name": "test", "value": 42}"#;
        let result = parse_config(json);
        assert!(result.is_ok());
        assert_eq!(result.unwrap().name, "test");
    }

    // ✅ GOOD: 에러 케이스 테스트
    #[test]
    fn parse_invalid_json_returns_error() {
        let json = "not valid json";
        let result = parse_config(json);
        assert!(result.is_err());
    }

    // ✅ GOOD: proptest로 속성 테스트
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

// ✅ GOOD: 문서 테스트
/// 두 숫자를 더합니다.
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

## 📋 섹션 6: 성능 최적화 규칙

### 📊 최적화 체크리스트

| 항목 | 도구 | 목표 |
|------|------|------|
| 불필요한 할당 | `cargo clippy` | 0개 |
| clone 최소화 | 코드 리뷰 | 필수만 |
| 인라인 | `#[inline]` | 핫 경로만 |
| SIMD | `packed_simd` | 성능 핵심부 |

### ✅ 최적화 패턴

```rust
// ✅ GOOD: 사전 할당
let mut items = Vec::with_capacity(1000);

// ✅ GOOD: 반복자 체이닝 (lazy evaluation)
let sum: i32 = items
    .iter()
    .filter(|x| **x > 0)
    .map(|x| x * 2)
    .sum();

// ✅ GOOD: Cow로 조건부 복사
use std::borrow::Cow;

fn normalize(s: &str) -> Cow<'_, str> {
    if s.is_ascii() {
        Cow::Borrowed(s)
    } else {
        Cow::Owned(s.to_lowercase())
    }
}

// ✅ GOOD: Box<[T]>로 크기 고정
let fixed: Box<[i32]> = vec![1, 2, 3].into_boxed_slice();
```

---

## 📋 섹션 7: Clippy 규칙

### 📊 필수 Clippy lint

```toml
# Cargo.toml 또는 clippy.toml
[lints.clippy]
# 필수 (deny)
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
todo = "deny"
unimplemented = "deny"

# 경고 (warn)
clone_on_ref_ptr = "warn"
inefficient_to_string = "warn"
large_types_passed_by_value = "warn"
needless_pass_by_value = "warn"
```

### ✅ CI 설정

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

## ✅ 자가 진단 체크리스트

### 🔴 Critical (반드시 완료)
- [ ] `unwrap()` / `expect()` 프로덕션 코드에 0개
- [ ] `panic!()` 사용 0개
- [ ] `clippy -- -D warnings` 통과
- [ ] 모든 에러는 `Result<T, E>` 반환

### 🟡 Important (80% 이상)
- [ ] 불필요한 `clone()` 제거
- [ ] `&str` vs `String` 적절히 선택
- [ ] 문서 테스트 작성
- [ ] 의미 있는 에러 메시지

### 🟢 Nice-to-have
- [ ] Property-based 테스트
- [ ] Miri로 UB 검사
- [ ] 벤치마크 작성

**합격 기준**: Critical 100% + Important 80% 이상

---

## 📚 참조

| 문서 | 링크 |
|------|------|
| The Rust Book | https://doc.rust-lang.org/book/ |
| Rust API Guidelines | https://rust-lang.github.io/api-guidelines/ |
| Clippy Lints | https://rust-lang.github.io/rust-clippy/ |
| Rustonomicon | https://doc.rust-lang.org/nomicon/ |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Auto-detect: `Cargo.toml`
