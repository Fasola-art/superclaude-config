#!/usr/bin/env python3
"""
물류 데이터 수집기 (Logistics Data Collector)

데이터 소스:
- UN Comtrade: 국제 무역 통계
- Freightos Baltic Index: 운임 지수
- OpenSeaMap: 해상 지도 데이터 (향후)

Version: 1.0.0
"""

import json
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import httpx

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class CollectorConfig:
    """수집기 설정"""
    db_connection: str
    comtrade_rate_limit: int = 100  # 월별 제한
    request_timeout: int = 30
    batch_size: int = 100


class UNComtradeCollector:
    """UN Comtrade 국제 무역 통계 수집기"""

    BASE_URL = "https://comtradeapi.un.org/data/v1/get"

    # 주요 리포터 국가 코드
    REPORTERS = {
        "USA": "842",
        "CHN": "156",
        "DEU": "276",
        "JPN": "392",
        "KOR": "410",
    }

    # 주요 상품 HS 코드 (2자리)
    COMMODITIES = {
        "27": "광물성 연료 (석유, 가스)",
        "84": "기계류",
        "85": "전기기기",
        "87": "자동차",
        "90": "광학/의료기기",
    }

    def __init__(self, config: CollectorConfig):
        self.config = config
        self.client = httpx.Client(timeout=config.request_timeout)

    def fetch_trade_data(
        self,
        reporter_code: str,
        partner_code: str = "0",  # 0 = World
        period: Optional[str] = None,
        flow_code: str = "M,X",  # M=import, X=export
        commodity_code: str = "TOTAL",
    ) -> List[Dict[str, Any]]:
        """
        무역 데이터 조회

        Args:
            reporter_code: 보고국 코드
            partner_code: 파트너국 코드 (0=전세계)
            period: 기간 (YYYYMM 형식, None=최신)
            flow_code: 무역 흐름 (M=수입, X=수출)
            commodity_code: HS 코드

        Returns:
            무역 데이터 리스트
        """
        params = {
            "reporterCode": reporter_code,
            "partnerCode": partner_code,
            "flowCode": flow_code,
            "cmdCode": commodity_code,
        }

        if period:
            params["period"] = period

        url = f"{self.BASE_URL}/C/M?{urlencode(params)}"

        try:
            response = self.client.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("data"):
                return self._transform_comtrade_data(data["data"])
            return []

        except httpx.HTTPError as e:
            logger.error(f"UN Comtrade API 오류: {e}")
            return []

    def _transform_comtrade_data(self, raw_data: List[Dict]) -> List[Dict[str, Any]]:
        """원시 데이터를 DB 스키마에 맞게 변환"""
        transformed = []

        for record in raw_data:
            transformed.append({
                "period": record.get("period"),
                "reporter_code": record.get("reporterCode"),
                "reporter_name": record.get("reporterDesc"),
                "partner_code": record.get("partnerCode"),
                "partner_name": record.get("partnerDesc"),
                "flow_code": record.get("flowCode"),
                "commodity_code": record.get("cmdCode"),
                "commodity_desc": record.get("cmdDesc"),
                "trade_value": Decimal(str(record.get("primaryValue", 0))),
                "net_weight": Decimal(str(record.get("netWgt", 0))) if record.get("netWgt") else None,
                "qty": Decimal(str(record.get("qty", 0))) if record.get("qty") else None,
                "qty_unit": record.get("qtyUnitDesc"),
                "source": "UN_COMTRADE",
                "metadata": json.dumps({
                    "raw_period": record.get("period"),
                    "classification": record.get("classificationCode"),
                }),
            })

        return transformed

    def collect_major_routes(self, months_back: int = 6) -> List[Dict[str, Any]]:
        """
        주요 무역 경로 데이터 수집

        Args:
            months_back: 수집할 과거 개월 수

        Returns:
            수집된 무역 데이터
        """
        all_data = []
        end_date = datetime.now()

        # 주요 무역 경로
        routes = [
            ("842", "156"),  # USA-China
            ("156", "842"),  # China-USA
            ("842", "392"),  # USA-Japan
            ("842", "410"),  # USA-Korea
            ("276", "156"),  # Germany-China
        ]

        for i in range(months_back):
            period_date = end_date - timedelta(days=30 * i)
            period = period_date.strftime("%Y%m")

            for reporter, partner in routes:
                logger.info(f"수집 중: {reporter} → {partner}, 기간: {period}")
                data = self.fetch_trade_data(
                    reporter_code=reporter,
                    partner_code=partner,
                    period=period
                )
                all_data.extend(data)

        return all_data


