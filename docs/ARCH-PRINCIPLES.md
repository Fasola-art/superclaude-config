# System Architecture Design Principles

> SuperClaude v2.0.9 Architecture Guidelines

---

## Core Principles

### 1. Single Source of Truth (SSOT)
```yaml
principle: "All data has exactly one authoritative source"
application:
  - State management: Use centralized store
  - Configuration: Single settings.json file
  - Types: Shared type definitions
```

### 2. Separation of Concerns (SoC)
```yaml
principle: "Each module has only one responsibility"
application:
  - UI: Presentation logic only
  - Business: Domain logic only
  - Data: Storage/retrieval logic only
```

### 3. Loose Coupling
```yaml
principle: "Minimize dependencies between modules"
application:
  - Interface-based design
  - Event-driven communication
  - Dependency injection
```

### 4. High Cohesion
```yaml
principle: "Keep related functionality together"
application:
  - Feature-based folder structure
  - Component-level modularization
  - Related logic in same file
```

---

## Layer Architecture

```
┌─────────────────────────────────────┐
│           Presentation              │  UI Components
├─────────────────────────────────────┤
│           Application               │  Use Cases, Services
├─────────────────────────────────────┤
│             Domain                  │  Business Logic, Entities
├─────────────────────────────────────┤
│          Infrastructure             │  DB, API, External Services
└─────────────────────────────────────┘
```

---

## File Structure Patterns

### Feature-First (Recommended)
```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   ├── types.ts
│   │   └── index.ts
│   └── dashboard/
│       ├── components/
│       ├── hooks/
│       └── ...
├── shared/
│   ├── components/
│   ├── hooks/
│   └── utils/
└── app/
    └── routes/
```

---

## Code Quality Standards

### Complexity Limits
| Metric                | Max Value |
|-----------------------|-----------|
| Function lines        | 50        |
| File lines            | 300       |
| Cyclomatic complexity | 10        |
| Parameter count       | 5         |

### Naming Conventions
| Type      | Convention  | Example      |
|-----------|-------------|--------------|
| Component | PascalCase  | UserProfile  |
| Function  | camelCase   | getUserById  |
| Constant  | UPPER_SNAKE | MAX_RETRIES  |
| Type      | PascalCase  | UserResponse |

---

## Error Handling Principles

### Never Throws Pattern
```typescript
// BAD
function getUser(id: string): User {
  if (!id) throw new Error('ID required')
  return fetch(...)
}

// GOOD
function getUser(id: string): Result<User, UserError> {
  if (!id) return err(UserError.InvalidId)
  return ok(await fetch(...))
}
```

### Error Type Definition
```typescript
type Result<T, E> = Ok<T> | Err<E>
type Ok<T> = { ok: true; value: T }
type Err<E> = { ok: false; error: E }
```

---

## Performance Principles

### Lazy Loading
- Route-level code splitting
- Image lazy loading
- Dynamic component imports

### Caching Strategy
- API response caching
- Computed result memoization
- Static asset browser caching

### Optimization Priority
1. Measure (identify performance bottlenecks)
2. Optimize (start with highest impact)
3. Verify (confirm improvements)
