import { useQuery } from '@tanstack/react-query';
import type { SummaryData, MarketIndex, TopMover, SectorData } from '@/types/api';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

async function fetchApi<T>(path: string): Promise<T> {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`API 에러 ${res.status}`);
  return res.json();
}

export function useSummary() {
  return useQuery({
    queryKey: ['summary'],
    queryFn: () => fetchApi<SummaryData>('/api/summary'),
    staleTime: 30_000,
  });
}

export function useIndices() {
  return useQuery({
    queryKey: ['stocks', 'indices'],
    queryFn: () => fetchApi<MarketIndex[]>('/api/stocks/indices'),
    staleTime: 30_000,
  });
}

export function useTopMovers() {
  return useQuery({
    queryKey: ['stocks', 'top-movers'],
    queryFn: () => fetchApi<TopMover[]>('/api/stocks/top-movers'),
    staleTime: 30_000,
  });
}

export function useSectors() {
  return useQuery({
    queryKey: ['stocks', 'sectors'],
    queryFn: () => fetchApi<SectorData[]>('/api/stocks/sectors'),
    staleTime: 30_000,
  });
}
