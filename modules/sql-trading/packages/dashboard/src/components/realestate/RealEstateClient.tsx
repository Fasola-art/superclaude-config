'use client';

import { MetricCard, CardSkeleton, ChangeIndicator } from '@/components/ui';
import { useRealEstateIndices, useInterestRates, useRegions } from '@/hooks';

export function RealEstateClient() {
  const { data: indices, isLoading: indicesLoading } = useRealEstateIndices();
  const { data: rates, isLoading: ratesLoading } = useInterestRates();
  const { data: regions, isLoading: regionsLoading } = useRegions();

  return (
    <div className="space-y-6">
      {/* 매매/전세 지수 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">주요 지수</h2>
        {indicesLoading ? (
          <div className="grid grid-cols-2 gap-3">
            {Array.from({ length: 4 }).map((_, i) => <CardSkeleton key={i} />)}
          </div>
        ) : indices && indices.length > 0 ? (
          <div className="grid grid-cols-2 gap-3">
            {indices.slice(0, 6).map((idx, i) => (
              <MetricCard
                key={i}
                label={`${idx.region} ${idx.index_type}`}
                value={idx.index_value.toFixed(2)}
                change={idx.change_pct}
              />
            ))}
          </div>
        ) : (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4 text-center text-[var(--text-muted)]">
            데이터가 없습니다
          </div>
        )}
      </section>

      {/* 금리 현황 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">금리 현황</h2>
        {ratesLoading ? (
          <CardSkeleton />
        ) : rates && rates.length > 0 ? (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-[var(--bg)] border-b border-[var(--border)]">
                <tr>
                  <th className="text-left px-3 py-2 text-[var(--text-muted)]">종류</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">금리</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">국가</th>
                </tr>
              </thead>
              <tbody>
                {rates.map((rate, idx) => (
                  <tr key={idx} className="border-b border-[var(--border)] last:border-0">
                    <td className="px-3 py-2 text-[var(--text)]">{rate.rate_type}</td>
                    <td className="px-3 py-2 text-right font-mono text-[var(--text)]">
                      {rate.rate_value.toFixed(2)}%
                    </td>
                    <td className="px-3 py-2 text-right text-[var(--text-muted)]">
                      {rate.country}
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

      {/* 지역별 시세 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">지역별 시세</h2>
        {regionsLoading ? (
          <CardSkeleton />
        ) : regions && regions.length > 0 ? (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-[var(--bg)] border-b border-[var(--border)]">
                <tr>
                  <th className="text-left px-3 py-2 text-[var(--text-muted)]">지역</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">매매</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">전세</th>
                </tr>
              </thead>
              <tbody>
                {regions.map((region, idx) => (
                  <tr key={idx} className="border-b border-[var(--border)] last:border-0">
                    <td className="px-3 py-2 text-[var(--text)]">{region.region}</td>
                    <td className="px-3 py-2 text-right">
                      <div className="font-mono text-[var(--text)]">{region.sale_index.toFixed(2)}</div>
                      <ChangeIndicator value={region.sale_change} size="sm" />
                    </td>
                    <td className="px-3 py-2 text-right">
                      <div className="font-mono text-[var(--text)]">{region.jeonse_index.toFixed(2)}</div>
                      <ChangeIndicator value={region.jeonse_change} size="sm" />
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
