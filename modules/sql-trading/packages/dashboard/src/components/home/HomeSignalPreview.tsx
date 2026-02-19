'use client';

import { Card, Badge, ConfidenceGauge, CardSkeleton } from '@/components/ui';
import { useLatestSignals, useRiskStatus } from '@/hooks';
import { SectionHeader } from './SectionHeader';

/** 홈 - 시그널 + 리스크 미리보기 */
export function HomeSignalPreview() {
  const { data: signals, isLoading: sl } = useLatestSignals();
  const { data: risk, isLoading: rl } = useRiskStatus();

  if (sl || rl) return <CardSkeleton />;

  const latest3 = signals?.slice(0, 3) || [];
  const avgConf = latest3.length > 0
    ? latest3.reduce((sum, s) => sum + s.confidence, 0) / latest3.length
    : 0;

  const riskLevel = risk?.current?.level || 'NORMAL';
  const riskColors: Record<string, string> = {
    NORMAL: 'var(--up)', WARNING: 'var(--warning)',
    CRITICAL: 'orange', EMERGENCY: 'var(--down)',
  };

  return (
    <section>
      <SectionHeader title="트레이딩 시그널" href="/signals" />
      <div className="grid grid-cols-2 gap-3">
        {/* 평균 컨피던스 */}
        <Card>
          <div className="text-xs text-[var(--text-muted)] mb-2">평균 신뢰도</div>
          <ConfidenceGauge value={avgConf} size="lg" />
          <div className="text-center text-xl font-bold mt-2">{(avgConf * 100).toFixed(0)}%</div>
        </Card>

        {/* 리스크 상태 */}
        <Card>
          <div className="text-xs text-[var(--text-muted)] mb-2">리스크 상태</div>
          <div className="flex items-center gap-2 mt-3">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: riskColors[riskLevel] }} />
            <span className="text-lg font-bold">{riskLevel}</span>
          </div>
          {risk?.current?.daily_pnl_pct != null && (
            <div className={`text-sm mt-2 ${Number(risk.current.daily_pnl_pct) >= 0 ? 'text-[var(--up)]' : 'text-[var(--down)]'}`}>
              일일 PnL: {Number(risk.current.daily_pnl_pct) > 0 ? '+' : ''}{Number(risk.current.daily_pnl_pct).toFixed(2)}%
            </div>
          )}
        </Card>
      </div>

      {/* 최근 시그널 3개 */}
      {latest3.length > 0 && (
        <div className="mt-3 space-y-2">
          {latest3.map((s, i) => (
            <div key={i} className="flex items-center justify-between bg-[var(--bg-card)] border border-[var(--border)] rounded-lg px-3 py-2">
              <div className="flex items-center gap-2">
                <span className="font-mono font-semibold text-sm">{s.symbol}</span>
                <Badge variant={s.signal_type === 'BUY' ? 'up' : s.signal_type === 'SELL' ? 'down' : 'neutral'}>
                  {s.signal_type}
                </Badge>
              </div>
              <span className="text-xs text-[var(--text-muted)]">{s.strategy}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
