import { useQuery } from '@tanstack/react-query';
import type { FreightIndex, OilPrice, LogisticsItem, TradeStats, NewsItem } from '@/types/api';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

async function fetchApi<T>(path: string): Promise<T> {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`API 에러 ${res.status}`);
  return res.json();
}

export function useFreight() {
  return useQuery({
    queryKey: ['commodities', 'freight'],
    queryFn: () => fetchApi<FreightIndex[]>('/api/commodities/freight'),
    staleTime: 60_000,
  });
}

export function useOilPrices() {
  return useQuery({
    queryKey: ['commodities', 'oil'],
    queryFn: () => fetchApi<OilPrice[]>('/api/commodities/oil'),
    staleTime: 60_000,
  });
}

export function useLogistics() {
  return useQuery({
    queryKey: ['commodities', 'logistics'],
    queryFn: () => fetchApi<LogisticsItem[]>('/api/commodities/logistics'),
    staleTime: 30_000,
  });
}

export function useTradeStats() {
  return useQuery({
    queryKey: ['commodities', 'trade'],
    queryFn: () => fetchApi<TradeStats[]>('/api/commodities/trade'),
    staleTime: 300_000,
  });
}

export function useNews(category: string = 'all') {
  const path = category === 'all' ? '/api/news/' : `/api/news/?category=${category}`;
  return useQuery({
    queryKey: ['news', category],
    queryFn: () => fetchApi<NewsItem[]>(path),
    staleTime: 60_000,
  });
}
