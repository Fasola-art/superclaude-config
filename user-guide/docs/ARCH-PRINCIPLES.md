# 시스템 아키텍처 설계 원칙

> SuperClaude v2.0.9 아키텍처 가이드라인

---

## 핵심 원칙

### 1. 단일 진실 공급원 (SSOT)
```yaml
principle: "모든 데이터는 단 하나의 출처를 가진다"
application:
  - 상태 관리: 중앙 저장소 사용
  - 설정: settings.json 단일 파일
  - 타입: 공유 타입 정의
```

### 2. 관심사 분리 (SoC)
```yaml
principle: "각 모듈은 하나의 책임만 가진다"
application:
  - UI: 표현 로직만
  - 비즈니스: 도메인 로직만
  - 데이터: 저장/조회 로직만
```

### 3. 느슨한 결합 (Loose Coupling)
```yaml
principle: "모듈 간 의존성을 최소화한다"
application:
  - 인터페이스 기반 설계
  - 이벤트 기반 통신
  - 의존성 주입
```

### 4. 높은 응집도 (High Cohesion)
```yaml
principle: "관련된 기능은 함께 모은다"
application:
  - 기능별 폴더 구조
  - 컴포넌트 단위 모듈화
  - 관련 로직 동일 파일
```

---

## 계층 구조

```
┌─────────────────────────────────────┐
│           Presentation              │  UI 컴포넌트
├─────────────────────────────────────┤
│           Application               │  유즈케이스, 서비스
├─────────────────────────────────────┤
│             Domain                  │  비즈니스 로직, 엔티티
├─────────────────────────────────────┤
│          Infrastructure             │  DB, API, 외부 서비스
└─────────────────────────────────────┘
```

---

## 파일 구조 패턴

### Feature-First (권장)
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

## 코드 품질 기준

### 복잡도 제한
| 지표 | 최대값 |
|------|--------|
| 함수 라인 수 | 50 |
| 파일 라인 수 | 300 |
| 순환 복잡도 | 10 |
| 매개변수 수 | 5 |

### 네이밍 규칙
| 타입 | 규칙 | 예시 |
|------|------|------|
| 컴포넌트 | PascalCase | UserProfile |
| 함수 | camelCase | getUserById |
| 상수 | UPPER_SNAKE | MAX_RETRIES |
| 타입 | PascalCase | UserResponse |

---

## 에러 처리 원칙

### Never Throws 패턴
```typescript
// ❌ 잘못된 방식
function getUser(id: string): User {
  if (!id) throw new Error('ID required')
  return fetch(...)
}

// ✅ 올바른 방식
function getUser(id: string): Result<User, UserError> {
  if (!id) return err(UserError.InvalidId)
  return ok(await fetch(...))
}
```

### 에러 타입 정의
```typescript
type Result<T, E> = Ok<T> | Err<E>
type Ok<T> = { ok: true; value: T }
type Err<E> = { ok: false; error: E }
```

---

## 성능 원칙

### 지연 로딩
- 라우트 단위 코드 스플리팅
- 이미지 lazy loading
- 컴포넌트 동적 import

### 캐싱 전략
- API 응답 캐싱
- 계산 결과 메모이제이션
- 정적 자산 브라우저 캐시

### 최적화 우선순위
1. 측정 (성능 병목 식별)
2. 최적화 (가장 큰 영향부터)
3. 검증 (개선 확인)
