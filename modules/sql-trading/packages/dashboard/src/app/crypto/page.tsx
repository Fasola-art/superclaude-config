import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { CryptoClient } from '@/components/crypto/CryptoClient';

export const metadata: Metadata = {
  title: '암호화폐 - 시장 브리핑',
  description: '암호화폐 시장 현황',
};

export default function CryptoPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <CryptoClient />
    </Suspense>
  );
}
