'use client';

import { useFreight } from '@/hooks';
import { Card, ChangeIndicator } from '@/components/ui';

export function FreightClient() {
  const { data, isLoading, error } = useFreight();

  if (isLoading) return <div className="text-[var(--text-muted)]">로딩 중...</div>;
  if (error) return <div className="text-[var(--down)]">에러 발생</div>;
  if (!data || data.length === 0) return <div className="text-[var(--text-muted)]">데이터 없음</div>;

  const grouped = data.reduce((acc, item) => {
    if (!acc[item.index_name]) acc[item.index_name] = [];
    acc[item.index_name].push(item);
    return acc;
  }, {} as Record<string, typeof data>);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-[var(--text)]">운임 지수</h1>

      {Object.entries(grouped).map(([indexName, items]) => (
        <Card key={indexName}>
          <h2 className="text-lg font-semibold mb-4 text-[var(--text)]">{indexName}</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-[var(--border)]">
                  <th className="text-left p-2 text-[var(--text-muted)]">항로</th>
                  <th className="text-right p-2 text-[var(--text-muted)]">현재가</th>
                  <th className="text-right p-2 text-[var(--text-muted)]">변동률</th>
                  <th className="text-right p-2 text-[var(--text-muted)]">기준일</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item, idx) => (
                  <tr key={idx} className="border-b border-[var(--border)]">
                    <td className="p-2 text-[var(--text)]">{item.route}</td>
                    <td className="p-2 text-right font-mono text-[var(--text)]">
                      ${Number(item.value).toLocaleString()}
                    </td>
                    <td className="p-2 text-right">
                      <ChangeIndicator value={item.change_pct}  />
                    </td>
                    <td className="p-2 text-right text-[var(--text-muted)] text-xs">
                      {new Date(item.date).toLocaleDateString('ko-KR')}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      ))}
    </div>
  );
}
