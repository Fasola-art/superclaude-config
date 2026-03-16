# Claude Code 생산성 향상 PRD & 구현 워크플로우

## Context

4개 URL 분석 결과 (Advent of Claude 2025, Bash for AI Engineers, 45 Claude Code Tips, 해커톤 우승자 70팁)에서 추출한 기능들을 기존 SuperClaude v2.0.9에 통합. 중복 구현 없이 누락된 기능만 추가.

---

## 현황 분석: 이미 구현된 기능 (스킵)

| 기능 | 파일 |
|------|------|
| 컨텍스트 70% 알림 | `hooks/UserPromptSubmit/auto-context-manager.py` |
| 위험 명령어 감사 (cc-safe 역할) | `hooks/PreToolUse/safety-snapshot.py` |
| 세션 저장 | `hooks/Stop/session-saver.py` |
| 컨텍스트 사용량 확인 | `commands/ctx.md` |
| CLAUDE.md 업데이트 | `commands/revise-claude-md.md` |

---

## 구현 대상 (10개 기능)

### Phase 1 — 즉시 적용 (의존성 없음)

#### 1. Custom Status Line
- **파일:** `C:\Users\MSI\.claude\statusline.sh`
- **용도:** 터미널 하단에 모델명, 디렉토리, Git 브랜치, 미커밋 수, 컨텍스트 % 표시
- **WSL2 alias:** `alias cst='bash ~/.claude/statusline.sh'` → `~/.bashrc`

```bash
#!/usr/bin/env bash
CLAUDE_DIR="/mnt/c/Users/MSI/.claude"
model=$(python3 -c "import json,pathlib; d=json.loads(pathlib.Path('$CLAUDE_DIR/settings.json').read_text()); print(d.get('model','sonnet'))" 2>/dev/null || echo "sonnet")
branch=$(git branch --show-current 2>/dev/null)
dirty=$(git status --porcelain 2>/dev/null | wc -l)
ctx=$(python3 -c "
import os,pathlib
d=pathlib.Path('$CLAUDE_DIR/projects')
files=list(d.rglob('*.jsonl')) if d.exists() else []
if not files: print('0%')
else:
    f=max(files,key=os.path.getmtime)
    print(f'{min(int(os.path.getsize(f)/1024/1024*50),100)}%')
" 2>/dev/null || echo "?%")
echo "[$model] $(basename $PWD) | ${branch:-no-git}(${dirty}files) | ctx:$ctx"
```

#### 2. /handoff 커맨드
- **파일:** `C:\Users\MSI\.claude\commands\handoff.md`
- **용도:** 세션 종료 시 HANDOFF.md 자동 생성 (완료작업 / 시도한해결책 / 다음단계 / 주의사항)
- **기존과 차별점:** `session-saver.py`는 JSON (기계용), `/handoff`는 Markdown (인간용)

```markdown
---
description: "HANDOFF.md 자동 생성 - 다음 세션 인수인계"
---
현재 세션을 분석하여 프로젝트 루트에 HANDOFF.md를 생성하세요.

## Completed
- 이번 세션 완료 작업 목록

## Attempted
- 성공한 접근법
- 실패한 접근법 + 이유

## Next Steps
- 우선순위 순 미완료 작업

## Watch Out
- 알려진 버그, 건드리지 말아야 할 파일

## Recovery
```bash
cat HANDOFF.md && /project-continue
```
```

#### 3. /fork 커맨드
- **파일:** `C:\Users\MSI\.claude\commands\fork.md`
- **용도:** 실험적 방향 시도를 위한 논리적 분기점 문서화
- **구현:** FORK_CONTEXT.md 생성 + `git checkout -b experiment/$(date +%Y%m%d)` 안내

#### 4. /half-clone 커맨드
- **파일:** `C:\Users\MSI\.claude\commands\half-clone.md`
- **용도:** 컨텍스트 과부하 시 최근 N개 메시지 핵심만 추출 후 /compact 안내
- **트리거:** 컨텍스트 85%+ 초과 시

---

### Phase 2 — 단기 (외부 도구 필요)

#### 5. /review-claudemd 커맨드 (기존 revise와 역할 분리)
- **파일:** `C:\Users\MSI\.claude\commands\review-claudemd.md`
- **용도:** CLAUDE.md 토큰 효율성 분석, 중복 규칙 감지, 개선 제안 (실행 X)
- **기존 revise-claude-md.md:** 업데이트 실행 도구 (역할 다름, 충돌 없음)

```markdown
---
description: "CLAUDE.md 분석 전용 - 토큰 효율성 평가 및 개선 제안"
---
~/.claude/CLAUDE.md를 읽고 분석:
1. 중복 규칙 식별 (같은 의미 반복)
2. 충돌 규칙 쌍 감지
3. 미사용 슬래시 커맨드 탐지
4. 예상 토큰 절감량 계산 (현재 ~19k → 목표 9k)
5. [HIGH/MED/LOW] 우선순위별 개선 제안 목록
```

#### 6. Gemini CLI 통합 스킬
- **파일:** `C:\Users\MSI\.claude\skills\gemini-fetch.md`
- **용도:** WebFetch 불가 사이트 크롤링 대안 (Reddit 등)
- **설치 (WSL2):**
  ```bash
  nvm use 24 && npm install -g @google/generative-ai-cli
  export GEMINI_API_KEY="your-key"  # ~/.bashrc에 추가
  ```
