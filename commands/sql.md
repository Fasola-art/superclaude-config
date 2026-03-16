---
description: "SQL 쿼리 실행 및 대체 데이터 분석 | SQL query execution and alt-data analysis"
argument-hint: "[query|analysis-type] [options]"
allowed-tools: ["Read", "Bash", "Write", "Edit", "Grep", "Glob", "WebFetch", "Task", "TodoWrite", "AskUserQuestion"]
---

# SQL Trading Command

SQL 기반 대체 데이터(위성, 물류, 지리) 분석 및 트레이딩 신호 생성

## 사용법

```
/sql <query|analysis-type> [options]
```

## 분석 유형

| 유형 | 설명 | 예시 |
|------|------|------|
| `logistics` | 물류/선박 추적 분석 | `/sql logistics delays` |
| `trade` | 국제 무역 통계 | `/sql trade china-us` |
| `freight` | 운임 지수 분석 | `/sql freight bdi` |
| `market` | 시장 데이터 조회 | `/sql market AAPL` |
| `indicators` | 경제 지표 분석 | `/sql indicators employment` |
| `signals` | 트레이딩 신호 | `/sql signals today` |
| `satellite` | 위성 데이터 (향후) | `/sql satellite ndvi` |
| `geo` | 지리 활동 (향후) | `/sql geo parking` |

## 예시 쿼리

### 직접 SQL 실행
```
/sql SELECT * FROM logistics_tracking WHERE status = 'delayed' LIMIT 10
/sql SELECT symbol, price, change_pct FROM v_latest_market WHERE asset_type = 'stock'
```

### 물류 분석
```
/sql logistics delays          # 물류 지연 현황
/sql logistics routes          # 주요 항로 분석
/sql logistics vessels         # 선박 추적
```

### 무역 분석
```
/sql trade summary             # 무역 요약
/sql trade china-us            # 중국-미국 무역
/sql trade commodities         # 주요 상품 분석
```

### 운임 지수
```
/sql freight bdi               # Baltic Dry Index
/sql freight fbx               # Freightos Baltic Index
/sql freight trends            # 운임 트렌드
```

### 시장 데이터
```
/sql market today              # 오늘 시장 요약
/sql market AAPL               # 특정 심볼 조회
/sql market crypto             # 암호화폐 시장
```

### 경제 지표
```
/sql indicators employment     # 고용 지표
/sql indicators inflation      # 인플레이션 지표
/sql indicators gdp            # GDP 관련 지표
/sql indicators latest         # 최신 발표 지표
```

### 트레이딩 신호
```
/sql signals today             # 오늘 생성된 신호
/sql signals buy               # 매수 신호
/sql signals high-confidence   # 고신뢰도 신호
```

## 옵션

| 옵션 | 설명 |
|------|------|
| `--days N` | 조회 기간 (기본: 30일) |
| `--limit N` | 결과 제한 (기본: 100) |
| `--format [table|json|csv]` | 출력 형식 |
| `--export FILE` | 파일로 내보내기 |

## 데이터베이스 정보

- **Host**: localhost:5432
- **Database**: claude_mcp
- **User**: reim
- **연결**: MCP 서버를 통한 PostgreSQL 연결

## 주요 테이블

| 테이블 | 설명 |
|--------|------|
| `logistics_tracking` | 물류/선박 추적 |
| `trade_statistics` | 국제 무역 통계 |
| `freight_indices` | 운임 지수 |
| `market_snapshots` | 시장 가격 스냅샷 |
| `economic_indicators` | 경제 지표 |
| `trading_signals` | 트레이딩 신호 |
| `satellite_data` | 위성 데이터 (향후) |
| `geo_activity` | 지리 활동 (향후) |

## 주요 뷰

| 뷰 | 설명 |
|----|------|
| `v_latest_market` | 최신 시장 데이터 |
| `v_latest_signals` | 최신 트레이딩 신호 |
| `v_logistics_delays` | 물류 지연 현황 |
| `v_latest_indicators` | 최신 경제 지표 |

## 실행 방법

1. **분석 유형 확인**: 요청된 분석 유형 파악
2. **쿼리 생성/실행**: MCP PostgreSQL 도구 또는 psql 사용
3. **결과 분석**: 데이터 해석 및 인사이트 제공
4. **신호 생성**: 필요시 트레이딩 신호 생성

## 관련 파일

- **스키마**: `~/.claude/modules/sql-trading/schema.sql`
- **설정**: `~/.claude/modules/sql-trading/config.json`
- **쿼리**: `~/.claude/modules/sql-trading/queries/`
- **수집기**: `~/.claude/modules/sql-trading/collectors/`

## 에이전트 연동

복잡한 분석이 필요한 경우 `sql-analyst` 에이전트 활용:
```
/sql 중국발 컨테이너 물동량 변화가 미국 소비재 주식에 미치는 영향 분석
```

---

**Version**: 1.0 | **Module**: sql-trading
