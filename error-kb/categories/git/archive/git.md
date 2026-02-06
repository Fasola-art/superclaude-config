# Git Error Patterns

> **Category**: git
> **Updated**: 2026-01-30

---

## 🔴 Critical Errors

### Merge Conflict

**Message**: `CONFLICT (content): Merge conflict in [file]`

**Solutions**:
```bash
# 1. Check conflicting files
git status

# 2. Resolve conflicts
# <<<<<<< HEAD
# Current branch content
# =======
# Branch being merged content
# >>>>>>> feature-branch

# 3. Remove markers and keep desired content

# 4. Stage & commit
git add [file]
git commit -m "Resolve merge conflict"

# Use tool
git mergetool
```

---

### Detached HEAD

**Message**: `You are in 'detached HEAD' state`

**Cause**: Checked out commit instead of branch

**Solutions**:
```bash
# 1. Create branch at current position
git checkout -b new-branch-name

# 2. Or return to existing branch
git checkout main

# 3. If there are changes
git stash
git checkout main
git stash pop
```

---

### Push Rejected (non-fast-forward)

**Message**: `Updates were rejected because the remote contains work`

**Cause**: Remote has commits not in local

**Solutions**:
```bash
# 1. Rebase (recommended)
git pull --rebase origin main
git push

# 2. Merge
git pull origin main
# After resolving conflicts
git push

# ⚠️ Force push (caution!)
git push --force-with-lease  # Verify no others' work
```

---

## 🟠 Common Errors

### Permission Denied (publickey)

**Cause**: SSH key authentication failed

**Solutions**:
```bash
# 1. Check SSH keys
ls -la ~/.ssh

# 2. Add key to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. Verify public key registered on GitHub
cat ~/.ssh/id_ed25519.pub
# Add to GitHub > Settings > SSH keys

# 4. Test connection
ssh -T git@github.com
```

---

### Failed to Push Some Refs

**Cause**: Local/remote mismatch

**Solutions**:
```bash
# 1. Fetch remote changes
git fetch origin

# 2. Check status
git status
git log --oneline --graph --all

# 3. Rebase or merge
git rebase origin/main
# Or
git merge origin/main
```

---

### Fatal: refusing to merge unrelated histories

**Cause**: Attempting to merge branches with no common ancestor

**Solutions**:
```bash
# Explicitly allow
git merge other-branch --allow-unrelated-histories

# Or rebase
git rebase other-branch --allow-unrelated-histories
```

---

### Cannot lock ref

**Cause**: Concurrent Git operation or stale lock file

**Solutions**:
```bash
# 1. Remove lock file
rm -f .git/refs/heads/[branch].lock
rm -f .git/index.lock

# 2. Retry
git [command]
```

---

## 🟡 Warnings

### Your branch is behind

**Solutions**:
```bash
# Update with pull
git pull origin main

# Or fetch then manual merge
git fetch origin
git merge origin/main
```

---

### Changes not staged for commit

**Solutions**:
```bash
# Stage
git add [file]

# Stage all (caution)
git add -A

# Interactive staging
git add -p
```

---

### Unstaged changes after reset

**Solutions**:
```bash
# Likely line ending issue
git config core.autocrlf input  # macOS/Linux

# Or
git config core.autocrlf true   # Windows

# Clear cache
git rm --cached -r .
git reset --hard
```

---

## 🔧 Recovery Commands

### Accidentally Deleted Commits

```bash
# Find in reflog
git reflog

# Recover
git checkout [commit-hash]
git checkout -b recovered-branch
```

### Fix Wrong Commit

```bash
# Amend last commit message
git commit --amend -m "new message"

# Add file to last commit
git add [file]
git commit --amend --no-edit

# Edit multiple commits (interactive rebase)
git rebase -i HEAD~3
```

### Temporarily Save Work

```bash
# Stash
git stash
git stash list
git stash pop

# Stash with name
git stash push -m "work description"
```

---

## 📊 Error Frequency

| Error | Frequency | Severity |
|-------|-----------|----------|
| Merge Conflict | High | Medium |
| Push Rejected | High | Low |
| Permission Denied | Medium | High |
| Detached HEAD | Medium | Low |

---

## 🔧 Useful Settings

```bash
# Common aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"

# Default branch setting
git config --global init.defaultBranch main

# Pull strategy
git config --global pull.rebase true
```

---

**META**
- Category: git
- Last Updated: 2026-01-30
