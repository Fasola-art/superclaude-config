# Type System Rules

## Type Definition Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `interface` | Object structure, extension | `interface User { name: string }` |
| `type` | Union, utility, complex | `type Status = 'ok' \| 'error'` |
| `enum` | Avoid (tree-shaking) | `const STATUS = { ... } as const` |
| `const assertion` | Preserve literals | `['a', 'b'] as const` |

## Type Writing Rules

```typescript
// GOOD: Explicit types
interface User {
  id: string;
  name: string;
  email: string | null;
  createdAt: Date;
}

// GOOD: Union types
type APIResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

// GOOD: Generic constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

## Anti-patterns

```typescript
// BAD: any usage
function process(data: any) { ... }

// BAD: Type assertion abuse
const user = response as User;  // without validation

// BAD: enum usage
enum Status { Active, Inactive }  // increases bundle
```

## Exception Handling

| Situation | Solution |
|-----------|----------|
| No types for library | `declare module 'lib'` or `@types` |
| Complex inference | Add explicit annotation |
| Legacy JS integration | `// @ts-check` + JSDoc |
