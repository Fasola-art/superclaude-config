'use client';

import { useBacktest } from '@/hooks';
import { Card, Badge, ConfidenceGauge, CardSkeleton } from '@/components/ui';
import type { BacktestResult } from '@/types/signals';

export function BacktestClient() {
  const { data: results, isLoading } = useBacktest();

  if (isLoading) return <CardSkeleton />;

  // 승인 기준
  const APPROVAL_CRITERIA = {
    sharpe: 1.5,
    mdd: 15,
    winRate: 55,
  };

  const checkApproval = (result: BacktestResult) => {
    return (
      Number(result.sharpe_ratio) >= APPROVAL_CRITERIA.sharpe &&
      Number(result.max_drawdown) <= APPROVAL_CRITERIA.mdd &&
      Number(result.win_rate) >= APPROVAL_CRITERIA.winRate
    );
  };

  return (
    <div className="space-y-6">
      {/* 승인 기준 */}
      <Card title="승인 기준">
        <div className="grid md:grid-cols-3 gap-4">
          <ConfidenceGauge
            value={APPROVAL_CRITERIA.sharpe / 3}
            label={`Sharpe Ratio ≥ ${APPROVAL_CRITERIA.sharpe}`}
            size="md"
          />
          <ConfidenceGauge
            value={1 - APPROVAL_CRITERIA.mdd / 100}
            label={`MDD ≤ ${APPROVAL_CRITERIA.mdd}%`}
            size="md"
          />
          <ConfidenceGauge
            value={APPROVAL_CRITERIA.winRate / 100}
            label={`승률 ≥ ${APPROVAL_CRITERIA.winRate}%`}
            size="md"
          />
        </div>
      </Card>

      {/* 백테스트 결과 테이블 */}
      <Card title="백테스트 결과">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-border">
              <tr>
                <th className="text-left p-2">전략</th>
                <th className="text-right p-2">기간</th>
                <th className="text-right p-2">거래 수</th>
                <th className="text-right p-2">승률</th>
                <th className="text-right p-2">Sharpe</th>
                <th className="text-right p-2">MDD</th>
                <th className="text-right p-2">총 수익률</th>
                <th className="text-center p-2">승인</th>
              </tr>
            </thead>
            <tbody>
              {results?.map((r, idx) => {
                const approved = checkApproval(r);
                return (
                  <tr key={idx} className="border-b border-border/50">
                    <td className="p-2 font-semibold">{r.strategy}</td>
                    <td className="p-2 text-right text-muted text-xs">
                      {r.start_date} ~ {r.end_date}
                    </td>
                    <td className="p-2 text-right font-mono">{r.total_trades}</td>
                    <td className="p-2 text-right font-mono">{Number(r.win_rate).toFixed(1)}%</td>
                    <td className="p-2 text-right font-mono">{Number(r.sharpe_ratio).toFixed(2)}</td>
                    <td className="p-2 text-right font-mono text-down">{Number(r.max_drawdown).toFixed(1)}%</td>
                    <td className="p-2 text-right font-mono">
                      <span className={Number(r.total_return) >= 0 ? 'text-up' : 'text-down'}>
                        {Number(r.total_return) > 0 ? '+' : ''}
                        {Number(r.total_return).toFixed(1)}%
                      </span>
                    </td>
                    <td className="p-2 text-center">
                      <Badge variant={approved ? 'success' : 'error'}>{approved ? '통과' : '미달'}</Badge>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
