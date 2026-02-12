'use client';

import { Badge } from '@/components/ui';
import type { PaperTrade } from '@/types/api';

interface TradeTableProps {
  trades: PaperTrade[];
}

export function TradeTable({ trades }: TradeTableProps) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead className="border-b border-border">
          <tr>
            <th className="text-left p-2">시간</th>
            <th className="text-left p-2">심볼</th>
            <th className="text-left p-2">방향</th>
            <th className="text-right p-2">수량</th>
            <th className="text-right p-2">진입가</th>
            <th className="text-right p-2">청산가</th>
            <th className="text-right p-2">손익</th>
            <th className="text-right p-2">수익률</th>
            <th className="text-left p-2">전략</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((trade, idx) => (
            <tr key={idx} className="border-b border-border/50">
              <td className="p-2 text-muted text-xs">{new Date(trade.timestamp).toLocaleString()}</td>
              <td className="p-2 font-mono font-semibold">{trade.symbol}</td>
              <td className="p-2">
                <Badge variant={trade.side === 'BUY' ? 'up' : 'down'}>{trade.side}</Badge>
              </td>
              <td className="p-2 text-right font-mono">{trade.quantity}</td>
              <td className="p-2 text-right font-mono">${trade.entry_price.toFixed(2)}</td>
              <td className="p-2 text-right font-mono">
                {trade.exit_price ? `$${trade.exit_price.toFixed(2)}` : '-'}
              </td>
              <td className="p-2 text-right font-mono">
                {trade.pnl !== null ? (
                  <span className={trade.pnl >= 0 ? 'text-up' : 'text-down'}>
                    {trade.pnl > 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                  </span>
                ) : (
                  '-'
                )}
              </td>
              <td className="p-2 text-right font-mono">
                {trade.pnl_pct !== null ? (
                  <span className={trade.pnl_pct >= 0 ? 'text-up' : 'text-down'}>
                    {trade.pnl_pct > 0 ? '+' : ''}
                    {trade.pnl_pct.toFixed(2)}%
                  </span>
                ) : (
                  '-'
                )}
              </td>
              <td className="p-2 text-muted text-xs">{trade.strategy}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
