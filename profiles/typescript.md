# TypeScript/React/Next.js 언어 프로필

> **버전**: 1.0.0
> **적용 대상**: TypeScript 5.x, React 18+, Next.js 14+
> **자동 감지**: `package.json` 또는 `tsconfig.json` 존재 시

---

## 🎯 목표

**Primary Outcome**: TypeScript 생태계에서 타입 안전하고 성능 최적화된 코드 생성

**Success Criteria**:
- [ ] `strict: true` 모드 준수
- [ ] any 타입 0개
- [ ] 번들 크기 최적화 (barrel import 없음)
- [ ] Server/Client 컴포넌트 올바른 분리

**Failure Cases**:
- 🔴 `@ts-ignore` 사용 → 타입 수정 필요
- 🔴 런타임 타입 에러 → 타입 가드 추가

---

## 🚀 빠른 참조

### 필수 규칙 (위반 시 빌드 실패)

| 규칙 | 설명 | 예시 |
|------|------|------|
| **strict mode** | tsconfig.json strict: true | 암묵적 any 금지 |
| **명시적 반환 타입** | 함수 반환 타입 명시 | `function fn(): string` |
| **null 체크** | optional chaining 사용 | `user?.name` |
| **barrel 금지** | 직접 import | `from '@/Button'` ✗ |

### 권장 규칙

| 규칙 | 이유 | 대안 |
|------|------|------|
| `unknown` > `any` | 타입 안전성 | 타입 가드로 좁히기 |
| `const assertion` | 리터럴 타입 보존 | `as const` |
| `satisfies` | 타입 검증 + 추론 | TS 4.9+ |

---

## 📋 섹션 1: 타입 시스템 규칙

### 📊 타입 정의 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| `interface` | 객체 구조, 확장 필요 | `interface User { name: string }` |
| `type` | 유니온, 유틸리티, 복잡한 타입 | `type Status = 'ok' \| 'error'` |
| `enum` | 사용 자제 (tree-shaking 문제) | `const STATUS = { ... } as const` |
| `const assertion` | 리터럴 값 보존 | `['a', 'b'] as const` |

### ✅ 타입 작성 규칙

```typescript
// ✅ GOOD: 명시적 타입
interface User {
  id: string;
  name: string;
  email: string | null;  // null 명시
  createdAt: Date;
}

// ✅ GOOD: 유니온 타입
type APIResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

// ✅ GOOD: 제네릭 제약
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### ❌ 안티패턴

```typescript
// ❌ BAD: any 사용
function process(data: any) { ... }

// ❌ BAD: 타입 단언 남용
const user = response as User;  // 검증 없이

// ❌ BAD: enum 사용
enum Status { Active, Inactive }  // bundle 크기 증가
```

### ⚠️ 예외 처리

| 상황 | 대응 방법 |
|------|----------|
| 외부 라이브러리 타입 없음 | `declare module 'lib'` 또는 `@types` 설치 |
| 복잡한 타입 추론 불가 | 명시적 타입 주석 추가 |
| 레거시 JS 코드 통합 | `// @ts-check` + JSDoc 또는 점진적 마이그레이션 |

---

## 📋 섹션 2: React 컴포넌트 규칙

### 📊 컴포넌트 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| **Server Component** | 데이터 페칭, 정적 UI | 기본값 (use client 없음) |
| **Client Component** | 인터랙션, 훅 사용 | `'use client'` 선언 |
| **Suspense 경계** | 비동기 로딩 | `<Suspense fallback={...}>` |

### ✅ 컴포넌트 타입 패턴

```typescript
// ✅ GOOD: Props 인터페이스
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';  // optional
  children: React.ReactNode;
  onClick?: () => void;
}

// ✅ GOOD: 함수 컴포넌트
function Button({ variant, size = 'md', children, onClick }: ButtonProps) {
  return (
    <button
      className={cn(styles[variant], styles[size])}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

// ✅ GOOD: forwardRef 패턴
const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, ...props }, ref) {
    return <input ref={ref} {...props} />;
  }
);
```

