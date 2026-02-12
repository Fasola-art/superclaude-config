import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { FavoritesClient } from '@/components/favorites/FavoritesClient';

export const metadata: Metadata = {
  title: '즐겨찾기 - 시장 브리핑',
  description: '즐겨찾기 종목',
};

export default function FavoritesPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <FavoritesClient />
    </Suspense>
  );
}
