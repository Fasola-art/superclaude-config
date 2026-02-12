'use client';

import { useState } from 'react';
import { useNews } from '@/hooks';
import { Card, Badge } from '@/components/ui';
import type { NewsItem } from '@/types/api';

const categories = [
  { value: 'all', label: '전체' },
  { value: 'stocks', label: '주식' },
  { value: 'crypto', label: '암호화폐' },
  { value: 'economy', label: '경제' },
  { value: 'realestate', label: '부동산' },
];

/** 감정 점수 → Badge variant */
function sentimentVariant(score: number | null): 'up' | 'down' | 'neutral' {
  if (score === null) return 'neutral';
  if (score > 0.2) return 'up';
  if (score < -0.2) return 'down';
  return 'neutral';
}

/** 감정 점수 → 퍼센트 문자열 */
function sentimentLabel(item: NewsItem): string {
  if (item.sentiment === null) return '분석중';
  const pct = Math.round(Math.abs(item.sentiment) * 100);
  const dir = item.sentiment > 0 ? '긍정' : item.sentiment < 0 ? '부정' : '중립';
  return `${dir} ${pct}%`;
}

/** metadata에서 투자의견 추출 */
function recLabel(item: NewsItem): string | null {
  return item.metadata?.recommendation ?? null;
}

function recVariant(key: string | undefined): 'up' | 'down' | 'neutral' {
  if (!key) return 'neutral';
  if (key.includes('buy')) return 'up';
  if (key.includes('sell')) return 'down';
  return 'neutral';
}

export function NewsClient() {
  const [category, setCategory] = useState('all');
  const { data, isLoading, error } = useNews(category);

  if (isLoading) return <div className="text-[var(--text-muted)]">로딩 중...</div>;
  if (error) return <div className="text-[var(--down)]">에러 발생</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-[var(--text)]">시장 뉴스</h1>
        <div className="flex gap-2">
          {categories.map((cat) => (
            <button
              key={cat.value}
              onClick={() => setCategory(cat.value)}
              className={`px-3 py-1 text-sm rounded-md transition-colors ${
                category === cat.value
                  ? 'bg-[var(--accent)] text-white'
                  : 'bg-[var(--bg-card)] text-[var(--text-muted)] hover:text-[var(--text)]'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid gap-4">
        {!data || data.length === 0 ? (
          <div className="text-[var(--text-muted)]">뉴스 없음</div>
        ) : (
          data.map((item, idx) => (
            <Card key={idx}>
              <div className="flex items-start gap-3">
                <div className="flex flex-col gap-1 min-w-[80px] items-center">
                  <Badge variant={sentimentVariant(item.sentiment)}>
                    {sentimentLabel(item)}
                  </Badge>
                  {recLabel(item) && (
                    <Badge variant={recVariant(item.metadata?.rec_key)}>
                      {recLabel(item)}
                    </Badge>
                  )}
                </div>
                <div className="flex-1">
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-semibold text-[var(--text)] hover:text-[var(--accent)] transition-colors"
                  >
                    {item.title}
                  </a>
                  <p className="text-sm text-[var(--text-muted)] mt-1">{item.summary}</p>
                  <div className="flex items-center gap-4 mt-3 text-xs text-[var(--text-muted)]">
                    <span>{item.source}</span>
                    <span>{new Date(item.timestamp).toLocaleString('ko-KR')}</span>
                    {item.symbols && item.symbols.length > 0 && (
                      <span className="flex gap-1">
                        {item.symbols.map((symbol, i) => (
                          <Badge key={i} variant="info">{symbol}</Badge>
                        ))}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
