/** 레거시/기타 타입 */

export interface Sector {
  sector: string;
  change: number;
  count: number;
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