class FreightosCollector:
    """Freightos Baltic Index (FBX) 운임 지수 수집기"""

    # 주요 항로
    ROUTES = {
        "FBX01": "China/East Asia - North America West Coast",
        "FBX02": "China/East Asia - North America East Coast",
        "FBX03": "China/East Asia - North Europe",
        "FBX04": "China/East Asia - Mediterranean",
        "FBX11": "North Europe - North America East Coast",
        "FBX12": "North America East Coast - North Europe",
    }

    def __init__(self, config: CollectorConfig):
        self.config = config
        self.client = httpx.Client(timeout=config.request_timeout)

    def fetch_fbx_data(self) -> List[Dict[str, Any]]:
        """
        FBX 운임 지수 데이터 조회

        Note: 실제 API 엔드포인트가 없으므로 웹 스크래핑 또는
              대체 데이터 소스 필요. 여기서는 구조만 정의.
        """
        # 실제 구현시 웹 스크래핑 또는 API 호출
        # 현재는 샘플 구조 반환
        logger.warning("FBX API 미구현 - 샘플 데이터 반환")

        sample_data = []
        today = datetime.now().date()

        for route_code, route_name in self.ROUTES.items():
            sample_data.append({
                "date": today.isoformat(),
                "index_name": "FBX",
                "route": route_name,
                "value": Decimal("2500.00"),  # 샘플 값
                "change_pct": Decimal("0.00"),
                "unit": "USD/FEU",
                "source": "FREIGHTOS",
                "metadata": json.dumps({"route_code": route_code}),
            })

        return sample_data


class BalticDryIndexCollector:
    """Baltic Dry Index (BDI) 수집기"""

    def __init__(self, config: CollectorConfig):
        self.config = config
        self.client = httpx.Client(timeout=config.request_timeout)

    def fetch_bdi_data(self) -> List[Dict[str, Any]]:
        """
        BDI 데이터 조회

        Note: 실제 API가 필요함. 무료 소스로는 제한적.
        """
        logger.warning("BDI API 미구현 - 샘플 데이터 반환")

        today = datetime.now().date()
        return [{
            "date": today.isoformat(),
            "index_name": "BDI",
            "route": "GLOBAL",
            "value": Decimal("1500.00"),  # 샘플 값
            "change_pct": Decimal("0.00"),
            "unit": "points",
            "source": "BALTIC_EXCHANGE",
            "metadata": json.dumps({"type": "composite"}),
        }]


class LogisticsDataCollector:
    """물류 데이터 통합 수집기"""

    def __init__(self, config: CollectorConfig):
        self.config = config
        self.comtrade = UNComtradeCollector(config)
        self.freightos = FreightosCollector(config)
        self.bdi = BalticDryIndexCollector(config)

    def collect_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """모든 물류 데이터 수집"""
        results = {
            "trade_statistics": [],
            "freight_indices": [],
        }

        # 1. UN Comtrade 무역 데이터
        logger.info("UN Comtrade 데이터 수집 시작...")
        try:
            trade_data = self.comtrade.collect_major_routes(months_back=3)
            results["trade_statistics"] = trade_data
            logger.info(f"무역 데이터 수집 완료: {len(trade_data)}건")
        except Exception as e:
            logger.error(f"무역 데이터 수집 실패: {e}")

        # 2. 운임 지수 데이터
        logger.info("운임 지수 데이터 수집 시작...")
        try:
            fbx_data = self.freightos.fetch_fbx_data()
            bdi_data = self.bdi.fetch_bdi_data()
            results["freight_indices"] = fbx_data + bdi_data
            logger.info(f"운임 지수 수집 완료: {len(results['freight_indices'])}건")
        except Exception as e:
            logger.error(f"운임 지수 수집 실패: {e}")

        return results

    def save_to_json(self, data: Dict[str, List], output_path: str) -> None:
        """수집 데이터를 JSON 파일로 저장"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Decimal을 float로 변환
        def convert_decimal(obj: Any) -> Any:
            if isinstance(obj, Decimal):
                return float(obj)
            if isinstance(obj, dict):
                return {k: convert_decimal(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [convert_decimal(item) for item in obj]
            return obj

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(convert_decimal(data), f, ensure_ascii=False, indent=2)

        logger.info(f"데이터 저장 완료: {output_file}")

    def generate_insert_sql(self, data: Dict[str, List]) -> str:
        """수집 데이터를 INSERT SQL로 변환"""
        sql_statements = []

        # trade_statistics INSERT
        if data.get("trade_statistics"):
            sql_statements.append("-- Trade Statistics")
            for record in data["trade_statistics"]:
                sql = f"""
