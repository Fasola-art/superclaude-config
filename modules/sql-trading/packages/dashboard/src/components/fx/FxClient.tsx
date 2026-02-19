'use client';

import { useState } from 'react';
import { Card, Badge, CardSkeleton } from '@/components/ui';
import { useFxFutures, useNews } from '@/hooks';
import type { NewsItem } from '@/types/api';
import { FxChart } from './FxChart';

const SYMBOLS = [
  { value: 'EURUSD', label: 'EURUSD', note: 'CME 6E=F' },
  { value: 'USDJPY', label: 'USDJPY', note: 'CME 6J=F' },
  { value: 'GBPUSD', label: 'GBPUSD', note: 'CME 6B=F' },
  { value: 'USDCNH', label: 'USDCNH', note: 'Yahoo spot (USDCNH=X)' },
];

const INTERVALS = [
  { value: '1m', label: '1m' },
  { value: '5m', label: '5m' },
  { value: '15m', label: '15m' },
  { value: '30m', label: '30m' },
  { value: '1h', label: '1h' },
  { value: '6h', label: '6h' },
  { value: '1d', label: '1d' },
  { value: '1w', label: '1w' },
  { value: '1mo', label: '1M' },
];

function sentimentVariant(score: number | null): 'up' | 'down' | 'neutral' {
  if (score === null) return 'neutral';
  if (score > 0.2) return 'up';
  if (score < -0.2) return 'down';
  return 'neutral';
}

function sentimentLabel(item: NewsItem): string {
  if (item.sentiment === null) return '분석중';
  const pct = Math.round(Math.abs(item.sentiment) * 100);
  const dir = item.sentiment > 0 ? '긍정' : item.sentiment < 0 ? '부정' : '중립';
  return `${dir} ${pct}%`;
}

function recLabel(item: NewsItem): string | null {
  return item.metadata?.recommendation ?? null;
}

function recVariant(key: string | undefined): 'up' | 'down' | 'neutral' {
  if (!key) return 'neutral';
  if (key.includes('buy')) return 'up';
  if (key.includes('sell')) return 'down';
  return 'neutral';
}

export function FxClient() {
  const [symbol, setSymbol] = useState('EURUSD');
  const [interval, setInterval] = useState('1h');
  const { data: fx, isLoading: fxLoading, error: fxError } = useFxFutures(symbol, interval);
  const { data: news, isLoading: newsLoading, error: newsError } = useNews('economy');
  const activeSymbol = SYMBOLS.find((s) => s.value === symbol);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-[var(--text)]">외환 시장</h1>
        <div className="text-xs text-[var(--text-muted)]">
          {fx?.source_symbol ? `소스: ${fx.source_symbol}` : '데이터 확인 중'}
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {SYMBOLS.map((item) => (
          <button
            key={item.value}
            onClick={() => setSymbol(item.value)}
            className={`px-3 py-1 text-sm rounded-md transition-colors ${
              symbol === item.value
                ? 'bg-[var(--accent)] text-white'
                : 'bg-[var(--bg-card)] text-[var(--text-muted)] hover:text-[var(--text)]'
            }`}
          >
            {item.label}
          </button>
        ))}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {INTERVALS.map((item) => (
          <button
            key={item.value}
            onClick={() => setInterval(item.value)}
            className={`px-3 py-1 text-xs rounded-md transition-colors ${
              interval === item.value
                ? 'bg-[var(--accent)] text-white'
                : 'bg-[var(--bg-card)] text-[var(--text-muted)] hover:text-[var(--text)]'
            }`}
          >
            {item.label}
          </button>
        ))}
      </div>

      {activeSymbol?.note && (
        <div className="text-xs text-[var(--text-muted)]">
          {activeSymbol.note}
        </div>
      )}

      {fxLoading ? (
        <CardSkeleton />
      ) : fxError ? (
        <Card>
          <div className="text-[var(--down)]">외환 차트 데이터를 불러오지 못했습니다.</div>
        </Card>
      ) : fx?.bars?.length ? (
        <Card>
          <FxChart bars={fx.bars} />
        </Card>
      ) : (
        <Card>
          <div className="text-[var(--text-muted)]">차트 데이터가 없습니다.</div>
        </Card>
      )}

      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-[var(--text)]">외환 관련 뉴스</h2>
          <span className="text-xs text-[var(--text-muted)]">FinBERT 감정 분석</span>
        </div>

        {newsLoading ? (
          <CardSkeleton />
        ) : newsError ? (
          <Card>
            <div className="text-[var(--down)]">뉴스 데이터를 불러오지 못했습니다.</div>
          </Card>
        ) : !news || news.length === 0 ? (
          <Card>
            <div className="text-[var(--text-muted)]">뉴스 없음</div>
          </Card>
        ) : (
          <div className="grid gap-3">
            {news.slice(0, 6).map((item, idx) => (
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
                    <p className="text-sm text-[var(--text-muted)] mt-1 whitespace-pre-wrap">
                      {(item.metadata?.original_summary && item.summary && item.metadata.original_summary.length > item.summary.length)
                        ? item.metadata.original_summary
                        : item.summary}
                    </p>
                    <div className="flex items-center gap-4 mt-3 text-xs text-[var(--text-muted)]">
                      <span>{item.source}</span>
                      <span>{new Date(item.timestamp).toLocaleString('ko-KR')}</span>
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="ml-auto inline-flex items-center px-2 py-1 rounded-md border border-[var(--border)] text-[var(--text-muted)] hover:text-[var(--text)] hover:border-[var(--accent)] transition-colors"
                      >
                        출처 링크
                      </a>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
