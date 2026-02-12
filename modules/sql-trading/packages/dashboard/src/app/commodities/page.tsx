import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { CommoditiesClient } from '@/components/commodities/CommoditiesClient';

export const metadata: Metadata = {
  title: '원자재 - 시장 브리핑',
  description: '원자재 및 물류 현황',
};

export default function CommoditiesPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <CommoditiesClient />
    </Suspense>
  );
}
