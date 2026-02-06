/**
 * DOM 렌더링 모듈
 */

import { SECTOR_NAMES, STOCK_INFO, SIGNAL_TEXT, INDICATOR_ICONS } from './constants.js';

// 섹터 렌더링
export function renderSectors(data) {
    const grid = document.getElementById('sectorGrid');
    if (!data.length) {
        grid.innerHTML = '<div class="loading">데이터 없음</div>';
        return;
    }
    grid.innerHTML = data.map(s => {
        const info = SECTOR_NAMES[s.sector] || { emoji: '📊', name: s.sector, desc: '' };
        const changeClass = s.change >= 0 ? 'positive' : 'negative';
        const sign = s.change >= 0 ? '+' : '';
        return `
            <div class="sector-card" title="${info.desc}">
                <div class="emoji">${info.emoji}</div>
                <div class="name">${info.name}</div>
                <div class="value ${changeClass}">${sign}${s.change}%</div>
                <div class="count">${s.count}종목</div>
            </div>
        `;
    }).join('');
}

// 신호 렌더링
export function renderSignals(data) {
    const list = document.getElementById('signalList');
    if (!data.length) {
        list.innerHTML = '<div class="loading">신호 없음</div>';
        return;
    }
    list.innerHTML = data.map(s => {
        const isBuy = s.signal.includes('BUY');
        const signalClass = isBuy ? 'buy' : 'sell';
        const info = STOCK_INFO[s.symbol] || { desc: s.symbol, commodity: '' };
        const signalText = SIGNAL_TEXT[s.signal] || s.signal;
        return `
            <li class="signal-item ${signalClass}" title="${info.commodity}">
                <div>
                    <div class="symbol">${s.symbol}</div>
                    <div class="price">${info.desc} · $${s.price}</div>
                </div>
                <div class="meta">
                    <div class="signal-badge ${signalClass}">${signalText}</div>
                    <div class="confidence">${s.confidence}% 신뢰도</div>
                </div>
            </li>
        `;
    }).join('');
}

// 종목 렌더링
export function renderStocks(data) {
    const grid = document.getElementById('stockGrid');
    const sorted = data.sort((a, b) => Math.abs(b.change) - Math.abs(a.change));
    grid.innerHTML = sorted.slice(0, 12).map(s => {
        const changeClass = s.change >= 0 ? 'positive' : 'negative';
        const sign = s.change >= 0 ? '+' : '';
        const info = STOCK_INFO[s.symbol] || { name: s.name, desc: s.name, commodity: '' };
        return `
            <div class="stock-item">
                <div>
                    <div class="symbol">${s.symbol} <span style="color:#666;font-weight:normal;font-size:11px">$${s.price}</span></div>
                    <div class="name">${info.desc}</div>
                    ${info.commodity ? `<div class="commodity">→ ${info.commodity}</div>` : ''}
                </div>
                <div class="change ${changeClass}">${sign}${s.change}%</div>
            </div>
        `;
    }).join('');
}

// 경제지표 렌더링
export function renderIndicators(data) {
    const grid = document.getElementById('indicatorGrid');
    if (!data.length) {
        grid.innerHTML = '<div class="loading">데이터 없음</div>';
        return;
    }
    grid.innerHTML = data.map(ind => {
        const changeClass = ind.change >= 0 ? 'positive' : 'negative';
        const sign = ind.change >= 0 ? '+' : '';
        const icon = INDICATOR_ICONS[ind.category] || '📈';
        const unit = ind.category === '에너지' ? '$' : '';
        return `
            <div class="indicator-item">
                <div>
                    <div class="name">${icon} ${ind.name}</div>
                    <div class="category">${ind.date} 기준</div>
                </div>
                <div style="text-align:right">
                    <div class="value">${unit}${ind.value.toFixed(2)}</div>
                    <div class="change ${changeClass}">${sign}${ind.change.toFixed(2)}%</div>
                </div>
            </div>
        `;
    }).join('');
}

// 요약 렌더링
export function renderSummary(data) {
    document.getElementById('totalRecords').textContent = data.total_records.toLocaleString();
    document.getElementById('buySignals').textContent = data.buy_signals;
    document.getElementById('sellSignals').textContent = data.sell_signals;
    document.getElementById('lastUpdate').textContent =
        new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}
