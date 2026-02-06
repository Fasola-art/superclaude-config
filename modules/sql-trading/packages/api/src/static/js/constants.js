/**
 * 상수 및 설정
 */

export const API_BASE = '';

// 섹터 이름 매핑
export const SECTOR_NAMES = {
    'dry_bulk': { emoji: '🏭', name: '벌크선 (철광석/석탄/곡물)', desc: '원자재 운송' },
    'container': { emoji: '📦', name: '컨테이너선 (소비재/전자)', desc: '완제품 운송' },
    'tanker': { emoji: '🛢️', name: '유조선 (원유/LNG)', desc: '에너지 운송' },
    'commodity': { emoji: '💎', name: '원자재 ETF', desc: '원자재 가격' },
    'index': { emoji: '📊', name: '주요 지수', desc: '시장 전체' }
};

// 종목별 상세 정보
export const STOCK_INFO = {
    // Dry Bulk
    'SBLK': { name: 'Star Bulk', desc: '🏭 철광석/석탄 벌크선', commodity: '철광석, 석탄, 곡물' },
    'DSX': { name: 'Diana Shipping', desc: '🏭 건화물 벌크선', commodity: '철광석, 석탄' },
    'EGLE': { name: 'Eagle Bulk', desc: '🏭 중형 벌크선', commodity: '곡물, 시멘트, 비료' },
    'NMM': { name: 'Navios Partners', desc: '🏭 대형 벌크선', commodity: '철광석, 석탄' },
    'GNK': { name: 'Genco Shipping', desc: '🏭 건화물 전문', commodity: '철광석, 곡물, 보크사이트' },
    'GOGL': { name: 'Golden Ocean', desc: '🏭 초대형 벌크선', commodity: '철광석' },
    // Tanker
    'FRO': { name: 'Frontline', desc: '🛢️ 초대형 유조선', commodity: '원유 (VLCC)' },
    'STNG': { name: 'Scorpio Tankers', desc: '🛢️ 정제유 운반선', commodity: '휘발유, 경유, 제트유' },
    'TNK': { name: 'Teekay Tankers', desc: '🛢️ 중형 유조선', commodity: '원유, 정제유' },
    // Container
    'ZIM': { name: 'ZIM Shipping', desc: '📦 컨테이너선', commodity: '전자제품, 의류, 소비재' },
    'MATX': { name: 'Matson', desc: '📦 태평양 컨테이너', commodity: '소비재 (미국-아시아)' },
    'DAC': { name: 'Danaos Corp', desc: '📦 컨테이너 용선', commodity: '소비재, 전자제품' },
    // Commodity ETF
    'DBC': { name: 'DB Commodity', desc: '💎 원자재 종합', commodity: '원유, 금, 농산물 종합' },
    'GSG': { name: 'S&P GSCI', desc: '💎 원자재 지수', commodity: '에너지 비중 높음' },
    'DBA': { name: 'DB Agriculture', desc: '🌾 농산물 ETF', commodity: '옥수수, 대두, 밀, 설탕' },
    'DBB': { name: 'DB Base Metals', desc: '⚙️ 비철금속 ETF', commodity: '구리, 알루미늄, 아연' },
    // Index
    '^GSPC': { name: 'S&P 500', desc: '📊 미국 대형주', commodity: '시장 전체' },
    '^DJI': { name: '다우존스', desc: '📊 미국 우량주', commodity: '산업주 30개' },
    '^IXIC': { name: '나스닥', desc: '📊 기술주 중심', commodity: '기술/성장주' },
};

// 신호 텍스트
export const SIGNAL_TEXT = {
    'STRONG_BUY': '🔥 강력 매수',
    'BUY': '📈 매수',
    'STRONG_SELL': '💥 강력 매도',
    'SELL': '📉 매도',
    'OVERSOLD': '🔄 과매도'
};

// 경제지표 아이콘
export const INDICATOR_ICONS = {
    '금리': '📊',
    '신용': '💳',
    '에너지': '🛢️'
};

// 화물 유형 한글
export const CARGO_KR = {
    'container': '📦 컨테이너',
    'tanker': '🛢️ 유조선',
    'bulk': '🏭 벌크'
};

// 상태 색상
export const STATUS_COLORS = {
    'delivered': '#66bb6a',
    'delayed': '#ef5350',
    'in_transit': '#4fc3f7'
};

// 상태 한글
export const STATUS_KR = {
    'delivered': '도착 완료',
    'delayed': '지연',
    'in_transit': '운항 중'
};
