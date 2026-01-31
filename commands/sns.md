---
description: "SNS 자동화 워크플로우 설계 및 관리 (SNS automation workflow)"
argument-hint: "[workflow_name or action]"
---

# SNS 자동화

SNS 콘텐츠 배포, 인게이지먼트, 트렌드 분석 자동화 워크플로우를 설계하고 관리합니다.

## 동작

1. 요청 분석 (워크플로우 설계 / n8n 설정 / 기존 워크플로우 수정)
2. 기술 스택 확인 (n8n, API, AI)
3. 워크플로우 설계 또는 수정
4. 구현 가이드 제공

## 사용 가능한 액션

| 액션 | 설명 |
|------|------|
| `design` | 새 워크플로우 설계 |
| `setup` | n8n 환경 설정 가이드 |
| `check` | 기존 워크플로우 점검 |
| `improve` | 워크플로우 개선 제안 |

## 사용 예시

```bash
/sns                          # 전체 SNS 자동화 가이드
/sns design content           # 콘텐츠 배포 워크플로우 설계
/sns setup                    # n8n 설정 가이드
/sns check                    # 기존 워크플로우 점검
```

## 워크플로우 종류

| # | 워크플로우 | 트리거 | 기능 |
|---|-----------|--------|------|
| 1 | 콘텐츠 배포 | Webhook | 멀티플랫폼 자동 업로드 |
| 2 | 인게이지먼트 | 15분 스케줄 | 댓글/DM 자동 응답 |
| 3 | 트렌드 분석 | 매일 06:00 | 트렌드 수집 + 아이디어 |
| 4 | 분석 리포팅 | 매주 일요일 | 주간 성과 리포트 |

## 관련 문서

- 스킬 상세: `~/.claude/skills/sns-automation/SKILL.md`
- n8n 가이드: `~/.claude/docs/N8N-PYTHON-UPLOAD.md`
- 모듈 폴더: `~/.claude/modules/sns-automation/`

## 기술 스택

| 레이어 | 도구 |
|--------|------|
| 워크플로우 | n8n (셀프호스팅) |
| AI | OpenAI / Claude |
| 미디어 | FFmpeg / Cloudinary |
| 알림 | Telegram / Slack |
