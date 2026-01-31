# Error KB - Patterns 폴더

> **목적**: 공통 에러 패턴 및 Quick Fix 솔루션 매핑
> **갱신일**: 2026-01-30

---

## 📁 파일 구조

```
patterns/
├── README.md              # 이 파일
└── error-success-map.json # 에러 패턴 → 솔루션 매핑
```

---

## 🎯 작동 원리

1. **에러 발생** → 에러 메시지 추출
2. **패턴 매칭** → `error-success-map.json`의 regex와 비교
3. **Quick Fix 제안** → 매칭된 패턴의 `fix` 명령어 제안
4. **자동 적용** (선택) → 사용자 승인 후 `fix` 실행

---

## 📋 패턴 유형

| 유형 | 설명 | 예시 |
|------|------|------|
| **quick_fixes** | 정규식 기반 즉시 해결 | `npm install $1` |
| **error_classifications** | 카테고리별 일반 솔루션 | `typescript_error` |

---

## 🔧 패턴 추가 방법

### Quick Fix 추가
```json
{
  "id": "qf_xxx",
  "regex": "에러 메시지 패턴 (캡처 그룹 사용)",
  "fix": "해결 명령어 ($1, $2 등으로 캡처 그룹 참조)",
  "description": "한글 설명",
  "category": "분류 카테고리"
}
```

### 에러 분류 추가
```json
{
  "type": "new_error_type",
  "patterns": ["패턴1", "패턴2"],
  "solutions": ["솔루션1", "솔루션2"]
}
```

---

## 📊 연관 파일

- `~/.claude/error-kb/categories/` - 카테고리별 상세 문서
- `~/.claude/error-kb/pending/` - 미해결 에러
- `~/.claude/error-kb/resolved/` - 해결된 에러

---

**META**
- Category: error-kb/patterns
- Last Updated: 2026-01-30
