'use client';

import { useEffect, useRef, useState } from 'react';
import { useSummaryDetail } from '@/hooks';
import type { SummaryDetail } from '@/types/api';
import { TableDetailPanel } from './TableDetailPanel';

/** 전체 데이터 현황 팝오버 - 테이블별 건수 + 클릭 시 상세 */
export function DataOverviewPopover({ count }: { count: number }) {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState<SummaryDetail | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  const { data: details } = useSummaryDetail();

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

  return (
    <div ref={ref} className="relative">
      <div className="text-[var(--text-muted)]">전체 데이터</div>
      <button
        onClick={() => { setOpen((v) => !v); setSelected(null); }}
        className="font-mono text-lg font-bold cursor-pointer rounded-md px-2 py-0.5 transition-all hover:scale-105 active:scale-95 text-[var(--text)]"
        style={{ backgroundColor: 'color-mix(in srgb, var(--accent) 12%, transparent)' }}
      >
        {count.toLocaleString()}
      </button>

      {open && details && !selected && (
        <div className="absolute top-full left-0 mt-2 z-50 min-w-[300px] rounded-lg border border-[var(--border)] bg-[var(--bg-card)] shadow-xl">
          <div className="px-3 py-2 border-b border-[var(--border)] text-xs font-semibold text-[var(--text-muted)]">
            테이블별 데이터 현황
          </div>
          <ul className="py-1">
            {details.map((d) => (
              <li
                key={d.table}
                onClick={() => setSelected(d)}
                className="flex items-center justify-between px-3 py-2 hover:bg-[var(--bg-hover)] cursor-pointer transition-colors"
              >
                <div className="min-w-0">
                  <div className="text-sm font-medium text-[var(--text)]">{d.label}</div>
                  <div className="text-[10px] text-[var(--text-muted)] font-mono">{d.table}</div>
                </div>
                <div className="flex items-center gap-2">
                  <div className="text-right">
                    <div className="font-mono text-sm font-semibold text-[var(--text)]">{d.count.toLocaleString()}</div>
                    <div className="text-[10px] text-[var(--text-muted)]">
                      {d.latest ? formatRelative(d.latest) : '-'}
                    </div>
                  </div>
                  <span className="text-[var(--text-muted)] text-xs">›</span>
                </div>
              </li>
            ))}
          </ul>
          <div className="px-3 py-2 border-t border-[var(--border)] text-xs text-[var(--text-muted)] text-right">
            합계: <strong className="text-[var(--text)]">{details.reduce((s, d) => s + d.count, 0).toLocaleString()}</strong>건
          </div>
        </div>
      )}

      {open && selected && (
        <TableDetailPanel detail={selected} onBack={() => setSelected(null)} />
      )}
    </div>
  );
}

/** 상대 시간 포맷 */
function formatRelative(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const min = Math.floor(diff / 60_000);
  if (min < 1) return '방금';
  if (min < 60) return `${min}분 전`;
  const hr = Math.floor(min / 60);
  if (hr < 24) return `${hr}시간 전`;
  return `${Math.floor(hr / 24)}일 전`;
}
