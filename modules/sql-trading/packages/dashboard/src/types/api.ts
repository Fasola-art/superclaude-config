/** API 응답 타입 정의 */

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

export interface Sector {
  sector: string;
  change: number;
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

export interface Freight {
  index: string;
  route: string;
  value: number;
  change: number;
}

export interface Indicator {
  id: string;
  name: string;
  value: number;
  change: number;
  category: string;
  date: string;
}

export interface Logistics {
  id: string;
  lat: number | null;
  lng: number | null;
  status: string;
  origin: string;
  dest: string;
  vessel: string;
  cargo: string;
  departure: string | null;
  arrival: string | null;
}
