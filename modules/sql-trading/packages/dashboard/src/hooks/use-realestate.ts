import { useQuery } from '@tanstack/react-query';
import type { RealEstateIndex, InterestRate, RegionData } from '@/types/api';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

async function fetchApi<T>(path: string): Promise<T> {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`API 에러 ${res.status}`);
  return res.json();
}

export function useRealEstateIndices() {
  return useQuery({
    queryKey: ['realestate', 'indices'],
    queryFn: () => fetchApi<RealEstateIndex[]>('/api/realestate/indices'),
    staleTime: 30_000,
  });
}

export function useInterestRates() {
  return useQuery({
    queryKey: ['realestate', 'rates'],
    queryFn: () => fetchApi<InterestRate[]>('/api/realestate/rates'),
    staleTime: 30_000,
  });
}

export function useRegions() {
  return useQuery({
    queryKey: ['realestate', 'regions'],
    queryFn: () => fetchApi<RegionData[]>('/api/realestate/regions'),
    staleTime: 30_000,
  });
}
