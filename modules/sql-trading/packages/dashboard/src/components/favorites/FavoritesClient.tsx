'use client';

import { useState } from 'react';
import { Card, Badge } from '@/components/ui';

interface FavoriteItem {
  symbol: string;
  price?: number;
  change?: number;
}

export function FavoritesClient() {
  const [favorites, setFavorites] = useState<string[]>(() => {
    if (typeof window === 'undefined') return [];
    const stored = localStorage.getItem('favorites');
    if (!stored) return [];
    try {
      const parsed = JSON.parse(stored);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  });

  const removeFavorite = (symbol: string) => {
    const updated = favorites.filter(s => s !== symbol);
    setFavorites(updated);
    localStorage.setItem('favorites', JSON.stringify(updated));
  };

  const mockData: Record<string, FavoriteItem> = {
    '삼성전자': { symbol: '삼성전자', price: 72500, change: 1.2 },
    'AAPL': { symbol: 'AAPL', price: 185.5, change: -0.5 },
    'BTC': { symbol: 'BTC', price: 65000, change: 3.4 },
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-[var(--text)]">즐겨찾기</h1>

      {favorites.length === 0 ? (
        <Card>
          <p className="text-[var(--text-muted)]">
            즐겨찾기한 종목이 없습니다. 종목 페이지에서 별 아이콘을 클릭하여 추가하세요.
          </p>
        </Card>
      ) : (
        <div className="grid gap-4">
          {favorites.map((symbol) => {
            const data = mockData[symbol] || { symbol, price: undefined, change: undefined };

            return (
              <Card key={symbol}>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-[var(--text)]">{data.symbol}</h3>
                    {data.price && (
                      <div className="flex items-center gap-2 mt-1">
                        <span className="font-mono text-[var(--text)]">
                          {data.price.toLocaleString()}
                        </span>
                        {data.change !== undefined && (
                          <Badge variant={data.change >= 0 ? 'up' : 'down'}>
                            {data.change >= 0 ? '+' : ''}{data.change.toFixed(2)}%
                          </Badge>
                        )}
                      </div>
                    )}
                  </div>

                  <button
                    onClick={() => removeFavorite(symbol)}
                    className="text-[var(--text-muted)] hover:text-[var(--down)] transition-colors"
                  >
                    제거
                  </button>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
