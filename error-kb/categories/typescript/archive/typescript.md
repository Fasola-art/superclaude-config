# TypeScript Error Patterns

> **Category**: typescript
> **Updated**: 2026-01-30

---

## 🔴 Critical Errors

### TS2304: Cannot find name 'X'

**Cause**: Type/variable not defined

**Solutions**:
1. Check import statement
2. Install `@types/` package
3. Verify `tsconfig.json` settings

```typescript
// ❌ Error
const user: User = { ... };  // Cannot find name 'User'

// ✅ Fix
import type { User } from '@/types';
const user: User = { ... };
```

**Prevention**: `strict: true` + ESLint import rules

---

### TS2345: Argument type mismatch

**Cause**: Function argument type mismatch

**Solutions**:
1. Verify and fix type
2. Add type guard
3. Use generics

```typescript
// ❌ Error
function process(id: number) { ... }
process("123");  // string to number

// ✅ Fix 1: Type conversion
process(parseInt("123", 10));

// ✅ Fix 2: Modify function signature
function process(id: number | string) { ... }
```

---

### TS2322: Type 'X' is not assignable to type 'Y'

**Cause**: Type assignment mismatch

**Solutions**:
1. Check type definition
2. Type narrowing
3. Type assertion (last resort)

```typescript
// ❌ Error
const status: 'active' | 'inactive' = getStatus();
// Type 'string' is not assignable to type...

// ✅ Fix: Type narrowing
const status = getStatus();
if (status === 'active' || status === 'inactive') {
  // status: 'active' | 'inactive'
}

// ✅ Or: as const
function getStatus() {
  return 'active' as const;
}
```

---

## 🟠 Common Errors

### TS2339: Property does not exist

**Cause**: Property not on object

**Solutions**:
```typescript
// ❌ Error
const user = { name: 'test' };
console.log(user.email);  // Property 'email' does not exist

// ✅ Fix 1: Type definition
interface User {
  name: string;
  email?: string;
}

// ✅ Fix 2: Optional chaining
console.log(user.email ?? 'N/A');
```

---

### TS7006: Parameter implicitly has 'any' type

**Cause**: Parameter type not specified (strict mode)

**Solutions**:
```typescript
// ❌ Error
const double = (n) => n * 2;  // Parameter 'n' implicitly has 'any'

// ✅ Fix
const double = (n: number): number => n * 2;
```

**Prevention**: Keep `noImplicitAny: true`

---

### TS2531: Object is possibly 'null'

**Cause**: Missing null check (strict null checks)

**Solutions**:
```typescript
// ❌ Error
const name = user.name;  // 'user' is possibly 'null'

// ✅ Fix 1: Optional chaining
const name = user?.name;

// ✅ Fix 2: Null check
if (user) {
  const name = user.name;
}

// ✅ Fix 3: Assertion (use only when certain)
const name = user!.name;  // Not recommended
```

---

## 🟡 Config Errors

### Cannot find module 'X' or its type declarations

**Cause**: Module resolution failed

**Solutions**:
1. Check package installation
2. Install `@types/`
3. Configure `tsconfig.json` paths

```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

---

### Duplicate identifier

**Cause**: Same name defined multiple times

**Solutions**:
1. `skipLibCheck: true` (temporary)
2. Remove duplicate `@types`
3. Namespace separation

---

## 📊 Error Code Reference

| Code | Category | Frequency |
|------|----------|-----------|
| TS2304 | Undefined name | High |
| TS2345 | Argument type | High |
| TS2322 | Assignment type | High |
| TS2339 | Property missing | Medium |
| TS7006 | Implicit any | Medium |
| TS2531 | Possibly null | Medium |

---

## 🔧 Debugging Commands

```bash
# Type check only
npx tsc --noEmit

# Detailed errors
npx tsc --noEmit --pretty

# Specific file only
npx tsc --noEmit src/file.ts
```

---

**META**
- Category: typescript
- Last Updated: 2026-01-30
