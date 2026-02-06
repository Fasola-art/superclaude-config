# Browser Automation Module

Playwright 기반 브라우저 자동화 모듈

## 파일 구조

```
browser/
├── __init__.py      # 모듈 export
├── base.py          # 기본 클래스 (70줄)
└── automation.py    # 자동화 기능 (57줄)
```

## 사용 예시

```python
from automation.browser import BrowserAutomation

browser = BrowserAutomation()
browser.start(headless=True)

# 네비게이션
browser.navigate("https://example.com")

# 스크린샷
browser.screenshot("/tmp/screenshot.png")

# 요소 대기
browser.wait_for("#content")

# 정리
browser.stop()
```

## 의존성

```bash
pip install playwright
playwright install
```

## 테스트

```bash
python3 tests/test_browser.py
```