### ❌ React 안티패턴

```typescript
// ❌ BAD: React.FC 사용 (children 암묵적 포함 문제)
const Button: React.FC<Props> = ({ ... }) => { ... };

// ❌ BAD: 인라인 객체/함수 (불필요한 리렌더)
<Child style={{ color: 'red' }} onClick={() => handle()} />

// ❌ BAD: barrel import
import { Button, Input, Card } from '@/components';
```

### ⚠️ 예외 처리

| 상황 | 대응 방법 |
|------|----------|
| children 타입 복잡 | `React.ReactNode` 사용 |
| 이벤트 타입 | `React.MouseEvent<HTMLButtonElement>` |
| ref 전달 필요 | `forwardRef` 패턴 |

---

## 📋 섹션 3: Next.js App Router 규칙

### 📊 라우팅 패턴

| 파일 | 용도 | 주의사항 |
|------|------|----------|
| `page.tsx` | 라우트 페이지 | Server Component 기본 |
| `layout.tsx` | 레이아웃 | 중첩 가능, 상태 유지 |
| `loading.tsx` | 로딩 UI | Suspense 자동 적용 |
| `error.tsx` | 에러 UI | `'use client'` 필수 |
| `route.ts` | API Route | GET, POST 등 export |

### ✅ 데이터 페칭 패턴

```typescript
// ✅ GOOD: Server Component에서 직접 fetch
async function ProductList() {
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 }  // ISR
  });
  return <div>{/* ... */}</div>;
}

// ✅ GOOD: 병렬 데이터 페칭
async function Dashboard() {
  const [user, posts, stats] = await Promise.all([
    getUser(),
    getPosts(),
    getStats()
  ]);
  return <div>{/* ... */}</div>;
}

// ✅ GOOD: Server Action
'use server';
export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  await db.post.create({ data: { title } });
  revalidatePath('/posts');
}
```

### ❌ Next.js 안티패턴

```typescript
// ❌ BAD: Client Component에서 불필요한 데이터 페칭
'use client';
function Page() {
  const [data, setData] = useState(null);
  useEffect(() => { fetch(...) }, []);  // 서버에서 해야 함
}

// ❌ BAD: 순차 데이터 페칭 (waterfall)
const user = await getUser();
const posts = await getPosts(user.id);  // 의존성 없으면 병렬로

// ❌ BAD: 과도한 'use client'
'use client';  // 정적 UI인데 불필요하게 선언
function StaticCard() { return <div>...</div>; }
```

---

## 📋 섹션 4: Import/Export 규칙

### 📊 Import 순서

```typescript
// 1. React/Next.js
import { useState } from 'react';
import Link from 'next/link';

// 2. 외부 라이브러리
import { clsx } from 'clsx';
import { format } from 'date-fns';

// 3. 내부 모듈 (절대 경로)
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/lib/utils';

// 4. 상대 경로 (같은 폴더)
import { helpers } from './helpers';

// 5. 타입 (type-only import)
import type { User } from '@/types';

// 6. 스타일
import styles from './styles.module.css';
```

### ✅ Export 패턴

```typescript
// ✅ GOOD: Named export (tree-shaking 가능)
export function Button() { ... }
export function Input() { ... }

// ✅ GOOD: 타입 분리 export
export type { ButtonProps, InputProps };

// ✅ GOOD: 상수 export
export const BUTTON_VARIANTS = ['primary', 'secondary'] as const;
```

### ❌ Import 안티패턴

```typescript
// ❌ BAD: Barrel import (번들 크기 증가)
import { Button, Input, Card, Modal } from '@/components';

// ❌ BAD: 전체 라이브러리 import
import _ from 'lodash';
import * as R from 'ramda';

// ❌ BAD: default export (리팩토링 어려움)
export default function Button() { ... }
```

---

## 📋 섹션 5: 에러 처리 규칙

