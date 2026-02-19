'use client';

import { useGetSignalsApiSignalsGet, useGetStocksApiStocksGet } from '@/api/endpoints/default/default';
import type { Signal, Stock } from '@/types/api';

// ============================================
// SignalsTable
// ============================================
const signalColors: Record<string, string> = {
  BUY: 'text-green-400 bg-green-500/20',
  STRONG_BUY: 'text-green-300 bg-green-500/30',
  SELL: 'text-red-400 bg-red-500/20',
  STRONG_SELL: 'text-red-300 bg-red-500/30',
  OVERSOLD: 'text-yellow-400 bg-yellow-500/20',
};

export function SignalsTable() {
  const { data, isLoading } = useGetSignalsApiSignalsGet();
  const signals = (data?.data || []) as Signal[];

  if (isLoading) return <p className="text-gray-400">로딩 중...</p>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-700">
            <th className="text-left py-2 px-2">심볼</th>
            <th className="text-left py-2 px-2">신호</th>
            <th className="text-right py-2 px-2">신뢰도</th>
            <th className="text-right py-2 px-2">가격</th>
          </tr>
        </thead>
        <tbody>
          {signals.map((s, i) => (
            <tr key={i} className="border-b border-gray-800 hover:bg-gray-800/50">
              <td className="py-2 px-2 font-mono">{s.symbol}</td>
              <td className="py-2 px-2">
                <span className={`px-2 py-1 rounded text-xs ${signalColors[s.signal] || ''}`}>
                  {s.signal}
                </span>
              </td>
              <td className="py-2 px-2 text-right">{s.confidence}%</td>
              <td className="py-2 px-2 text-right font-mono">${s.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {signals.length === 0 && <p className="text-center text-gray-500 py-4">신호 없음</p>}
    </div>
  );
}

// ============================================
// StocksTable
// ============================================
export function StocksTable() {
  const { data, isLoading } = useGetStocksApiStocksGet();
  const stocks = (data?.data || []) as Stock[];

  if (isLoading) return <p className="text-gray-400">로딩 중...</p>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-700">
            <th className="text-left py-2 px-2">심볼</th>
            <th className="text-left py-2 px-2">이름</th>
            <th className="text-left py-2 px-2">섹터</th>
            <th className="text-right py-2 px-2">가격</th>
            <th className="text-right py-2 px-2">변동</th>
            <th className="text-right py-2 px-2">거래량</th>
          </tr>
        </thead>
        <tbody>
          {stocks.slice(0, 20).map((s) => (
            <tr key={s.symbol} className="border-b border-gray-800 hover:bg-gray-800/50">
              <td className="py-2 px-2 font-mono font-bold">{s.symbol}</td>
              <td className="py-2 px-2 text-gray-400 truncate max-w-[150px]">{s.name}</td>
              <td className="py-2 px-2 text-xs text-gray-500">{s.sector || '-'}</td>
              <td className="py-2 px-2 text-right font-mono">${Number(s.price).toFixed(2)}</td>
              <td className={`py-2 px-2 text-right ${Number(s.change) >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                {Number(s.change) > 0 ? '+' : ''}{Number(s.change).toFixed(2)}%
              </td>
              <td className="py-2 px-2 text-right text-gray-400">{Number(s.volume).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {stocks.length === 0 && <p className="text-center text-gray-500 py-4">종목 데이터 없음</p>}
    </div>
  );
}
