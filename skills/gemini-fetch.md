---
name: gemini-fetch
description: Gemini CLI로 WebFetch 불가 사이트 크롤링 (Reddit, 인증 필요 사이트 등)
version: "1.0.0"
triggers:
  - /gemini-fetch
  - "gemini로 가져와"
  - "reddit 크롤링"
  - "WebFetch 안 될 때"
---

# Gemini Fetch - WebFetch 대안 크롤러

## 설치 (WSL2 - 최초 1회)

```bash
# Node.js v24 환경에서
nvm use 24
npm install -g @google/generative-ai-cli

# API 키 설정 (~/.bashrc에 추가)
echo 'export GEMINI_API_KEY="your-key-here"' >> ~/.bashrc
source ~/.bashrc

# 설치 확인
gemini --version
```

## 사용 패턴

```bash
# URL 내용 분석
gemini --url "https://reddit.com/r/programming/..." "주요 포인트 한국어로 요약"

# 여러 URL 비교
gemini --url "URL1" --url "URL2" "두 내용 비교 분석"

# 구조화된 데이터 추출
gemini --url "URL" "JSON 형식으로 제목, 작성자, 날짜 추출"
```

## Claude Code 통합 워크플로우

1. Claude가 URL 접근 실패 감지
2. `gemini --url <URL> "<프롬프트>"` 명령 생성
3. 사용자가 WSL2에서 실행
4. 결과를 Claude에게 붙여넣기
5. Claude가 결과 분석

## 적용 대상 사이트

| 사이트 | 이유 |
|--------|------|
| Reddit | 봇 차단 |
| Paywalled 뉴스 | 인증 필요 |
| LinkedIn | 로그인 필요 |
| Twitter/X | API 제한 |

## API 키 관리

```bash
# ~/.claude/credentials/api-keys.json에 추가
{
  "gemini": "your-gemini-api-key"
}
```
