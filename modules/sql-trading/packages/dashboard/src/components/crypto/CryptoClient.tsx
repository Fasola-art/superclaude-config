'use client';

import { MetricCard, CardSkeleton, ChangeIndicator, ConfidenceGauge } from '@/components/ui';
import { useCryptoPrices, useKimchiPremium, useDominance } from '@/hooks';

export function CryptoClient() {
  const { data: prices, isLoading: pricesLoading } = useCryptoPrices();
  const { data: kimchi, isLoading: kimchiLoading } = useKimchiPremium();
  const { data: dominance, isLoading: domLoading } = useDominance();

  return (
    <div className="space-y-6">
      {/* 주요 코인 시세 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">주요 코인</h2>
        {pricesLoading ? (
          <div className="grid grid-cols-2 gap-3">
            {Array.from({ length: 4 }).map((_, i) => <CardSkeleton key={i} />)}
          </div>
        ) : prices && prices.length > 0 ? (
          <div className="grid grid-cols-2 gap-3">
            {prices.slice(0, 6).map((coin) => (
              <MetricCard
                key={coin.symbol}
                label={coin.symbol}
                value={`$${coin.price_usd.toLocaleString()}`}
                change={coin.change_pct_24h}
              />
            ))}
          </div>
        ) : (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4 text-center text-[var(--text-muted)]">
            데이터가 없습니다
          </div>
        )}
      </section>

      {/* BTC 도미넌스 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">BTC 도미넌스</h2>
        {domLoading ? (
          <CardSkeleton />
        ) : dominance ? (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4">
            <div className="mb-3">
              <div className="text-xs text-[var(--text-muted)] mb-1">BTC 도미넌스</div>
              <div className="text-2xl font-bold text-[var(--text)]">
                {dominance.btc_dominance.toFixed(2)}%
              </div>
            </div>
            <ConfidenceGauge value={dominance.btc_dominance / 100} />
            <div className="mt-3 text-xs text-[var(--text-muted)]">
              총 시가총액: ${(dominance.total_market_cap / 1e12).toFixed(2)}T
            </div>
          </div>
        ) : (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4 text-center text-[var(--text-muted)]">
            데이터가 없습니다
          </div>
        )}
      </section>

      {/* 김치프리미엄 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">김치프리미엄</h2>
        {kimchiLoading ? (
          <CardSkeleton />
        ) : kimchi && kimchi.length > 0 ? (
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-[var(--bg)] border-b border-[var(--border)]">
                <tr>
                  <th className="text-left px-3 py-2 text-[var(--text-muted)]">종목</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">글로벌</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">한국</th>
                  <th className="text-right px-3 py-2 text-[var(--text-muted)]">프리미엄</th>
                </tr>
              </thead>
              <tbody>
                {kimchi.map((item, idx) => (
                  <tr key={idx} className="border-b border-[var(--border)] last:border-0">
                    <td className="px-3 py-2 text-[var(--text)]">{item.symbol}</td>
                    <td className="px-3 py-2 text-right font-mono text-[var(--text)]">
                      ${item.global_price_usd.toLocaleString()}
                    </td>
                    <td className="px-3 py-2 text-right font-mono text-[var(--text)]">
                      ₩{item.korea_price_krw.toLocaleString()}
                    </td>
                    <td className="px-3 py-2 text-right">
                      <ChangeIndicator value={item.premium_pct} />
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
