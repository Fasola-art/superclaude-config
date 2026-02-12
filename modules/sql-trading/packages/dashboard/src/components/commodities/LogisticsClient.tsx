'use client';

import dynamic from 'next/dynamic';
import { useLogistics } from '@/hooks';
import { Card, Badge } from '@/components/ui';

/* Leaflet은 SSR 미지원 → dynamic import */
const ShippingMap = dynamic(() => import('./ShippingMap'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[460px] rounded-lg border border-[var(--border)] bg-[var(--card)] flex items-center justify-center text-[var(--text-muted)]">
      지도 로딩 중...
    </div>
  ),
});

const statusVariant = {
  in_transit: 'info',
  delayed: 'warning',
  delivered: 'success',
  customs: 'accent',
} as const;

export function LogisticsClient() {
  const { data, isLoading, error } = useLogistics();

  if (isLoading) return <div className="text-[var(--text-muted)]">로딩 중...</div>;
  if (error) return <div className="text-[var(--down)]">에러 발생</div>;
  if (!data || data.length === 0) return <div className="text-[var(--text-muted)]">데이터 없음</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-[var(--text)]">
        물류 추적 <span className="text-sm font-normal text-[var(--text-muted)]">({data.length}건)</span>
      </h1>

      {/* 해상 지도 */}
      <ShippingMap data={data} />

      {/* 카드 리스트 */}
      <div className="grid gap-4 md:grid-cols-2">
        {data.map((item) => (
          <Card key={item.shipment_id}>
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-semibold text-[var(--text)]">{item.shipment_id}</h3>
                <p className="text-sm text-[var(--text-muted)]">{item.vessel_name}</p>
              </div>
              <Badge variant={statusVariant[item.status as keyof typeof statusVariant] || 'neutral'}>
                {item.status}
              </Badge>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-[var(--text-muted)]">출발항: </span>
                <span className="text-[var(--text)]">{item.origin_port}</span>
              </div>
              <div>
                <span className="text-[var(--text-muted)]">도착항: </span>
                <span className="text-[var(--text)]">{item.dest_port}</span>
              </div>
              <div>
                <span className="text-[var(--text-muted)]">화물: </span>
                <span className="text-[var(--text)]">{item.cargo_type}</span>
              </div>
              <div>
                <span className="text-[var(--text-muted)]">예상도착: </span>
                <span className="text-[var(--text)]">
                  {item.estimated_arrival
                    ? new Date(item.estimated_arrival).toLocaleDateString('ko-KR')
                    : '-'}
                </span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
