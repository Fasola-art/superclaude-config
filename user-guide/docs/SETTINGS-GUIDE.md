# 시스템 설정 가이드

> settings.json 상세 매뉴얼

---

## 파일 위치

```
~/.claude/settings.json
```

---

## 전체 구조

```json
{
  "$schema": "https://claude.ai/schemas/settings.json",
  "version": "2.0.9",
  "platform": "macOS",
  "hardware": { ... },
  "permissions": { ... },
  "parallelExecution": { ... },
  "context": { ... },
  "writerReviewer": { ... },
  "errorKB": { ... },
  "session": { ... },
  "language": { ... },
  "hooks": { ... }
}
```

---

## 섹션별 상세

### hardware (하드웨어 정보)

```json
{
  "hardware": {
    "model": "Mac Studio Ultra M2",
    "cpu_cores": 24,
    "gpu_cores": 76,
    "memory_gb": 192,
    "storage_tb": 8
  }
}
```

**용도**: 적응형 병렬 실행 최적화에 사용

---

### permissions (권한 설정)

```json
{
  "permissions": {
    "allow": [
      "Read:**",
      "Write:**",
      "Bash:npm install*",
      "Bash:git status*"
    ],
    "deny": [
      "Bash:git push*",
      "Bash:rm -rf*",
      "Read:.env*"
    ],
    "ask": []
  }
}
```

**패턴 문법**:
- `*`: 와일드카드
- `**`: 재귀 와일드카드
- 정확한 명령어 매칭

---

### parallelExecution (병렬 실행)

```json
{
  "parallelExecution": {
    "initial": 10,
    "scaleUp": 5,
    "scaleDown": 3,
    "maximum": 24,
    "consecutiveSuccessForScaleUp": 3
  }
}
```

| 설정 | 설명 | 기본값 |
|------|------|--------|
| initial | 시작 동시 실행 수 | 10 |
| scaleUp | 성공 시 증가량 | 5 |
| scaleDown | 실패 시 감소량 | 3 |
| maximum | 최대 동시 실행 (CPU 코어) | 24 |
| consecutiveSuccessForScaleUp | 스케일업 조건 | 3 |

---

### context (컨텍스트 관리)

```json
{
  "context": {
    "warningThreshold": 75,
    "criticalThreshold": 90,
    "emergencyThreshold": 95,
    "autoArchive": true
  }
}
```

| 설정 | 설명 | 기본값 |
|------|------|--------|
| warningThreshold | 경고 임계값 | 75% |
| criticalThreshold | 자동 DCP 임계값 | 90% |
| emergencyThreshold | 강제 압축 임계값 | 95% |
| autoArchive | 자동 아카이브 | true |

---

### writerReviewer (코드 검토)

```json
{
  "writerReviewer": {
    "enabled": true,
    "targetScore": 0.85,
    "maxIterations": 10,
    "convergenceThreshold": 0.015,
    "agents": {
      "quality": { "weight": 0.30 },
      "security": { "weight": 0.30, "minScore": 0.85 },
      "performance": { "weight": 0.20 },
      "accessibility": { "weight": 0.20 }
    }
  }
}
```

| 설정 | 설명 | 기본값 |
|------|------|--------|
| enabled | 활성화 여부 | true |
| targetScore | 목표 점수 | 0.85 |
| maxIterations | 최대 반복 | 10 |
| convergenceThreshold | 수렴 임계값 | 0.015 |

---

### errorKB (에러 지식베이스)

```json
{
  "errorKB": {
    "enabled": true,
    "similarityThreshold": 0.70,
    "maxRalphLoopRetries": 10,
    "autoLearnOnSuccess": true
  }
}
```

| 설정 | 설명 | 기본값 |
|------|------|--------|
| enabled | 활성화 여부 | true |
| similarityThreshold | Jaccard 유사도 임계값 | 0.70 |
| maxRalphLoopRetries | Ralph Loop 최대 재시도 | 10 |
| autoLearnOnSuccess | 성공 시 자동 학습 | true |

---

### session (세션 관리)

```json
{
  "session": {
    "autoSnapshot": true,
    "maxSnapshots": 10,
    "autoResume": true
  }
}
```

| 설정 | 설명 | 기본값 |
|------|------|--------|
| autoSnapshot | 자동 스냅샷 | true |
| maxSnapshots | 최대 스냅샷 수 | 10 |
| autoResume | 자동 복구 | true |

---

### language (언어 설정)

```json
{
  "language": {
    "response": "ko",
    "codeComments": "ko"
  }
}
```

| 설정 | 설명 | 기본값 |
|------|------|--------|
| response | 응답 언어 | ko |
| codeComments | 코드 주석 언어 | ko |

---

### hooks (훅 설정)

```json
{
  "hooks": {
    "enabled": true,
    "path": "~/.claude/hooks"
  }
}
```

| 설정 | 설명 | 기본값 |
|------|------|--------|
| enabled | 훅 활성화 | true |
| path | 훅 디렉토리 | ~/.claude/hooks |

---

## 환경별 오버라이드

### settings.local.json

로컬 환경 전용 설정 (git에서 제외)

```json
{
  "permissions": {
    "allow": [
      "Bash:sudo*"
    ]
  }
}
```

**우선순위**: settings.local.json > settings.json

---

## 설정 검증

```bash
# 설정 유효성 검사
claude config validate

# 현재 설정 확인
claude config show
```
