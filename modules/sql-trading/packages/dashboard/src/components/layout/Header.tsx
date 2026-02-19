'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Search, Share2, Star, Moon, Sun } from 'lucide-react';
import { useTheme } from '@/lib/theme-provider';

export function Header() {
  const { theme, toggle } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <header className="sticky top-0 z-40 bg-[var(--bg)]/80 backdrop-blur-sm border-b border-[var(--border)]">
      <div className="max-w-[960px] mx-auto flex items-center justify-between px-5 h-14">
        <Link href="/" className="font-bold text-lg text-[var(--text)]">
          마켓브리핑
        </Link>

        <div className="flex items-center gap-3">
          <Link href="/search" className="p-2 hover:opacity-80" aria-label="검색">
            <Search size={20} className="text-[var(--text-muted)]" />
          </Link>
          <button className="p-2 hover:opacity-80" aria-label="공유">
            <Share2 size={20} className="text-[var(--text-muted)]" />
          </button>
          <Link href="/favorites" className="p-2 hover:opacity-80" aria-label="즐겨찾기">
            <Star size={20} className="text-[var(--text-muted)]" />
          </Link>
          <button onClick={toggle} className="p-2 hover:opacity-80" aria-label="테마 변경">
            {mounted ? (
              theme === 'dark'
                ? <Sun size={20} className="text-[var(--text-muted)]" />
                : <Moon size={20} className="text-[var(--text-muted)]" />
            ) : (
              <span className="block w-[20px] h-[20px]" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