### 📊 에러 처리 패턴

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| `Result<T, E>` | 예상 가능한 실패 | API 호출, 파싱 |
| `try/catch` | 예외적 상황 | 외부 라이브러리 호출 |
| `Error Boundary` | React 렌더링 에러 | 컴포넌트 crash 방지 |

### ✅ 에러 처리 패턴

```typescript
// ✅ GOOD: Result 타입 패턴
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

// ✅ GOOD: 사용부
const result = await fetchUser('123');
if (!result.ok) {
  console.error(result.error);
  return;
}
console.log(result.value.name);  // 타입 안전
```

### ❌ 에러 처리 안티패턴

```typescript
// ❌ BAD: 에러 무시
try {
  await riskyOperation();
} catch (e) {
  // 아무것도 안함
}

// ❌ BAD: any로 catch
catch (e: any) {
  console.log(e.message);
}

// ❌ BAD: throw 문자열
throw 'Something went wrong';
```

---

## 📋 섹션 6: 성능 최적화 규칙

### 📊 최적화 체크리스트

| 항목 | 확인 방법 | 목표 |
|------|----------|------|
| **번들 크기** | `npx @next/bundle-analyzer` | < 100KB (초기) |
| **LCP** | Lighthouse | < 2.5s |
| **CLS** | Lighthouse | < 0.1 |
| **리렌더링** | React DevTools Profiler | 불필요한 리렌더 0 |

### ✅ 최적화 패턴

```typescript
// ✅ GOOD: 동적 import
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <Skeleton />,
  ssr: false
});

// ✅ GOOD: 메모이제이션
const sortedItems = useMemo(
  () => items.sort((a, b) => a.price - b.price),
  [items]
);

// ✅ GOOD: 이미지 최적화
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // LCP 이미지
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

---

## 📋 섹션 7: 테스트 규칙

### 📊 테스트 전략

| 테스트 유형 | 도구 | 커버리지 목표 |
|------------|------|--------------|
| 단위 테스트 | Vitest/Jest | 80% |
| 컴포넌트 테스트 | Testing Library | 핵심 컴포넌트 100% |
| E2E 테스트 | Playwright | Happy Path 100% |
| 타입 테스트 | tsd, expect-type | 유틸리티 타입 |

### ✅ 테스트 패턴

```typescript
// ✅ GOOD: 컴포넌트 테스트
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('버튼 클릭 시 카운터 증가', async () => {
  render(<Counter />);

  await userEvent.click(screen.getByRole('button', { name: /증가/i }));

  expect(screen.getByText('1')).toBeInTheDocument();
});

// ✅ GOOD: 타입 테스트
import { expectTypeOf } from 'expect-type';

test('fetchUser 반환 타입', () => {
  expectTypeOf(fetchUser).returns.toMatchTypeOf<Promise<Result<User>>>();
});
```

---

## ✅ 자가 진단 체크리스트

### 🔴 Critical (반드시 완료)
- [ ] `tsconfig.json`에 `strict: true` 설정
- [ ] `any` 타입 사용 0개
- [ ] barrel import 사용 0개
- [ ] Server/Client 컴포넌트 올바르게 분리

### 🟡 Important (80% 이상)
- [ ] 모든 함수에 반환 타입 명시
- [ ] 에러 처리 패턴 통일
- [ ] 불필요한 리렌더링 제거
- [ ] 이미지 최적화 적용

### 🟢 Nice-to-have
- [ ] 타입 테스트 작성
- [ ] 번들 분석 수행
- [ ] Lighthouse 90+ 달성

**합격 기준**: Critical 100% + Important 80% 이상

---

## 📚 참조

| 문서 | 링크 |
|------|------|
| TypeScript 공식 | https://www.typescriptlang.org/docs/ |
| React 공식 | https://react.dev/ |
| Next.js 공식 | https://nextjs.org/docs |
| Vercel Best Practices | `~/.claude/rules/react/REACT-RULES.md` |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Auto-detect: `package.json`, `tsconfig.json`
