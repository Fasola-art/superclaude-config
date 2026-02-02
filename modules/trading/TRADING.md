# Trading Module

> SuperClaude trading analysis and automation module

---

## Overview

Trading module provides financial market analysis, strategy backtesting, and real-time alerts.
Leverages Mac Studio Ultra M2 performance for large-scale data processing and parallel analysis.

---

## Folder Structure

```
~/.claude/modules/trading/
├── TRADING.md          # This file (module guide)
├── config.json         # Module configuration
├── strategies/         # Trading strategies
│   ├── momentum.ts
│   ├── mean-reversion.ts
│   └── custom/
├── indicators/         # Technical indicators
│   ├── moving-average.ts
│   ├── rsi.ts
│   ├── macd.ts
│   └── custom/
├── backtesting/        # Backtesting
│   ├── engine.ts
│   ├── results/
│   └── reports/
└── alerts/             # Alerts
    ├── rules.json
    └── history/
```

---

## Features

### 1. Technical Analysis

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

### 2. Trading Strategies

```yaml
built_in_strategies:
  momentum:
    description: "Trend following strategy"
    indicators: [EMA, MACD, RSI]
    signals:
      buy: "EMA golden cross + RSI < 70"
      sell: "EMA death cross + RSI > 30"

  mean_reversion:
    description: "Mean reversion strategy"
    indicators: [Bollinger Bands, RSI]
    signals:
      buy: "Price < lower band + RSI < 30"
      sell: "Price > upper band + RSI > 70"

  breakout:
    description: "Breakout strategy"
    indicators: [ATR, Volume]
    signals:
      buy: "New high + volume spike"
      sell: "New low + volume spike"
```

### 3. Backtesting

```yaml
backtesting:
  data_sources:
    - Yahoo Finance
    - Alpha Vantage
    - Binance (cryptocurrency)

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
    max_concurrent: 24  # M2 Ultra optimized
```

### 4. Alert System

```yaml
alerts:
  channels:
    - Desktop Notification
    - Telegram
    - Discord
    - Email

  trigger_conditions:
    - price_cross_ma: "Price crosses moving average"
    - rsi_oversold: "RSI below 30"
    - rsi_overbought: "RSI above 70"
    - volume_spike: "Volume spike detected"
    - custom_condition: "User-defined condition"
```

---

## Skill Commands

| Command | Description |
|---------|-------------|
| /trade-analyze [symbol] | Run technical analysis |
| /trade-strategy [strategy] | Run strategy simulation |
| /backtest [strategy] [period] | Run backtesting |
| /trade-alert [condition] | Set up alerts |

---

## Configuration (config.json)

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

## Usage Examples

```bash
# Samsung Electronics technical analysis
/trade-analyze 005930.KS

# Backtest with momentum strategy
/backtest momentum 2023-01-01:2024-01-01

# Set RSI oversold alert
/trade-alert "RSI < 30" --ticker AAPL --channel telegram
```

---

## Roadmap

- [ ] Machine learning prediction models
- [ ] Automated trading API integration
- [ ] Portfolio optimization
- [ ] News sentiment integration
