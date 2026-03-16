---
description: "Claude Code 대화 이력 키워드 검색 (~/.claude/projects/*.jsonl)"
---

이전 Claude Code 세션 대화 이력에서 키워드를 검색합니다.

$ARGUMENTS

## 실행 방법

사용자가 제공한 키워드로 아래 명령을 실행하세요:

```bash
# WSL2에서 실행
python3 /mnt/c/Users/MSI/.claude/scripts/search-history.py "$ARGUMENTS"

# 옵션 사용 예시
python3 /mnt/c/Users/MSI/.claude/scripts/search-history.py "$ARGUMENTS" --last 30
python3 /mnt/c/Users/MSI/.claude/scripts/search-history.py "$ARGUMENTS" --role user
```

## 사용 예시

```
/search-history API 키                    # API 키 관련 대화 검색
/search-history supabase --last 50        # 최근 50개 파일에서 검색
/search-history 에러 해결 --role user     # 사용자 발화에서만 검색
```

## 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--last N` | 최근 N개 파일 검색 | 20 |
| `--context K` | 스니펫 표시 길이 | 200 |
| `--role` | user/assistant/all | all |

## 결과 해석

```
[2026-02-19 10:30] abc123.jsonl:45 (user)
  ...검색 키워드가 포함된 대화 내용 스니펫...
```

- `[타임스탬프]`: 해당 메시지 시간
- `파일명:줄번호`: 원본 위치
- `(역할)`: user 또는 assistant
