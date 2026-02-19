'use client';

import { useRiskStatus } from '@/hooks';
import { Card, Badge, CardSkeleton } from '@/components/ui';
import { CircuitBreakerStatus } from '@/components/charts';

export function RiskClient() {
  const { data: riskStatus, isLoading } = useRiskStatus();

  if (isLoading) return <CardSkeleton />;

  const currentRisk = riskStatus?.current;
  const recentEvents = riskStatus?.recent_events || [];
  const dailyPnl = currentRisk?.daily_pnl_pct != null ? Number(currentRisk.daily_pnl_pct) : undefined;
  const maxDrawdown = currentRisk?.total_drawdown_pct != null ? Number(currentRisk.total_drawdown_pct) : undefined;

  // 서킷브레이커 레벨 매핑
  const getCircuitBreakerLevel = () => {
    if (!currentRisk) return 'NORMAL';
    return currentRisk.level as 'WARNING' | 'CRITICAL' | 'EMERGENCY';
  };

  return (
    <div className="space-y-6">
      {/* 서킷브레이커 현재 상태 */}
      <Card title="서킷브레이커 현재 상태">
        <CircuitBreakerStatus
          level={getCircuitBreakerLevel()}
          dailyPnl={dailyPnl ?? 0}
          maxDrawdown={maxDrawdown ?? 0}
        />

        {currentRisk && (
          <div className="mt-4 p-4 bg-card border border-border rounded-lg">
            <div className="font-semibold mb-2">{currentRisk.event_type}</div>
            <div className="text-sm text-muted mb-3">{currentRisk.description}</div>
            <div className="text-xs text-muted">
              발생 시각: {new Date(currentRisk.timestamp).toLocaleString()}
            </div>
          </div>
        )}
      </Card>

      {/* 손익 현황 */}
      {currentRisk && (
        <div className="grid md:grid-cols-2 gap-4">
          <Card title="일일 손익">
            <div className="text-center p-6">
              <div
                className="text-4xl font-bold"
                style={{ color: (dailyPnl ?? 0) >= 0 ? 'var(--up)' : 'var(--down)' }}
              >
                {dailyPnl != null ? `${dailyPnl > 0 ? '+' : ''}${dailyPnl.toFixed(2)}%` : '-'}
              </div>
              <div className="text-sm text-muted mt-2">Daily P&L</div>
            </div>
          </Card>

          <Card title="최대 낙폭 (MDD)">
            <div className="text-center p-6">
              <div className="text-4xl font-bold text-down">
                {maxDrawdown != null ? `${maxDrawdown.toFixed(2)}%` : '-'}
              </div>
              <div className="text-sm text-muted mt-2">Max Drawdown</div>
            </div>
          </Card>
        </div>
      )}

      {/* 최근 리스크 이벤트 */}
      <Card title="최근 리스크 이벤트">
        <div className="space-y-3">
          {recentEvents.length === 0 ? (
            <div className="text-center text-muted py-8">최근 리스크 이벤트가 없습니다</div>
          ) : (
            recentEvents.map((event, idx) => (
              <div key={idx} className="p-3 bg-card border border-border rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold">{event.event_type}</span>
                  <Badge
                    variant={
                      event.level === 'WARNING'
                        ? 'warning'
                        : event.level === 'CRITICAL'
                        ? 'error'
                        : 'down'
                    }
                  >
                    {event.level}
                  </Badge>
                </div>
                <div className="text-sm text-muted mb-2">{event.description}</div>
                <div className="flex justify-between text-xs text-muted">
                  <span>{new Date(event.timestamp).toLocaleString()}</span>
                  {event.daily_pnl_pct != null && (
                    <span className={Number(event.daily_pnl_pct) >= 0 ? 'text-up' : 'text-down'}>
                      P&L: {Number(event.daily_pnl_pct) > 0 ? '+' : ''}
                      {Number(event.daily_pnl_pct).toFixed(2)}%
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </Card>
    </div>
  );
}
