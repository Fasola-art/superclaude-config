import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { PaperClient } from '@/components/signals';

export const metadata: Metadata = {
  title: '페이퍼 트레이딩 - 시장 브리핑',
  description: '모의 거래 기록 및 전략별 성과',
};

export default function PaperPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <PaperClient />
    </Suspense>
  );
}
