/** 암호화폐 관련 타입 */

export interface CryptoPrice {
  symbol: string;
  price_usd: number;
  price_krw: number;
  change_pct_24h: number;
  volume_24h: number;
  market_cap: number;
  timestamp: string;
}

export interface KimchiPremium {
  symbol: string;
  global_price_usd: number;
  korea_price_krw: number;
  exchange_rate: number;
  premium_pct: number;
  timestamp: string;
}

export interface CryptoDominance {
  btc_dominance: number;
  total_market_cap: number;
}
