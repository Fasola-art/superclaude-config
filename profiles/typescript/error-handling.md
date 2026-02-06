# Error Handling Rules

## Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| `Result<T, E>` | Expected failures | API calls, parsing |
| `try/catch` | Exceptional situations | External library |
| `Error Boundary` | React render errors | Prevent crash |

## Result Type Pattern

```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) {
      return { ok: false, error: new Error(`HTTP ${res.status}`) };
    }
    const user = await res.json();
    return { ok: true, value: user };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e : new Error(String(e)) };
  }
}

// Usage
const result = await fetchUser('123');
if (!result.ok) {
  console.error(result.error);
  return;
}
console.log(result.value.name);  // type safe
```

## Anti-patterns

```typescript
// BAD: Ignore error
try {
  await riskyOperation();
} catch (e) {
  // do nothing
}

// BAD: any catch
catch (e: any) {
  console.log(e.message);
}

// BAD: throw string
throw 'Something went wrong';
```
