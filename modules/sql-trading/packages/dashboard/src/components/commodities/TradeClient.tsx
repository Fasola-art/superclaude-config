'use client';

import { useTradeStats } from '@/hooks';
import { Card } from '@/components/ui';

export function TradeClient() {
  const { data, isLoading, error } = useTradeStats();

  if (isLoading) return <div className="text-[var(--text-muted)]">로딩 중...</div>;
  if (error) return <div className="text-[var(--down)]">에러 발생</div>;
  if (!data || data.length === 0) return <div className="text-[var(--text-muted)]">데이터 없음</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-[var(--text)]">무역 통계</h1>

      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[var(--border)]">
                <th className="text-left p-2 text-[var(--text-muted)]">기간</th>
                <th className="text-left p-2 text-[var(--text-muted)]">수출국</th>
                <th className="text-left p-2 text-[var(--text-muted)]">수입국</th>
                <th className="text-left p-2 text-[var(--text-muted)]">품목</th>
                <th className="text-right p-2 text-[var(--text-muted)]">무역액 ($)</th>
                <th className="text-right p-2 text-[var(--text-muted)]">순중량 (kg)</th>
                <th className="text-center p-2 text-[var(--text-muted)]">구분</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item, idx) => (
                <tr key={idx} className="border-b border-[var(--border)]">
                  <td className="p-2 text-[var(--text)]">{item.period}</td>
                  <td className="p-2 text-[var(--text)]">{item.reporter_name}</td>
                  <td className="p-2 text-[var(--text)]">{item.partner_name}</td>
                  <td className="p-2 text-[var(--text-muted)] max-w-xs truncate">
                    {item.commodity_desc}
                  </td>
                  <td className="p-2 text-right font-mono text-[var(--text)]">
                    {item.trade_value != null ? Number(item.trade_value).toLocaleString() : '-'}
                  </td>
                  <td className="p-2 text-right font-mono text-[var(--text-muted)]">
                    {item.net_weight != null ? Number(item.net_weight).toLocaleString() : '-'}
                  </td>
                  <td className="p-2 text-center text-xs text-[var(--text-muted)]">
                    {item.flow_code}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
