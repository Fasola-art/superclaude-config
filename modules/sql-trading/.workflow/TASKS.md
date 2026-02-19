# Tasks

> Claude가 작성, Codex가 소비. 1 Task = 1 Module 원칙.

---

## Task 1: 스키마 및 인덱스 정리

- **Status**: DONE
- **Assignee**: Codex
- **Module**: schema.sql
- **Priority**: P0
- **Dependencies**: -

### Acceptance Criteria

- [ ] `schema.sql`이 모든 핵심 테이블을 포함한다 (market_snapshots 등)
- [ ] 모든 시계열 테이블에 timestamp 인덱스가 있다
- [ ] 빈 DB에 적용 시 오류 없이 실행된다

## Task 2: 데이터 수집 파이프라인 정비

- **Status**: DONE
- **Assignee**: Codex
- **Module**: collectors/
- **Priority**: P0
- **Dependencies**: 1

### Acceptance Criteria

- [ ] 주요 수집기들이 공통 DB 유틸을 통해 적재한다
- [ ] 실패 시 재시도/백오프가 적용된다
- [ ] `collectors/collect_all.py`로 일괄 수집이 가능하다

## Task 3: API 엔드포인트 안정화

- **Status**: DONE
- **Assignee**: Codex
- **Module**: packages/api/src
- **Priority**: P0
- **Dependencies**: 1

### Acceptance Criteria

- [ ] 주요 테이블을 조회하는 엔드포인트가 존재한다
- [ ] DB 연결 풀/재사용이 적용된다
- [ ] 오류 응답 포맷이 일관된다

## Task 4: 대시보드 UI 기능 보강

- **Status**: DONE
- **Assignee**: Codex
- **Module**: packages/dashboard/src
- **Priority**: P1
- **Dependencies**: 3

### Acceptance Criteria

- [ ] 핵심 지표 화면에서 차트가 렌더링된다
- [ ] API 연동 로딩/에러 상태가 있다
- [ ] 모바일/데스크톱 레이아웃이 모두 동작한다

## Task 5: SQL 쿼리 라이브러리 정비

- **Status**: PENDING
- **Assignee**: Codex
- **Module**: queries/
- **Priority**: P1
- **Dependencies**: 1

### Acceptance Criteria

- [ ] 주요 분석 쿼리가 파일로 분리되어 있다
- [ ] 모든 쿼리에 `LIMIT`이 포함된다
- [ ] `SELECT *` 사용을 지양한다

## Task 6: CLI 도구 안정화

- **Status**: PENDING
- **Assignee**: Codex
- **Module**: trade
- **Priority**: P2
- **Dependencies**: 2

### Acceptance Criteria

- [ ] 수집 실행/상태 확인 명령이 있다
- [ ] 실패 시 사용자 친화적 메시지를 출력한다
- [ ] 기본 사용법이 `--help`에 노출된다

---

**Total**: 6 tasks | **Done**: 0 | **In Progress**: 0 | **Blocked**: 0
