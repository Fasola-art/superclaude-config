# Goal 1: Trading (Side Hustle → Main)

## Required Agents

| Agent | Role |
|-------|------|
| `quant-analyst` | Quant strategy analysis, backtesting design |
| `data-analyst` | Market data analysis, visualization |
| `data-scientist` | ML model (FinBERT, YOLO) design |
| `data-engineer` | Data pipeline construction |
| `performance-profiler` | System performance optimization |

## Recommended Personas

| Persona | Usage |
|---------|-------|
| `analyzer` | Market pattern analysis, root cause tracking |
| `architect` | Trading system architecture design |
| `performance` | Execution speed optimization, latency reduction |
| `risk_analyst` | Risk management strategy |
| `cfo` | Fund management, ROI analysis |

## Usage Examples

```bash
# Start quant analysis
> "str para design trading pipeline.
   Jetson(FinBERT) + RPi5(YOLO) + 4090(Main) integration"

# Backtesting optimization
> "perf analyze backtesting performance.
   Currently takes too long to process 5 years of data"

# Data pipeline
> "data-engineer agent to build real-time news → sentiment analysis pipeline"
```

## Trading System Architecture

```
     News API          Exchange API       Chart Screenshot
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Jetson Orin    │ │  4090 Laptop    │ │  Raspberry Pi   │
│  ────────────── │ │  ────────────── │ │  ────────────── │
│  FinBERT Anal.  │ │  Real-time Price│ │  YOLO Pattern   │
│  Sentiment Score│ │  Order Execution│ │  Candle/Pattern │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                   ┌─────────────────┐
                   │   Integrated    │
                   │     Signal      │
                   │  (Weighted)     │
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
         Telegram      Auto Order      Dashboard
          Alert        Execution      (Tab/Phone)
```

---

**Related**: [development.md](development.md)
