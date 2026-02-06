#!/usr/bin/env python3
"""
JARVIS Browser Automation
브라우저 자동화 모듈 (Playwright 기반)
"""

from .browser import BrowserAutomation, PLAYWRIGHT_AVAILABLE
from .booking import BookingAutomation

__all__ = ["BrowserAutomation", "BookingAutomation", "PLAYWRIGHT_AVAILABLE"]


if __name__ == "__main__":
    print("JARVIS Browser Automation Module")
    print(f"Playwright available: {PLAYWRIGHT_AVAILABLE}")

    if PLAYWRIGHT_AVAILABLE:
        browser = BrowserAutomation()
        print("Browser automation ready.")
    else:
        print("Install playwright: pip install playwright && playwright install")
