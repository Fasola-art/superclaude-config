import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { SignalsClient } from '@/components/signals';

export const metadata: Metadata = {
  title: '시그널 - 시장 브리핑',
  description: 'LLM 4-Agent 통합 트레이딩 시그널 대시보드',
};

export default function SignalsPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <SignalsClient />
    </Suspense>
  );
}
