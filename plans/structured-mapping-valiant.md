# 클로바노트 → Notion 자동 업로드 시스템 구축 계획

> 이전 세션에서 작업했으나 저장 안 됨 → 새로 구축

---

## 🎯 목표

**음악 레슨 녹음 → CLOVA STT → Claude 요약 → Notion 자동 업로드**

---

## 📁 구현 파일 구조

```
~/.claude/modules/music-lesson/
├── clova_stt.py          # CLOVA Speech STT 호출
├── summarizer.py         # Claude Haiku 요약 생성
├── notion_uploader.py    # Notion 페이지 생성
├── pipeline.py           # 전체 파이프라인 통합
├── watcher.py            # 폴더 감시 (새 녹음 파일 감지)
├── config.json           # 설정 파일
└── README.md             # 사용법
```

---

## 🔧 구현 단계

### Step 1: CLOVA Speech STT 모듈
- 녹음 파일(mp3/m4a/wav) → 텍스트 변환
- API: `https://clovaspeech-gw.ncloud.com/recog/v1/stt`
- 인증: `~/.claude/credentials/api-keys.json` 사용

### Step 2: Claude 요약 모듈
- STT 결과 → Claude Haiku로 요약
- 형식: 주요 포인트, 핵심 개념, 다음 수업 준비사항

### Step 3: Notion 업로드 모듈
- 요약 내용 → Notion 페이지 생성
- 페이지 ID: `2f8ecc9a6ef580018794f0ba232ece99`
- 자동 태깅: 날짜, 학생명, 레슨 주제

### Step 4: 폴더 감시 (선택)
- 클로바노트 폴더 감시
- 새 녹음 파일 → 자동 처리
- 위치: `~/Library/CloudStorage/GoogleDrive-.../클로바노트/`

---

## 📋 API 키 (이미 설정됨)

```json
{
  "clova_speech": {
    "secret_key": "2c7965096774471b94acbcdd01e98d7",
    "invoke_url": "https://clovaspeech-gw.ncloud.com/recog/v1/stt"
  },
  "notion": {
    "internal_secret": "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",
    "page_id": "2f8ecc9a6ef580018794f0ba232ece99"
  },
  "anthropic": {
    "api_key": "sk-ant-api03-..."
  }
}
```

---

## ✅ 검증 방법

1. 테스트 녹음 파일로 STT 실행
2. 요약 결과 확인
3. Notion 페이지 생성 확인
4. 전체 파이프라인 테스트

---

## 📊 예상 소요 시간

| 단계 | 예상 시간 |
|------|----------|
| CLOVA STT 모듈 | 15분 |
| Claude 요약 모듈 | 10분 |
| Notion 업로드 | 15분 |
| 파이프라인 통합 | 10분 |
| 테스트 및 검증 | 10분 |
| **총** | **~1시간** |
