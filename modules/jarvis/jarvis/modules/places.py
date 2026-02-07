"""
장소 검색 - Brave Search API (primary) + Google Places API (fallback)
"""
import gzip
import json
import re
import urllib.request
import urllib.parse
from html import unescape
from pathlib import Path
from typing import List, Dict, Any, Optional

CATEGORY_KEYWORDS = {
    "restaurant": "맛집",
    "cafe": "카페",
    "attraction": "관광지",
    "activity": "액티비티 체험",
    "accommodation": "숙소 펜션",
}

_KEYS_PATH = Path.home() / ".claude/credentials/api-keys.json"


def _load_keys() -> Dict[str, Any]:
    """API 키 로드"""
    with open(_KEYS_PATH) as f:
        return json.load(f)


def _clean_html(text: str) -> str:
    """HTML 태그 및 엔티티 제거"""
    text = re.sub(r"<[^>]+>", "", unescape(text))
    return text.strip()


class PlaceSearcher:
    """장소 검색 (Brave Search 기반)"""

    BRAVE_URL = "https://api.search.brave.com/res/v1/web/search"

    def __init__(self):
        keys = _load_keys()
        brave = keys.get("brave_search", {})
        brave_keys = brave.get("keys", {})
        if isinstance(brave_keys, dict):
            self._brave_key = list(brave_keys.values())[0]
        elif isinstance(brave_keys, list):
            self._brave_key = brave_keys[0]
        else:
            self._brave_key = str(brave_keys)

    def search(self, query: str, count: int = 5) -> List[Dict[str, Any]]:
        """Brave Search로 장소 검색 (Rate Limit 자동 재시도)"""
        import time
        params = urllib.parse.urlencode({"q": query, "count": count})
        url = f"{self.BRAVE_URL}?{params}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self._brave_key,
        })
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    raw = resp.read()
                    try:
                        data = json.loads(gzip.decompress(raw))
                    except (gzip.BadGzipFile, OSError):
                        data = json.loads(raw)
                web_results = data.get("web", {}).get("results", [])
                return [self._parse_result(r) for r in web_results[:count]]
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 2:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                return []
        return []

    def search_by_category(self, category: str, region: str = "",
                           count: int = 5) -> List[Dict[str, Any]]:
        """카테고리+지역 기반 장소 검색"""
        keyword = CATEGORY_KEYWORDS.get(category, category)
        query = f"{region} {keyword} 추천".strip()
        return self.search(query, count=count)

    def search_for_booking(self, place_name: str) -> List[Dict[str, Any]]:
        """예약 링크 검색"""
        return self.search(f"{place_name} 예약", count=3)

    def _parse_result(self, result: Dict) -> Dict[str, Any]:
        """Brave Search 결과 파싱"""
        return {
            "name": _clean_html(result.get("title", "")),
            "url": result.get("url", ""),
            "description": _clean_html(result.get("description", "")),
            "source": result.get("meta_url", {}).get("hostname", ""),
        }
