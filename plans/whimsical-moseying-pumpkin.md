# 대시보드 데이터 수정 + 물류 지도 + 항공 추적 구현

## Context

대시보드에 데이터가 0으로 표시되는 미구현 섹션이 있음. 원인은 프론트엔드 심볼과 DB 심볼 불일치. 이전 SQL 대시보드에 구현된 Leaflet 물류 지도를 React로 포팅 필요. 실시간 항공기 추적(Flightradar24) 연동 추가.

---

## 1. 심볼 매핑 수정 (홈 화면 0 데이터 해결)

**문제**: `HomeMarketPreview.tsx:13`에서 `['KOSPI', 'SPX', 'IXIC', 'DJI']`로 필터링하지만, DB에는 `^GSPC`, `^IXIC`, `^DJI` 저장. KOSPI(`^KS11`)는 DB에 없음.

**수정 파일**: `components/home/HomeMarketPreview.tsx`

```
변경:
- stockSymbols = ['KOSPI', 'SPX', 'IXIC', 'DJI']
+ stockSymbols = ['^GSPC', '^IXIC', '^DJI']
```

API(`routers/stocks.py:11`)는 `^GSPC, ^IXIC, ^DJI, ^KS11` 등 8개 조회 → 프론트에서 받은 symbol 그대로 매칭하면 해결.

**추가**: `StocksClient.tsx`는 API 응답을 그대로 표시 → 수정 불필요.

---

## 2. Leaflet 물류 지도 (React 포팅)

**기존 자산**:
- `api/src/static/js/map-data.js` — 25개 항구 (PORTS), 좌표 (PORT_COORDS), 92개 해상 항로 (ROUTE_WAYPOINTS)
- `api/src/static/js/map.js` — initMap, createSeaRoute, renderLogistics 등
- `api/src/static/js/constants.js` — STATUS_COLORS, CARGO_KR, STATUS_KR

**DB 데이터**: `logistics_tracking` 15건 (lat/lng, origin_port, dest_port, status 포함)

**신규 파일**:

| 파일 | 설명 | 줄수 |
|------|------|------|
| `components/commodities/map-data.ts` | PORTS, PORT_COORDS, SEA_WAYPOINTS, ROUTE_WAYPOINTS (TS 타입 변환) | ~90 |
| `components/commodities/ShippingMap.tsx` | React Leaflet 지도 (dynamic import, SSR 비활성화) | ~100 |
| `components/commodities/LogisticsClient.tsx` | 기존 수정: 지도 추가 + 카드 리스트 유지 | ~90 |

**구현 방식**:
- `react-leaflet` + `leaflet` 패키지 설치
- `dynamic(() => import('./ShippingMap'), { ssr: false })` — Leaflet은 SSR 미지원
- 25개 항구 마커 (CircleMarker, 색상별 지역 구분)
- DB 물류 데이터 → 선박 마커 (아이콘/색상으로 상태 표시)
- 출발항-도착항 해상 항로 Polyline (ROUTE_WAYPOINTS 활용)
- 항구 클릭 시 팝업 (항구명, 국가)

**기존 map.js 로직 재활용**:
- 태평양 경도 래핑 (`lng > 180 → lng - 360`)
- 항로 경유지 해석 (`string → SEA_WAYPOINTS[key]`, `array → 그대로 사용`)

---

## 3. Flightradar24 항공 추적 연동

**방식**: iframe 임베드 (API 키 불필요, 무료)

**신규 파일**:

| 파일 | 설명 | 줄수 |
|------|------|------|
| `app/commodities/flights/page.tsx` | 라우트 페이지 | ~20 |
| `components/commodities/FlightsClient.tsx` | FR24 iframe + 안내 텍스트 | ~50 |

**iframe URL**: `https://www.flightradar24.com` (전체 화면 임베드)

**CommoditiesClient.tsx 수정**: 네비게이션에 "항공 추적" 카드 추가 (기존 3개 → 4개 그리드)

---

## 수정 파일 요약

| 파일 | 작업 | 유형 |
|------|------|------|
| `components/home/HomeMarketPreview.tsx` | 심볼 매핑 수정 | 수정 |
| `components/commodities/map-data.ts` | 항구/항로 TS 데이터 | 신규 |
| `components/commodities/ShippingMap.tsx` | React Leaflet 지도 | 신규 |
| `components/commodities/LogisticsClient.tsx` | 지도 통합 | 수정 |
| `app/commodities/flights/page.tsx` | 항공 추적 라우트 | 신규 |
| `components/commodities/FlightsClient.tsx` | FR24 iframe | 신규 |
| `components/commodities/CommoditiesClient.tsx` | 네비 카드 추가 | 수정 |

**패키지 설치**: `pnpm add react-leaflet leaflet @types/leaflet`

---

## 검증

```bash
# 1. 패키지 설치
cd packages/dashboard && pnpm add react-leaflet leaflet && pnpm add -D @types/leaflet

# 2. 빌드 확인
pnpm build

# 3. 개발 서버 실행
pnpm dev

# 4. 확인 항목
# - / (홈): 주식 시장 섹션에 S&P, 나스닥, 다우 데이터 표시 (0 아님)
# - /commodities/logistics: 25개 항구 마커 + 선박 위치 + 해상 항로 표시
# - /commodities/flights: Flightradar24 실시간 항공 지도
# - /commodities: 네비 카드 4개 (운임, 물류, 무역, 항공)
```
