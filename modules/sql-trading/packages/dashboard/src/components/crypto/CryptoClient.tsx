'use client';

import { MetricCard, CardSkeleton, ChangeIndicator, ConfidenceGauge, Card } from '@/components/ui';
import { useCryptoPrices, useKimchiPremium, useDominance, useStockQuotes } from '@/hooks';

export function CryptoClient() {
  const { data: prices, isLoading: pricesLoading } = useCryptoPrices();
  const { data: kimchi, isLoading: kimchiLoading } = useKimchiPremium();
  const { data: dominance, isLoading: domLoading } = useDominance();
  const { data: relatedStocks } = useStockQuotes(['BMNR', 'DFDV']);

  const excludedCoins = new Set(['ADA', 'AVAX']);
  const preferredOrder = ['BTC', 'XRP', 'SOL', 'ETH', 'BNB', 'DOGE'];
  const coins = (prices || []).filter((c) => !excludedCoins.has(c.symbol));
  const orderedCoins = [
    ...preferredOrder
      .map((sym) => coins.find((c) => c.symbol === sym))
      .filter((c): c is NonNullable<typeof c> => Boolean(c)),
    ...coins.filter((c) => !preferredOrder.includes(c.symbol)),
  ];

  return (
    <div className="space-y-6">
      {/* 주요 코인 시세 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">주요 코인</h2>
        {pricesLoading ? (
          <div className="grid grid-cols-2 gap-3">
            {Array.from({ length: 4 }).map((_, i) => <CardSkeleton key={i} />)}
          </div>
        ) : orderedCoins.length > 0 ? (
          <div className="grid grid-cols-2 gap-3">
            {orderedCoins.map((coin) => (
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

      {/* 연관 주식 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">연관 주식</h2>
        {!relatedStocks || relatedStocks.length === 0 ? (
          <Card>
            <div className="text-[var(--text-muted)]">데이터가 없습니다</div>
          </Card>
        ) : (
          <div className="grid grid-cols-2 gap-3">
            {relatedStocks.map((stock) => (
              <MetricCard
                key={stock.symbol}
                label={stock.symbol}
                value={`$${stock.price.toFixed(2)}`}
                change={stock.change_pct}
              />
            ))}
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
