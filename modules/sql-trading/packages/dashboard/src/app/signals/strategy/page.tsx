import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { StrategyClient } from '@/components/signals';

export const metadata: Metadata = {
  title: '전략 현황 - 시장 브리핑',
  description: '4분할 가격 레벨, 세션 타임라인, EMA 상태',
};

export default function StrategyPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <StrategyClient />
    </Suspense>
  );
}
