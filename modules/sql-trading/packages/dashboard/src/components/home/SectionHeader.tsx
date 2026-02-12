import Link from 'next/link';
import { ChevronRight } from 'lucide-react';

interface SectionHeaderProps {
  title: string;
  href: string;
  linkText?: string;
}

/** 섹션 제목 + "더보기" 링크 */
export function SectionHeader({ title, href, linkText = '더보기' }: SectionHeaderProps) {
  return (
    <div className="flex items-center justify-between mb-3">
      <h2 className="text-sm font-semibold text-[var(--text)]">{title}</h2>
      <Link
        href={href}
        className="flex items-center gap-0.5 text-xs text-[var(--accent)] hover:underline"
      >
        {linkText}
        <ChevronRight size={14} />
      </Link>
    </div>
  );
}
