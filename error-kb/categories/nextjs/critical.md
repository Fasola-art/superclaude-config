# 🔴 Next.js Critical Errors

## Module not found: Can't resolve 'X'

**Cause**: Module resolution failed

```typescript
// Cause 1: Path error
import { Button } from '@/components/button';  // Check case sensitivity

// Fix: Exact path
import { Button } from '@/components/Button';

// Cause 2: Server-only module
import fs from 'fs';  // Cannot use in client

// Fix: Dynamic import or use only in server component
```

---

## You're importing a component that needs useState

**Message**: `It only works in a Client Component`

**Cause**: Client features used in Server Component

```typescript
// ❌ Error: Hook in Server Component
import { useState } from 'react';

export default function Page() {
  const [count, setCount] = useState(0);  // Error
}

// ✅ Fix 1: Add 'use client'
'use client';
import { useState } from 'react';

export default function Page() {
  const [count, setCount] = useState(0);
}

// ✅ Fix 2: Separate Client Component
// components/Counter.tsx
'use client';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// app/page.tsx (keep as Server Component)
import { Counter } from '@/components/Counter';
export default function Page() {
  return <Counter />;
}
```

---

## Error: Unsupported Server Component type

**Cause**: Non-serializable value passed from Server to Client

```typescript
// ❌ Error: Passing function from Server → Client
<ClientComponent onClick={() => console.log('click')} />

// ✅ Fix 1: Use Server Action
'use server';
async function handleClick() {
  console.log('click');
}
<ClientComponent onClick={handleClick} />

// ✅ Fix 2: Define in Client Component
'use client';
export function ClientComponent() {
  const handleClick = () => console.log('click');
  return <button onClick={handleClick}>Click</button>;
}
```
