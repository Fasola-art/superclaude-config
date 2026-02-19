import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  title?: string;
}

export function Card({ children, className = '', title }: CardProps) {
  return (
    <div className={`bg-[var(--bg-card)] rounded-xl border border-[var(--border)] p-4 ${className}`}>
      {title && (
        <h3 className="text-sm font-semibold text-[var(--text-muted)] mb-3">{title}</h3>
      )}
      {children}
    </div>
  );
}

export function MetricCard({
  label, value, change, prefix = '',
}: {
  label: string; value: string | number; change?: number; prefix?: string;
}) {
  const c = change !== undefined ? Number(change) || 0 : undefined;
  return (
    <Card>
      <p className="text-xs text-[var(--text-muted)]">{label}</p>
      <p className="text-xl font-bold mt-1">{prefix}{typeof value === 'number' ? value.toLocaleString() : value}</p>
      {c !== undefined && (
        <p className={`text-sm mt-1 ${c >= 0 ? 'text-[var(--up)]' : 'text-[var(--down)]'}`}>
          {c > 0 ? '+' : ''}{c.toFixed(2)}%
        </p>
      )}
    </Card>
  );
}
