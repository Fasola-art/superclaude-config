import { Suspense } from 'react';
import { CardSkeleton } from '@/components/ui';
import { FxClient } from '@/components/fx/FxClient';

export const metadata = {
  title: '외환 시장 - 마켓브리핑',
  description: '유로, 달러, 엔화, 파운드, 위안화 실시간 환율과 뉴스',
};

export default function FxPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <FxClient />
    </Suspense>
  );
}
