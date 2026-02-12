type BadgeVariant = 'up' | 'down' | 'warning' | 'neutral' | 'accent' | 'info' | 'success' | 'error';

const variants: Record<BadgeVariant, string> = {
  up: 'bg-[var(--up)]/15 text-[var(--up)]',
  down: 'bg-[var(--down)]/15 text-[var(--down)]',
  warning: 'bg-[var(--warning)]/15 text-[var(--warning)]',
  neutral: 'bg-[var(--text-secondary)]/15 text-[var(--text-secondary)]',
  accent: 'bg-[var(--accent)]/15 text-[var(--accent)]',
  info: 'bg-blue-500/15 text-blue-500',
  success: 'bg-green-500/15 text-green-500',
  error: 'bg-red-500/15 text-red-500',
};

export function Badge({
  children, variant = 'neutral',
}: {
  children: React.ReactNode; variant?: BadgeVariant;
}) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${variants[variant]}`}>
      {children}
    </span>
  );
}
