import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { StocksClient } from '@/components/stocks/StocksClient';

export const metadata: Metadata = {
  title: '주식 - 시장 브리핑',
  description: '글로벌 주식 시장 현황',
};

export default function StocksPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <StocksClient />
    </Suspense>
  );
}
