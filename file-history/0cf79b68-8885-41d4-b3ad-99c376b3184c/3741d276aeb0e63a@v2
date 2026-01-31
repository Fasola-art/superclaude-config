# Realtime Analysis Module

> SuperClaude 실시간 데이터 분석 모듈

---

## 개요

실시간 분석 모듈은 WebSocket을 통해 실시간 데이터 스트림을 처리하고,
대시보드를 통해 시각화합니다. M2 Ultra의 멀티코어 성능을 활용합니다.

---

## 폴더 구조

```
~/.claude/modules/realtime-analysis/
├── REALTIME.md         # 이 파일 (모듈 가이드)
├── config.json         # 모듈 설정
├── streams/            # 데이터 스트림 정의
│   ├── market.json
│   ├── social.json
│   └── custom/
├── processors/         # 데이터 프로세서
│   ├── aggregator.ts
│   ├── analyzer.ts
│   └── transformer.ts
├── dashboards/         # 대시보드 정의
│   ├── market.json
│   ├── portfolio.json
│   └── custom/
└── websocket/          # WebSocket 서버
    ├── server.ts
    └── handlers/
```

---

## 기능

### 1. 데이터 스트림

```yaml
streams:
  market_data:
    sources:
      - provider: "binance"
        type: "websocket"
        url: "wss://stream.binance.com:9443"
        channels: ["btcusdt@trade", "ethusdt@trade"]

      - provider: "yahoo"
        type: "polling"
        interval: 1000  # ms

    data_types:
      - price
      - volume
      - orderbook

  social_data:
    sources:
      - provider: "twitter"
        type: "streaming"
        keywords: ["$BTC", "$ETH"]

      - provider: "reddit"
        type: "polling"
        subreddits: ["cryptocurrency", "stocks"]

  custom_data:
    sources:
      - name: "internal_api"
        type: "websocket"
        url: "ws://localhost:8080"
```

### 2. 데이터 처리 파이프라인

```yaml
pipeline:
  stages:
    1_ingest:
      - validate_schema
      - parse_timestamp
      - normalize_format

    2_transform:
      - calculate_indicators
      - aggregate_timeframes
      - enrich_metadata

    3_analyze:
      - detect_anomalies
      - calculate_metrics
      - generate_signals

    4_output:
      - store_timeseries
      - broadcast_websocket
      - trigger_alerts

  parallel_processing:
    enabled: true
    workers: 24  # M2 Ultra 코어 수
    buffer_size: 10000
```

### 3. 실시간 지표

```yaml
realtime_metrics:
  price:
    - current_price
    - price_change_1m
    - price_change_5m
    - price_change_1h

  volume:
    - volume_1m
    - volume_5m
    - volume_ratio

  volatility:
    - realtime_atr
    - bollinger_width
    - vix_proxy

  orderbook:
    - bid_ask_spread
    - depth_imbalance
    - large_orders

  sentiment:
    - social_score
    - news_score
    - combined_score
```

### 4. 대시보드

```yaml
dashboards:
  market_overview:
    widgets:
      - type: "price_chart"
        data: "btcusdt"
        timeframe: "1m"

      - type: "orderbook"
        data: "btcusdt"
        depth: 20

      - type: "trades"
        data: "btcusdt"
        limit: 50

      - type: "metrics"
        items: ["volume_1h", "price_change_24h"]

  portfolio:
    widgets:
      - type: "positions"
        columns: ["symbol", "pnl", "size"]

      - type: "performance_chart"
        timeframe: "1d"

      - type: "alerts"
        filter: "active"

  custom:
    layout: "grid"
    widgets: []
```

### 5. 알림 시스템

```yaml
realtime_alerts:
  price_alerts:
    - condition: "price > threshold"
      threshold: 50000
      symbol: "BTCUSDT"

    - condition: "price_change_1m > 1%"
      cooldown: 300  # 초

  volume_alerts:
    - condition: "volume_spike > 300%"
      timeframe: "5m"

  anomaly_alerts:
    - condition: "zscore > 3"
      metric: "price_change"

  channels:
    - desktop
    - telegram
    - sound
```

---

## 스킬 명령어

| 명령어 | 설명 |
|--------|------|
| /stream-start [소스] | 스트림 시작 |
| /stream-stop [소스] | 스트림 중지 |
| /stream-status | 스트림 상태 확인 |
| /dashboard [이름] | 대시보드 열기 |
| /realtime-alert [조건] | 실시간 알림 설정 |

---

## 설정 (config.json)

```json
{
  "server": {
    "port": 8080,
    "maxConnections": 100
  },
  "processing": {
    "workers": 24,
    "bufferSize": 10000,
    "batchInterval": 100
  },
  "storage": {
    "enabled": true,
    "type": "timescaledb",
    "retentionDays": 30
  },
  "alerts": {
    "enabled": true,
    "channels": ["desktop", "sound"]
  }
}
```

---

## 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Binance  │  │  Yahoo   │  │ Twitter  │  │ Custom   │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
└───────┼─────────────┼─────────────┼─────────────┼───────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Stream Manager                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Message Queue (Buffer)                 │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Parallel Processing (24 Workers)                │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ... ┌────┐     │
│  │ W1 │ │ W2 │ │ W3 │ │ W4 │ │ W5 │ │ W6 │     │W24 │     │
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘     └────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Storage    │    │  WebSocket   │    │   Alerts     │
│  TimescaleDB │    │   Server     │    │   System     │
└──────────────┘    └──────────────┘    └──────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  Dashboard   │
                    │   Clients    │
                    └──────────────┘
```

---

## 사용 예시

```bash
# BTC 실시간 스트림 시작
/stream-start binance:btcusdt

# 대시보드 열기
/dashboard market_overview

# 가격 알림 설정
/realtime-alert "BTCUSDT > 50000"

# 스트림 상태 확인
/stream-status
```

---

## 성능 최적화

```yaml
optimization:
  m2_ultra:
    cpu_affinity: true
    numa_aware: true
    memory_mapping: true

  buffering:
    ring_buffer: true
    zero_copy: true

  networking:
    tcp_nodelay: true
    keep_alive: true

  storage:
    batch_insert: true
    compression: "lz4"
```

---

## 향후 계획

- [ ] GPU 가속 분석 (Metal)
- [ ] 분산 처리 지원
- [ ] 머신러닝 실시간 예측
- [ ] Trading/News 모듈 통합
