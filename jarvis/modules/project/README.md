# Project Monitor

프로젝트 파일 시스템 모니터링 모듈.

## 기능

- 프로젝트 파일 구조 스캔
- 파일 타입별 통계
- 변경사항 감지 (추가/삭제/수정)
- .gitignore 자동 존중

## 사용법

```python
from modules.project import ProjectMonitor

monitor = ProjectMonitor()

# 프로젝트 스캔
state = monitor.scan_project('/path/to/project')
print(f"총 파일: {state.total_files}개")
print(f"파일 타입: {state.file_types}")

# 변경사항 감지
changes = monitor.detect_changes('/path/to/project')
print(f"추가: {changes['added']}개")
print(f"삭제: {changes['removed']}개")
print(f"수정: {changes['modified']}개")
```

## 파일 구조

- `monitor.py` - ProjectMonitor 클래스 (93줄)
- `scanner.py` - 파일 시스템 스캐너 (76줄)
- `types.py` - 타입 정의 (24줄)
- `test_monitor.py` - 테스트 (110줄)
- `demo.py` - 데모 (46줄)

## 테스트

```bash
python3 -m modules.project.test_monitor
```

## 데모

```bash
python3 -m modules.project.demo
```
