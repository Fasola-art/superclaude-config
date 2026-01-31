# Git 에러 패턴

> **카테고리**: git
> **갱신일**: 2026-01-30

---

## 🔴 Critical 에러

### Merge Conflict

**메시지**: `CONFLICT (content): Merge conflict in [파일]`

**해결책**:
```bash
# 1. 충돌 파일 확인
git status

# 2. 충돌 해결
# <<<<<<< HEAD
# 현재 브랜치 내용
# =======
# 머지하려는 브랜치 내용
# >>>>>>> feature-branch

# 3. 마커 제거 후 원하는 내용 유지

# 4. 스테이징 & 커밋
git add [파일]
git commit -m "Resolve merge conflict"

# 도구 사용
git mergetool
```

---

### Detached HEAD

**메시지**: `You are in 'detached HEAD' state`

**원인**: 브랜치 대신 커밋 체크아웃

**해결책**:
```bash
# 1. 현재 위치에서 브랜치 생성
git checkout -b new-branch-name

# 2. 또는 기존 브랜치로 복귀
git checkout main

# 3. 변경사항 있는 경우
git stash
git checkout main
git stash pop
```

---

### Push Rejected (non-fast-forward)

**메시지**: `Updates were rejected because the remote contains work`

**원인**: 리모트에 로컬에 없는 커밋 존재

**해결책**:
```bash
# 1. rebase (권장)
git pull --rebase origin main
git push

# 2. merge
git pull origin main
# 충돌 해결 후
git push

# ⚠️ force push (주의!)
git push --force-with-lease  # 다른 사람 작업 확인
```

---

## 🟠 Common 에러

### Permission Denied (publickey)

**원인**: SSH 키 인증 실패

**해결책**:
```bash
# 1. SSH 키 확인
ls -la ~/.ssh

# 2. SSH 에이전트에 키 추가
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. GitHub에 공개키 등록 확인
cat ~/.ssh/id_ed25519.pub
# GitHub > Settings > SSH keys에 추가

# 4. 연결 테스트
ssh -T git@github.com
```

---

### Failed to Push Some Refs

**원인**: 로컬/리모트 불일치

**해결책**:
```bash
# 1. 리모트 변경사항 가져오기
git fetch origin

# 2. 상태 확인
git status
git log --oneline --graph --all

# 3. rebase 또는 merge
git rebase origin/main
# 또는
git merge origin/main
```

---

### Fatal: refusing to merge unrelated histories

**원인**: 공통 조상 없는 브랜치 머지 시도

**해결책**:
```bash
# 명시적 허용
git merge other-branch --allow-unrelated-histories

# 또는 rebase
git rebase other-branch --allow-unrelated-histories
```

---

### Cannot lock ref

**원인**: 동시 Git 작업 또는 잠금 파일 잔존

**해결책**:
```bash
# 1. 잠금 파일 제거
rm -f .git/refs/heads/[브랜치].lock
rm -f .git/index.lock

# 2. 재시도
git [명령어]
```

---

## 🟡 Warning

### Your branch is behind

**해결책**:
```bash
# pull로 최신화
git pull origin main

# 또는 fetch 후 수동 머지
git fetch origin
git merge origin/main
```

---

### Changes not staged for commit

**해결책**:
```bash
# 스테이징
git add [파일]

# 전체 스테이징 (주의)
git add -A

# 변경사항 확인 후 스테이징
git add -p
```

---

### Unstaged changes after reset

**해결책**:
```bash
# line ending 문제일 가능성
git config core.autocrlf input  # macOS/Linux

# 또는
git config core.autocrlf true   # Windows

# 캐시 초기화
git rm --cached -r .
git reset --hard
```

---

## 🔧 복구 명령어

### 실수로 커밋 삭제

```bash
# reflog에서 찾기
git reflog

# 복구
git checkout [커밋해시]
git checkout -b recovered-branch
```

### 잘못된 커밋 수정

```bash
# 마지막 커밋 메시지 수정
git commit --amend -m "새 메시지"

# 마지막 커밋에 파일 추가
git add [파일]
git commit --amend --no-edit

# 여러 커밋 수정 (interactive rebase)
git rebase -i HEAD~3
```

### 작업 내용 임시 저장

```bash
# stash
git stash
git stash list
git stash pop

# stash 이름 지정
git stash push -m "작업 설명"
```

---

## 📊 에러 빈도

| 에러 | 빈도 | 심각도 |
|------|------|--------|
| Merge Conflict | 높음 | 중간 |
| Push Rejected | 높음 | 낮음 |
| Permission Denied | 중간 | 높음 |
| Detached HEAD | 중간 | 낮음 |

---

## 🔧 유용한 설정

```bash
# 자주 쓰는 alias
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"

# 기본 브랜치 설정
git config --global init.defaultBranch main

# pull 전략
git config --global pull.rebase true
```

---

**META**
- Category: git
- Last Updated: 2026-01-30
