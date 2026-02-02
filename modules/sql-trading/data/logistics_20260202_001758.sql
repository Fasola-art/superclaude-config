
-- Freight Indices
INSERT INTO freight_indices (date, index_name, route, value, change_pct, unit, source, metadata)
VALUES ('2026-02-02', 'FBX', 'China/East Asia - North America West Coast', 2500.00, 0.00, 'USD/FEU', 'FREIGHTOS', '{"route_code": "FBX01"}')
ON CONFLICT (date, index_name, route) DO UPDATE SET value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;
INSERT INTO freight_indices (date, index_name, route, value, change_pct, unit, source, metadata)
VALUES ('2026-02-02', 'FBX', 'China/East Asia - North America East Coast', 2500.00, 0.00, 'USD/FEU', 'FREIGHTOS', '{"route_code": "FBX02"}')
ON CONFLICT (date, index_name, route) DO UPDATE SET value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;
INSERT INTO freight_indices (date, index_name, route, value, change_pct, unit, source, metadata)
VALUES ('2026-02-02', 'FBX', 'China/East Asia - North Europe', 2500.00, 0.00, 'USD/FEU', 'FREIGHTOS', '{"route_code": "FBX03"}')
ON CONFLICT (date, index_name, route) DO UPDATE SET value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;
INSERT INTO freight_indices (date, index_name, route, value, change_pct, unit, source, metadata)
VALUES ('2026-02-02', 'FBX', 'China/East Asia - Mediterranean', 2500.00, 0.00, 'USD/FEU', 'FREIGHTOS', '{"route_code": "FBX04"}')
ON CONFLICT (date, index_name, route) DO UPDATE SET value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;
INSERT INTO freight_indices (date, index_name, route, value, change_pct, unit, source, metadata)
VALUES ('2026-02-02', 'FBX', 'North Europe - North America East Coast', 2500.00, 0.00, 'USD/FEU', 'FREIGHTOS', '{"route_code": "FBX11"}')
ON CONFLICT (date, index_name, route) DO UPDATE SET value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;
INSERT INTO freight_indices (date, index_name, route, value, change_pct, unit, source, metadata)
VALUES ('2026-02-02', 'FBX', 'North America East Coast - North Europe', 2500.00, 0.00, 'USD/FEU', 'FREIGHTOS', '{"route_code": "FBX12"}')
ON CONFLICT (date, index_name, route) DO UPDATE SET value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;
INSERT INTO freight_indices (date, index_name, route, value, change_pct, unit, source, metadata)
VALUES ('2026-02-02', 'BDI', 'GLOBAL', 1500.00, 0.00, 'points', 'BALTIC_EXCHANGE', '{"type": "composite"}')
ON CONFLICT (date, index_name, route) DO UPDATE SET value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;