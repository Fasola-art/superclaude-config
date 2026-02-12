import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { RiskClient } from '@/components/signals';

export const metadata: Metadata = {
  title: '리스크 모니터 - 시장 브리핑',
  description: '서킷브레이커, 일일 손익, MDD 추적',
};

export default function RiskPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <RiskClient />
    </Suspense>
  );
}
