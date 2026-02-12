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
  return (
    <Card>
      <p className="text-xs text-[var(--text-muted)]">{label}</p>
      <p className="text-xl font-bold mt-1">{prefix}{typeof value === 'number' ? value.toLocaleString() : value}</p>
      {change !== undefined && (
        <p className={`text-sm mt-1 ${change >= 0 ? 'text-[var(--up)]' : 'text-[var(--down)]'}`}>
          {change > 0 ? '+' : ''}{change.toFixed(2)}%
        </p>
      )}
    </Card>
  );
}
