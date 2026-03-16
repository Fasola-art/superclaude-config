# 코덱스 작업 명세서 템플릿

> 이 템플릿을 복사하여 각 작업에 맞게 채워 에이전트에 전달하세요.
> 모든 섹션을 완성해야 합니다. 빈 섹션은 허용되지 않습니다.

---

## 섹션 1: 작업 목표

**단일 문장으로 작성 (What + Why):**

```
[예시] 사용자 인증 미들웨어를 JWT 기반으로 구현하여 API 보안을 강화한다.
```

**우선순위**: [ ] P0-Critical  [ ] P1-High  [ ] P2-Normal  [ ] P3-Low

---

## 섹션 2: 환경 정보

```yaml
# 실행 환경
platform: wsl2          # wsl2 | windows | linux | macos
working_dir: ~/project  # WSL2 절대경로 (Windows 경로 사용 금지)
runtime:
  language: typescript  # typescript | python | go | rust
  version: "20"         # Node.js 20 / Python 3.12 / Go 1.22
  package_manager: pnpm # npm | pnpm | yarn | pip | go mod

# 모델 선택 (CLAUDE.md Cost Strategy 기반)
model: sonnet            # opus(복잡로직/아키텍처) | sonnet(표준구현) | haiku(단순수정)
model_reason: "표준 기능 구현"
```

---

## 섹션 3: 기술 스택 및 패턴

```yaml
# 프레임워크/라이브러리
framework: next.js       # 버전 포함
key_libraries:
  - "zod@3.22"
  - "prisma@5.8"

# 아키텍처 패턴
patterns:
  - "Repository Pattern"
  - "Clean Architecture"

# 코딩 규칙 참조
rules_ref:
  - "~/.claude/rules/typescript/critical.md"
  - "~/.claude/rules/react/critical.md"
```

---

## 섹션 4: 입력 파일 (읽기 전용)

```yaml
# 참조할 기존 파일 (수정 금지)
readonly_files:
  - path: ~/project/src/types/user.ts
    purpose: "User 타입 정의 참조"
  - path: ~/project/prisma/schema.prisma
    purpose: "DB 스키마 참조"

# 컨텍스트 파일
context_files:
  - ~/project/.planning/context.md
  - ~/project/TASKS.md
```

---

## 섹션 5: 출력 파일

```yaml
# 생성할 파일
create_files:
  - path: ~/project/src/middleware/auth.ts
    description: "JWT 인증 미들웨어"
    max_lines: 80
  - path: ~/project/src/middleware/index.ts
    description: "Barrel export"
    max_lines: 10

# 수정할 파일
modify_files:
  - path: ~/project/src/app.ts
    change: "auth 미들웨어 등록 추가"

# 절대 수정 금지
protected_files:
  - ~/project/.env
  - ~/project/prisma/migrations/
```

---

## 섹션 6: 세부 요구사항

### 기능 요구사항

```
FR-001: JWT access token 검증 (HS256 알고리즘)
FR-002: 만료된 토큰 → 401 응답 + 명시적 에러 메시지
FR-003: 유효하지 않은 토큰 → 403 응답
FR-004: 성공 시 req.user에 페이로드 주입
```

### 비기능 요구사항

```
NFR-001: 인증 처리 < 10ms
NFR-002: 메모리 누수 없음 (토큰 캐싱 시 LRU 사용)
NFR-003: 로그 포함 (성공/실패 모두)
```

---

## 섹션 7: 인터페이스 명세

```typescript
// 에이전트가 준수해야 할 인터페이스

// 입력 타입
interface AuthRequest extends Request {
  user?: JWTPayload;
}

// 출력 타입
interface JWTPayload {
  userId: string;
  email: string;
  role: 'admin' | 'user';
  iat: number;
  exp: number;
}

// 에러 응답 형식
interface AuthError {
  code: 'EXPIRED' | 'INVALID' | 'MISSING';
  message: string;
}
```

---

## 섹션 8: 금지 사항 (PROHIBITED)

```
PROHIBITED-001: 환경 변수 하드코딩 (JWT_SECRET 등)
PROHIBITED-002: console.log 디버그 코드 남기기
PROHIBITED-003: any 타입 사용
PROHIBITED-004: 테스트 파일 수정 또는 삭제
PROHIBITED-005: 명세서에 없는 파일 생성
PROHIBITED-006: 기존 API 인터페이스 변경
PROHIBITED-007: 의존성 무단 추가 (package.json 수정 금지)
```

---

## 섹션 9: 검증 방법

```bash
# 에이전트가 완료 후 실행해야 할 명령어

# 1. 타입 체크
npx tsc --noEmit

# 2. 린트
npx eslint src/middleware/

# 3. 테스트 실행
npm test -- --testPathPattern=middleware

# 4. 빌드 확인
npm run build

# 기대 결과
# - 타입 에러 0개
# - 린트 에러 0개
# - 테스트 통과율 100%
# - 빌드 성공
```

---

## 섹션 10: 성공 기준 + 클로드 검증 체크포인트

### 에이전트 완료 기준

```
[ ] 모든 FR/NFR 구현 완료
[ ] 타입 에러 0개
[ ] 린트 에러 0개
[ ] 테스트 통과
[ ] 파일 줄 제한 준수
[ ] 금지 사항 위반 없음
```

### 클로드 검증 체크포인트

```
[ ] 인터페이스 호환성 확인
[ ] 보안 취약점 검토
[ ] 아키텍처 패턴 준수 확인
[ ] 에러 처리 완성도
[ ] 성능 기준 충족 여부
[ ] TASKS.md 업데이트
```

---

## 핸드오프 메모 (클로드 → 에이전트)

```
작성일시: YYYY-MM-DD HH:MM
컨텍스트: [현재 프로젝트 상태 한 줄 요약]
주의사항: [특별히 신경써야 할 사항]
완료 후: [에이전트 완료 보고 형식 참조]
```

---

**Version**: 1.0.0
**Template Type**: Codex/Agent Task Specification
