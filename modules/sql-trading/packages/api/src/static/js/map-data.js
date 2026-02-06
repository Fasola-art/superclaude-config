/**
 * 지도 데이터 (항구, 좌표, 항로)
 */

// 주요 항구 목록
export const PORTS = [
    // 아시아
    { name: "🇨🇳 상하이", code: "Shanghai", lat: 31.2, lng: 121.5, color: "#66bb6a" },
    { name: "🇨🇳 칭다오", code: "Qingdao", lat: 36.1, lng: 120.4, color: "#66bb6a" },
    { name: "🇨🇳 홍콩", code: "Hong Kong", lat: 22.3, lng: 114.2, color: "#66bb6a" },
    { name: "🇯🇵 도쿄", code: "Tokyo", lat: 35.6, lng: 139.7, color: "#ff7043" },
    { name: "🇯🇵 요코하마", code: "Yokohama", lat: 35.4, lng: 139.6, color: "#ff7043" },
    { name: "🇰🇷 부산", code: "Busan", lat: 35.1, lng: 129.0, color: "#f06292" },
    { name: "🇸🇬 싱가포르", code: "Singapore", lat: 1.3, lng: 103.8, color: "#ffb74d" },
    { name: "🇮🇳 첸나이", code: "Chennai", lat: 13.1, lng: 80.3, color: "#ce93d8" },
    // 미국
    { name: "🇺🇸 로스앤젤레스", code: "Los Angeles", lat: 33.7, lng: -118.3, color: "#4fc3f7" },
    { name: "🇺🇸 롱비치", code: "Long Beach", lat: 33.8, lng: -118.2, color: "#4fc3f7" },
    { name: "🇺🇸 시애틀", code: "Seattle", lat: 47.6, lng: -122.3, color: "#4fc3f7" },
    { name: "🇺🇸 뉴욕", code: "New York", lat: 40.7, lng: -74.0, color: "#4fc3f7" },
    { name: "🇺🇸 사바나", code: "Savannah", lat: 32.1, lng: -81.1, color: "#4fc3f7" },
    // 유럽
    { name: "🇳🇱 로테르담", code: "Rotterdam", lat: 51.9, lng: 4.5, color: "#ba68c8" },
    { name: "🇩🇪 함부르크", code: "Hamburg", lat: 53.5, lng: 10.0, color: "#ba68c8" },
    { name: "🇧🇪 앤트워프", code: "Antwerp", lat: 51.2, lng: 4.4, color: "#ba68c8" },
    { name: "🇮🇹 제노바", code: "Genoa", lat: 44.4, lng: 8.9, color: "#ba68c8" },
    // 중동
    { name: "🇸🇦 라스타누라", code: "Ras Tanura", lat: 26.6, lng: 50.2, color: "#ffd54f" },
    { name: "🇰🇼 쿠웨이트", code: "Kuwait", lat: 29.4, lng: 47.9, color: "#ffd54f" },
    { name: "🇪🇬 포트사이드", code: "Port Said", lat: 31.3, lng: 32.3, color: "#ffd54f" },
    // 호주/남미/아프리카
    { name: "🇦🇺 포트헤들랜드", code: "Port Hedland", lat: -20.3, lng: 118.6, color: "#a1887f" },
    { name: "🇦🇺 뉴캐슬", code: "Newcastle", lat: -32.9, lng: 151.8, color: "#a1887f" },
    { name: "🇧🇷 산토스", code: "Santos", lat: -23.9, lng: -46.3, color: "#81c784" },
    { name: "🇿🇦 더반", code: "Durban", lat: -29.9, lng: 31.0, color: "#90a4ae" },
    { name: "🇳🇬 라고스", code: "Lagos", lat: 6.5, lng: 3.4, color: "#90a4ae" },
];

// 항구 좌표
export const PORT_COORDS = {
    'Shanghai': [31.2, 121.5], 'Busan': [35.1, 129.0], 'Tokyo': [35.6, 139.7],
    'Yokohama': [35.4, 139.6], 'Hong Kong': [22.3, 114.2], 'Singapore': [1.3, 103.8],
    'Qingdao': [36.0, 120.3], 'Chennai': [13.0, 80.3],
    'Los Angeles': [33.7, -118.3], 'Long Beach': [33.75, -118.2], 'Seattle': [47.6, -122.4],
    'New York': [40.6, -74.0], 'Savannah': [32.0, -81.0],
    'Rotterdam': [51.9, 4.5], 'Hamburg': [53.5, 9.9], 'Antwerp': [51.2, 4.4], 'Genoa': [44.4, 8.9],
    'Ras Tanura': [26.6, 50.0], 'Kuwait': [29.3, 48.0], 'Port Said': [31.2, 32.3],
    'Port Hedland': [-20.3, 118.6], 'Newcastle': [-32.9, 151.8],
};

