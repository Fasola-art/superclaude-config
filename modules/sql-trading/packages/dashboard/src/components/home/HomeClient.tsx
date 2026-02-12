'use client';

import { Badge, CardSkeleton } from '@/components/ui';
import { useSummary } from '@/hooks';
import { HomeQuickNav } from './HomeQuickNav';
import { HomeMarketPreview } from './HomeMarketPreview';
import { HomeSignalPreview } from './HomeSignalPreview';
import { SectionHeader } from './SectionHeader';

export function HomeClient() {
  const { data: summary, isLoading } = useSummary();

  return (
    <div className="space-y-6">
      {/* 시스템 현황 */}
      {isLoading ? (
        <CardSkeleton />
      ) : summary ? (
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-sm font-semibold text-[var(--text)]">시스템 현황</h2>
            <Badge variant="info">{summary.server_time.slice(11, 16)}</Badge>
          </div>
          <div className="grid grid-cols-4 gap-3 text-sm">
            <div>
              <div className="text-[var(--text-muted)]">전체 데이터</div>
              <div className="text-[var(--text)] font-mono">{summary.total_records.toLocaleString()}</div>
            </div>
            <div>
              <div className="text-[var(--text-muted)]">매수 신호</div>
              <div className="text-[var(--up)] font-mono">{summary.buy_signals.toLocaleString()}</div>
            </div>
            <div>
              <div className="text-[var(--text-muted)]">매도 신호</div>
              <div className="text-[var(--down)] font-mono">{summary.sell_signals.toLocaleString()}</div>
            </div>
            <div>
              <div className="text-[var(--text-muted)]">업데이트</div>
              <div className="text-[var(--text)] font-mono text-xs">
                {summary.last_update ? new Date(summary.last_update).toLocaleDateString('ko-KR') : 'N/A'}
              </div>
            </div>
          </div>
        </div>
      ) : null}

      {/* 빠른 이동 */}
      <HomeQuickNav />

      {/* 주식 + 코인 미리보기 */}
      <HomeMarketPreview />

      {/* 시그널 미리보기 */}
      <HomeSignalPreview />
    </div>
  );
}
