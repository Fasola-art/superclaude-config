'use client';

import { useEffect, useRef, useState } from 'react';
import { Badge } from '@/components/ui';
import type { TradingSignal } from '@/types/api';
import { SIGNAL_NAMES } from './signal-names';
import { SignalDetail } from './SignalDetail';

type FilterType = 'buy' | 'sell';

/** 매수/매도 종목 리스트 팝오버 + 상세 뷰 */
export function SignalPopover({
  signals, filter, count,
}: {
  signals: TradingSignal[];
  filter: FilterType;
  count: number;
}) {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState<TradingSignal | null>(null);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
        setSelected(null);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [open]);

  const isBuy = filter === 'buy';
  const filtered = signals.filter((s) =>
    isBuy
      ? s.signal_type === 'BUY' || s.signal_type === 'STRONG_BUY'
      : s.signal_type === 'SELL' || s.signal_type === 'STRONG_SELL',
  );

  const colorVar = isBuy ? 'var(--up)' : 'var(--down)';
  const label = isBuy ? '매수 신호' : '매도 신호';

  return (
    <div ref={ref} className="relative">
      <div className="text-[var(--text-muted)]">{label}</div>
      <button
        onClick={() => { setOpen((v) => !v); setSelected(null); }}
        className="font-mono text-lg font-bold cursor-pointer rounded-md px-2 py-0.5 transition-all hover:scale-105 active:scale-95"
        style={{ color: colorVar, backgroundColor: `color-mix(in srgb, ${colorVar} 12%, transparent)` }}
      >
        {count.toLocaleString()}
      </button>

      {open && filtered.length > 0 && !selected && (
        <div className="absolute top-full left-0 mt-2 z-50 min-w-[280px] rounded-lg border border-[var(--border)] bg-[var(--bg-card)] shadow-xl">
          <div className="px-3 py-2 border-b border-[var(--border)] text-xs font-semibold text-[var(--text-muted)]">
            {label} {filtered.length}개 종목
          </div>
          <ul className="max-h-[280px] overflow-y-auto py-1">
            {filtered.map((s, i) => (
              <li
                key={i}
                onClick={() => setSelected(s)}
                className="flex items-center justify-between px-3 py-2 hover:bg-[var(--bg-hover)] cursor-pointer transition-colors"
              >
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-semibold text-sm text-[var(--text)]">{s.symbol}</span>
                    <Badge variant={s.signal_type.includes('STRONG') ? (isBuy ? 'success' : 'error') : (isBuy ? 'up' : 'down')}>
                      {s.signal_type}
                    </Badge>
                    <span className="text-xs text-[var(--text-muted)]">{(s.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <div className="text-xs text-[var(--text-secondary)] mt-0.5 truncate">
                    {SIGNAL_NAMES[s.symbol] || s.symbol}
                  </div>
                </div>
                <span className="text-[var(--text-muted)] text-xs ml-2">›</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {open && selected && (
        <SignalDetail signal={selected} onBack={() => setSelected(null)} />
      )}
    </div>
  );
}
