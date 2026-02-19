import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export function ChangeIndicator({
  value: raw, size = 'sm',
}: {
  value: number; size?: 'sm' | 'md' | 'lg';
}) {
  const v = Number(raw) || 0;
  const sizeClasses = { sm: 'text-xs', md: 'text-sm', lg: 'text-base' };
  const iconSize = { sm: 12, md: 16, lg: 20 };

  if (v === 0) {
    return (
      <span className={`inline-flex items-center gap-1 text-[var(--text-muted)] ${sizeClasses[size]}`}>
        <Minus size={iconSize[size]} />
        0.00%
      </span>
    );
  }

  const isUp = v > 0;
  return (
    <span className={`inline-flex items-center gap-1 ${isUp ? 'text-[var(--up)]' : 'text-[var(--down)]'} ${sizeClasses[size]}`}>
      {isUp ? <TrendingUp size={iconSize[size]} /> : <TrendingDown size={iconSize[size]} />}
      {isUp ? '+' : ''}{v.toFixed(2)}%
    </span>
  );
}
