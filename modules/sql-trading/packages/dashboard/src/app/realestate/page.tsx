import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { RealEstateClient } from '@/components/realestate/RealEstateClient';

export const metadata: Metadata = {
  title: '부동산 - 시장 브리핑',
  description: '부동산 시장 현황',
};

export default function RealEstatePage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <RealEstateClient />
    </Suspense>
  );
}
