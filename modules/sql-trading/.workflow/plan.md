# Project Plan

> Claude(지휘자)가 작성. 아키텍처 결정과 전체 설계를 기록.

---

## Architecture

- Ingestion: `collectors/`가 외부 소스 데이터를 수집해 Postgres에 적재
- Storage: `schema.sql`이 핵심 테이블과 인덱스 정의 (timestamp 인덱스 포함)
- Access: `packages/api/src`의 FastAPI가 읽기 API 제공, 복잡 쿼리는 `queries/`에 보관
- Consumption: Next.js 대시보드(`packages/dashboard/src`), CLI(`trade`), 정적 HTML(`packages/api/src/*.html`)
- Ops: `deploy/` 및 실행 스크립트로 수집/배포 자동화

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Language | Python 3.11, TypeScript 5, SQL | 수집/백엔드, 프론트, 쿼리 분리 |
| Framework | FastAPI, Next.js 16, React 19 | API/대시보드 표준화 |
| Database | PostgreSQL 15 | 시계열/분석 쿼리 안정성 |
| Testing | pytest, eslint | API 유닛/스타일 검증 |
| CI/CD | Turbo + pnpm scripts (local) | 모노레포 빌드/실행 |

## Modules

| Module | Path | Description | Status |
|--------|------|-------------|--------|
| Database schema | schema.sql | 테이블/인덱스 정의 | PENDING |
| Collectors | collectors/ | 데이터 수집 및 적재 | PENDING |
| API | packages/api/src | FastAPI 엔드포인트 | PENDING |
| Dashboard | packages/dashboard/src | UI/차트/지도 | PENDING |
| Queries | queries/ | 재사용 SQL 쿼리 | PENDING |
| CLI | trade | 수집/점검 실행 도구 | PENDING |
| Deploy | deploy/ | 배포/운영 스크립트 | PENDING |

## Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| `schema.sql`을 단일 진실원본으로 유지 | 스키마 변경 추적 용이 | 2026-02-17 |
| 수집기는 직접 DB 적재 | 파이프라인 단순화 | 2026-02-17 |
| 대시보드는 API 기반으로만 데이터 접근 | 보안/캐시 일원화 | 2026-02-17 |

## Risks

| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| 외부 소스 레이트리밋 | 데이터 공백 | 백오프/캐시 | OPEN |
| 스키마 변경 누락 | 쿼리 실패 | `schema.sql` 선수정 규칙 | OPEN |
| 시계열 인덱스 미비 | 성능 저하 | timestamp 인덱스 점검 | OPEN |

---

**Updated**: 2026-02-17
