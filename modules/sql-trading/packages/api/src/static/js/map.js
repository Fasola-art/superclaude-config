/**
 * Leaflet 지도 모듈
 */

import { CARGO_KR, STATUS_COLORS, STATUS_KR } from './constants.js';
import { PORT_COORDS, SEA_WAYPOINTS, ROUTE_WAYPOINTS, PORTS } from './map-data.js';

let map = null;
let markers = [];
let routeLines = [];
export const portMarkers = {};

// 지도 초기화
export function initMap() {
    const mapContainer = document.getElementById('map');
    const containerWidth = mapContainer.offsetWidth;
    const minZoomCalc = Math.ceil(Math.log2(containerWidth / 256));

    map = L.map('map', {
        zoomSnap: 0.25,
        zoomDelta: 0.5,
        wheelPxPerZoomLevel: 120,
        center: [25, 30],
        zoom: 2.5,
        minZoom: Math.max(2, minZoomCalc),
        maxZoom: 18,
        maxBounds: [[-90, -180], [90, 180]],
        maxBoundsViscosity: 1.0,
        worldCopyJump: false
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap © CARTO',
        subdomains: 'abcd',
        noWrap: true,
        bounds: [[-90, -180], [90, 180]]
    }).addTo(map);

    // 주요 항구 마커
    PORTS.forEach(port => {
        const marker = L.circleMarker([port.lat, port.lng], {
            radius: 7,
            fillColor: port.color,
            color: "#fff",
            weight: 2,
            fillOpacity: 0.9
        }).addTo(map);

        marker.bindTooltip(port.name, {
            permanent: false,
            direction: 'top',
            offset: [0, -8],
            className: 'port-tooltip'
        });

        portMarkers[port.code] = { marker, name: port.name };
    });

    window.addEventListener('resize', () => map.invalidateSize());
}

// 구간 부드럽게 연결
function smoothSegment(start, end, numPoints) {
    const points = [];
    for (let i = 0; i < numPoints; i++) {
        const t = i / numPoints;
        const lat = start[0] + (end[0] - start[0]) * t;
        const lng = start[1] + (end[1] - start[1]) * t;
        points.push([lat, lng]);
    }
    return points;
}

// 실제 해상 항로 생성
function createSeaRoute(origin, dest) {
    const start = PORT_COORDS[origin];
    const end = PORT_COORDS[dest];
    if (!start || !end) return null;

    const routeKey = `${origin}_${dest}`;
    const waypoints = ROUTE_WAYPOINTS[routeKey];

    const asianPorts = ['Shanghai', 'Busan', 'Tokyo', 'Hong Kong', 'Singapore', 'Yokohama', 'Qingdao'];
    const americanPorts = ['Los Angeles', 'Long Beach', 'Seattle', 'New York', 'Savannah'];
    const isAsiaToAmerica = asianPorts.includes(origin) && americanPorts.includes(dest);
    const isAmericaToAsia = americanPorts.includes(origin) && asianPorts.includes(dest);

    let adjustedStart = [...start];
    let adjustedEnd = [...end];

    if (isAsiaToAmerica && end[1] < 0) {
        adjustedEnd = [end[0], end[1] + 360];
    } else if (isAmericaToAsia && end[1] > 0) {
        adjustedEnd = [end[0], end[1] - 360];
    }

    let points = [adjustedStart];

    if (waypoints) {
        waypoints.forEach(wp => {
            if (Array.isArray(wp)) {
                points.push(wp);
            } else if (SEA_WAYPOINTS[wp]) {
                points.push(SEA_WAYPOINTS[wp]);
            }
        });
    }

    points.push(adjustedEnd);

    const smoothedPoints = [];
    for (let i = 0; i < points.length - 1; i++) {
        const segmentPoints = smoothSegment(points[i], points[i + 1], 10);
        smoothedPoints.push(...segmentPoints);
    }
    smoothedPoints.push(adjustedEnd);

    return smoothedPoints;
}

