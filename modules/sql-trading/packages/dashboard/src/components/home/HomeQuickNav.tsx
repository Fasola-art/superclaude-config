'use client';

import Link from 'next/link';
import {
  TrendingUp, Bitcoin, Building2, Package, Signal, Newspaper, DollarSign,
} from 'lucide-react';

const sections = [
  { href: '/stocks', icon: TrendingUp, label: '주식', desc: '글로벌 인덱스, 등락 상위', color: '#3b82f6' },
  { href: '/crypto', icon: Bitcoin, label: '코인', desc: 'BTC, ETH, 김프', color: '#f59e0b' },
  { href: '/fx', icon: DollarSign, label: '외환', desc: '달러, 유로, 엔, 위안', color: '#22c55e' },
  { href: '/realestate', icon: Building2, label: '부동산', desc: '매매/전세 지수, 금리', color: '#10b981' },
  { href: '/commodities', icon: Package, label: '원자재', desc: '유가, 운임, 물류', color: '#8b5cf6' },
  { href: '/signals', icon: Signal, label: '시그널', desc: '트레이딩 시그널, 전략', color: '#ef4444' },
  { href: '/news', icon: Newspaper, label: '뉴스', desc: '시장 뉴스, 분석', color: '#06b6d4' },
];

/** 홈 - 6개 섹션 빠른 이동 그리드 */
export function HomeQuickNav() {
  return (
    <section>
      <h2 className="text-sm font-semibold text-[var(--text)] mb-3">빠른 이동</h2>
      <div className="grid grid-cols-3 gap-3">
        {sections.map(({ href, icon: Icon, label, desc, color }) => (
          <Link
            key={href}
            href={href}
            className="flex flex-col items-center p-4 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl hover:border-[var(--accent)] transition group"
          >
            <Icon size={24} style={{ color }} className="mb-2 group-hover:scale-110 transition-transform" />
            <span className="text-sm font-semibold text-[var(--text)]">{label}</span>
            <span className="text-[10px] text-[var(--text-muted)] text-center mt-1">{desc}</span>
          </Link>
        ))}
      </div>
    </section>
  );
}
