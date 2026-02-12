import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { BacktestClient } from '@/components/signals';

export const metadata: Metadata = {
  title: '백테스트 - 시장 브리핑',
  description: '전략별 백테스트 결과 및 승인 기준',
};

export default function BacktestPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <BacktestClient />
    </Suspense>
  );
}
