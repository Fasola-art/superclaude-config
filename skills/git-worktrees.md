---
name: git-worktrees
description: Git Worktrees로 병렬 브랜치 개발 - 탭별 독립 Claude Code 컨텍스트
version: "1.0.0"
triggers:
  - /git-worktrees
  - "worktree 만들어"
  - "병렬 브랜치 개발"
  - "동시에 여러 브랜치"
---

# Git Worktrees - 병렬 브랜치 개발

## 핵심 개념

- 하나의 Git 저장소 → 여러 디렉토리에 동시 체크아웃
- 각 worktree = 독립 작업 공간 (브랜치 충돌 없음)
- WSL2 Windows Terminal 탭별 독립 Claude Code 세션 실행 가능

## 핵심 명령어

```bash
# 새 worktree 생성 (원격 브랜치 기반)
git worktree add ../project-feature origin/feature

# 새 브랜치와 함께 생성
git worktree add -b my-experiment ../project-experiment

# 목록 확인
git worktree list

# 정리 (worktree 제거)
git worktree remove ../project-feature

# 사용 안 하는 worktree 정리
git worktree prune
```

## WSL2 워크플로우

```bash
# 탭 1: 메인 개발
wsl -d Ubuntu
cd ~/projects/myapp        # 메인 브랜치
claude                     # Claude Code 세션 1

# 탭 2: 실험적 기능
wsl -d Ubuntu
git worktree add ~/projects/myapp-experiment -b experiment/new-api
cd ~/projects/myapp-experiment
claude                     # 독립 Claude Code 세션 2

# 탭 3: 핫픽스
wsl -d Ubuntu
git worktree add ~/projects/myapp-hotfix -b hotfix/urgent-bug
cd ~/projects/myapp-hotfix
claude                     # 독립 Claude Code 세션 3
```

## 주의사항

| 항목 | 내용 |
|------|------|
| 같은 브랜치 | 동일 브랜치 2개 동시 체크아웃 불가 |
| 파일 위치 | WSL2 내부(`~/projects/`) 권장 (Windows 경로 사용 금지) |
| 정리 | 작업 완료 후 `git worktree remove` 실행 |

## Claude Code 연동 패턴

각 worktree에서 독립적으로:
- 별도 CLAUDE.md 설정 가능
- 별도 context 유지
- 병렬 작업 후 PR 생성
