'use client';

import { useEffect, useMemo, useRef } from 'react';
import { createChart, CandlestickSeries, type UTCTimestamp } from 'lightweight-charts';
import type { FxCandle } from '@/types/api';

interface FxChartProps {
  bars: FxCandle[];
}

export function FxChart({ bars }: FxChartProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);

  const data = useMemo(() => bars.map((b) => ({
    time: b.t as UTCTimestamp,
    open: b.o,
    high: b.h,
    low: b.l,
    close: b.c,
  })), [bars]);

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      height: 320,
      layout: {
        textColor: 'var(--text)',
        background: { color: 'transparent' },
      },
      grid: {
        vertLines: { color: 'rgba(148, 163, 184, 0.15)' },
        horzLines: { color: 'rgba(148, 163, 184, 0.15)' },
      },
      timeScale: {
        borderColor: 'rgba(148, 163, 184, 0.3)',
      },
      rightPriceScale: {
        borderColor: 'rgba(148, 163, 184, 0.3)',
      },
    });

    const series = chart.addSeries(CandlestickSeries, {
      upColor: '#16a34a',
      downColor: '#dc2626',
      borderUpColor: '#16a34a',
      borderDownColor: '#dc2626',
      wickUpColor: '#16a34a',
      wickDownColor: '#dc2626',
    });

    series.setData(data);

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        chart.applyOptions({ width: entry.contentRect.width });
      }
    });
    resizeObserver.observe(containerRef.current);

    return () => {
      resizeObserver.disconnect();
      chart.remove();
    };
  }, [data]);

  return <div ref={containerRef} className="w-full" />;
}
