# Archive 폴더

> **목적**: 완료된 프로젝트 및 오래된 설정의 아카이브 저장소
> **갱신일**: 2026-01-30

---

## 📁 폴더 구조

```
archive/
├── README.md           # 이 파일
├── projects/           # 완료된 프로젝트 아카이브
│   └── {project-name}_{date}/
├── sessions/           # 중요 세션 이력 보관
│   └── session_{id}_{date}.json
├── configs/            # 이전 버전 설정 백업
│   └── {config-name}_{version}.json
└── exports/            # 내보낸 데이터
    └── {export-name}_{date}.{ext}
```

---

## 🎯 사용 목적

| 용도 | 설명 | 보관 기간 |
|------|------|----------|
| **완료 프로젝트** | 성공적으로 완료된 프로젝트 전체 | 무기한 |
| **중요 세션** | 학습 가치가 높은 세션 로그 | 1년 |
| **이전 설정** | 버전 업그레이드 전 설정 | 6개월 |
| **내보낸 데이터** | 외부 공유용 데이터 | 3개월 |

---

## 📋 아카이브 절차

### 1. 프로젝트 아카이브
```bash
# 프로젝트 완료 시
mkdir -p ~/.claude/archive/projects/{project-name}_{YYYYMMDD}
cp -r {project-path}/* ~/.claude/archive/projects/{project-name}_{YYYYMMDD}/
```

### 2. 세션 아카이브
```bash
# 중요 세션 보관
cp ~/.claude/sessions/{session-id}.json \
   ~/.claude/archive/sessions/session_{session-id}_{YYYYMMDD}.json
```

### 3. 설정 아카이브
```bash
# 버전 업그레이드 전
cp ~/.claude/settings.json \
   ~/.claude/archive/configs/settings_v{version}.json
```

---

## 🔖 명명 규칙

| 유형 | 패턴 | 예시 |
|------|------|------|
| 프로젝트 | `{name}_{YYYYMMDD}` | `trading-bot_20260130` |
| 세션 | `session_{id}_{YYYYMMDD}` | `session_abc123_20260130` |
| 설정 | `{name}_v{version}` | `settings_v2.0.8` |
| 내보내기 | `{name}_{YYYYMMDD}.{ext}` | `error-kb_20260130.json` |

---

## ⚠️ 주의사항

- 민감한 정보(API 키, 비밀번호)는 아카이브 전 제거
- 대용량 파일(>100MB)은 압축 후 저장
- 정기적으로 오래된 아카이브 정리 (6개월 주기)

---

**META**
- Category: archive
- Last Updated: 2026-01-30
- Version: 1.0.0
