'use client';

import { Badge } from '@/components/ui';
import { TABLE_INFO } from './table-descriptions';
import type { SummaryDetail } from '@/types/api';

/** 테이블 상세 정보 패널 */
export function TableDetailPanel({
  detail: d, onBack,
}: {
  detail: SummaryDetail;
  onBack: () => void;
}) {
  const info = TABLE_INFO[d.table];
  if (!info) return null;

  return (
    <div className="absolute top-full left-0 mt-2 z-50 w-[340px] rounded-lg border border-[var(--border)] bg-[var(--bg-card)] shadow-xl">
      {/* 헤더 */}
      <div className="flex items-center gap-2 px-3 py-2 border-b border-[var(--border)]">
        <button onClick={onBack} className="text-[var(--text-muted)] hover:text-[var(--text)] text-sm">
          ← 목록
        </button>
        <span className="font-semibold text-sm text-[var(--text)]">{d.label}</span>
        <Badge variant="info">{d.count.toLocaleString()}건</Badge>
      </div>

      {/* 설명 */}
      <div className="px-3 py-2 space-y-2 border-b border-[var(--border)]">
        <div className="text-sm text-[var(--text)]">{info.description}</div>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <InfoCell label="데이터 소스" value={info.source} />
          <InfoCell label="수집 주기" value={info.interval} />
          <InfoCell label="테이블명" value={d.table} mono />
          <InfoCell label="최근 업데이트" value={d.latest ? formatRelative(d.latest) : '없음'} />
        </div>
      </div>

      {/* 주요 컬럼 */}
      <div className="px-3 py-2">
        <div className="text-xs font-semibold text-[var(--text-muted)] mb-1.5">주요 컬럼</div>
        <div className="flex flex-wrap gap-1">
          {info.columns.map((col) => (
            <span key={col} className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-[var(--bg-hover)] text-[var(--text-secondary)]">
              {col}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

function InfoCell({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div>
      <span className="text-[var(--text-muted)]">{label}</span>
      <div className={`text-[var(--text)] ${mono ? 'font-mono text-[10px]' : 'text-xs'}`}>{value}</div>
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
