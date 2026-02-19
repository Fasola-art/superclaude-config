'use client';

import { usePaperTrades } from '@/hooks';
import { Card, CardSkeleton } from '@/components/ui';
import { TradeTable } from './TradeTable';

export function PaperClient() {
  const { data: trades, isLoading } = usePaperTrades();

  if (isLoading) return <CardSkeleton />;

  // 총 수익/손실 계산
  const totalPnl = trades?.reduce((sum, t) => sum + (t.pnl || 0), 0) || 0;
  const totalPnlPct =
    trades && trades.length > 0
      ? trades.reduce((sum, t) => sum + (t.pnl_pct || 0), 0) / trades.length
      : 0;

  // 전략별 성과
  const strategyPerf = trades?.reduce((acc, t) => {
    if (!acc[t.strategy]) {
      acc[t.strategy] = { count: 0, totalPnl: 0, wins: 0 };
    }
    acc[t.strategy].count += 1;
    acc[t.strategy].totalPnl += t.pnl || 0;
    if ((t.pnl || 0) > 0) acc[t.strategy].wins += 1;
    return acc;
  }, {} as Record<string, { count: number; totalPnl: number; wins: number }>);

  return (
    <div className="space-y-6">
      {/* 총 수익/손실 요약 */}
      <div className="grid md:grid-cols-3 gap-4">
        <Card title="총 거래">
          <div className="text-center p-4">
            <div className="text-3xl font-bold">{trades?.length || 0}</div>
            <div className="text-sm text-muted mt-1">Total Trades</div>
          </div>
        </Card>

        <Card title="총 수익">
          <div className="text-center p-4">
            <div className={`text-3xl font-bold ${totalPnl >= 0 ? 'text-up' : 'text-down'}`}>
              {totalPnl > 0 ? '+' : ''}${totalPnl.toFixed(2)}
            </div>
            <div className="text-sm text-muted mt-1">Total P&L</div>
          </div>
        </Card>

        <Card title="평균 수익률">
          <div className="text-center p-4">
            <div className={`text-3xl font-bold ${totalPnlPct >= 0 ? 'text-up' : 'text-down'}`}>
              {totalPnlPct > 0 ? '+' : ''}
              {totalPnlPct.toFixed(2)}%
            </div>
            <div className="text-sm text-muted mt-1">Avg Return</div>
          </div>
        </Card>
      </div>

      {/* 전략별 성과 */}
      <Card title="전략별 성과">
        <div className="grid md:grid-cols-3 gap-4">
          {strategyPerf &&
            Object.entries(strategyPerf).map(([strategy, perf]) => (
              <div key={strategy} className="p-4 bg-card border border-border rounded-lg">
                <div className="font-semibold mb-3">{strategy}</div>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted">거래 수</span>
                    <span>{perf.count}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted">승률</span>
                    <span>{((perf.wins / perf.count) * 100).toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted">총 수익</span>
                    <span className={perf.totalPnl >= 0 ? 'text-up' : 'text-down'}>
                      {perf.totalPnl > 0 ? '+' : ''}${perf.totalPnl.toFixed(2)}
                    </span>
                  </div>
                </div>
              </div>
            ))}
        </div>
      </Card>

      {/* 페이퍼 트레이딩 기록 테이블 */}
      <Card title="거래 기록">
        {trades && <TradeTable trades={trades} />}
      </Card>
    </div>
  );
}
