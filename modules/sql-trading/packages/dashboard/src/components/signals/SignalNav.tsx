'use client';

import Link from 'next/link';
import { Activity, FlaskConical, ShieldAlert, FileText } from 'lucide-react';

const navItems = [
  { href: '/signals/strategy', icon: Activity, title: '전략 현황', desc: '4분할 가격 레벨, EMA 상태' },
  { href: '/signals/backtest', icon: FlaskConical, title: '백테스트', desc: '전략별 백테스트 결과' },
  { href: '/signals/risk', icon: ShieldAlert, title: '리스크 모니터', desc: '서킷브레이커, MDD 추적' },
  { href: '/signals/paper', icon: FileText, title: '페이퍼 트레이딩', desc: '모의 거래 기록' },
];

export function SignalNav() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {navItems.map(({ href, icon: Icon, title, desc }) => (
        <Link
          key={href}
          href={href}
          className="p-4 bg-[var(--bg-card)] border border-[var(--border)] rounded-lg hover:border-[var(--accent)] transition"
        >
          <Icon size={18} className="text-[var(--accent)] mb-2" />
          <div className="font-semibold text-sm mb-1">{title}</div>
          <div className="text-xs text-[var(--text-muted)]">{desc}</div>
        </Link>
      ))}
    </div>
  );
}
