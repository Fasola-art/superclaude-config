/** 종목 티커 → 한글 설명 매핑 */
export const SIGNAL_NAMES: Record<string, string> = {
  SBLK: 'Star Bulk | 벌크 해운', DSX: 'Diana Shipping | 벌크 해운',
  EGLE: 'Eagle Bulk | 벌크 해운', NMM: 'Navios Maritime | 벌크 해운',
  GNK: 'Genco Shipping | 벌크 해운',
  ZIM: 'ZIM Shipping | 컨테이너 해운', MATX: 'Matson | 컨테이너 해운',
  DAC: 'Danaos | 컨테이너 해운',
  FRO: 'Frontline | 유조선', STNG: 'Scorpio Tankers | 유조선',
  TNK: 'Teekay Tankers | 유조선',
  DBC: 'Invesco DB Commodity | 원자재 ETF', GSG: 'iShares GSCI | 원자재 ETF',
  DBA: 'Invesco Agriculture | 농산물 ETF', DBB: 'Invesco Base Metals | 비철금속 ETF',
  '^GSPC': 'S&P 500 | 미국 대형주', '^DJI': 'Dow Jones | 미국 산업주',
  '^IXIC': 'NASDAQ | 미국 기술주',
  BTC: 'Bitcoin | 암호화폐', ETH: 'Ethereum | 암호화폐',
};

type SectorMapping = { cats: string[]; keywords: string[] };

/** 종목 → 뉴스 매칭용 카테고리/키워드 */
export const SECTOR_NEWS: Record<string, SectorMapping> = {
  SBLK: { cats: ['stocks'], keywords: ['shipping', 'freight', 'bulk', 'BDI'] },
  DSX: { cats: ['stocks'], keywords: ['shipping', 'freight', 'bulk'] },
  EGLE: { cats: ['stocks'], keywords: ['shipping', 'freight', 'bulk'] },
  NMM: { cats: ['stocks'], keywords: ['shipping', 'maritime'] },
  GNK: { cats: ['stocks'], keywords: ['shipping', 'freight', 'bulk'] },
  ZIM: { cats: ['stocks'], keywords: ['shipping', 'container', 'supply chain'] },
  MATX: { cats: ['stocks'], keywords: ['shipping', 'container', 'logistics'] },
  DAC: { cats: ['stocks'], keywords: ['shipping', 'container'] },
  FRO: { cats: ['stocks', 'economy'], keywords: ['oil', 'tanker', 'energy'] },
  STNG: { cats: ['stocks', 'economy'], keywords: ['oil', 'tanker', 'energy'] },
  TNK: { cats: ['stocks', 'economy'], keywords: ['oil', 'tanker', 'energy'] },
  DBC: { cats: ['economy'], keywords: ['commodity', 'inflation'] },
  '^GSPC': { cats: ['stocks'], keywords: [] },
  BTC: { cats: ['crypto'], keywords: [] },
};
