import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { SearchClient } from '@/components/search/SearchClient';

export const metadata: Metadata = {
  title: '검색 - 시장 브리핑',
  description: '종목 및 키워드 검색',
};

export default function SearchPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <SearchClient />
    </Suspense>
  );
}