- **패턴:** `gemini --url <URL> "내용 요약"` → Claude가 결과 분석

#### 7. Git Worktrees 워크플로우 스킬
- **파일:** `C:\Users\MSI\.claude\skills\git-worktrees.md`
- **용도:** 병렬 브랜치 개발 (탭별 독립 Claude Code 컨텍스트)
- **핵심 명령:**
  ```bash
  git worktree add ../project-feature origin/feature  # 새 worktree
  git worktree list                                    # 목록
  git worktree remove ../project-feature               # 정리
  ```
- **WSL2:** Windows Terminal 탭마다 별도 WSL 세션 → 자연 분리됨

---

### Phase 3 — 중기 (스크립트 개발)

#### 8. 대화 이력 검색
- **파일:** `C:\Users\MSI\.claude\scripts\search-history.py`
- **커맨드:** `C:\Users\MSI\.claude\commands\search-history.md`
- **용도:** `~/.claude/projects/*.jsonl` JSONL 파싱으로 키워드 검색
- **사용:** `/search-history <키워드>`

```python
#!/usr/bin/env python3
import json, sys, argparse
from pathlib import Path

PROJECTS_DIR = Path("/mnt/c/Users/MSI/.claude/projects")

def search(keyword, last_n=20):
    files = sorted(PROJECTS_DIR.rglob("*.jsonl"),
                   key=lambda f: f.stat().st_mtime, reverse=True)
    for f in files[:last_n]:
        for line in f.read_text(errors='ignore').splitlines():
            try:
                entry = json.loads(line)
                text = str(entry.get("message", ""))
                if keyword.lower() in text.lower():
                    print(f"[{f.name}] {text[:200]}")
            except: pass

if __name__ == "__main__":
    search(sys.argv[1] if len(sys.argv) > 1 else "")
```

#### 9. 컨텍스트 85% 임계값 훅
- **파일:** `C:\Users\MSI\.claude\hooks\UserPromptSubmit\context-threshold-85.py`
- **용도:** 85% 도달 시 `/handoff` 자동 실행 권장 알림
- **기존 70% 훅과 충돌 없음** (다른 임계값, 다른 액션)
- **settings.json 추가:**
  ```json
  {"type": "command", "command": "python C:/Users/MSI/.claude/hooks/UserPromptSubmit/context-threshold-85.py"}
  ```

---

### Phase 4 — 장기 (선택)

#### 10. 시스템 프롬프트 최적화
- **목표:** CLAUDE.md 토큰 19k → 9k (50% 감소)
- **방법:** `/review-claudemd` 실행 후 중복 제거
- **프로젝트별 CLAUDE.md:** 각 프로젝트 루트에 언어별 간소화 버전 배치

---

## 파일 생성 목록 (우선순위 순)

```
Phase 1 (즉시):
C:\Users\MSI\.claude\statusline.sh
C:\Users\MSI\.claude\commands\handoff.md
C:\Users\MSI\.claude\commands\fork.md
C:\Users\MSI\.claude\commands\half-clone.md

Phase 2 (단기):
C:\Users\MSI\.claude\commands\review-claudemd.md
C:\Users\MSI\.claude\skills\gemini-fetch.md
C:\Users\MSI\.claude\skills\git-worktrees.md

Phase 3 (중기):
C:\Users\MSI\.claude\scripts\search-history.py
C:\Users\MSI\.claude\commands\search-history.md
C:\Users\MSI\.claude\hooks\UserPromptSubmit\context-threshold-85.py
+ settings.json UserPromptSubmit 배열에 훅 추가
```

---

## settings.json 변경 사항

`UserPromptSubmit` 훅 배열 마지막에 추가:
```json
{
  "type": "command",
  "command": "python C:/Users/MSI/.claude/hooks/UserPromptSubmit/context-threshold-85.py"
}
```

---

## 검증 방법

```bash
# Phase 1 검증
bash ~/.claude/statusline.sh                    # 상태 표시 확인
/handoff                                         # HANDOFF.md 생성 확인
/fork "실험적 방향"                              # FORK_CONTEXT.md 생성 확인

# Phase 2 검증
/review-claudemd                                 # 분석 보고서 출력 확인
gemini --version                                 # Gemini CLI 설치 확인
git worktree list                                # Worktree 동작 확인

# Phase 3 검증
python3 ~/.claude/scripts/search-history.py "테스트" # 검색 결과 확인
/search-history "이전 작업"                      # 커맨드 동작 확인
```

---

## 예상 효과

| 기능 | 구현 시간 | 일일 절감 |
|------|-----------|-----------|
| statusline | 1h | 2-3min (ctx 확인 불필요) |
| /handoff | 30min | 10-15min (세션 재개 빠름) |
| /fork | 30min | 5-10min (실험 관리) |
| Git Worktrees | 1h | 20-30min (브랜치 전환) |
| search-history | 2h | 5-10min (이전 작업 탐색) |
| **총합** | **~8h** | **~45min/일** |

**월간 ROI:** 8h 투자 → 약 15h 절감
