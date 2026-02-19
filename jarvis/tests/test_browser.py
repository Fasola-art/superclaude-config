#!/usr/bin/env python3
"""브라우저 자동화 테스트"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jarvis.automation.browser import BrowserAutomation, PLAYWRIGHT_AVAILABLE


def test_browser_init():
    """브라우저 초기화 테스트"""
    if not PLAYWRIGHT_AVAILABLE:
        print("⚠️  Playwright 미설치, 테스트 스킵")
        return

    browser = BrowserAutomation()
    try:
        browser.start(headless=True)
        assert browser.page is not None
        print("✅ Browser init test passed")
    finally:
        browser.stop()


def test_browser_navigate():
    """브라우저 네비게이션 테스트"""
    if not PLAYWRIGHT_AVAILABLE:
        print("⚠️  Playwright 미설치, 테스트 스킵")
        return

    browser = BrowserAutomation()
    try:
        browser.start(headless=True)
        success = browser.navigate("https://example.com")
        assert success is True
        print("✅ Browser navigate test passed")
    finally:
        browser.stop()


def test_browser_screenshot():
    """스크린샷 테스트"""
    if not PLAYWRIGHT_AVAILABLE:
        print("⚠️  Playwright 미설치, 테스트 스킵")
        return

    browser = BrowserAutomation()
    try:
        browser.start(headless=True)
        browser.navigate("https://example.com")
        success = browser.screenshot("/tmp/test_screenshot.png")
        assert success is True
        print("✅ Browser screenshot test passed")
    finally:
        browser.stop()


if __name__ == "__main__":
    print(f"Playwright available: {PLAYWRIGHT_AVAILABLE}")

    test_browser_init()
    test_browser_navigate()
    test_browser_screenshot()

    print("\n🎉 All browser tests passed!")
