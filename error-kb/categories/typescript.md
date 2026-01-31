# TypeScript 에러 패턴

> **카테고리**: typescript
> **갱신일**: 2026-01-30

---

## 🔴 Critical 에러

### TS2304: Cannot find name 'X'

**원인**: 타입/변수가 정의되지 않음

**해결책**:
1. import 문 확인
2. `@types/` 패키지 설치
3. `tsconfig.json` 설정 확인

```typescript
// ❌ 에러
const user: User = { ... };  // Cannot find name 'User'

// ✅ 해결
import type { User } from '@/types';
const user: User = { ... };
```

**예방**: `strict: true` + ESLint import 규칙

---

### TS2345: Argument type mismatch

**원인**: 함수 인자 타입 불일치

**해결책**:
1. 타입 확인 후 수정
2. 타입 가드 추가
3. 제네릭 활용

```typescript
// ❌ 에러
function process(id: number) { ... }
process("123");  // string을 number로

// ✅ 해결 1: 타입 변환
process(parseInt("123", 10));

// ✅ 해결 2: 함수 시그니처 수정
function process(id: number | string) { ... }
```

---

### TS2322: Type 'X' is not assignable to type 'Y'

**원인**: 타입 할당 불일치

**해결책**:
1. 타입 정의 확인
2. 타입 좁히기 (narrowing)
3. 타입 단언 (최후 수단)

```typescript
// ❌ 에러
const status: 'active' | 'inactive' = getStatus();
// Type 'string' is not assignable to type...

// ✅ 해결: 타입 좁히기
const status = getStatus();
if (status === 'active' || status === 'inactive') {
  // status: 'active' | 'inactive'
}

// ✅ 또는: as const
function getStatus() {
  return 'active' as const;
}
```

---

## 🟠 Common 에러

### TS2339: Property does not exist

**원인**: 객체에 속성이 없음

**해결책**:
```typescript
// ❌ 에러
const user = { name: 'test' };
console.log(user.email);  // Property 'email' does not exist

// ✅ 해결 1: 타입 정의
interface User {
  name: string;
  email?: string;
}

// ✅ 해결 2: optional chaining
console.log(user.email ?? 'N/A');
```

---

### TS7006: Parameter implicitly has 'any' type

**원인**: 매개변수 타입 미지정 (strict 모드)

**해결책**:
```typescript
// ❌ 에러
const double = (n) => n * 2;  // Parameter 'n' implicitly has 'any'

// ✅ 해결
const double = (n: number): number => n * 2;
```

**예방**: `noImplicitAny: true` 유지

---

### TS2531: Object is possibly 'null'

**원인**: null 체크 누락 (strict null checks)

**해결책**:
```typescript
// ❌ 에러
const name = user.name;  // 'user' is possibly 'null'

// ✅ 해결 1: optional chaining
const name = user?.name;

// ✅ 해결 2: null 체크
if (user) {
  const name = user.name;
}

// ✅ 해결 3: 단언 (확실한 경우만)
const name = user!.name;  // 비권장
```

---

## 🟡 Config 에러

### Cannot find module 'X' or its type declarations

**원인**: 모듈 해석 실패

**해결책**:
1. 패키지 설치 확인
2. `@types/` 설치
3. `tsconfig.json` paths 설정

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

**원인**: 같은 이름 중복 정의

**해결책**:
1. `skipLibCheck: true` (임시)
2. 중복 `@types` 제거
3. 네임스페이스 분리

---

## 📊 에러 코드 레퍼런스

| 코드 | 분류 | 빈도 |
|------|------|------|
| TS2304 | 미정의 이름 | 높음 |
| TS2345 | 인자 타입 | 높음 |
| TS2322 | 할당 타입 | 높음 |
| TS2339 | 속성 없음 | 중간 |
| TS7006 | 암묵적 any | 중간 |
| TS2531 | null 가능 | 중간 |

---

## 🔧 디버깅 명령어

```bash
# 타입 체크만
npx tsc --noEmit

# 상세 에러
npx tsc --noEmit --pretty

# 특정 파일만
npx tsc --noEmit src/file.ts
```

---

**META**
- Category: typescript
- Last Updated: 2026-01-30
