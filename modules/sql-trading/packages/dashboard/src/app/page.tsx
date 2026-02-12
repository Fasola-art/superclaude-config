import { Suspense } from 'react';
import { CardSkeleton } from '@/components/ui';
import { HomeClient } from '@/components/home/HomeClient';

export default function HomePage() {
  return (
    <div>
      <h1 className="sr-only">마켓브리핑 — 글로벌 금융 시장 대시보드</h1>
      <p className="text-xs text-[var(--text-muted)] mb-4">
        매일 오전 9시, 오후 11시 AI가 최신 시장 데이터를 분석하여 업데이트합니다.
      </p>
      <Suspense fallback={
        <div className="grid grid-cols-2 gap-3">
          {Array.from({ length: 4 }).map((_, i) => <CardSkeleton key={i} />)}
        </div>
      }>
        <HomeClient />
      </Suspense>
    </div>
  );
}
