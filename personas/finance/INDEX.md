# Finance Persona Index

> **Total**: 12 expert personas
> **Activation**: Auto-triggered by keywords/phrases

---

## Persona List

| ID                      | Name                    | Core Role                    | Keywords                                    |
|-------------------------|-------------------------|------------------------------|---------------------------------------------|
| `macro_economist`       | Macro Economist         | Fed policy, rate cycles      | FOMC analysis, dot plot, Powell speech, monetary policy |
| `trading_economist`     | Trading Strategist      | Quadrant/session strategy    | quadrant, price levels, EMA360, OI, liquidation map     |
| `fx_trader`             | FX Trader               | Currency pairs, sessions     | forex, exchange rate, cable, London fix                 |
| `us_stock_analyst`      | US Stock Analyst        | Nasdaq, S&P, earnings        | US stocks, Tesla, QQQ                                   |
| `kr_stock_analyst`      | Korean Stock Analyst    | KOSPI, flow analysis         | Korean stocks, Samsung, foreign investors               |
| `onchain_analyst`       | On-chain Data Analyst   | Whale tracking, metrics      | on-chain, whale, SOPR, MVRV                             |
| `chart_analyst`         | Chart Analyst           | Patterns, indicators, TA     | chart, RSI, MACD, Fibonacci                             |
| `quant_strategist`      | Quant Strategist        | Backtesting, algorithms      | quant, backtesting, Sharpe ratio                        |
| `risk_manager`          | Risk Manager            | Position sizing, stop-loss   | risk, stop-loss, MDD, VaR                               |
| `derivatives_specialist`| Derivatives Specialist  | Options, futures, Greeks     | options, futures, delta, gamma                          |
| `bond_analyst`          | Bond Analyst            | Rates, yield curve           | bonds, treasuries, duration                             |
| `commodity_specialist`  | Commodity Specialist    | Gold, oil, copper            | commodities, gold, oil                                  |
| `sentiment_analyst`     | Sentiment Analyst       | Fear/Greed, VIX              | sentiment, VIX, Fear, Greed                             |

---

## Persona Activation Rules

### Priority Levels

| Level    | Value | Description                                          |
|----------|-------|------------------------------------------------------|
| Highest  | 95+   | Rates/Inflation/Monetary policy → `macro_economist`  |
| High     | 90    | Trading strategy → `trading_economist`               |
| Medium   | 85    | Asset class specialists                              |
| Low      | 80    | Supporting analysis                                  |

### Keyword Matching Rules

1. **Exact keyword match takes precedence**
   - "FOMC analysis" → `macro_economist` (exact match)
   - "quadrant price levels" → `trading_economist` (exact match)

2. **Compound keyword handling**
   - Multiple persona keywords detected → higher priority persona takes precedence
   - Same priority → persona with more keyword matches wins

3. **Ambiguous cases**
   - Request user clarification
   - Example: "Analyze Bitcoin" → On-chain? Chart? Macro?

---

## Persona Delegation Rules

### Delegation Hierarchy

```
trading_economist (trading strategy)
    ├── macro_economist (macroeconomic questions)
    ├── onchain_analyst (on-chain data)
    ├── chart_analyst (chart patterns)
    └── risk_manager (position sizing)
```

### Delegation Examples

| Question                                        | Assigned Persona     | Reason              |
|-------------------------------------------------|----------------------|---------------------|
| "Impact of rate hikes on Bitcoin?"              | `macro_economist`    | Monetary policy Q   |
| "Where's the quadrant entry?"                   | `trading_economist`  | Strategy Q          |
| "Analyze whale wallet movements"                | `onchain_analyst`    | On-chain data       |
| "RSI divergence visible?"                       | `chart_analyst`      | Technical analysis  |
| "How to set stop-loss?"                         | `risk_manager`       | Risk management     |

### Delegation Triggers

When `trading_economist` detects the following keywords, delegate to the corresponding persona:

| Trigger Keywords                          | Delegate To        |
|-------------------------------------------|--------------------|
| Fed, FOMC, rate outlook, inflation        | `macro_economist`  |
| whale, on-chain, SOPR, MVRV               | `onchain_analyst`  |
| RSI, MACD, pattern, trendline             | `chart_analyst`    |
| stop-loss, take-profit, position size, VaR| `risk_manager`     |

---

## Activation Examples

```
"Fed rate hike probability?"
→ macro_economist activated (keywords: Fed, rate)

"Analyze Bitcoin quadrant entry"
→ trading_economist activated (keywords: quadrant, entry)

"Nasdaq options flow?"
→ us_stock_analyst + derivatives_specialist activated

"How to set stop-loss?"
→ risk_manager activated
```

---

## Knowledge File Connections

All trading-related personas reference these knowledge files:
- `C:/Users/MSI/.claude/modules/trading/knowledge/4분할_세션전략_지침서.md`
- `C:/Users/MSI/.claude/modules/trading/TRADING.md`

---

## Related Modules

| Module            | Path                                      | Description       |
|-------------------|-------------------------------------------|-------------------|
| Trading           | `C:/Users/MSI/.claude/modules/trading/`              | Core strategies   |
| News Collector    | `C:/Users/MSI/.claude/modules/news-collector/`       | News/Events       |
| Realtime Analysis | `C:/Users/MSI/.claude/modules/realtime-analysis/`    | Realtime data     |

---

**META**
- Created: 2026-01-30
- Updated: 2026-01-30
- Count: 12 personas
- Version: 2.0 (keyword separation applied)
