'use client';

type CircuitBreakerLevel = 'NORMAL' | 'WARNING' | 'CRITICAL' | 'EMERGENCY';

interface CircuitBreakerStatusProps {
  level: CircuitBreakerLevel;
  dailyPnl?: number;
  maxDrawdown?: number;
}

const LEVEL_CONFIG = {
  NORMAL: { color: 'text-up', bg: 'bg-up/10', label: '정상' },
  WARNING: { color: 'text-warning', bg: 'bg-warning/10', label: '경고' },
  CRITICAL: { color: 'text-orange-500', bg: 'bg-orange-500/10', label: '위험' },
  EMERGENCY: { color: 'text-down', bg: 'bg-down/10', label: '긴급' },
};

export function CircuitBreakerStatus({
  level,
  dailyPnl,
  maxDrawdown,
}: CircuitBreakerStatusProps) {
  const config = LEVEL_CONFIG[level];

  return (
    <div className={`p-4 ${config.bg} rounded-lg border border-border`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-medium">서킷브레이커 상태</span>
        <span className={`text-xl font-bold ${config.color}`}>{config.label}</span>
      </div>

      {(dailyPnl !== undefined || maxDrawdown !== undefined) && (
        <div className="space-y-2 text-sm">
          {dailyPnl !== undefined && (
            <div className="flex justify-between">
              <span className="text-muted">일일 손익</span>
              <span className={dailyPnl >= 0 ? 'text-up' : 'text-down'}>
                {Number(dailyPnl) > 0 ? '+' : ''}
                {Number(dailyPnl).toFixed(2)}%
              </span>
            </div>
          )}
          {maxDrawdown !== undefined && (
            <div className="flex justify-between">
              <span className="text-muted">최대 낙폭 (MDD)</span>
              <span className="text-down">{Number(maxDrawdown).toFixed(2)}%</span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
