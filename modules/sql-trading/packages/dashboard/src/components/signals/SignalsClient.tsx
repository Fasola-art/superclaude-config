'use client';

import { useLatestSignals, useStrategy } from '@/hooks';
import { Card, Badge, ConfidenceGauge, CardSkeleton } from '@/components/ui';
import { SignalNav } from './SignalNav';
import type { AgentConfidence, FinalScore } from '@/types/api';

export function SignalsClient() {
  const { data: signals, isLoading: signalsLoading } = useLatestSignals();
  const { data: strategy, isLoading: strategyLoading } = useStrategy();

  if (signalsLoading || strategyLoading) return <CardSkeleton />;

  // LLM 4-Agent 컨피던스 (Mock - 실제 API 연동 필요)
  const agentConfidence: AgentConfidence = {
    news: 0.72,
    macro: 0.68,
    tech: 0.85,
    signal: 0.78,
  };

  const finalScore: FinalScore = {
    score:
      agentConfidence.news * 0.25 +
      agentConfidence.macro * 0.25 +
      agentConfidence.tech * 0.3 +
      agentConfidence.signal * 0.2,
    action: agentConfidence.tech > 0.75 ? 'BUY' : agentConfidence.tech < 0.4 ? 'SELL' : 'HOLD',
    confidence: agentConfidence,
  };

  const latestSignals = signals?.slice(0, 10) || [];

  return (
    <div className="space-y-6">
      {/* LLM 4-Agent 컨피던스 */}
      <Card title="LLM 4-Agent 통합 분석">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <ConfidenceGauge value={agentConfidence.news} label="News Agent (25%)" size="md" />
          <ConfidenceGauge value={agentConfidence.macro} label="Macro Agent (25%)" size="md" />
          <ConfidenceGauge value={agentConfidence.tech} label="Tech Agent (30%)" size="md" />
          <ConfidenceGauge value={agentConfidence.signal} label="Signal Agent (20%)" size="md" />
        </div>

        <div className="flex items-center justify-between p-4 bg-card border border-border rounded-lg">
          <div>
            <div className="text-sm text-muted mb-1">최종 스코어</div>
            <div className="text-3xl font-bold">{(finalScore.score * 100).toFixed(1)}%</div>
          </div>
          <Badge variant={finalScore.action === 'BUY' ? 'up' : finalScore.action === 'SELL' ? 'down' : 'neutral'}>
            {finalScore.action}
          </Badge>
        </div>
      </Card>

      {/* 최근 시그널 */}
      <Card title="최근 시그널">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-b border-border">
              <tr>
                <th className="text-left p-2">시간</th>
                <th className="text-left p-2">심볼</th>
                <th className="text-left p-2">시그널</th>
                <th className="text-right p-2">신뢰도</th>
                <th className="text-left p-2">전략</th>
                <th className="text-left p-2">사유</th>
              </tr>
            </thead>
            <tbody>
              {latestSignals.map((signal, idx) => (
                <tr key={idx} className="border-b border-border/50">
                  <td className="p-2 text-muted">{new Date(signal.timestamp).toLocaleTimeString()}</td>
                  <td className="p-2 font-mono font-semibold">{signal.symbol}</td>
                  <td className="p-2">
                    <Badge variant={signal.signal_type === 'BUY' ? 'up' : signal.signal_type === 'SELL' ? 'down' : 'neutral'}>
                      {signal.signal_type}
                    </Badge>
                  </td>
                  <td className="p-2 text-right font-mono">{(Number(signal.confidence) * 100).toFixed(0)}%</td>
                  <td className="p-2 text-muted">{signal.strategy}</td>
                  <td className="p-2 text-xs text-muted truncate max-w-xs">{signal.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* 전략별 성과 요약 */}
      <Card title="전략별 성과 요약">
        <div className="grid md:grid-cols-3 gap-4">
          {strategy?.slice(0, 3).map((s) => (
            <div key={s.strategy} className="p-4 bg-card border border-border rounded-lg">
              <div className="font-semibold mb-2">{s.strategy}</div>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted">총 시그널</span>
                  <span>{s.total}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted">평균 신뢰도</span>
                  <span>{(Number(s.avg_confidence) * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* 하위 페이지 네비게이션 */}
      <SignalNav />
    </div>
  );
}