// 물류 추적 렌더링
export function renderLogistics(data) {
    // 기존 마커/라인 제거
    markers.forEach(m => map.removeLayer(m));
    routeLines.forEach(l => map.removeLayer(l));
    markers = [];
    routeLines = [];

    data.forEach(ship => {
        if (!ship.lat || !ship.lng) return;

        const color = STATUS_COLORS[ship.status] || '#ffb74d';
        const originCoord = PORT_COORDS[ship.origin];
        const destCoord = PORT_COORDS[ship.dest];
        const shipCoord = [ship.lat, ship.lng];

        const tooltipContent = `
            <div style="font-size:12px;line-height:1.5;min-width:160px;">
                <b>${CARGO_KR[ship.cargo] || '🚢 화물'}</b><br>
                <hr style="margin:4px 0;border:none;border-top:1px solid #ddd;">
                🚀 <b>출발:</b> ${ship.origin}<br>
                　 ${ship.departure || '-'} (KST)<br>
                🎯 <b>도착:</b> ${ship.dest}<br>
                　 ${ship.arrival || '-'} (KST)
            </div>
        `;

        if (originCoord && destCoord) {
            const seaRoute = createSeaRoute(ship.origin, ship.dest);
            const routePoints = seaRoute || [originCoord, destCoord];

            const dashLine = L.polyline(routePoints, {
                color: color,
                weight: 2,
                opacity: 0.5,
                dashArray: '12, 8',
                className: 'animated-route'
            }).addTo(map);
            routeLines.push(dashLine);

            const arrowDecorator = L.polylineDecorator(routePoints, {
                patterns: [{
                    offset: 50,
                    repeat: 100,
                    symbol: L.Symbol.arrowHead({
                        pixelSize: 10,
                        polygon: false,
                        pathOptions: { color: color, weight: 2.5, opacity: 0.9 }
                    })
                }]
            }).addTo(map);
            routeLines.push(arrowDecorator);

            dashLine.bindTooltip(tooltipContent, { sticky: true, opacity: 0.95, className: 'route-tooltip' });
        }

        const marker = L.circleMarker(shipCoord, {
            radius: 7,
            fillColor: color,
            color: '#fff',
            weight: 2,
            fillOpacity: 0.9
        }).addTo(map);

        marker.bindPopup(`
            <div style="font-size:13px;">
                <b>${CARGO_KR[ship.cargo] || '🚢'} ${ship.vessel || ship.id}</b><br>
                <span style="color:#666;">📍 ${ship.origin} → ${ship.dest}</span><br>
                <span style="color:${color};font-weight:600;">● ${STATUS_KR[ship.status] || ship.status}</span>
            </div>
        `);
        markers.push(marker);
    });

    updatePortTooltips(data);
    updateMapTitle(data.length);
}

// 항구 툴팁 업데이트
function updatePortTooltips(data) {
    const portStats = {};
    data.forEach(ship => {
        if (ship.origin) {
            if (!portStats[ship.origin]) portStats[ship.origin] = { departures: [], arrivals: [] };
            portStats[ship.origin].departures.push({
                cargo: CARGO_KR[ship.cargo] || '화물',
                dest: ship.dest,
                time: ship.departure
            });
        }
        if (ship.dest) {
            if (!portStats[ship.dest]) portStats[ship.dest] = { departures: [], arrivals: [] };
            portStats[ship.dest].arrivals.push({
                cargo: CARGO_KR[ship.cargo] || '화물',
                origin: ship.origin,
                time: ship.arrival
            });
        }
    });

    Object.entries(portStats).forEach(([portCode, stats]) => {
        const portData = portMarkers[portCode];
        if (!portData) return;

        let html = `<div style="min-width:180px;"><b style="font-size:14px;">${portData.name}</b>`;

        if (stats.departures.length > 0) {
            html += `<div style="margin-top:8px;padding-top:6px;border-top:1px solid rgba(102,187,106,0.3);">`;
            html += `<b style="color:#43a047;">🚀 출발 (${stats.departures.length}건)</b>`;
            stats.departures.forEach(dep => {
                html += `<div style="font-size:11px;margin:4px 0 0 8px;color:#5f6368;">`;
                html += `${dep.cargo} → ${dep.dest}<br><span style="color:#78909c;">　${dep.time || '-'} (KST)</span></div>`;
            });
            html += `</div>`;
        }

        if (stats.arrivals.length > 0) {
            html += `<div style="margin-top:8px;padding-top:6px;border-top:1px solid rgba(30,136,229,0.3);">`;
            html += `<b style="color:#1e88e5;">🎯 도착 (${stats.arrivals.length}건)</b>`;
            stats.arrivals.forEach(arr => {
                html += `<div style="font-size:11px;margin:4px 0 0 8px;color:#5f6368;">`;
                html += `${arr.cargo} ← ${arr.origin}<br><span style="color:#78909c;">　${arr.time || '-'} (KST)</span></div>`;
            });
            html += `</div>`;
        }

        html += `</div>`;
        portData.marker.unbindTooltip();
        portData.marker.bindTooltip(html, { permanent: false, direction: 'top', offset: [0, -10], className: 'port-tooltip' });
    });
}

function updateMapTitle(count) {
    if (count > 0) {
        document.querySelector('.card:has(#map) h2').innerHTML =
            `🗺️ 물류 추적 <span style="color:#4fc3f7;font-size:11px;">(${count}척 운항중)</span>`;
    }
}
