---
name: sql-trading
description: SQL 기반 대체 데이터 트레이딩 분석 + 실시간 대시보드
version: "2.0.0"
triggers:
  - /sql-trading
  - SQL 트레이딩 분석
  - 대체 데이터로 트레이딩
  - 물류 대시보드
---

# SQL Trading Skill

SQL을 활용한 대체 데이터(위성, 물류, 지리) 분석 및 트레이딩 인사이트 생성

## 🚀 실시간 대시보드

### 실행 방법
```bash
cd ~/.claude/modules/sql-trading/dashboard
python3 api_server.py
# 브라우저: http://localhost:8080
```

### 대시보드 기능
| 기능 | 설명 |
|------|------|
| 섹터 현황 | 원자재/물류 섹터별 등락률 |
| 트레이딩 신호 | BUY/SELL 신호 + 신뢰도 |
| 경제지표 | 금리차, 하이일드스프레드, 유가 |
| 물류 추적 | 세계 항로 시각화 + 항구별 물류 정보 |
| 운임 지수 | BDI, 컨테이너 운임 |

### 데이터 수집 (LaunchAgent)
- **수집 주기**: 1시간
- **데이터 소스**: Alpha Vantage (ETF), yfinance (주식), FRED (경제지표)
- **plist**: `~/Library/LaunchAgents/com.claude.sql-trading-collector.plist`

```bash
# 수집기 상태 확인
launchctl list | grep sql-trading

# 수동 실행
~/.claude/modules/sql-trading/collectors/run_collector.sh
```

## 개요

이 스킬은 PostgreSQL 데이터베이스에 저장된 다양한 대체 데이터를 분석하여
트레이딩에 활용 가능한 인사이트와 신호를 생성합니다.

## 사용법

```
/sql-trading [분석유형] [옵션]
```

## 분석 유형

### 1. 물류 분석 (logistics)

선박/컨테이너 추적 데이터를 분석하여 공급망 동향 파악

```
/sql-trading logistics delays      # 지연 현황
/sql-trading logistics routes      # 항로별 물동량
/sql-trading logistics ports       # 항구별 활동
```

**트레이딩 활용**:
- 물동량 증가 → 관련 소비재/제조업 수요 증가 예상
- 지연 증가 → 공급망 병목, 인플레이션 압력

### 2. 무역 분석 (trade)

UN Comtrade 국제 무역 통계 분석

```
/sql-trading trade summary         # 전체 요약
/sql-trading trade china-us        # 특정 국가간 무역
/sql-trading trade commodities     # 상품별 분석
```

**트레이딩 활용**:
- 수출입 변화 → 해당 산업 주식 영향
- 무역 적자/흑자 → 환율 영향

### 3. 운임 분석 (freight)

해상/항공 운임 지수 추이 분석

```
/sql-trading freight bdi           # Baltic Dry Index
/sql-trading freight fbx           # Freightos Baltic Index
/sql-trading freight trends        # 장기 트렌드
```

**트레이딩 활용**:
- 운임 상승 → 해운주 수혜, 물가 상승 압력
- 운임 하락 → 경기 둔화 신호 가능

### 4. 통합 분석 (combined)

다중 데이터 소스 결합 분석

```
/sql-trading combined sector-impact    # 섹터별 영향
/sql-trading combined macro-signal     # 거시 신호
/sql-trading combined alpha            # 알파 신호 탐색
```

## 워크플로우

### Step 1: 데이터 현황 확인

```sql
SELECT
    'logistics' as category,
    COUNT(*) as records,
    MAX(timestamp) as latest
FROM logistics_tracking
UNION ALL
SELECT 'trade', COUNT(*), MAX(created_at) FROM trade_statistics
UNION ALL
SELECT 'freight', COUNT(*), MAX(date) FROM freight_indices;
```

### Step 2: 분석 쿼리 실행

사용자 요청에 맞는 SQL 쿼리 생성 및 실행

### Step 3: 인사이트 도출

- 통계적 유의성 확인
- 역사적 패턴과 비교
- 시장 영향 평가

### Step 4: 신호 생성 (선택)

분석 결과가 명확한 트레이딩 기회를 시사하는 경우:

```sql
INSERT INTO trading_signals (timestamp, symbol, signal_type, confidence, strategy, reason, alt_data_source)
VALUES (NOW(), 'SYMBOL', 'BUY/SELL', 0.75, 'strategy_name', '분석 근거', 'data_source');
```

## 데이터베이스 스키마

### 주요 테이블

| 테이블 | 설명 | 주요 컬럼 |
|--------|------|-----------|
| `logistics_tracking` | 물류 추적 | shipment_id, origin_port, dest_port, status |
| `trade_statistics` | 무역 통계 | period, reporter, commodity, trade_value |
| `freight_indices` | 운임 지수 | date, index_name, value |
| `market_snapshots` | 시장 데이터 | symbol, price, change_pct |
| `economic_indicators` | 경제 지표 | series_id, date, value |
| `trading_signals` | 신호 저장 | symbol, signal_type, confidence |

### 유용한 뷰

| 뷰 | 설명 |
|----|------|
| `v_latest_market` | 최신 시장 가격 |
| `v_logistics_delays` | 물류 지연 현황 |
| `v_latest_indicators` | 최신 경제 지표 |
| `v_latest_signals` | 최신 트레이딩 신호 |

## 예시

### 물류 지연 → 소비재 영향 분석

```
/sql-trading logistics delays --sector consumer
```

결과:
```
## 물류 지연 현황 (최근 30일)

| 항로 | 지연율 | 전월 대비 |
|------|--------|-----------|
| 중국 → LA | 15.2% | +3.2%p |
| 중국 → NY | 12.8% | +1.5%p |

### 영향 분석
- 소비재 공급 지연 예상
- 관련 종목: COST, WMT, TGT
- 신호: 단기 재고 보유 기업 유리
```

### BDI 분석 → 해운주 전망

```
/sql-trading freight bdi --correlation shipping
```

결과:
```
## Baltic Dry Index 분석

현재: 1,523 (MA30: 1,412, +7.8%)

### 해운주 상관관계
| 종목 | 상관계수 | 추천 |
|------|----------|------|
| SBLK | 0.82 | BUY |
| GOGL | 0.78 | BUY |
| DSX | 0.71 | HOLD |

신뢰도: 75%
```

## 관련 파일

| 파일 | 경로 |
|------|------|
| 대시보드 HTML | `~/.claude/modules/sql-trading/dashboard/realtime.html` |
| API 서버 | `~/.claude/modules/sql-trading/dashboard/api_server.py` |
| 데이터 수집기 | `~/.claude/modules/sql-trading/collectors/realtime_collector.py` |
| LaunchAgent | `~/Library/LaunchAgents/com.claude.sql-trading-collector.plist` |
| DB 스키마 | `~/.claude/modules/sql-trading/schema.sql` |
| API 키 | `~/.claude/credentials/api-keys.json` (alpha_vantage, fred) |
| 커맨드 | `~/.claude/commands/sql.md` |

## 주의사항

1. **데이터 신선도**: 분석 전 데이터 최신성 확인
2. **상관관계 ≠ 인과관계**: 통계적 상관은 인과를 의미하지 않음
3. **리스크 관리**: 대체 데이터는 보조 지표로 활용
4. **백테스팅 필수**: 신호 전략은 반드시 백테스팅 수행

---

**Version**: 1.0 | **Skill**: sql-trading
