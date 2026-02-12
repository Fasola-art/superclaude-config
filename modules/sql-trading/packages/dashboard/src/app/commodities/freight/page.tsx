import { Suspense } from 'react';
import { Metadata } from 'next';
import { TableSkeleton } from '@/components/ui';
import { FreightClient } from '@/components/commodities/FreightClient';

export const metadata: Metadata = {
  title: '운임 지수 - 원자재',
  description: '해운 운임 지수 현황',
};

export default function FreightPage() {
  return (
    <Suspense fallback={<TableSkeleton />}>
      <FreightClient />
    </Suspense>
  );
}
