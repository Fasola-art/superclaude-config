'use client';

interface ConfidenceGaugeProps {
  value: number;  // 0~1
  label?: string;
  size?: 'sm' | 'md' | 'lg';
}

export function ConfidenceGauge({ value, label, size = 'md' }: ConfidenceGaugeProps) {
  const pct = Math.round(value * 100);
  const color = pct >= 70 ? 'var(--up)' : pct >= 40 ? 'var(--warning)' : 'var(--down)';
  const sizes = { sm: 'h-1.5', md: 'h-2.5', lg: 'h-4' };

  return (
    <div>
      {label && (
        <div className="flex justify-between text-xs mb-1">
          <span className="text-[var(--text-muted)]">{label}</span>
          <span style={{ color }} className="font-medium">{pct}%</span>
        </div>
      )}
      <div className={`w-full ${sizes[size]} bg-[var(--border)] rounded-full overflow-hidden`}>
        <div
          className={`${sizes[size]} rounded-full transition-all duration-500`}
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
}
