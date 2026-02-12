/** 부동산 관련 타입 */

export interface RealEstateIndex {
  region: string;
  index_type: string;
  index_value: number;
  change_pct: number;
  date: string;
}

export interface InterestRate {
  rate_type: string;
  rate_value: number;
  date: string;
  country: string;
}

export interface RegionData {
  region: string;
  sale_index: number;
  jeonse_index: number;
  sale_change: number;
  jeonse_change: number;
}
