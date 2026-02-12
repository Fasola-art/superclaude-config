import { Suspense } from 'react';
import { Metadata } from 'next';
import { TableSkeleton } from '@/components/ui';
import { TradeClient } from '@/components/commodities/TradeClient';

export const metadata: Metadata = {
  title: '무역 통계 - 원자재',
  description: '글로벌 무역 통계',
};

export default function TradePage() {
  return (
    <Suspense fallback={<TableSkeleton />}>
      <TradeClient />
    </Suspense>
  );
}
