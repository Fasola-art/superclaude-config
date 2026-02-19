'use client';

import Link from 'next/link';
import { useOilPrices, useFreight } from '@/hooks';
import { Card, MetricCard, ChangeIndicator } from '@/components/ui';

export function CommoditiesClient() {
  const { data: oilData, isLoading: oilLoading } = useOilPrices();
  const { data: freightData, isLoading: freightLoading } = useFreight();

  if (oilLoading || freightLoading) {
    return <div className="text-[var(--text-muted)]">로딩 중...</div>;
  }

  const wti = oilData?.find(d => d.series_id.includes('WTI'));
  const brent = oilData?.find(d => d.series_id.includes('Brent'));

  const bdi = freightData?.find(d => d.index_name === 'BDI');
  const fbxChina = freightData?.find(d => d.route?.includes('China'));

  const wtiValue = wti?.value;
  const brentValue = brent?.value;
  const bdiValue = bdi?.value;
  const fbxChinaValue = fbxChina?.value;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-[var(--text)]">원자재 시장</h1>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          label="WTI 원유"
          value={wtiValue != null ? `$${wtiValue.toFixed(2)} /배럴` : '-'}
          change={wti?.change_pct}
        />
        <MetricCard
          label="Brent 원유"
          value={brentValue != null ? `$${brentValue.toFixed(2)} /배럴` : '-'}
          change={brent?.change_pct}
        />
        <MetricCard
          label="BDI 지수"
          value={bdiValue != null ? bdiValue.toFixed(0) : '-'}
          change={bdi?.change_pct}
        />
        <MetricCard
          label="FBX China"
          value={fbxChinaValue != null ? `$${fbxChinaValue.toFixed(0)}` : '-'}
          change={fbxChina?.change_pct}
        />
      </div>

      <Card>
        <h2 className="text-lg font-semibold mb-4 text-[var(--text)]">주요 운임 지수</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[var(--border)]">
                <th className="text-left p-2 text-[var(--text-muted)]">지수</th>
                <th className="text-left p-2 text-[var(--text-muted)]">항로</th>
                <th className="text-right p-2 text-[var(--text-muted)]">현재가</th>
                <th className="text-right p-2 text-[var(--text-muted)]">변동률</th>
              </tr>
            </thead>
            <tbody>
              {freightData?.slice(0, 5).map((item, idx) => (
                <tr key={idx} className="border-b border-[var(--border)]">
                  <td className="p-2 text-[var(--text)]">{item.index_name}</td>
                  <td className="p-2 text-[var(--text-muted)]">{item.route}</td>
                  <td className="p-2 text-right text-[var(--text)]">${item.value.toFixed(0)}</td>
                  <td className="p-2 text-right">
                    <ChangeIndicator value={item.change_pct}  />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Link href="/commodities/freight">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <h3 className="font-semibold text-[var(--text)]">운임 지수</h3>
            <p className="text-sm text-[var(--text-muted)] mt-2">해운 운임 지수 상세</p>
          </Card>
        </Link>
        <Link href="/commodities/logistics">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <h3 className="font-semibold text-[var(--text)]">물류 추적</h3>
            <p className="text-sm text-[var(--text-muted)] mt-2">실시간 선박 위치</p>
          </Card>
        </Link>
        <Link href="/commodities/trade">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <h3 className="font-semibold text-[var(--text)]">무역 통계</h3>
            <p className="text-sm text-[var(--text-muted)] mt-2">글로벌 무역 데이터</p>
          </Card>
        </Link>
        <Link href="/commodities/flights">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <h3 className="font-semibold text-[var(--text)]">항공 추적</h3>
            <p className="text-sm text-[var(--text-muted)] mt-2">실시간 항공기 위치</p>
          </Card>
        </Link>
      </div>
    </div>
  );
}
