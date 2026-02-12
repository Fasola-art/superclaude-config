import { useQuery } from '@tanstack/react-query';
import type { CryptoPrice, KimchiPremium, CryptoDominance } from '@/types/api';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

async function fetchApi<T>(path: string): Promise<T> {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`API 에러 ${res.status}`);
  return res.json();
}

export function useCryptoPrices() {
  return useQuery({
    queryKey: ['crypto', 'prices'],
    queryFn: () => fetchApi<CryptoPrice[]>('/api/crypto/prices'),
    staleTime: 30_000,
  });
}

export function useKimchiPremium() {
  return useQuery({
    queryKey: ['crypto', 'kimchi'],
    queryFn: () => fetchApi<KimchiPremium[]>('/api/crypto/kimchi'),
    staleTime: 30_000,
  });
}

export function useDominance() {
  return useQuery({
    queryKey: ['crypto', 'dominance'],
    queryFn: () => fetchApi<CryptoDominance>('/api/crypto/dominance'),
    staleTime: 30_000,
  });
}
