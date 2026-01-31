# News Collector Module

> SuperClaude 뉴스 수집 및 분석 모듈

---

## 개요

뉴스 수집 모듈은 다양한 소스에서 뉴스를 자동 수집하고,
필터링, 요약, 센티멘트 분석을 수행합니다.

---

## 폴더 구조

```
~/.claude/modules/news-collector/
├── NEWS.md             # 이 파일 (모듈 가이드)
├── config.json         # 모듈 설정
├── sources/            # 뉴스 소스 정의
│   ├── rss.json
│   ├── api.json
│   └── custom/
├── filters/            # 필터링 규칙
│   ├── keywords.json
│   ├── categories.json
│   └── exclude.json
├── alerts/             # 알림 설정
│   └── rules.json
└── archive/            # 아카이브
    ├── 2026/
    │   ├── 01/
    │   └── ...
    └── index.json
```

---

## 기능

### 1. 뉴스 소스

```yaml
sources:
  rss_feeds:
    - name: "Bloomberg"
      url: "https://www.bloomberg.com/feed"
      category: "finance"

    - name: "TechCrunch"
      url: "https://techcrunch.com/feed"
      category: "tech"

    - name: "Reuters"
      url: "https://www.reuters.com/rssFeed"
      category: "general"

  api_sources:
    - name: "NewsAPI"
      type: "api"
      endpoint: "https://newsapi.org/v2"
      requires_key: true

    - name: "Google News"
      type: "scraper"
      url: "https://news.google.com"

  custom_sources:
    - name: "회사 블로그"
      type: "rss"
      url: "custom_url"
```

### 2. 필터링

```yaml
filters:
  keywords:
    include:
      - "AI"
      - "머신러닝"
      - "트레이딩"
      - "암호화폐"
    exclude:
      - "광고"
      - "스팸"

  categories:
    - tech
    - finance
    - crypto

  language:
    - ko
    - en

  time_range:
    max_age_hours: 24

  deduplication:
    enabled: true
    similarity_threshold: 0.8
```

### 3. 센티멘트 분석

```yaml
sentiment:
  enabled: true
  model: "local"  # 또는 "api"

  output:
    - score: -1.0 ~ 1.0
    - label: "positive" | "neutral" | "negative"
    - confidence: 0.0 ~ 1.0

  aggregation:
    - by_source
    - by_category
    - by_keyword
    - by_time
```

### 4. 요약

```yaml
summarization:
  enabled: true
  max_length: 200  # 글자 수
  language: "ko"

  output:
    - title: "원본 제목"
    - summary: "AI 생성 요약"
    - key_points: ["핵심 포인트 1", "핵심 포인트 2"]
    - entities: ["회사명", "인물명"]
```

### 5. 알림

```yaml
alerts:
  channels:
    - Desktop Notification
    - Telegram
    - Slack
    - Email

  triggers:
    keyword_mention:
      keywords: ["긴급", "속보"]
      priority: high

    sentiment_spike:
      threshold: 0.5  # 급격한 변화
      direction: "negative"

    volume_spike:
      threshold: 200  # % 증가
      timeframe: "1h"
```

---

## 스킬 명령어

| 명령어 | 설명 |
|--------|------|
| /news-fetch | 최신 뉴스 수집 |
| /news-filter [키워드] | 키워드로 필터링 |
| /news-summary [URL] | 뉴스 요약 |
| /news-sentiment [주제] | 센티멘트 분석 |
| /news-alert [조건] | 알림 설정 |

---

## 설정 (config.json)

```json
{
  "fetchInterval": 3600,
  "maxArticlesPerSource": 50,
  "archiveRetentionDays": 90,
  "sentiment": {
    "enabled": true,
    "model": "local"
  },
  "summarization": {
    "enabled": true,
    "maxLength": 200
  },
  "alerts": {
    "enabled": true,
    "channels": ["desktop"]
  }
}
```

---

## 사용 예시

```bash
# 최신 뉴스 수집
/news-fetch

# AI 관련 뉴스만 필터링
/news-filter "AI"

# 특정 기사 요약
/news-summary https://example.com/article

# 암호화폐 센티멘트 분석
/news-sentiment "Bitcoin"

# 부정적 뉴스 알림 설정
/news-alert "sentiment < -0.5" --keyword "내 포트폴리오"
```

---

## 스케줄링

```yaml
schedule:
  fetch:
    interval: "1h"  # 매시간
    sources: "all"

  archive:
    interval: "1d"  # 매일
    cleanup: true

  report:
    interval: "1d"
    time: "09:00"
    format: "daily_digest"
```

---

## 향후 계획

- [ ] 실시간 스트리밍 수집
- [ ] 다국어 번역
- [ ] 이미지/차트 분석
- [ ] Trading 모듈 연동
