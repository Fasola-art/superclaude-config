'use client';

interface QuartileChartProps {
  current: number;
  dayLow: number;
  dayHigh: number;
}

export function QuartileChart({ current, dayLow, dayHigh }: QuartileChartProps) {
  const range = dayHigh - dayLow;
  const q1 = dayLow + range * 0.25;
  const q2 = dayLow + range * 0.5;
  const q3 = dayLow + range * 0.75;

  const position = ((current - dayLow) / range) * 100;

  return (
    <div className="space-y-2">
      <div className="relative h-8 bg-gradient-to-r from-red-500/20 via-yellow-500/20 to-green-500/20 rounded">
        {/* 구분선 */}
        <div className="absolute inset-y-0 left-1/4 w-px bg-border" />
        <div className="absolute inset-y-0 left-1/2 w-px bg-border" />
        <div className="absolute inset-y-0 left-3/4 w-px bg-border" />

        {/* 현재 가격 마커 */}
        <div
          className="absolute inset-y-0 w-1 bg-accent rounded-full"
          style={{ left: `calc(${position}% - 2px)` }}
        />
      </div>

      <div className="flex justify-between text-xs text-muted">
        <span>{dayLow.toFixed(2)}</span>
        <span>Q1: {q1.toFixed(2)}</span>
        <span>Q2: {q2.toFixed(2)}</span>
        <span>Q3: {q3.toFixed(2)}</span>
        <span>{dayHigh.toFixed(2)}</span>
      </div>

      <div className="text-sm text-center">
        현재: <span className="font-semibold text-accent">{current.toFixed(2)}</span>
      </div>
    </div>
  );
}
