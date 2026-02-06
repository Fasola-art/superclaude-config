/**
 * API 호출 모듈
 */

import { API_BASE } from './constants.js';

async function fetchJson(endpoint) {
    const res = await fetch(`${API_BASE}${endpoint}`);
    if (!res.ok) throw new Error(`API Error: ${res.status}`);
    return res.json();
}

export async function getSectors() {
    return fetchJson('/api/sectors');
}

export async function getSignals() {
    return fetchJson('/api/signals');
}

export async function getStocks() {
    return fetchJson('/api/stocks');
}

export async function getFreight() {
    return fetchJson('/api/freight');
}

export async function getSummary() {
    return fetchJson('/api/summary');
}

export async function getIndicators() {
    return fetchJson('/api/indicators');
}

export async function getLogistics() {
    return fetchJson('/api/logistics');
}

// 모든 데이터 병렬 로드
export async function loadAllData() {
    const [summary, sectors, signals, stocks, indicators, freight, logistics] = await Promise.all([
        getSummary(),
        getSectors(),
        getSignals(),
        getStocks(),
        getIndicators(),
        getFreight(),
        getLogistics()
    ]);
    return { summary, sectors, signals, stocks, indicators, freight, logistics };
}
