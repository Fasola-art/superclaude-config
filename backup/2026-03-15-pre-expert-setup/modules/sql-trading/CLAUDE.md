# SQL Trading Module Rules

> 이 폴더에서 작업하는 에이전트는 반드시 준수

## DB 연결 정보

| 항목 | 값 |
|------|------|
| Database | claude_mcp |
| Host | localhost |
| Type | PostgreSQL 15+ |

## 필수 규칙

| 규칙 | 설명 |
|------|------|
| 스키마 수정 | schema.sql 먼저 수정 후 적용 |
| 쿼리 저장 | queries/ 폴더에 저장 |
| 인덱스 | 시계열 데이터는 timestamp 인덱스 필수 |

## 폴더 구조

```
sql-trading/
├── schema.sql       # DB 스키마 (수정 시 여기 먼저)
├── config.json      # 설정
├── trade            # CLI 도구
├── collectors/      # 데이터 수집기
├── queries/         # SQL 쿼리 파일
├── dashboard/       # Streamlit 대시보드
└── data/            # 로컬 데이터
```

## 테이블 요약

| 테이블 | 용도 |
|--------|------|
| market_snapshots | 시장 스냅샷 |
| logistics_tracking | 물류 추적 |
| economic_indicators | 경제 지표 |
| trade_statistics | 무역 통계 |
| freight_indices | 운임 지수 |

## SQL 규칙 참조

- 상세: `~/.claude/rules/sql/SQL-TRADING-RULES.md`
- 핵심: LIMIT 필수, SELECT * 지양, 인덱스 활용
