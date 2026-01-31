# Next.js 에러 패턴

> **카테고리**: nextjs
> **갱신일**: 2026-01-30

---

## 🔴 Critical 에러

### Module not found: Can't resolve 'X'

**원인**: 모듈 해석 실패

**해결책**:
```typescript
// 원인 1: 경로 오류
import { Button } from '@/components/button';  // 대소문자 확인

// 해결: 정확한 경로
import { Button } from '@/components/Button';

// 원인 2: 서버 전용 모듈
import fs from 'fs';  // 클라이언트에서 사용 불가

// 해결: 동적 import 또는 서버 컴포넌트에서만 사용
```

---

### You're importing a component that needs useState (Client Component)

**메시지**: `You're importing a component that needs useState. It only works in a Client Component`

**원인**: Server Component에서 Client 기능 사용

**해결책**:
```typescript
// ❌ 에러: Server Component에서 Hook 사용
// app/page.tsx (기본 Server Component)
import { useState } from 'react';  // 에러

export default function Page() {
  const [count, setCount] = useState(0);  // 에러
  return <div>{count}</div>;
}

// ✅ 해결 1: 'use client' 추가
'use client';

import { useState } from 'react';

export default function Page() {
  const [count, setCount] = useState(0);
  return <div>{count}</div>;
}

// ✅ 해결 2: Client Component 분리
// components/Counter.tsx
'use client';
export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// app/page.tsx (Server Component 유지)
import { Counter } from '@/components/Counter';
export default function Page() {
  return <Counter />;
}
```

---

### Error: Unsupported Server Component type

**원인**: Server Component에서 직렬화 불가능한 값 전달

**해결책**:
```typescript
// ❌ 에러: 함수를 Server → Client로 전달
<ClientComponent onClick={() => console.log('click')} />

// ✅ 해결 1: Server Action 사용
'use server';
async function handleClick() {
  console.log('click');
}

<ClientComponent onClick={handleClick} />

// ✅ 해결 2: Client Component에서 정의
// ClientComponent.tsx
'use client';
export function ClientComponent() {
  const handleClick = () => console.log('click');
  return <button onClick={handleClick}>Click</button>;
}
```

---

## 🟠 Build 에러

### Dynamic server usage

**메시지**: `Dynamic server usage: Page couldn't be rendered statically`

**원인**: 정적 페이지에서 동적 API 사용

**해결책**:
```typescript
// 원인: cookies(), headers() 등 사용
import { cookies } from 'next/headers';

export default function Page() {
  const cookieStore = cookies();  // 동적 렌더링 필요
  return <div>...</div>;
}

// 해결 1: dynamic 설정
export const dynamic = 'force-dynamic';

// 해결 2: 동적 라우트로 변경
// app/[slug]/page.tsx

// 해결 3: generateStaticParams 제공
export async function generateStaticParams() {
  return [{ slug: 'a' }, { slug: 'b' }];
}
```

---

### Error during SSG

**원인**: 정적 생성 중 에러

**해결책**:
```typescript
// 원인: 외부 API 실패
export async function generateStaticParams() {
  const posts = await fetchPosts();  // API 실패 시 빌드 실패
  return posts.map(p => ({ id: p.id }));
}

// 해결: 에러 핸들링
export async function generateStaticParams() {
  try {
    const posts = await fetchPosts();
    return posts.map(p => ({ id: p.id }));
  } catch {
    return [];  // 빈 배열 반환
  }
}
```

---

## 🟡 Runtime 에러

### NEXT_REDIRECT

**메시지**: `NEXT_REDIRECT` 에러 (정상 동작)

**설명**: `redirect()` 함수의 정상 동작

**해결책**:
```typescript
// redirect()는 내부적으로 에러를 throw
// try-catch에서 잡히지 않도록 주의

// ❌ 문제
try {
  redirect('/login');
} catch (e) {
  console.log(e);  // NEXT_REDIRECT 잡힘
}

// ✅ 해결: redirect 타입 체크
import { isRedirectError } from 'next/dist/client/components/redirect';

try {
  redirect('/login');
} catch (e) {
  if (isRedirectError(e)) throw e;  // 다시 throw
  console.log(e);
}
```

---

### fetch failed

**원인**: 서버 컴포넌트에서 fetch 실패

**해결책**:
```typescript
// 에러 핸들링 추가
async function getData() {
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 }
  });

  if (!res.ok) {
    // 에러 페이지로 라우팅
    throw new Error('Failed to fetch data');
  }

  return res.json();
}

// 또는 notFound() 사용
import { notFound } from 'next/navigation';

async function getData(id: string) {
  const res = await fetch(`/api/items/${id}`);
  if (!res.ok) notFound();
  return res.json();
}
```

---

## 🔧 Config 에러

### Invalid next.config.js options

**해결책**:
```javascript
// next.config.js 타입 체크
/** @type {import('next').NextConfig} */
const nextConfig = {
  // 올바른 옵션만 사용
};

module.exports = nextConfig;
```

---

### Conflicting paths

**원인**: 라우트 충돌

**해결책**:
```
// 충돌 예시
app/blog/[slug]/page.tsx
app/blog/new/page.tsx      // [slug]와 충돌

// 해결: 순서 재배치 또는 라우트 그룹
app/blog/(list)/page.tsx
app/blog/(detail)/[slug]/page.tsx
```

---

## 📊 에러 빈도

| 에러 | 빈도 | 심각도 |
|------|------|--------|
| Server/Client 혼동 | 높음 | 높음 |
| Hydration Mismatch | 높음 | 중간 |
| Dynamic server usage | 중간 | 중간 |
| Module not found | 중간 | 낮음 |

---

## 🔧 디버깅

```bash
# 빌드 로그 상세
next build --debug

# 번들 분석
ANALYZE=true next build

# 프로덕션 모드 로컬 실행
next build && next start
```

---

**META**
- Category: nextjs
- Last Updated: 2026-01-30
