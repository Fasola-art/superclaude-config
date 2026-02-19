/** 외환 API 타입 */

export interface FxRate {
  currency: string;
  rate_usd: number;
  rate_krw: number;
}

export interface FxRatesResponse {
  base: string;
  as_of: string;
  rates: FxRate[];
}

export interface FxCandle {
  t: number;
  o: number;
  h: number;
  l: number;
  c: number;
  v: number;
}

export interface FxFuturesResponse {
  symbol: string;
  source_symbol: string;
  interval: string;
  note: string;
  bars: FxCandle[];
}
