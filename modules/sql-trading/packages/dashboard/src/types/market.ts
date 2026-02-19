/** 시장 관련 타입 */

export interface SummaryData {
  total_records: number;
  buy_signals: number;
  sell_signals: number;
  last_update: string | null;
  server_time: string;
}

export interface Signal {
  symbol: string;
  signal: string;
  confidence: number;
  price: number;
  reason: string;
}

export interface MarketIndex {
  symbol: string;
  price: number;
  change_pct: number;
  volume: number;
  timestamp: string;
  name: string;
}

export interface TopMover {
  symbol: string;
  price: number;
  change_pct: number;
  volume: number;
  name: string;
  sector: string;
}

export interface SectorData {
  sector: string;
  avg_change: number;
  count: number;
}

export interface Stock {
  symbol: string;
  price: number;
  change: number;
  volume: number;
  sector: string | null;
  name: string;
}

export interface StockQuote {
  symbol: string;
  price: number;
  change_pct: number;
  volume: number;
  timestamp: string;
  name: string | null;
}

export interface NewsMetadata {
  positive?: number;
  negative?: number;
  neutral?: number;
  recommendation?: string;
  rec_key?: string;
  original_title?: string;
  original_summary?: string;
}

export interface SummaryDetail {
  table: string;
  label: string;
  count: number;
  latest: string | null;
}

export interface NewsItem {
  title: string;
  summary: string;
  url: string;
  source: string;
  category: string;
  sentiment: number | null;
  symbols: string[] | null;
  timestamp: string;
  metadata: NewsMetadata | null;
}
