'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Home, TrendingUp, Bitcoin, Building2,
  Package, Signal, Settings,
} from 'lucide-react';

const tabs = [
  { href: '/', icon: Home, label: '홈' },
  { href: '/stocks', icon: TrendingUp, label: '주식' },
  { href: '/crypto', icon: Bitcoin, label: '코인' },
  { href: '/realestate', icon: Building2, label: '부동산' },
  { href: '/commodities', icon: Package, label: '원자재' },
  { href: '/signals', icon: Signal, label: '시그널' },
  { href: '/settings', icon: Settings, label: '설정' },
];

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-[var(--bg-nav)] border-t border-[var(--border)] z-50">
      <div className="max-w-[960px] mx-auto flex justify-around">
        {tabs.map(({ href, icon: Icon, label }) => {
          const active = href === '/' ? pathname === '/' : pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={`flex flex-col items-center py-2 px-1 text-xs transition-colors
                ${active ? 'text-[var(--accent)]' : 'text-[var(--text-muted)]'}`}
            >
              <Icon size={20} strokeWidth={active ? 2.5 : 1.5} />
              <span className="mt-1">{label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
