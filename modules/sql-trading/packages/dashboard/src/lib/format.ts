/**
 * DB DECIMAL/NUMERIC → 안전한 number 변환 유틸
 *
 * PostgreSQL DECIMAL은 JSON 직렬화 시 문자열로 올 수 있음.
 * null/undefined/NaN 모두 fallback 값 반환.
 */

/** null-safe number 변환 */
export function safeNum(v: unknown, fallback = 0): number {
  if (v == null) return fallback;
  const n = Number(v);
  return Number.isFinite(n) ? n : fallback;
}

/** 안전한 toFixed */
export function safeFix(v: unknown, digits = 2, fallback = '-'): string {
  if (v == null) return fallback;
  const n = Number(v);
  return Number.isFinite(n) ? n.toFixed(digits) : fallback;
}

/** 안전한 toLocaleString */
export function safeLoc(v: unknown, fallback = '-'): string {
  if (v == null) return fallback;
  const n = Number(v);
  return Number.isFinite(n) ? n.toLocaleString() : fallback;
}
