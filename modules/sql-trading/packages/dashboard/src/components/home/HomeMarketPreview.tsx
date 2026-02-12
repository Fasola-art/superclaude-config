'use client';

import { MetricCard, CardSkeleton } from '@/components/ui';
import { useIndices, useCryptoPrices } from '@/hooks';
import { SectionHeader } from './SectionHeader';

/** 홈 - 주식 + 코인 미리보기 */
export function HomeMarketPreview() {
  const { data: indices, isLoading: il } = useIndices();
  const { data: crypto, isLoading: cl } = useCryptoPrices();

  /* 주식: S&P 500, 나스닥, 다우 (DB 심볼 기준) */
  const stockSymbols = ['^GSPC', '^IXIC', '^DJI'];
  const keyStocks = indices?.filter((i) => stockSymbols.includes(i.symbol)) || [];

  /* 코인: BTC, ETH */
  const keyCoins = crypto?.slice(0, 2) || [];

  return (
    <>
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

      {/* 코인 */}
      <section>
        <SectionHeader title="암호화폐" href="/crypto" />
        {cl ? (
          <div className="grid grid-cols-2 gap-3">
            <CardSkeleton /><CardSkeleton />
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-3">
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
      </section>
    </>
  );
}
