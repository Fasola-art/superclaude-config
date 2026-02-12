import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { NewsClient } from '@/components/news/NewsClient';

export const metadata: Metadata = {
  title: '뉴스 - 시장 브리핑',
  description: '시장 뉴스 및 분석',
};

export default function NewsPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <NewsClient />
    </Suspense>
  );
}
