'use client';

import { useState } from 'react';
import { Card, Badge } from '@/components/ui';

const popularKeywords = ['삼성전자', '비트코인', '금리', '환율', '유가'];

export function SearchClient() {
  const [query, setQuery] = useState('');
  const [recentSearches, setRecentSearches] = useState<string[]>(() => {
    if (typeof window === 'undefined') return [];
    const stored = localStorage.getItem('recentSearches');
    if (!stored) return [];
    try {
      const parsed = JSON.parse(stored);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  });

  const handleSearch = (term: string) => {
    if (!term.trim()) return;

    const updated = [term, ...recentSearches.filter(s => s !== term)].slice(0, 5);
    setRecentSearches(updated);
    localStorage.setItem('recentSearches', JSON.stringify(updated));
    setQuery('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSearch(query);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-[var(--text)]">검색</h1>

      <Card>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="종목, 키워드 검색..."
          className="w-full px-4 py-3 bg-transparent border border-[var(--border)] rounded-md text-[var(--text)] placeholder:text-[var(--text-muted)] focus:outline-none focus:ring-2 focus:ring-[var(--accent)]"
        />
      </Card>

      <Card>
        <h2 className="font-semibold text-[var(--text)] mb-3">최근 검색어</h2>
        {recentSearches.length === 0 ? (
          <p className="text-sm text-[var(--text-muted)]">검색 기록이 없습니다</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {recentSearches.map((term, idx) => (
              <div key={idx} className="cursor-pointer" onClick={() => handleSearch(term)}>
                <Badge variant="neutral">{term}</Badge>
              </div>
            ))}
          </div>
        )}
      </Card>

      <Card>
        <h2 className="font-semibold text-[var(--text)] mb-3">인기 키워드</h2>
        <div className="flex flex-wrap gap-2">
          {popularKeywords.map((keyword, idx) => (
            <div key={idx} className="cursor-pointer" onClick={() => handleSearch(keyword)}>
              <Badge variant="accent">{keyword}</Badge>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
