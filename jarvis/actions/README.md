# JARVIS Actions Module

자연어 명령 실행(Do) 및 작업 컨텍스트 저장/복원(Remember/Recall)

## Quick Start

```python
from actions import save_context, get_last_context, search_contexts

# 작업 저장
save_context("/path/to/project", "API 연동 완료", tags=["api", "fastapi"])

# 복원
ctx = get_last_context("/path/to/project")
print(ctx['conversation_summary'])

# 검색
results = search_contexts("api")
```

## 주요 기능

### Remember (저장)

```python
from actions import save_context, save_quick_context

# 상세 저장
save_context(
    project_path="/path/to/project",
    summary="작업 요약",
    tags=["tag1", "tag2"],
    last_file="main.py"
)

# 빠른 저장
save_quick_context("메모 내용", tags=["memo"])
```

### Recall (조회)

```python
from actions import (
    get_last_context,      # 최근 컨텍스트
    get_contexts_by_tag,   # 태그 검색
    get_recent_contexts,   # 최근 N개
    search_contexts        # 키워드 검색
)

ctx = get_last_context()
results = get_contexts_by_tag("api")
recent = get_recent_contexts(limit=10)
found = search_contexts("데이터베이스")
```

### Do (자율실행)

```python
from actions.do import execute_command

execute_command('내일까지 "보고서 작성" 추가해줘')
execute_command('할 일 목록 보여줘')
execute_command('지금까지 작업 내용 기억해줘')
```

## CLI 데모

```bash
# 저장
python3 actions/demo_remember_recall.py save /tmp/project "요약" tag1 tag2
python3 actions/demo_remember_recall.py quick "메모" tag1

# 조회
python3 actions/demo_remember_recall.py last
python3 actions/demo_remember_recall.py tag api
python3 actions/demo_remember_recall.py recent 5
python3 actions/demo_remember_recall.py search keyword
```

## 파일 구조

```
actions/
├── remember.py (77줄)    # 컨텍스트 저장
├── recall.py (61줄)      # 컨텍스트 조회
├── do.py (100줄)         # 자율실행
├── handlers_*.py         # Do 핸들러
├── demo_*.py             # 데모 CLI
└── test_*.py             # 테스트
```

## 테스트

```bash
python3 actions/test_remember_recall.py
python3 actions/test_do.py
```
