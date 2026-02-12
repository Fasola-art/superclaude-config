'use client';

import { Card } from '@/components/ui';

const FR24_URL = 'https://www.flightradar24.com';

/** 실시간 항공기 추적 (Flightradar24 임베드) */
export function FlightsClient() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-[var(--text)]">항공 추적</h1>

      <Card className="p-0 overflow-hidden">
        <iframe
          src={FR24_URL}
          title="Flightradar24 실시간 항공 추적"
          className="w-full border-0"
          style={{ height: 'calc(100vh - 220px)', minHeight: '500px' }}
          allow="geolocation"
          loading="lazy"
          referrerPolicy="no-referrer"
        />
      </Card>

      <div className="flex gap-4 text-sm text-[var(--text-muted)]">
        <div className="flex items-center gap-1">
          <span className="inline-block w-3 h-3 rounded-full bg-[#f7c948]" />
          일반 항공
        </div>
        <div className="flex items-center gap-1">
          <span className="inline-block w-3 h-3 rounded-full bg-[#4fc3f7]" />
          화물 항공
        </div>
        <div className="flex items-center gap-1">
          <span className="inline-block w-3 h-3 rounded-full bg-[#ef5350]" />
          지연/긴급
        </div>
      </div>

      <p className="text-xs text-[var(--text-muted)]">
        데이터 제공: Flightradar24. 클릭하여 항공편 상세 정보를 확인할 수 있습니다.
        화물 항공 추적은 공급망 분석에 활용됩니다.
      </p>
    </div>
  );
}
