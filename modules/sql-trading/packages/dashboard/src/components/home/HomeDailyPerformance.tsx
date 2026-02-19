'use client';

import { Card, CardSkeleton, Badge } from '@/components/ui';
import { useDailyPerformance } from '@/hooks';

function outcomeBadge(outcome: 'win' | 'loss' | 'flat') {
  if (outcome === 'win') return <Badge variant="success">성공</Badge>;
  if (outcome === 'loss') return <Badge variant="error">실패</Badge>;
  return <Badge variant="neutral">횡보</Badge>;
}

export function HomeDailyPerformance() {
  const { data, isLoading, error } = useDailyPerformance();

  if (isLoading) return <CardSkeleton />;
  if (error || !data) {
    return (
      <Card>
        <div className="text-[var(--down)]">어제 추천 성과를 불러오지 못했습니다.</div>
      </Card>
    );
  }

  const { summary, items, window } = data;
  const start = new Date(window.start_kst).toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
  const end = new Date(window.end_kst).toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });

  return (
    <Card>
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-[var(--text)]">어제 추천 성과</h2>
        <span className="text-xs text-[var(--text-muted)]">
          미국장 시작 기준: {start} → {end}
        </span>
      </div>
      <div className="grid grid-cols-4 gap-3 text-sm mb-4">
        <div>
          <div className="text-[var(--text-muted)]">승률</div>
          <div className="text-[var(--text)] font-mono">{Number(summary.win_rate).toFixed(2)}%</div>
        </div>
        <div>
          <div className="text-[var(--text-muted)]">성공</div>
          <div className="text-[var(--up)] font-mono">{summary.wins}</div>
        </div>
        <div>
          <div className="text-[var(--text-muted)]">실패</div>
          <div className="text-[var(--down)] font-mono">{summary.losses}</div>
        </div>
        <div>
          <div className="text-[var(--text-muted)]">횡보</div>
          <div className="text-[var(--text)] font-mono">{summary.flats}</div>
        </div>
      </div>

      {items.length === 0 ? (
        <div className="text-[var(--text-muted)] text-sm">어제 추천 종목이 없습니다.</div>
      ) : (
        <div className="space-y-2">
          {items.map((it) => (
            <div key={`${it.symbol}-${it.entry_time}`} className="flex items-center justify-between bg-[var(--bg)] border border-[var(--border)] rounded-lg px-3 py-2 text-sm">
              <div className="flex items-center gap-2">
                <span className="font-mono font-semibold">{it.symbol}</span>
                <span className="text-xs text-[var(--text-muted)]">{it.signal_type}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className={Number(it.pct_change) >= 0 ? 'text-[var(--up)]' : 'text-[var(--down)]'}>
                  {Number(it.pct_change) > 0 ? '+' : ''}{Number(it.pct_change).toFixed(2)}%
                </span>
                {outcomeBadge(it.outcome)}
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}
