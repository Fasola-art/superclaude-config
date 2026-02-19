import { useQuery } from '@tanstack/react-query';
import type { FxRatesResponse, FxFuturesResponse } from '@/types/api';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

async function fetchApi<T>(path: string): Promise<T> {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`API 에러 ${res.status}`);
  return res.json();
}

export function useFxRates() {
  return useQuery({
    queryKey: ['fx', 'rates'],
    queryFn: () => fetchApi<FxRatesResponse>('/api/fx/rates'),
    staleTime: 30_000,
  });
}

export function useFxFutures(symbol: string, interval: string) {
  return useQuery({
    queryKey: ['fx', 'futures', symbol, interval],
    queryFn: () =>
      fetchApi<FxFuturesResponse>(`/api/fx/futures?symbol=${symbol}&interval=${interval}`),
    staleTime: 20_000,
  });
}
