/** Trading Signals 타입 정의 */

export interface TradingSignal {
  symbol: string;
  signal_type: 'BUY' | 'STRONG_BUY' | 'SELL' | 'STRONG_SELL' | 'HOLD';
  confidence: number;
  price: number;
  target_price: number | null;
  stop_loss: number | null;
  strategy: string;
  reason: string;
  timestamp: string;
}

export interface StrategyPerf {
  strategy: string;
  total: number;
  buys: number;
  sells: number;
  avg_confidence: number;
}

export interface BacktestResult {
  strategy: string;
  start_date: string;
  end_date: string;
  total_trades: number;
  win_rate: number;
  sharpe_ratio: number;
  max_drawdown: number;
  total_return: number;
}

export interface RiskEvent {
  level: 'WARNING' | 'CRITICAL' | 'EMERGENCY';
  event_type: string;
  description: string;
  daily_pnl_pct: number | null;
  total_drawdown_pct: number | null;
  timestamp: string;
}

export interface RiskStatus {
  current: RiskEvent | null;
  recent_events: RiskEvent[];
}

export interface PaperTrade {
  symbol: string;
  side: 'BUY' | 'SELL';
  quantity: number;
  entry_price: number;
  exit_price: number | null;
  pnl: number | null;
  pnl_pct: number | null;
  strategy: string;
  timestamp: string;
}

export interface DailyPerformanceItem {
  symbol: string;
  signal_type: 'BUY' | 'SELL' | 'STRONG_BUY' | 'STRONG_SELL';
  entry_time: string;
  entry_price: number;
  exit_time: string;
  exit_price: number;
  pct_change: number;
  outcome: 'win' | 'loss' | 'flat';
}

export interface DailyPerformanceSummary {
  total: number;
  wins: number;
  losses: number;
  flats: number;
  win_rate: number;
}

export interface DailyPerformanceWindow {
  start_kst: string;
  end_kst: string;
}

export interface DailyPerformance {
  window: DailyPerformanceWindow;
  summary: DailyPerformanceSummary;
  items: DailyPerformanceItem[];
}

export interface AgentConfidence {
  news: number;
  macro: number;
  tech: number;
  signal: number;
}

export interface FinalScore {
  score: number;
  action: 'BUY' | 'SELL' | 'HOLD';
  confidence: AgentConfidence;
}
