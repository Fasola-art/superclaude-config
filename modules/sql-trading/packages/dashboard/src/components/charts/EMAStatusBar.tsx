'use client';

interface EMAStatusBarProps {
  ema360: number;
  ema720: number;
  ema1440: number;
  ema2880: number;
  current: number;
}

export function EMAStatusBar({ ema360, ema720, ema1440, ema2880, current }: EMAStatusBarProps) {
  const isBullish =
    current > ema360 && ema360 > ema720 && ema720 > ema1440 && ema1440 > ema2880;

  const status = isBullish ? 'BULLISH' : 'BEARISH';
  const statusColor = isBullish ? 'text-up' : 'text-down';
  const bgColor = isBullish ? 'bg-up/10' : 'bg-down/10';

  return (
    <div className={`p-4 ${bgColor} rounded-lg border border-border`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-medium">EMA 정배열 상태</span>
        <span className={`text-lg font-bold ${statusColor}`}>{status}</span>
      </div>

      <div className="space-y-1.5 text-sm">
        <div className="flex justify-between">
          <span className="text-muted">현재가</span>
          <span className="font-mono">{current.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted">EMA 360</span>
          <span className="font-mono">{ema360.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted">EMA 720</span>
          <span className="font-mono">{ema720.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted">EMA 1440</span>
          <span className="font-mono">{ema1440.toFixed(2)}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-muted">EMA 2880</span>
          <span className="font-mono">{ema2880.toFixed(2)}</span>
        </div>
      </div>
    </div>
  );
}
