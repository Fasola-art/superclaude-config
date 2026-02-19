/** 테이블별 상세 설명 및 컬럼 정보 */
type TableInfo = {
  description: string;
  source: string;
  interval: string;
  columns: string[];
};

export const TABLE_INFO: Record<string, TableInfo> = {
  market_snapshots: {
    description: '해운/원자재/지수 등 주요 종목의 실시간 시세 스냅샷. 가격, 변동률, 거래량, 섹터 정보를 포함.',
    source: 'yfinance (Yahoo Finance)',
    interval: '1시간 주기 수집',
    columns: ['symbol', 'price', 'change_pct', 'volume', 'timestamp', 'metadata(sector, name)'],
  },
  trading_signals: {
    description: '모멘텀/감정분석/운임지수 전략 기반 자동 생성 매수·매도 신호. 신뢰도, 목표가, 손절가 포함.',
    source: 'signal_generator.py (자체 생성)',
    interval: '1시간 주기 생성',
    columns: ['symbol', 'signal_type', 'confidence', 'price', 'target_price', 'stop_loss', 'strategy', 'reason'],
  },
  market_news: {
    description: 'FinBERT 감정분석이 적용된 시장 뉴스. 주식/암호화폐/경제 카테고리별 긍정·부정 점수 포함.',
    source: 'Google News RSS + FinBERT',
    interval: '1시간 주기 수집',
    columns: ['title', 'summary', 'sentiment', 'category', 'source', 'symbols'],
  },
  crypto_prices: {
    description: 'Bitcoin, Ethereum 등 주요 암호화폐 실시간 시세 및 시가총액, 24시간 거래량 정보.',
    source: 'CoinGecko API',
    interval: '1시간 주기 수집',
    columns: ['symbol', 'price_usd', 'change_24h', 'market_cap', 'volume_24h'],
  },
  interest_rates: {
    description: '미국 국채 금리(2년/10년), 연방기금금리, 하이일드 스프레드 등 금리 데이터.',
    source: 'FRED (Federal Reserve)',
    interval: '일간 업데이트',
    columns: ['series_id', 'date', 'value', 'name'],
  },
  freight_indices: {
    description: 'BDI(Baltic Dry Index) 등 해상 운임 지수. 벌크 해운주 트레이딩 핵심 지표.',
    source: 'Trading Economics',
    interval: '일간 업데이트',
    columns: ['index_name', 'date', 'value', 'change_pct'],
  },
  economic_indicators: {
    description: 'CPI, 실업률, GDP, 소매판매 등 거시 경제 지표. FRED 시리즈 기반.',
    source: 'FRED API',
    interval: '발표 시 업데이트',
    columns: ['series_id', 'date', 'value', 'category', 'name'],
  },
};
