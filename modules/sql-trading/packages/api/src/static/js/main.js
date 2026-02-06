/**
 * 메인 진입점 - 초기화 및 자동 갱신
 */

import { loadAllData } from './api.js';
import { renderSectors, renderSignals, renderStocks, renderIndicators, renderSummary } from './render.js';
import { renderFreightChart } from './charts.js';
import { initMap, renderLogistics } from './map.js';

// 전체 데이터 로드 및 렌더링
async function loadAll() {
    try {
        const data = await loadAllData();

        renderSummary(data.summary);
        renderSectors(data.sectors);
        renderSignals(data.signals);
        renderStocks(data.stocks);
        renderIndicators(data.indicators);
        renderFreightChart(data.freight);
        renderLogistics(data.logistics);
    } catch (e) {
        console.error('데이터 로드 오류:', e);
        document.getElementById('lastUpdate').textContent = '연결 실패';
    }
}

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    initMap();
    loadAll();

    // 10초마다 자동 갱신
    setInterval(loadAll, 10000);
});
