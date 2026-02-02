# SQL 기반 대체 데이터 트레이딩 워크플로우

> **목표**: SQL을 활용한 대체 데이터(위성, 물류, 지리) 분석 시스템 구축

**Version**: 1.0 | **Date**: 2026-02-01

---

## 📋 Quick Summary

| 항목 | 내용 |
|------|------|
| **데이터베이스** | PostgreSQL (claude_mcp) - MCP 서버 활성화됨 |
| **우선 데이터** | 🚢 물류 추적 (컨테이너, 선박) |
| **데이터 소스** | 무료 공개 API (MarineTraffic, UN Comtrade 등) |
| **생성 파일** | DB 스키마 + Command + Skill + Agent |
| **TDD/E2E** | 선택사항 (수집기 단위 테스트 권장) |

---

## 🎯 현재 상태

### 활성화된 인프라
- ✅ PostgreSQL MCP 서버: `postgresql://reim@localhost:5432/claude_mcp`
- ✅ Trading 모듈: JSON 기반 (DB 마이그레이션 필요)
- ✅ Realtime-analysis: 스트림 처리 패턴 있음
- ✅ News-collector: 다중 소스 수집 패턴 있음

### 필요한 구성
- ❌ 대체 데이터용 DB 스키마
- ❌ `/sql` 커맨드
- ❌ sql-analyst 에이전트
- ❌ 데이터 수집 스케줄러

---

## 📐 아키텍처 설계

### 1. 데이터베이스 스키마

```sql
-- 대체 데이터 테이블
CREATE TABLE satellite_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    location_code VARCHAR(50),
    lat DECIMAL(10, 6),
    lng DECIMAL(10, 6),
    sensor VARCHAR(50),        -- sentinel-2, landsat-8
    band VARCHAR(20),
    value DECIMAL(15, 6),
    ndvi DECIMAL(5, 4),        -- 정규 식생 지수
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE logistics_tracking (
    id SERIAL PRIMARY KEY,
    shipment_id VARCHAR(100) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    lat DECIMAL(10, 6),
    lng DECIMAL(10, 6),
    status VARCHAR(50),        -- in_transit, delivered, delayed
    carrier VARCHAR(100),
    origin_port VARCHAR(100),
    dest_port VARCHAR(100),
    cargo_type VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE geo_activity (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    region_code VARCHAR(50),
    activity_type VARCHAR(50), -- parking, traffic, construction
    intensity DECIMAL(10, 4),
    lat DECIMAL(10, 6),
    lng DECIMAL(10, 6),
    source VARCHAR(100),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 기존 트레이딩 데이터 마이그레이션
CREATE TABLE market_snapshots (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    price DECIMAL(15, 6),
    change_pct DECIMAL(10, 4),
    volume BIGINT,
    source VARCHAR(50),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE economic_indicators (
    id SERIAL PRIMARY KEY,
    series_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    value DECIMAL(20, 6),
    previous_value DECIMAL(20, 6),
    change_pct DECIMAL(10, 4),
    category VARCHAR(50),
    importance VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE trading_signals (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20),
    signal_type VARCHAR(20),   -- BUY, SELL, HOLD
    confidence DECIMAL(5, 4),
    price DECIMAL(15, 6),
    strategy VARCHAR(50),
    indicators JSONB,
    reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스
CREATE INDEX idx_satellite_timestamp ON satellite_data(timestamp);
CREATE INDEX idx_satellite_location ON satellite_data(location_code);
CREATE INDEX idx_logistics_shipment ON logistics_tracking(shipment_id);
CREATE INDEX idx_logistics_timestamp ON logistics_tracking(timestamp);
CREATE INDEX idx_geo_region ON geo_activity(region_code);
CREATE INDEX idx_market_symbol ON market_snapshots(symbol, timestamp);
CREATE INDEX idx_indicators_series ON economic_indicators(series_id, date);
```

### 2. 파일 구조

```
~/.claude/
├── modules/
│   └── sql-trading/
│       ├── config.json           # DB 연결 및 설정
│       ├── schema.sql            # 스키마 정의
│       ├── queries/              # 재사용 쿼리
│       │   ├── satellite.sql
│       │   ├── logistics.sql
│       │   ├── geo_activity.sql
│       │   └── market_analysis.sql
│       └── collectors/           # 데이터 수집기
│           ├── satellite_collector.py
│           ├── logistics_collector.py
│           └── geo_collector.py
├── commands/
│   └── sql.md                    # /sql 커맨드
├── skills/
│   └── sql-trading/
│       └── SKILL.md              # SQL 트레이딩 스킬
├── agents/
│   └── sql-analyst.md            # SQL 분석 에이전트
└── rules/
    └── sql/
        └── SQL-TRADING-RULES.md  # SQL 쿼리 규칙
```

---

## 🛠️ 구현 범위

### Phase 1: 기반 구축

| 파일 | 경로 | 설명 |
|------|------|------|
| schema.sql | `modules/sql-trading/` | DB 스키마 |
| config.json | `modules/sql-trading/` | 연결 설정 |
| sql.md | `commands/` | `/sql` 커맨드 |

### Phase 2: 에이전트 & 스킬

