#!/usr/bin/env python3
"""
부동산 지수 시드 데이터 생성기

KB부동산 기준 현실적 시드 데이터 생성
대상 테이블: realestate_indices
"""

import random
import sys
from datetime import datetime, timedelta

from _db_utils import count_table, run_sql

# 지역별 기준 지수 (KB부동산 2026년 초 기준 현실적 값)
REGIONS = {
    "전국": {"sale": 100.0, "jeonse": 97.5},
    "서울": {"sale": 102.3, "jeonse": 99.1},
    "경기": {"sale": 99.8, "jeonse": 96.4},
    "인천": {"sale": 98.5, "jeonse": 95.2},
    "부산": {"sale": 97.1, "jeonse": 94.8},
    "대구": {"sale": 95.3, "jeonse": 93.1},
    "대전": {"sale": 98.2, "jeonse": 95.7},
    "광주": {"sale": 97.8, "jeonse": 95.0},
    "울산": {"sale": 94.6, "jeonse": 92.3},
    "세종": {"sale": 96.0, "jeonse": 93.5},
    "제주": {"sale": 93.2, "jeonse": 90.8},
}


def collect_and_save(verbose: bool = True) -> int:
    """12주치 부동산 시드 데이터 생성"""
    existing = count_table("realestate_indices")
    if existing > 0:
        if verbose:
            print(f"  ℹ️ 이미 {existing}건 존재, 스킵")
        return 0

    random.seed(42)
    today = datetime.now().date()
    values = []

    for region, base_indices in REGIONS.items():
        for idx_type, base_val in base_indices.items():
            current_val = base_val
            for week in range(12, 0, -1):
                date = today - timedelta(weeks=week)
                # 현실적 주간 변동률: -0.05% ~ +0.02% (하락 추세 반영)
                change_pct = round(random.uniform(-0.05, 0.02), 3)
                current_val = round(current_val * (1 + change_pct / 100), 2)
                values.append(
                    f"('{date}', '{region}', '{idx_type}', {current_val}, "
                    f"{change_pct}, 'seed')"
                )

    sql = ("INSERT INTO realestate_indices "
           "(date, region, index_type, index_value, change_pct, source) "
           "VALUES\n" + ",\n".join(values) + ";")
    run_sql(sql)

    if verbose:
        print(f"  ✅ realestate_indices: {len(values)}건 생성")
    return len(values)


if __name__ == "__main__":
    try:
        print("🏠 부동산 시드 데이터 생성 중...")
        collect_and_save()
    except Exception as e:
        print(f"❌ 부동산 시드 생성 실패: {e}")
        sys.exit(1)
