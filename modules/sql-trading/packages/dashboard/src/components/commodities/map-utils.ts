/** 해상 항로 유틸리티 */

import { PORT_COORDS, SEA_WAYPOINTS, ROUTE_WAYPOINTS } from './map-data';

type Coord = [number, number];

const ASIAN_PORTS = ['Shanghai', 'Busan', 'Tokyo', 'Hong Kong', 'Singapore', 'Yokohama', 'Qingdao'];
const US_PORTS = ['Los Angeles', 'Long Beach', 'Seattle', 'New York', 'Savannah'];

/** 구간 보간 */
function interpolate(start: Coord, end: Coord, n: number): Coord[] {
  const pts: Coord[] = [];
  for (let i = 0; i < n; i++) {
    const t = i / n;
    pts.push([
      start[0] + (end[0] - start[0]) * t,
      start[1] + (end[1] - start[1]) * t,
    ]);
  }
  return pts;
}

/** 태평양 횡단 경도 보정 후 해상 항로 좌표 생성 */
export function buildSeaRoute(origin: string, dest: string): Coord[] | null {
  const start = PORT_COORDS[origin];
  const end = PORT_COORDS[dest];
  if (!start || !end) return null;

  const key = `${origin}_${dest}`;
  const wps = ROUTE_WAYPOINTS[key];

  /* 태평양 경도 보정 */
  const adjStart: Coord = [...start];
  let adjEnd: Coord = [...end];
  if (ASIAN_PORTS.includes(origin) && US_PORTS.includes(dest) && end[1] < 0) {
    adjEnd = [end[0], end[1] + 360];
  } else if (US_PORTS.includes(origin) && ASIAN_PORTS.includes(dest) && end[1] > 0) {
    adjEnd = [end[0], end[1] - 360];
  }

  const pts: Coord[] = [adjStart];
  if (wps) {
    wps.forEach((wp) => {
      if (Array.isArray(wp)) pts.push(wp as Coord);
      else if (SEA_WAYPOINTS[wp]) pts.push(SEA_WAYPOINTS[wp]);
    });
  }
  pts.push(adjEnd);

  /* 보간으로 부드럽게 */
  const smooth: Coord[] = [];
  for (let i = 0; i < pts.length - 1; i++) {
    smooth.push(...interpolate(pts[i], pts[i + 1], 8));
  }
  smooth.push(adjEnd);
  return smooth;
}
