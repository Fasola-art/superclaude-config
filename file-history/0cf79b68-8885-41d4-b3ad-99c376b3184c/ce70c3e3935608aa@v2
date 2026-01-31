# Writer-Reviewer v2.0 시스템

> 4-Agent 병렬 코드 검토 시스템

---

## 기본 설정

```yaml
target_score: 0.85           # 목표 점수
max_iterations: 10           # 최대 반복
convergence_threshold: 0.015 # 수렴 임계값
```

---

## 코드 타입별 적응형 가중치

| 타입 | Quality | Security | Performance | Accessibility |
|------|---------|----------|-------------|---------------|
| frontend_component | 0.25 | 0.25 | 0.20 | **0.30** |
| backend_api | 0.25 | **0.40** | 0.25 | 0.10 |
| utility_function | **0.35** | 0.25 | 0.30 | 0.10 |
| database_query | 0.20 | **0.40** | **0.35** | 0.05 |

---

## 타입 감지

```yaml
frontend:
  keywords: [component, tsx, jsx, ui, form, button, modal]
  file_patterns: ["*.tsx", "*.jsx", "components/"]

backend:
  keywords: [api, route, endpoint, controller, service, handler]
  file_patterns: ["/api/", "/routes/", "*.controller.ts"]

utility:
  keywords: [util, helper, lib, function, hook]
  file_patterns: ["/utils/", "/lib/", "/hooks/"]

database:
  keywords: [query, sql, database, migration, schema]
  file_patterns: ["/db/", "/migrations/", "*.sql"]
```

---

## 에이전트 상세

### Quality Agent (30%)

**검사 항목**
- 코드 가독성 (네이밍, 구조)
- 타입 안전성 (TypeScript 활용)
- 에러 처리 (try-catch, 엣지 케이스)
- SOLID 원칙 준수
- 코드 중복 최소화 (DRY)

**감점 규칙**
| 항목 | 감점 |
|------|------|
| react-hook-form 미사용 | -0.15 |
| 인라인 상수 정의 | -0.10 |
| Zod 검증 누락 | -0.20 |
| 권한 검사 누락 | -0.30 |
| 패턴 불일치 | -0.10 |

---

### Security Agent (30%)

**검사 항목**
- XSS 취약점 방지
- SQL/Command Injection 방지
- 인증/권한 처리
- 민감 정보 노출 방지
- 입력 검증

**치명적 이슈 (즉시 수정 필요)**
- SQL Injection 가능성
- XSS 취약점
- 하드코딩된 비밀번호/API 키
- 인증 우회 가능성
- CSRF 취약점

**치명적 발견 시: max_score = 0.3**

---

### Performance Agent (20%)

**검사 항목**
- 알고리즘 효율성 (시간/공간 복잡도)
- 불필요한 렌더링 (React)
- 메모리 누수 가능성
- N+1 쿼리 문제
- 번들 크기 영향

**React 전용**
- useMemo/useCallback 적절한 사용
- 불필요한 state 업데이트
- React.memo 필요성
- Lazy loading 기회

---

### Accessibility Agent (20%)

**검사 항목**
- 시맨틱 HTML 사용
- ARIA 레이블 적절성
- 키보드 네비게이션
- 색상 대비
- 포커스 관리

**표준: WCAG 2.1 AA**

---

## 수렴 조건

### 조기 종료 조건
- 목표 점수 (0.85) 달성
- 모든 카테고리 0.80 이상
- 2회 연속 점수 변화 < 0.015

### 보안 최소 점수

```yaml
security_minimum:
  score: 0.85
  block_early_exit_if:
    security_score < 0.85
    has_critical_issues: true
    any_category < 0.70
```

---

## 출력 형식

```
[Code Block]
---
Quality Score: 86% (3 iterations)
├── Quality: 87% | Security: 88% | Performance: 83% | Accessibility: 86%
└── Issues: [해결된 이슈 요약]
```

---

## 플래그

| 플래그 | 효과 |
|--------|------|
| --no-review | Writer-Reviewer 비활성화 (보안 코드 제외) |
| --review-strict | 목표 점수 0.90으로 상향 |
| --review-quick | 최대 3회 반복 |
| --review-verbose | 각 반복 상세 출력 |
