'use client';

import { useGetSectorsApiSectorsGet } from '@/api/endpoints/default/default';
import type { Sector } from '@/types/api';

// ============================================
// SummaryCard
// ============================================
interface SummaryCardProps {
  title: string;
  value: string | number;
  color: 'blue' | 'green' | 'red' | 'purple';
}

const colorClasses = {
  blue: 'bg-blue-500/20 border-blue-500 text-blue-400',
  green: 'bg-green-500/20 border-green-500 text-green-400',
  red: 'bg-red-500/20 border-red-500 text-red-400',
  purple: 'bg-purple-500/20 border-purple-500 text-purple-400',
};

export function SummaryCard({ title, value, color }: SummaryCardProps) {
  return (
    <div className={`rounded-lg border p-4 ${colorClasses[color]}`}>
      <h3 className="text-sm font-medium text-gray-400">{title}</h3>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  );
}

// ============================================
// SectorsChart
// ============================================
export function SectorsChart() {
  const { data, isLoading } = useGetSectorsApiSectorsGet();
  const sectors = (data?.data || []) as Sector[];

  if (isLoading) return <p className="text-gray-400">로딩 중...</p>;

  const maxChange = Math.max(...sectors.map((s) => Math.abs(s.change)), 1);

  return (
    <div className="space-y-3">
      {sectors.map((s) => (
        <div key={s.sector} className="flex items-center gap-3">
          <span className="w-24 text-sm truncate">{s.sector}</span>
          <div className="flex-1 h-6 bg-gray-800 rounded overflow-hidden relative">
            <div
              className={`h-full ${s.change >= 0 ? 'bg-green-500' : 'bg-red-500'}`}
              style={{ width: `${Math.abs(s.change) / maxChange * 100}%` }}
            />
            <span className="absolute inset-0 flex items-center justify-end pr-2 text-xs">
              {s.change > 0 ? '+' : ''}{s.change.toFixed(2)}%
            </span>
          </div>
          <span className="w-8 text-xs text-gray-500">{s.count}</span>
        </div>
      ))}
      {sectors.length === 0 && <p className="text-center text-gray-500">섹터 데이터 없음</p>}
    </div>
  );
}
