import { Suspense } from 'react';
import { Metadata } from 'next';
import { TableSkeleton } from '@/components/ui';
import { LogisticsClient } from '@/components/commodities/LogisticsClient';

export const metadata: Metadata = {
  title: '물류 추적 - 원자재',
  description: '글로벌 물류 추적 현황',
};

export default function LogisticsPage() {
  return (
    <Suspense fallback={<TableSkeleton />}>
      <LogisticsClient />
    </Suspense>
  );
}
