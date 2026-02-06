#!/usr/bin/env python3
"""브라우저 자동화 핵심 기능"""

from __future__ import annotations
from typing import Optional, List, Dict
from .base import BrowserBase


class BrowserAutomation(BrowserBase):
    """브라우저 자동화 클래스"""

    def screenshot(self, path: str) -> bool:
        """스크린샷 저장"""
        if not self.page:
            return False
        try:
            self.page.screenshot(path=path)
            return True
        except Exception as e:
            print(f"Screenshot error: {e}")
            return False

    def get_text(self, selector: str) -> Optional[str]:
        """요소 텍스트 가져오기"""
        if not self.page:
            return None
        try:
            return self.page.text_content(selector)
        except Exception as e:
            print(f"Get text error: {e}")
            return None

    def wait_for(self, selector: str, timeout: int = 30000) -> bool:
        """요소 대기"""
        if not self.page:
            return False
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception as e:
            print(f"Wait error: {e}")
            return False

    def search(self, query: str, engine: str = "google") -> List[Dict]:
        """웹 검색"""
        engines = {
            "google": f"https://www.google.com/search?q={query}",
            "naver": f"https://search.naver.com/search.naver?query={query}",
            "bing": f"https://www.bing.com/search?q={query}"
        }

        url = engines.get(engine, engines["google"])
        self.navigate(url)

        # 검색 결과 파싱 (각 엔진별 셀렉터 필요)
        results: list[dict[str, str]] = []
        return results
