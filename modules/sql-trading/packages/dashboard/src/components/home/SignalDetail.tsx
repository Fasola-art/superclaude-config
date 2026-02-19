'use client';

import { Badge } from '@/components/ui';
import { useNews } from '@/hooks';
import type { TradingSignal, NewsItem } from '@/types/api';
import { SIGNAL_NAMES, SECTOR_NEWS } from './signal-names';

/** 신호 상세: 근거 + 관련 FinBERT 뉴스 */
export function SignalDetail({
  signal: s, onBack,
}: {
  signal: TradingSignal;
  onBack: () => void;
}) {
  const { data: news } = useNews('all');
  const isBuy = s.signal_type.includes('BUY');
  const recentNews = filterRecent(news || [], 60);
  const related = findRelatedNews(s, recentNews);
  const hasOlderNews = related.length === 0 && findRelatedNews(s, news || []).length > 0;

  return (
    <div className="absolute top-full left-0 mt-2 z-50 w-[340px] rounded-lg border border-[var(--border)] bg-[var(--bg-card)] shadow-xl">
      {/* 헤더 */}
      <div className="flex items-center gap-2 px-3 py-2 border-b border-[var(--border)]">
        <button onClick={onBack} className="text-[var(--text-muted)] hover:text-[var(--text)] text-sm">← 목록</button>
        <span className="font-mono font-bold text-sm">{s.symbol}</span>
        <Badge variant={isBuy ? 'up' : 'down'}>{s.signal_type}</Badge>
      </div>

      {/* 종목 정보 + 근거 */}
      <div className="px-3 py-2 space-y-2 border-b border-[var(--border)]">
        <div className="text-xs text-[var(--text-secondary)]">{SIGNAL_NAMES[s.symbol] || s.symbol}</div>
        <div className="text-sm text-[var(--text)]">{s.reason}</div>
        <div className="grid grid-cols-3 gap-2 text-xs">
          <PriceCell label="현재가" value={s.price} />
          <PriceCell label="목표가" value={s.target_price} color="var(--up)" />
          <PriceCell label="손절가" value={s.stop_loss} color="var(--down)" />
        </div>
        <div className="flex items-center gap-3 text-xs text-[var(--text-muted)]">
          <span>전략: <strong className="text-[var(--text)]">{s.strategy}</strong></span>
          <span>신뢰도: <strong className="text-[var(--text)]">{(s.confidence * 100).toFixed(0)}%</strong></span>
        </div>
      </div>

      {/* FinBERT 관련 뉴스 */}
      <div className="px-3 py-2">
        <div className="text-xs font-semibold text-[var(--text-muted)] mb-2">
          FinBERT 감정분석 뉴스 {related.length > 0 ? `(${related.length}건)` : ''}
        </div>
        {related.length === 0 ? (
          <div className="text-xs text-[var(--text-muted)] py-2">
            {hasOlderNews ? '1시간 내 최신 뉴스 없음 (이전 뉴스는 존재)' : '관련 뉴스 없음'}
          </div>
        ) : (
          <ul className="space-y-1.5 max-h-[200px] overflow-y-auto">
            {related.map((n, i) => <NewsRow key={i} news={n} />)}
          </ul>
        )}
      </div>
    </div>
  );
}

function PriceCell({ label, value, color }: { label: string; value: number | null; color?: string }) {
  return (
    <div>
      <span className="text-[var(--text-muted)]">{label}</span>
      <div className="font-mono" style={color ? { color } : undefined}>${value?.toLocaleString() || '-'}</div>
    </div>
  );
}

function NewsRow({ news: n }: { news: NewsItem }) {
  const sent = n.sentiment == null ? { t: '-', c: 'neutral' as const }
    : n.sentiment >= 0.3 ? { t: '긍정', c: 'up' as const }
    : n.sentiment <= -0.3 ? { t: '부정', c: 'down' as const }
    : { t: '중립', c: 'neutral' as const };

  return (
    <li>
      <a href={n.url} target="_blank" rel="noopener noreferrer"
        className="block rounded px-2 py-1.5 hover:bg-[var(--bg-hover)] transition-colors">
        <div className="flex items-center gap-1.5 mb-0.5">
          <Badge variant={sent.c}>{sent.t} {n.sentiment?.toFixed(2)}</Badge>
          <span className="text-[10px] text-[var(--text-muted)]">{n.source}</span>
        </div>
        <div className="text-xs text-[var(--text)] line-clamp-2">{n.title}</div>
      </a>
    </li>
  );
}

/** 최근 N분 이내 뉴스만 필터 */
function filterRecent(news: NewsItem[], minutes: number): NewsItem[] {
  const cutoff = Date.now() - minutes * 60_000;
  return news.filter((n) => new Date(n.timestamp).getTime() > cutoff);
}

/** 심볼 직접 → 섹터 카테고리 → 키워드 순 매칭 */
function findRelatedNews(s: TradingSignal, news: NewsItem[]): NewsItem[] {
  const direct = news.filter((n) => n.symbols?.includes(s.symbol));
  if (direct.length >= 3) return direct.slice(0, 5);

  const mapping = SECTOR_NEWS[s.symbol];
  if (!mapping) return direct.slice(0, 5);

  const byCat = news.filter((n) => mapping.cats.includes(n.category) && !direct.includes(n));
  const byKw = mapping.keywords.length > 0
    ? byCat.filter((n) => {
        const text = `${n.title} ${n.summary}`.toLowerCase();
        return mapping.keywords.some((kw) => text.includes(kw.toLowerCase()));
      })
    : byCat;

  return [...direct, ...(byKw.length > 0 ? byKw : byCat)].slice(0, 5);
}
