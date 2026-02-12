'use client';

import { MetricCard, CardSkeleton, ChangeIndicator } from '@/components/ui';
import { useIndices, useTopMovers, useSectors } from '@/hooks';

export function StocksClient() {
  const { data: indices, isLoading: indicesLoading } = useIndices();
  const { data: movers, isLoading: moversLoading } = useTopMovers();
  const { data: sectors, isLoading: sectorsLoading } = useSectors();

  return (
    <div className="space-y-6">
      {/* 글로벌 인덱스 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">글로벌 인덱스</h2>
        {indicesLoading ? (
          <div className="grid grid-cols-2 gap-3">
            {Array.from({ length: 8 }).map((_, i) => <CardSkeleton key={i} />)}
          </div>
        ) : indices && indices.length > 0 ? (
          <div className="grid grid-cols-2 gap-3">
            {indices.map((idx) => (
              <MetricCard
                key={idx.symbol}
                label={idx.name}
                value={idx.price.toLocaleString()}
                change={idx.change_pct}
                prefix={['BTC', 'ETH'].includes(idx.symbol) ? '$' : undefined}
              />
            ))}
          </div>
        ) : (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4 text-center text-[var(--text-muted)]">
            데이터가 없습니다
          </div>
        )}
      </section>

      {/* 등락 상위 종목 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">등락 상위</h2>
        {moversLoading ? (
          <CardSkeleton />
        ) : movers && movers.length > 0 ? (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-[var(--bg)] border-b border-[var(--border)]">
                <tr>
                  <th className="text-left px-3 py-2 text-[var(--text-muted)]">종목</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">가격</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">변동</th>
                </tr>
              </thead>
              <tbody>
                {movers.map((mover, idx) => (
                  <tr key={idx} className="border-b border-[var(--border)] last:border-0">
                    <td className="px-3 py-2">
                      <div className="text-[var(--text)]">{mover.name}</div>
                      <div className="text-xs text-[var(--text-muted)]">{mover.sector}</div>
                    </td>
                    <td className="px-3 py-2 text-right font-mono text-[var(--text)]">
                      {mover.price.toLocaleString()}
                    </td>
                    <td className="px-3 py-2 text-right">
                      <ChangeIndicator value={mover.change_pct} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4 text-center text-[var(--text-muted)]">
            데이터가 없습니다
          </div>
        )}
      </section>

      {/* 섹터별 현황 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">섹터별 현황</h2>
        {sectorsLoading ? (
          <CardSkeleton />
        ) : sectors && sectors.length > 0 ? (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-[var(--bg)] border-b border-[var(--border)]">
                <tr>
                  <th className="text-left px-3 py-2 text-[var(--text-muted)]">섹터</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">평균변동</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">종목수</th>
                </tr>
              </thead>
              <tbody>
                {sectors.map((sector, idx) => (
                  <tr key={idx} className="border-b border-[var(--border)] last:border-0">
                    <td className="px-3 py-2 text-[var(--text)]">{sector.sector}</td>
                    <td className="px-3 py-2 text-right">
                      <ChangeIndicator value={sector.avg_change} />
                    </td>
                    <td className="px-3 py-2 text-right font-mono text-[var(--text)]">
                      {sector.count}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4 text-center text-[var(--text-muted)]">
            데이터가 없습니다
          </div>
        )}
      </section>
    </div>
  );
}