// 해상 경유지
export const SEA_WAYPOINTS = {
    'malacca': [1.3, 103.8], 'suez_n': [31.2, 32.3], 'suez_s': [29.9, 32.5],
    'aden': [12.8, 45.0], 'hormuz': [26.5, 56.5], 'pacific_mid': [25.0, 180.0],
    'pacific_n': [40.0, -170.0], 'atlantic_n': [45.0, -40.0], 'cape_good': [-34.0, 18.5],
    'indian_mid': [0.0, 75.0], 'south_china': [15.0, 115.0], 'east_china': [30.0, 125.0],
    'japan_south': [30.0, 135.0], 'med_east': [35.0, 25.0], 'med_west': [36.0, 5.0], 'biscay': [45.0, -5.0],
};

// 항로 경유지
export const ROUTE_WAYPOINTS = {
    // 아시아 → 미국 서해안
    'Shanghai_Los Angeles': ['east_china', [35, 140], [40, 160], [42, 175], [42, 190], [40, 210], [36, 230]],
    'Shanghai_Long Beach': ['east_china', [35, 140], [40, 160], [42, 175], [42, 190], [40, 210], [36, 230]],
    'Busan_Seattle': [[37, 135], [42, 155], [45, 175], [48, 190], [50, 210], [50, 225]],
    'Busan_Long Beach': [[37, 135], [40, 155], [42, 175], [42, 190], [40, 210], [36, 230]],
    'Tokyo_Los Angeles': [[35, 145], [40, 160], [42, 175], [42, 190], [40, 210], [36, 230]],
    'Hong Kong_Los Angeles': ['south_china', [25, 130], [35, 145], [40, 165], [42, 180], [42, 195], [40, 215], [36, 235]],
    // 아시아 → 유럽
    'Singapore_Rotterdam': ['indian_mid', 'aden', 'suez_s', 'suez_n', 'med_east', 'med_west', 'biscay'],
    'Chennai_Antwerp': ['indian_mid', 'aden', 'suez_s', 'suez_n', 'med_east', 'med_west', 'biscay'],
    'Hong Kong_Rotterdam': ['south_china', 'malacca', 'indian_mid', 'aden', 'suez_s', 'suez_n', 'med_east', 'med_west', 'biscay'],
    'Shanghai_Rotterdam': ['east_china', 'south_china', 'malacca', 'indian_mid', 'aden', 'suez_s', 'suez_n', 'med_east', 'med_west', 'biscay'],
    'Singapore_Hamburg': ['indian_mid', 'aden', 'suez_s', 'suez_n', 'med_east', 'med_west', 'biscay'],
    // 중동 → 아시아
    'Ras Tanura_Yokohama': ['hormuz', [20, 65], 'indian_mid', 'malacca', 'south_china', 'east_china'],
    'Ras Tanura_Singapore': ['hormuz', [20, 65], 'indian_mid'],
    'Ras Tanura_Shanghai': ['hormuz', [20, 65], 'indian_mid', 'malacca', 'south_china', 'east_china'],
    'Kuwait_Singapore': ['hormuz', [20, 60], 'indian_mid'],
    // 호주 → 아시아
    'Port Hedland_Qingdao': [[-15, 115], [0, 115], 'south_china', 'east_china'],
    'Port Hedland_Shanghai': [[-15, 115], [0, 115], 'south_china', 'east_china'],
    'Newcastle_Shanghai': [[-30, 155], [-20, 140], [0, 130], 'south_china', 'east_china'],
    // 유럽 → 미국
    'Rotterdam_New York': ['biscay', [50, -10], [48, -25], [45, -40], [43, -55], [41, -70]],
    'Rotterdam_Savannah': ['biscay', [48, -15], [44, -30], [40, -45], [36, -60], [33, -75]],
    'Hamburg_New York': [[54, 5], [52, -5], [50, -15], [48, -30], [45, -45], [42, -60], [41, -70]],
    // 미국 → 아시아
    'Los Angeles_Shanghai': [[35, -125], [38, -140], [42, -165], [42, -185], [40, -200], [38, -215], [35, -230]],
    'Los Angeles_Tokyo': [[35, -125], [38, -140], [42, -165], [42, -185], [40, -200], [37, -215]],
    'Seattle_Busan': [[48, -130], [50, -150], [50, -175], [48, -185], [45, -200], [40, -215], [37, -228]],
};
