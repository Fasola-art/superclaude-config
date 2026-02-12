import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

export function ChangeIndicator({
  value, size = 'sm',
}: {
  value: number; size?: 'sm' | 'md' | 'lg';
}) {
  const sizeClasses = { sm: 'text-xs', md: 'text-sm', lg: 'text-base' };
  const iconSize = { sm: 12, md: 16, lg: 20 };

  if (value === 0) {
    return (
      <span className={`inline-flex items-center gap-1 text-[var(--text-muted)] ${sizeClasses[size]}`}>
        <Minus size={iconSize[size]} />
        0.00%
      </span>
    );
  }

  const isUp = value > 0;
  return (
    <span className={`inline-flex items-center gap-1 ${isUp ? 'text-[var(--up)]' : 'text-[var(--down)]'} ${sizeClasses[size]}`}>
      {isUp ? <TrendingUp size={iconSize[size]} /> : <TrendingDown size={iconSize[size]} />}
      {isUp ? '+' : ''}{value.toFixed(2)}%
    </span>
  );
}
