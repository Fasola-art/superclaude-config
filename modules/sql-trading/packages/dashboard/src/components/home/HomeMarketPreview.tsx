'use client';

import { MetricCard, CardSkeleton } from '@/components/ui';
import { useIndices, useCryptoPrices, useStockQuotes } from '@/hooks';
import { SectionHeader } from './SectionHeader';

/** 홈 - 주식 + 코인 미리보기 */
export function HomeMarketPreview() {
  const { data: indices, isLoading: il } = useIndices();
  const { data: crypto, isLoading: cl } = useCryptoPrices();
  const { data: relatedStocks } = useStockQuotes(['BMNR', 'DFDV']);

  /* 주식: S&P 500, 나스닥, 다우 (DB 심볼 기준) */
  const stockSymbols = ['^GSPC', '^IXIC', '^DJI'];
  const keyStocks = indices?.filter((i) => stockSymbols.includes(i.symbol)) || [];

  /* 코인: ADA/AVAX 제외, BTC/XRP/SOL 우선 */
  const excludedCoins = new Set(['ADA', 'AVAX']);
  const preferredOrder = ['BTC', 'XRP', 'SOL', 'ETH', 'BNB', 'DOGE'];
  const coins = (crypto || []).filter((c) => !excludedCoins.has(c.symbol));
  const keyCoins = [
    ...preferredOrder
      .map((sym) => coins.find((c) => c.symbol === sym))
      .filter((c): c is NonNullable<typeof c> => Boolean(c)),
    ...coins.filter((c) => !preferredOrder.includes(c.symbol)),
  ];

  return (
    <>
      {/* 코인 */}
      <section>
        <SectionHeader title="암호화폐" href="/crypto" />
        {cl ? (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            <CardSkeleton /><CardSkeleton />
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {keyCoins.map((coin) => (
              <MetricCard
                key={coin.symbol}
                label={coin.symbol}
                value={coin.price_usd?.toLocaleString() ?? '-'}
                change={coin.change_pct_24h}
                prefix="$"
              />
            ))}
          </div>
        )}
        {relatedStocks && relatedStocks.length > 0 && (
          <div className="mt-3 space-y-2">
            {relatedStocks.map((stock) => (
              <div key={stock.symbol} className="flex items-center justify-between bg-[var(--bg-card)] border border-[var(--border)] rounded-lg px-3 py-2">
                <div className="flex items-center gap-2">
                  <span className="font-mono font-semibold text-sm">{stock.symbol}</span>
                  <span className="text-xs text-[var(--text-muted)]">{stock.name || ''}</span>
                </div>
                <div className="flex items-center gap-2 text-xs">
                  <span className="font-mono text-[var(--text)]">${stock.price.toFixed(2)}</span>
                  <span className={stock.change_pct >= 0 ? 'text-[var(--up)]' : 'text-[var(--down)]'}>
                    {stock.change_pct > 0 ? '+' : ''}{stock.change_pct.toFixed(2)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* 주식 */}
      <section>
        <SectionHeader title="주식 시장" href="/stocks" />
        {il ? (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {Array.from({ length: 3 }).map((_, i) => <CardSkeleton key={i} />)}
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {keyStocks.map((idx) => (
              <MetricCard key={idx.symbol} label={idx.name} value={idx.price.toLocaleString()} change={idx.change_pct} />
            ))}
          </div>
        )}
      </section>
    </>
  );
}
