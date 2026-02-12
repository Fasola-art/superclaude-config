'use client';

import { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import type { LogisticsItem } from '@/types/api';
import { PORTS, STATUS_COLORS, STATUS_KR, CARGO_KR } from './map-data';
import { buildSeaRoute } from './map-utils';

interface Props {
  data: LogisticsItem[];
}

export default function ShippingMap({ data }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<L.Map | null>(null);

  /* 지도 초기화 (1회) */
  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = L.map(containerRef.current, {
      center: [25, 30],
      zoom: 2.5,
      minZoom: 2,
      maxZoom: 10,
      zoomSnap: 0.25,
      maxBounds: [[-90, -180], [90, 180]],
      maxBoundsViscosity: 1.0,
    });
    mapRef.current = map;

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      noWrap: true,
    }).addTo(map);

    /* 항구 마커 */
    PORTS.forEach((p) => {
      L.circleMarker([p.lat, p.lng], {
        radius: 6, fillColor: p.color, color: '#fff', weight: 2, fillOpacity: 0.9,
      })
        .bindTooltip(p.name, { direction: 'top', offset: [0, -8] })
        .addTo(map);
    });

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  /* 물류 데이터 레이어 */
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !data.length) return;

    const layers: L.Layer[] = [];

    data.forEach((ship) => {
      if (!ship.lat || !ship.lng) return;
      const color = STATUS_COLORS[ship.status] || '#ffb74d';

      /* 항로 Polyline */
      const route = buildSeaRoute(ship.origin_port, ship.dest_port);
      if (route) {
        const line = L.polyline(route, {
          color, weight: 2, opacity: 0.5, dashArray: '10, 6',
        }).addTo(map);
        line.bindTooltip(
          `${CARGO_KR[ship.cargo_type] || ship.cargo_type} | ${ship.origin_port} → ${ship.dest_port}`,
          { sticky: true },
        );
        layers.push(line);
      }

      /* 선박 마커 */
      const marker = L.circleMarker([ship.lat, ship.lng], {
        radius: 7, fillColor: color, color: '#fff', weight: 2, fillOpacity: 0.9,
      }).addTo(map);

      marker.bindPopup(
        `<b>${ship.vessel_name || ship.shipment_id}</b><br/>`
        + `${ship.origin_port} → ${ship.dest_port}<br/>`
        + `<span style="color:${color};font-weight:600">${STATUS_KR[ship.status] || ship.status}</span>`,
      );
      layers.push(marker);
    });

    return () => {
      layers.forEach((l) => map.removeLayer(l));
    };
  }, [data]);

  return (
    <div
      ref={containerRef}
      className="w-full rounded-lg border border-[var(--border)] overflow-hidden"
      style={{ height: '460px' }}
    />
  );
}
