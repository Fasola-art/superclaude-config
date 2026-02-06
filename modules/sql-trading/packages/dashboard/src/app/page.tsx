'use client';

import { useGetSummaryApiSummaryGet } from '@/api/endpoints/default/default';
import { SummaryCard, SectorsChart } from '@/components/cards';
import { SignalsTable, StocksTable } from '@/components/tables';
import type { SummaryData } from '@/types/api';

export default function DashboardPage() {
  const { data: summaryRes, isLoading } = useGetSummaryApiSummaryGet();
  const summary = summaryRes?.data as SummaryData | undefined;

  return (
    <main className="min-h-screen bg-gray-950 text-white p-6">
      <header className="mb-8">
        <h1 className="text-3xl font-bold">SQL Trading Dashboard</h1>
        <p className="text-gray-400">
          {isLoading ? '로딩 중...' : `마지막 업데이트: ${summary?.last_update || '-'}`}
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <SummaryCard
          title="총 레코드"
          value={summary?.total_records ?? 0}
          color="blue"
        />
        <SummaryCard
          title="매수 신호"
          value={summary?.buy_signals ?? 0}
          color="green"
        />
        <SummaryCard
          title="매도 신호"
          value={summary?.sell_signals ?? 0}
          color="red"
        />
        <SummaryCard
          title="서버 시간"
          value={summary?.server_time?.slice(11, 19) ?? '-'}
          color="purple"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <section className="bg-gray-900 rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-4">트레이딩 신호</h2>
          <SignalsTable />
        </section>

        <section className="bg-gray-900 rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-4">섹터별 현황</h2>
          <SectorsChart />
        </section>
      </div>

      <section className="bg-gray-900 rounded-lg p-4">
        <h2 className="text-xl font-semibold mb-4">종목 현황</h2>
        <StocksTable />
      </section>
    </main>
  );
}
