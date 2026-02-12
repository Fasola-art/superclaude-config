/** Commodities API 타입 */

export interface FreightIndex {
  index_name: string;
  route: string;
  value: number;
  change_pct: number;
  date: string;
}

export interface OilPrice {
  series_id: string;
  indicator_name: string;
  value: number;
  change_pct: number;
  date: string;
}

export interface LogisticsItem {
  shipment_id: string;
  lat: number | null;
  lng: number | null;
  status: string;
  origin_port: string;
  dest_port: string;
  vessel_name: string;
  cargo_type: string;
  timestamp: string;
  estimated_arrival: string | null;
}

export interface TradeStats {
  period: string;
  reporter_name: string;
  partner_name: string;
  flow_code: string;
  commodity_desc: string;
  trade_value: number;
  net_weight: number;
}