| 파일 | 경로 | 설명 |
|------|------|------|
| sql-analyst.md | `agents/` | SQL 분석 전문 에이전트 |
| SKILL.md | `skills/sql-trading/` | SQL 트레이딩 스킬 |
| SQL-TRADING-RULES.md | `rules/sql/` | SQL 쿼리 규칙 |

### Phase 3: 물류 데이터 수집기 (우선)

| 파일 | 경로 | 설명 |
|------|------|------|
| logistics_collector.py | `modules/sql-trading/collectors/` | 🚢 물류 데이터 수집 |

**무료 물류 API 소스:**

| API | 데이터 | 무료 티어 |
|-----|--------|----------|
| UN Comtrade | 국제 무역 통계 | 무제한 (월 100회) |
| MarineTraffic (Free) | 선박 위치/항구 | 제한적 AIS 데이터 |
| OpenSeaMap | 해상 지도 데이터 | 완전 무료 |
| Port API | 항구 정보 | 기본 정보 무료 |
| Freightos Baltic Index | 운임 지수 | 일일 데이터 무료 |

**향후 확장:**
| 파일 | 경로 | 설명 |
|------|------|------|
| satellite_collector.py | `modules/sql-trading/collectors/` | 위성 데이터 (Phase 2) |
| geo_collector.py | `modules/sql-trading/collectors/` | 지리 활동 (Phase 3) |

### Phase 4: 자동화 훅

| 파일 | 경로 | 설명 |
|------|------|------|
| sql-data-collector.py | `hooks/PostToolUse/` | 자동 데이터 수집 |
| sql-alert-monitor.py | `hooks/PostToolUse/` | SQL 기반 알림 |

---

## 📝 주요 컴포넌트 설계

### /sql 커맨드

```markdown
---
description: SQL 쿼리 실행 및 대체 데이터 분석
argument-hint: "[query or analysis-type]"
allowed-tools: ["Read", "Bash", "TodoWrite", "AskUserQuestion"]
---

# SQL Trading Workflow

## 사용 예시
- `/sql 오늘 위성 데이터 요약`
- `/sql SELECT * FROM satellite_data WHERE timestamp > NOW() - INTERVAL '1 day'`
- `/sql 물류 지연 현황`
- `/sql 경제 지표 변화율 분석`

## 분석 유형
1. satellite - 위성 이미지 분석 (NDVI, 변화 감지)
2. logistics - 물류 추적 분석 (지연, 경로)
3. geo - 지리 활동 분석 (주차장, 교통)
4. market - 시장 데이터 분석
5. indicators - 경제 지표 분석
6. signals - 트레이딩 신호 조회
```

### sql-analyst 에이전트

```markdown
---
name: sql-analyst
description: SQL 기반 대체 데이터 분석 전문가
triggers:
  - SQL 분석
  - 데이터베이스 쿼리
  - 대체 데이터 트레이딩
tools:
  - Read
  - Bash
  - Grep
  - WebSearch
---

# SQL Analyst Agent

## 전문 분야
- PostgreSQL 쿼리 최적화
- 대체 데이터 분석 (위성, 물류, 지리)
- 트레이딩 신호 생성
- 시계열 데이터 분석

## 분석 패턴
- 위성: NDVI 변화 → 농작물 생산 예측
- 물류: 컨테이너 이동 → 무역 트렌드 감지
- 지리: 주차장 점유 → 소매 트래픽 예측
```

---

## 🔄 데이터 흐름

```
외부 API 소스
    ↓
[Collectors] ← 스케줄 실행
    ↓
PostgreSQL DB (claude_mcp)
    ↓
[/sql 커맨드] ← 사용자 쿼리
    ↓
[sql-analyst 에이전트] ← 분석
    ↓
트레이딩 인사이트/신호
```

---

## 🧪 TDD/E2E 필요성

| 항목 | 필요도 | 이유 |
|------|--------|------|
| TDD (단위 테스트) | **권장** | API 응답 파싱, 데이터 변환 로직 검증 |
| E2E (통합 테스트) | 선택 | DB 연결 → 수집 → 저장 파이프라인 검증 |

**권장 접근법:**
1. 먼저 기본 구조 구축 (스키마, 수집기, 커맨드)
2. 수집기 안정화 후 단위 테스트 추가 (`/tdd` 활용)
3. 필요시 E2E 테스트로 전체 파이프라인 검증

---

## ✅ 검증 방법

1. DB 연결 테스트: `psql -U reim -d claude_mcp`
2. 스키마 생성 확인: `\dt` 명령으로 테이블 목록
3. `/sql` 커맨드 실행 테스트
4. 샘플 데이터 삽입 및 쿼리 테스트
5. 물류 API 연동 테스트 (UN Comtrade 쿼리)

---

## 📊 예상 결과

| 카테고리 | 파일 수 |
|----------|---------|
| 모듈 | 6개 (스키마, 설정, 수집기 3개, 쿼리) |
| 커맨드 | 1개 |
| 에이전트 | 1개 |
| 스킬 | 1개 |
| 규칙 | 1개 |
| 훅 | 2개 |
| **총계** | **12개 파일** |
