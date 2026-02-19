'use client';

import { useStrategy } from '@/hooks';
import { Card, Badge, CardSkeleton } from '@/components/ui';
import { QuartileChart, SessionTimeline, EMAStatusBar } from '@/components/charts';

export function StrategyClient() {
  const { data: strategies, isLoading, error } = useStrategy();

  if (isLoading) return <CardSkeleton />;
  if (error) {
    return (
      <Card>
        <div className="text-[var(--down)]">전략 데이터를 불러오지 못했습니다.</div>
      </Card>
    );
  }

  // Mock 데이터 (실제 API 연동 필요)
  const priceData = {
    current: 185.42,
    dayLow: 183.15,
    dayHigh: 186.98,
  };

  const emaData = {
    current: 185.42,
    ema360: 184.2,
    ema720: 183.5,
    ema1440: 182.8,
    ema2880: 181.6,
  };

  return (
    <div className="space-y-6">
      {/* 4분할 가격 레벨 */}
      <Card title="4분할 가격 레벨 (전일 범위 기준)">
        <QuartileChart current={priceData.current} dayLow={priceData.dayLow} dayHigh={priceData.dayHigh} />
      </Card>

      {/* 세션 타임라인 */}
      <Card title="세션 타임라인 (KST)">
        <SessionTimeline />
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
          <div className="p-2 bg-blue-500/10 rounded">
            <div className="font-semibold">아시아</div>
            <div className="text-muted">09:00 - 15:30</div>
          </div>
          <div className="p-2 bg-green-500/10 rounded">
            <div className="font-semibold">런던 Open</div>
            <div className="text-muted">16:00</div>
          </div>
          <div className="p-2 bg-purple-500/10 rounded">
            <div className="font-semibold">뉴욕 Open</div>
            <div className="text-muted">22:30</div>
          </div>
          <div className="p-2 bg-yellow-500/10 rounded">
            <div className="font-semibold">런던 Fix</div>
            <div className="text-muted">00:00</div>
          </div>
        </div>
      </Card>

      {/* EMA 상태 */}
      <Card title="EMA 정배열 상태">
        <EMAStatusBar
          current={emaData.current}
          ema360={emaData.ema360}
          ema720={emaData.ema720}
          ema1440={emaData.ema1440}
          ema2880={emaData.ema2880}
        />
      </Card>

      {/* 전략별 성과 테이블 */}
      <Card title="전략별 성과">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-border">
              <tr>
                <th className="text-left p-2">전략</th>
                <th className="text-right p-2">총 시그널</th>
                <th className="text-right p-2">매수</th>
                <th className="text-right p-2">매도</th>
                <th className="text-right p-2">평균 신뢰도</th>
              </tr>
            </thead>
            <tbody>
              {strategies?.map((s) => (
                <tr key={s.strategy} className="border-b border-border/50">
                  <td className="p-2 font-semibold">{s.strategy}</td>
                  <td className="p-2 text-right font-mono">{s.total}</td>
                  <td className="p-2 text-right">
                    <Badge variant="up">{s.buys}</Badge>
                  </td>
                  <td className="p-2 text-right">
                    <Badge variant="down">{s.sells}</Badge>
                  </td>
                  <td className="p-2 text-right font-mono">{(s.avg_confidence * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
