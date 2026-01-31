# Error Knowledge Base (Error KB)

> **버전**: 1.0.0
> **목적**: 에러 패턴 학습 및 자동 해결 지원

---

## 🎯 목표

**Primary Outcome**: 반복되는 에러를 자동으로 인식하고 해결책을 제안

**동작 방식**:
1. 에러 발생 → `pending/`에 기록
2. 해결 시 → `resolved/`로 이동 + 해결책 저장
3. 유사 에러 발생 → Jaccard 유사도로 매칭 (threshold: 0.70)
4. 매칭 성공 → 이전 해결책 자동 적용

---

## 📁 디렉토리 구조

```
error-kb/
├── README.md              # 이 파일 (인덱스)
├── pending/               # 미해결 에러
│   └── {hash}.json
├── resolved/              # 해결된 에러
│   └── {hash}.json
├── categories/            # 카테고리별 패턴
│   ├── typescript.md
│   ├── react.md
│   ├── nextjs.md
│   ├── mcp.md
│   └── git.md
├── patterns/              # Quick Fix 패턴 매핑
│   ├── README.md
│   └── error-success-map.json
└── templates/             # 등록 템플릿
    └── error-entry.json
```

---

## 📊 현재 상태

### 통계

| 항목 | 수 |
|------|-----|
| 해결된 에러 | 8개 |
| 미해결 에러 | 4개 |
| 카테고리 | 5개 |

### 최근 해결된 에러

| ID | 타입 | 메시지 | 해결책 |
|----|------|--------|--------|
| cd40c474953d | mcp-protocol | 서버 시작 실패: gdrive | @isaacphi/mcp-gdrive로 대체 |
| 8153edd3e663 | mcp-protocol | - | - |

---

## 🔧 사용 방법

### 에러 검색

```bash
# 슬래시 명령어
/error-search "에러 메시지"

# 또는 Vibe 키워드
"고쳐 이 TypeError"
```

### 수동 등록

```bash
# pending에 새 에러 추가
cp templates/error-entry.json pending/{new-hash}.json
# 내용 수정 후 저장
```

### 해결 완료 처리

```bash
# resolved로 이동
mv pending/{hash}.json resolved/{hash}.json
# resolution 필드 업데이트
```

---

## 📋 JSON 스키마

### 에러 엔트리 구조

```json
{
  "id": "string (12자 해시)",
  "type": "string (에러 카테고리)",
  "message": "string (에러 메시지)",
  "timestamp": "string (발생 시각)",
  "raw_log": "string (원본 로그)",
  "created_at": "string (ISO 8601)",
  "resolved": "boolean",
  "resolution": "string | null (해결책)",
  "context": "object (추가 컨텍스트)",
  "resolved_at": "string | null (해결 시각)",
  "tags": ["string"] (선택),
  "related_files": ["string"] (선택),
  "prevention": "string (재발 방지책, 선택)"
}
```

### 필수 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | string | 고유 해시 (12자) |
| `type` | string | 에러 카테고리 |
| `message` | string | 에러 메시지 |
| `resolved` | boolean | 해결 여부 |

### 선택 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `resolution` | string | 해결 방법 |
| `context` | object | 추가 정보 |
| `tags` | string[] | 검색용 태그 |
| `prevention` | string | 재발 방지책 |

---

## 🏷️ 에러 타입 (카테고리)

| 타입 | 설명 | 예시 |
|------|------|------|
| `typescript` | TS 컴파일 에러 | TS2304, TS2345 |
| `react` | React 런타임 에러 | Hydration, Hook rules |
| `nextjs` | Next.js 에러 | Build, SSR, App Router |
| `mcp-protocol` | MCP 서버 에러 | 연결 실패, 타임아웃 |
| `git` | Git 에러 | 충돌, 권한, 리모트 |
| `npm` | 패키지 에러 | 설치, 버전 충돌 |
| `build` | 빌드 에러 | Webpack, Vite |
| `runtime` | 런타임 에러 | TypeError, ReferenceError |

---

## 🔍 유사도 매칭

### Jaccard 유사도

```python
def jaccard_similarity(a: str, b: str) -> float:
    tokens_a = set(tokenize(a))
    tokens_b = set(tokenize(b))
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union)
```

### 매칭 설정

```yaml
threshold: 0.70          # 70% 이상 유사 시 매칭
max_suggestions: 3       # 최대 3개 제안
boost_same_type: 0.1     # 같은 타입이면 가산점
```

---

## 📚 카테고리별 문서

### 빠른 링크

| 카테고리 | 문서 | 주요 패턴 |
|---------|------|----------|
| TypeScript | [typescript.md](categories/typescript.md) | TS2304, TS2345, strict mode |
| React | [react.md](categories/react.md) | Hydration, Hook rules |
| Next.js | [nextjs.md](categories/nextjs.md) | App Router, SSR |
| MCP | [mcp.md](categories/mcp.md) | 연결, 타임아웃 |
| Git | [git.md](categories/git.md) | 충돌, 리모트 |

---

## 🔄 자동 학습

### Self-Healing 흐름

```
1. 에러 발생
2. Error KB 검색 (유사도 0.70+)
3. 매칭 시:
   - 이전 해결책 자동 적용
   - 빌드/테스트 확인
   - 성공 시 완료
   - 실패 시 다음 해결책 시도 (최대 10회)
4. 미매칭 시:
   - pending에 기록
   - 사용자에게 알림
```

### 학습 트리거

| 이벤트 | 동작 |
|--------|------|
| 수동 해결 | resolution 필드 업데이트 |
| 패턴 인식 | 유사 에러 그룹화 |
| 빈번한 발생 | 우선순위 상향 |

---

## ⚠️ 주의사항

1. **개인정보 제외**: 에러 로그에 API 키, 비밀번호 포함 금지
2. **컨텍스트 최소화**: 필요한 정보만 저장
3. **정기 정리**: 오래된 pending 항목 검토
4. **유사도 조정**: 너무 많은 오탐 시 threshold 상향

---

## 📊 통계 명령어

```bash
# 전체 통계
ls -la ~/.claude/error-kb/{pending,resolved}/ | wc -l

# 타입별 통계
grep -l '"type": "typescript"' ~/.claude/error-kb/**/*.json | wc -l

# 최근 해결된 에러
ls -lt ~/.claude/error-kb/resolved/ | head -5
```

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
- Similarity Threshold: 0.70
- Max Ralph Retries: 10
