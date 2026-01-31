# Trading Module

> SuperClaude 트레이딩 분석 및 자동화 모듈

---

## 개요

트레이딩 모듈은 금융 시장 분석, 전략 백테스팅, 실시간 알림을 제공합니다.
Mac Studio Ultra M2의 성능을 활용하여 대규모 데이터 처리와 병렬 분석이 가능합니다.

---

## 폴더 구조

```
~/.claude/modules/trading/
├── TRADING.md          # 이 파일 (모듈 가이드)
├── config.json         # 모듈 설정
├── strategies/         # 트레이딩 전략
│   ├── momentum.ts
│   ├── mean-reversion.ts
│   └── custom/
├── indicators/         # 기술적 지표
│   ├── moving-average.ts
│   ├── rsi.ts
│   ├── macd.ts
│   └── custom/
├── backtesting/        # 백테스팅
│   ├── engine.ts
│   ├── results/
│   └── reports/
└── alerts/             # 알림
    ├── rules.json
    └── history/
```

---

## 기능

### 1. 기술적 분석

```yaml
indicators:
  trend:
    - SMA (Simple Moving Average)
    - EMA (Exponential Moving Average)
    - MACD (Moving Average Convergence Divergence)
    - ADX (Average Directional Index)

  momentum:
    - RSI (Relative Strength Index)
    - Stochastic Oscillator
    - Williams %R
    - CCI (Commodity Channel Index)

  volatility:
    - Bollinger Bands
    - ATR (Average True Range)
    - Keltner Channel

  volume:
    - OBV (On Balance Volume)
    - VWAP (Volume Weighted Average Price)
    - Accumulation/Distribution
```

### 2. 트레이딩 전략

```yaml
built_in_strategies:
  momentum:
    description: "추세 추종 전략"
    indicators: [EMA, MACD, RSI]
    signals:
      buy: "EMA 골든크로스 + RSI < 70"
      sell: "EMA 데드크로스 + RSI > 30"

  mean_reversion:
    description: "평균 회귀 전략"
    indicators: [Bollinger Bands, RSI]
    signals:
      buy: "가격 < 하단 밴드 + RSI < 30"
      sell: "가격 > 상단 밴드 + RSI > 70"

  breakout:
    description: "돌파 전략"
    indicators: [ATR, Volume]
    signals:
      buy: "신고가 + 거래량 급증"
      sell: "신저가 + 거래량 급증"
```

### 3. 백테스팅

```yaml
backtesting:
  data_sources:
    - Yahoo Finance
    - Alpha Vantage
    - Binance (암호화폐)

  metrics:
    - Total Return
    - CAGR (Compound Annual Growth Rate)
    - Max Drawdown
    - Sharpe Ratio
    - Sortino Ratio
    - Win Rate
    - Profit Factor

  parallel_execution:
    enabled: true
    max_concurrent: 24  # M2 Ultra 최적화
```

### 4. 알림 시스템

```yaml
alerts:
  channels:
    - Desktop Notification
    - Telegram
    - Discord
    - Email

  trigger_conditions:
    - price_cross_ma: "가격이 이동평균 돌파"
    - rsi_oversold: "RSI 30 이하"
    - rsi_overbought: "RSI 70 이상"
    - volume_spike: "거래량 급증"
    - custom_condition: "사용자 정의 조건"
```

---

## 스킬 명령어

| 명령어 | 설명 |
|--------|------|
| /trade-analyze [종목] | 기술적 분석 실행 |
| /trade-strategy [전략] | 전략 시뮬레이션 |
| /backtest [전략] [기간] | 백테스팅 실행 |
| /trade-alert [조건] | 알림 설정 |

---

## 설정 (config.json)

```json
{
  "dataSource": {
    "provider": "yahoo",
    "apiKey": null
  },
  "defaultTimeframe": "1d",
  "defaultPeriod": "1y",
  "backtesting": {
    "initialCapital": 10000,
    "commission": 0.001,
    "slippage": 0.001
  },
  "alerts": {
    "enabled": true,
    "channels": ["desktop"]
  }
}
```

---

## 사용 예시

```bash
# 삼성전자 기술적 분석
/trade-analyze 005930.KS

# 모멘텀 전략으로 백테스팅
/backtest momentum 2023-01-01:2024-01-01

# RSI 과매도 알림 설정
/trade-alert "RSI < 30" --ticker AAPL --channel telegram
```

---

## 향후 계획

- [ ] 머신러닝 기반 예측 모델
- [ ] 자동 매매 연동 (API)
- [ ] 포트폴리오 최적화
- [ ] 뉴스 센티멘트 통합
