"""
트레이딩 모듈 설정.

환경 변수 또는 기본값으로 경로 설정.
"""

from __future__ import annotations

import os
from pathlib import Path

# 기본 경로
CLAUDE_HOME = Path(os.getenv('CLAUDE_HOME', Path.home() / '.claude'))
MODULES_ROOT = CLAUDE_HOME / 'modules'

# 트레이딩 모듈 경로
TRADING_MODULE = MODULES_ROOT / 'trading'
NEWS_COLLECTOR_MODULE = MODULES_ROOT / 'news-collector'

# 데이터 저장 경로
DATA_SOURCES_DIR = TRADING_MODULE / 'data_sources'
REPORTS_DIR = TRADING_MODULE / 'reports'
DAILY_REPORTS_DIR = REPORTS_DIR / 'daily'
MARKET_DATA_DIR = DATA_SOURCES_DIR / 'market_data'
CALENDAR_DIR = DATA_SOURCES_DIR / 'calendar'
KNOWLEDGE_DIR = TRADING_MODULE / 'knowledge'

# 디렉토리 생성
for dir_path in [DAILY_REPORTS_DIR, MARKET_DATA_DIR, CALENDAR_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# API 설정 (환경 변수에서 로드)
FRED_API_KEY = os.getenv('FRED_API_KEY', '')

# 타임아웃 설정
HTTP_TIMEOUT = int(os.getenv('HTTP_TIMEOUT', '30'))

# 로깅 설정
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
