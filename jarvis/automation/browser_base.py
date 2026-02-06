#!/usr/bin/env python3
"""
브라우저 자동화 기본 클래스
"""

from __future__ import annotations

from typing import Optional, Dict

# Playwright는 선택적 의존성
try:
    from playwright.sync_api import sync_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class BrowserBase:
    """브라우저 기본 클래스"""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self._playwright = None

    def start(self, headless: bool = True):
        """브라우저 시작"""
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright가 설치되지 않았습니다. pip install playwright && playwright install")

        self._playwright = sync_playwright().start()
        self.browser = self._playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()

    def stop(self):
        """브라우저 종료"""
        if self.browser:
            self.browser.close()
        if self._playwright:
            self._playwright.stop()

    def navigate(self, url: str) -> bool:
        """URL로 이동"""
        if not self.page:
            return False
        try:
            self.page.goto(url, wait_until="networkidle")
            return True
        except Exception as e:
            print(f"Navigation error: {e}")
            return False

    def click(self, selector: str) -> bool:
        """요소 클릭"""
        if not self.page:
            return False

        try:
            self.page.click(selector)
            return True
        except Exception as e:
            print(f"Click error: {e}")
            return False

    def fill_form(self, selectors: Dict[str, str]) -> bool:
        """폼 자동 입력"""
        if not self.page:
            return False

        try:
            for selector, value in selectors.items():
                self.page.fill(selector, value)
            return True
        except Exception as e:
            print(f"Form fill error: {e}")
            return False
