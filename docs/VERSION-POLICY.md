# 버전 관리 정책 (Version Policy)

> SuperClaude 버전 관리 및 릴리즈 정책

---

## 버전 체계

### Semantic Versioning
```
MAJOR.MINOR.PATCH
  │     │     └── 버그 수정, 작은 개선
  │     └──────── 새 기능, 하위 호환
  └────────────── 주요 변경, 호환성 파괴
```

### 현재 버전
```
SuperClaude v2.0.9
```

---

## 버전 파일

### VERSION 파일
```
~/.claude/VERSION
```

내용: `2.0.9`

### 메타데이터
```json
// ~/.claude/superclaude-metadata.json
{
  "version": "2.0.9",
  "installed": "2026-01-29",
  "lastUpdated": "2026-01-30"
}
```

---

## 업데이트 정책

### 자동 업데이트
- 패치 버전: 자동 적용
- 마이너 버전: 알림 후 적용
- 메이저 버전: 수동 승인 필요

### 업데이트 확인
```
# 훅으로 자동 확인
~/.claude/hooks/UserPromptSubmit/auto-update-checker.js
```

---

## 릴리즈 노트

### 형식
```markdown
## v2.0.9 (2026-01-30)

### 새 기능
- 기능 A 추가
- 기능 B 개선

### 버그 수정
- 이슈 #123 수정
- 이슈 #456 수정

### 변경 사항
- 설정 X 변경
- 동작 Y 개선
```

---

## 호환성

### 플러그인 호환성
| SuperClaude | 플러그인 최소 버전 |
|-------------|-------------------|
| 2.0.x       | 1.0.0             |
| 2.1.x       | 1.1.0             |

### Claude Code 호환성
| SuperClaude | Claude Code |
|-------------|-------------|
| 2.0.x       | 1.0.x       |
