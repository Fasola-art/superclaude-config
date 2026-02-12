import { Suspense } from 'react';
import type { Metadata } from 'next';
import { FlightsClient } from '@/components/commodities/FlightsClient';

export const metadata: Metadata = {
  title: '항공 추적 - 원자재',
  description: '실시간 항공기 추적 (Flightradar24)',
};

export default function FlightsPage() {
  return (
    <Suspense fallback={
      <div className="h-[500px] flex items-center justify-center text-[var(--text-muted)]">
        항공 지도 로딩 중...
      </div>
    }>
      <FlightsClient />
    </Suspense>
  );
}