INSERT INTO trade_statistics (period, reporter_code, reporter_name, partner_code, partner_name, flow_code, commodity_code, commodity_desc, trade_value, net_weight, qty, qty_unit, source, metadata)
VALUES ('{record['period']}', '{record['reporter_code']}', '{record['reporter_name']}', '{record['partner_code']}', '{record['partner_name']}', '{record['flow_code']}', '{record['commodity_code']}', '{record.get('commodity_desc', '')}', {record['trade_value']}, {record.get('net_weight') or 'NULL'}, {record.get('qty') or 'NULL'}, '{record.get('qty_unit', '')}', '{record['source']}', '{record['metadata']}')
ON CONFLICT DO NOTHING;
"""
                sql_statements.append(sql.strip())

        # freight_indices INSERT
        if data.get("freight_indices"):
            sql_statements.append("\n-- Freight Indices")
            for record in data["freight_indices"]:
                sql = f"""
INSERT INTO freight_indices (date, index_name, route, value, change_pct, unit, source, metadata)
VALUES ('{record['date']}', '{record['index_name']}', '{record['route']}', {record['value']}, {record['change_pct']}, '{record['unit']}', '{record['source']}', '{record['metadata']}')
ON CONFLICT (date, index_name, route) DO UPDATE SET value = EXCLUDED.value, change_pct = EXCLUDED.change_pct;
"""
                sql_statements.append(sql.strip())

        return "\n".join(sql_statements)


def main():
    """메인 실행 함수"""
    # 설정 로드
    config_path = Path.home() / ".claude" / "modules" / "sql-trading" / "config.json"

    if config_path.exists():
        with open(config_path) as f:
            config_data = json.load(f)
        db_connection = config_data.get("database", {}).get("connection", "")
    else:
        db_connection = os.environ.get("DATABASE_URL", "postgresql://reim@localhost:5432/claude_mcp")

    config = CollectorConfig(db_connection=db_connection)
    collector = LogisticsDataCollector(config)

    # 데이터 수집
    logger.info("물류 데이터 수집 시작...")
    data = collector.collect_all()

    # 결과 저장
    output_dir = Path.home() / ".claude" / "modules" / "sql-trading" / "data"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # JSON 저장
    json_path = output_dir / f"logistics_{timestamp}.json"
    collector.save_to_json(data, str(json_path))

    # SQL 생성
    sql_path = output_dir / f"logistics_{timestamp}.sql"
    sql_content = collector.generate_insert_sql(data)
    sql_path.parent.mkdir(parents=True, exist_ok=True)
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    logger.info(f"SQL 파일 저장: {sql_path}")

    # 요약 출력
    print("\n" + "=" * 50)
    print("📦 물류 데이터 수집 완료")
    print("=" * 50)
    print(f"무역 통계: {len(data.get('trade_statistics', []))}건")
    print(f"운임 지수: {len(data.get('freight_indices', []))}건")
    print(f"JSON 파일: {json_path}")
    print(f"SQL 파일: {sql_path}")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    sys.exit(main())
