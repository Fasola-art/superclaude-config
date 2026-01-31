# n8n 워크플로우

> SNS 자동화를 위한 n8n 워크플로우 JSON 파일

---

## 📁 파일 목록

| 파일 | 트리거 | 기능 |
|------|--------|------|
| `01-content-distributor.json` | Webhook | 멀티플랫폼 콘텐츠 배포 |
| `02-engagement-automation.json` | 15분 스케줄 | 댓글/DM 자동 응답 |
| `03-trend-analyzer.json` | 매일 06:00 | 트렌드 분석 + 아이디어 |
| `04-weekly-report.json` | 매주 일 21:00 | 주간 성과 리포트 |

---

## 🚀 Import 방법

1. n8n 접속 (`http://localhost:5678`)
2. **Workflows** → **Import from File**
3. JSON 파일 선택
4. **Credentials** 연결 (아래 참조)

---

## 🔐 필요한 Credentials

### 모든 워크플로우 공통

| Credential | n8n 타입 | 필요 정보 |
|------------|----------|----------|
| OpenAI | OpenAI API | API Key |
| Telegram | Telegram Bot | Bot Token |
| Google Sheets | Google Sheets OAuth2 | OAuth 연결 |

### 플랫폼별 (선택)

| Credential | 워크플로우 | 필요 정보 |
|------------|-----------|----------|
| Instagram | 01, 02 | Access Token, Business ID |
| TikTok | 01 | Access Token |
| Twitter | 01 | Bearer Token |

---

## ⚙️ 환경변수 설정

n8n Settings → Environment Variables에서 설정:

```bash
# 필수
OPENAI_API_KEY=sk-xxx
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
GOOGLE_SHEET_ID=xxx

# Instagram
INSTAGRAM_ACCESS_TOKEN=xxx
INSTAGRAM_BUSINESS_ID=xxx

# TikTok
TIKTOK_ACCESS_TOKEN=xxx

# Twitter
TWITTER_BEARER_TOKEN=xxx
```

---

## 🧪 테스트 방법

### 01. 콘텐츠 배포

```bash
curl -X POST http://localhost:5678/webhook/content \
  -H "Content-Type: application/json" \
  -d '{
    "media_url": "https://example.com/image.jpg",
    "caption": "테스트 캡션",
    "platforms": ["instagram"]
  }'
```

### 02. 인게이지먼트

- n8n에서 **Execute Workflow** 클릭
- 또는 15분 대기

### 03. 트렌드 분석

- n8n에서 **Execute Workflow** 클릭
- 또는 다음 06:00 대기

### 04. 주간 리포트

- n8n에서 **Execute Workflow** 클릭
- 또는 다음 일요일 21:00 대기

---

## ⚠️ Import 후 수정 필요 사항

1. **Credential ID 교체**: `OPENAI_CREDENTIAL_ID`, `TELEGRAM_CREDENTIAL_ID` 등을 실제 ID로 변경
2. **환경변수 확인**: 모든 `$env.XXX`가 설정되어 있는지 확인
3. **테스트 실행**: 각 노드별로 Execute Node 실행

---

## 📊 워크플로우 상세

### 01. Content Distributor

```
Webhook → Parse Input → AI Caption → Prepare Posts
    ↓
    ├── Instagram → Post
    └── TikTok → Post
    ↓
Aggregate → Telegram Notify → Respond
```

### 02. Engagement Automation

```
Schedule (15min) → Fetch Comments → Parse → AI Classify
    ↓
    ├── Fan Comment → Auto Reply
    └── Collab → Telegram Notify
    ↓
Log to Sheet
```

### 03. Trend Analyzer

```
Schedule (6AM) → Google Trends ─┐
                Instagram Trends ┴→ Merge → AI Analysis
    ↓
Format Briefing
    ├── Telegram
    └── Google Sheets
```

### 04. Weekly Report

```
Schedule (Sun 21:00) → IG Insights ─┐
                       IG Posts ────┴→ Aggregate → AI Analysis
    ↓
Format Report
    ├── Telegram
    └── Google Sheets
```

---

**META**
- Created: 2026-01-30
- Version: 1.0.0
