import { useQuery } from '@tanstack/react-query';
import type {
  TradingSignal,
  StrategyPerf,
  BacktestResult,
  RiskStatus,
  PaperTrade,
} from '@/types/api';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

async function fetchApi<T>(path: string): Promise<T> {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`API 에러 ${res.status}`);
  return res.json();
}

export function useLatestSignals() {
  return useQuery({
    queryKey: ['signals', 'latest'],
    queryFn: () => fetchApi<TradingSignal[]>('/api/signals/latest'),
    staleTime: 30_000,
  });
}

export function useStrategy() {
  return useQuery({
    queryKey: ['signals', 'strategy'],
    queryFn: () => fetchApi<StrategyPerf[]>('/api/signals/strategy'),
    staleTime: 60_000,
  });
}

export function useBacktest() {
  return useQuery({
    queryKey: ['signals', 'backtest'],
    queryFn: () => fetchApi<BacktestResult[]>('/api/signals/backtest'),
    staleTime: 300_000,
  });
}

export function useRiskStatus() {
  return useQuery({
    queryKey: ['signals', 'risk'],
    queryFn: () => fetchApi<RiskStatus>('/api/signals/risk'),
    staleTime: 10_000,
  });
}

export function usePaperTrades() {
  return useQuery({
    queryKey: ['signals', 'paper'],
    queryFn: () => fetchApi<PaperTrade[]>('/api/signals/paper'),
    staleTime: 30_000,
  });
}
