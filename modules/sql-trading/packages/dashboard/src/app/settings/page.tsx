import { Suspense } from 'react';
import { Metadata } from 'next';
import { CardSkeleton } from '@/components/ui';
import { SettingsClient } from '@/components/settings/SettingsClient';

export const metadata: Metadata = {
  title: '설정 - 시장 브리핑',
  description: '앱 설정',
};

export default function SettingsPage() {
  return (
    <Suspense fallback={<CardSkeleton />}>
      <SettingsClient />
    </Suspense>
  );
}
