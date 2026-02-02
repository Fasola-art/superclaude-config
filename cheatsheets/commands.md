# Slash Commands Cheatsheet

> **Version**: 1.0.0
> **Updated**: 2026-01-30

---

## Quick Reference

### Most Used Commands (Top 10)

| Command | Description | Shortcut |
|---------|-------------|----------|
| `/commit` | Create git commit | - |
| `/project-status` | Project progress status | - |
| `/project-continue` | Continue interrupted work | - |
| `/recover` | Session recovery | - |
| `/error-search` | Search Error KB | - |
| `/help` | Help | - |
| `/market` | Today's economic outlook | - |
| `/review-pr` | PR code review | - |
| `/vibe` | Session Vibe settings | - |
| `/hookify` | Create hooks from conversation | - |

---

## Commands by Category

### Project Management

| Command | Description | Usage Example |
|---------|-------------|---------------|
| `/project-plan` | Create project plan | PRD-based planning |
| `/project-status` | Current progress | Task status check |
| `/project-continue` | Continue interrupted work | Restore STATE.md |
| `/recover` | Session/system recovery | After abnormal exit |

### Git Operations

| Command | Description | Options |
|---------|-------------|---------|
| `/commit` | Create git commit | Auto message generation |
| `/commit-push-pr` | Commit → Push → PR | One-stop |
| `/clean_gone` | Clean gone branches | Local cleanup |
| `/sc:git` | Git operations helper | General purpose |

### Code Analysis

| Command | Description | Output |
|---------|-------------|--------|
| `/code-review` | Pull request review | Detailed review |
| `/review-pr` | Agent-powered PR review | Parallel review |
| `/sc:analyze` | Code/project analysis | Structure analysis |
| `/sc:explain` | Code/concept explanation | Detailed explanation |

### Development Tools

| Command | Description | Target |
|---------|-------------|--------|
| `/sc:implement` | Feature implementation | Code generation |
| `/sc:improve` | Code improvement | Refactoring |
| `/sc:cleanup` | Code cleanup | Remove unused code |
| `/sc:test` | Run tests | Auto test |
| `/sc:build` | Build project | Run build |

### Finance/Trading

| Command | Description | Output |
|---------|-------------|--------|
| `/market` | Today's economic outlook | Report |
| `/sc:calendar` | Economic indicator schedule | Calendar |
| `/sc:news` | News collection and summary | Summary |
| `/sc:report` | Daily economic report | Report |
| `/telegram` | Telegram monitoring | AI summary |

### Plugin/Skill Development

| Command | Description | Guide |
|---------|-------------|-------|
| `/create-plugin` | Create plugin | Workflow |
| `/new-sdk-app` | Create Agent SDK app | TS/Python |
| `/hookify` | Create hook rules | Conversation analysis |
| `/feature-dev` | Feature development guide | Architecture |

### Documentation/Guides

| Command | Description | Reference |
|---------|-------------|-----------|
| `/help` | Plugin description | Ralph Loop |
| `/daily` | Frequently used paths | Path lookup |
| `/sc:document` | Generate documentation | Auto documentation |
| `/sc:index` | SC command list | This cheatsheet |

### Settings/Management

| Command | Description | Target |
|---------|-------------|--------|
| `/vibe` | Session Vibe settings | Current session |
| `/list` | hookify rules list | Rule lookup |
| `/configure` | Enable/disable hookify rules | Enable/Disable |
| `/revise-claude-md` | Update CLAUDE.md | Apply learnings |

### Loops/Automation

| Command | Description | Action |
|---------|-------------|--------|
| `/ralph-loop` | Start Ralph Loop | Auto work |
| `/cancel-ralph` | Cancel Ralph Loop | Stop |
| `/sc:workflow` | Execute workflow | Automation |
| `/sc:spawn` | Spawn agent | Parallel processing |

### Stripe Related

| Command | Description | Output |
|---------|-------------|--------|
| `/test-cards` | Stripe test cards | Card numbers |
| `/explain-error` | Stripe error explanation | Solutions |
| `/stripe-best-practices` | Stripe best practices | Guide |

### Troubleshooting

| Command | Description | Action |
|---------|-------------|--------|
| `/error-search` | Search Error KB | Similar errors |
| `/sc:troubleshoot` | Troubleshooting | Auto diagnosis |
| `/recover` | Session recovery | State restore |

---

## SC (SuperClaude) Commands Overview

### Development

| Command | Description |
|---------|-------------|
| `/sc:implement` | Feature implementation |
| `/sc:improve` | Code improvement |
| `/sc:cleanup` | Code cleanup |
| `/sc:test` | Run tests |
| `/sc:build` | Build project |

### Analysis

| Command | Description |
|---------|-------------|
| `/sc:analyze` | Code/project analysis |
| `/sc:explain` | Code/concept explanation |
| `/sc:design` | System/component design |
| `/sc:estimate` | Estimate task scope |

### Documentation

| Command | Description |
|---------|-------------|
| `/sc:document` | Generate documentation |
| `/sc:index` | SC command list |
| `/sc:load` | Load context |

### Automation

| Command | Description |
|---------|-------------|
| `/sc:workflow` | Execute workflow |
| `/sc:spawn` | Spawn agent |
| `/sc:task` | Task management |
| `/sc:git` | Git operations helper |

### Finance

| Command | Description |
|---------|-------------|
| `/sc:calendar` | Economic indicator schedule |
| `/sc:news` | News collection and summary |
| `/sc:report` | Daily economic report |

---

## Usage Scenarios

### Starting New Project

```
1. /project-plan     → Create plan
2. /sc:design        → Architecture design
3. /sc:implement     → Feature implementation
4. /sc:test          → Run tests
5. /commit           → Commit
```

### Code Review Flow

```
1. /review-pr        → PR review (agent-powered)
2. /sc:improve       → Apply improvements
3. /sc:test          → Verify tests
4. /commit-push-pr   → Merge
```

### Troubleshooting Flow

```
1. /error-search     → Search Error KB
2. /sc:troubleshoot  → Auto diagnosis
3. /sc:improve       → Apply fixes
4. /sc:test          → Verify
```

### Finance Analysis Flow

```
1. /market           → Today's outlook
2. /sc:calendar      → Release schedule
3. /sc:news          → Collect news
4. /sc:report        → Generate report
```

---

## Cautions

| Command | Caution |
|---------|---------|
| `/commit-push-pr` | Includes remote push |
| `/ralph-loop` | May run for extended time |
| `/clean_gone` | Deletes local branches |
| `/hookify` | Creates hook files |

---

## References

| Document | Path |
|----------|------|
| Skills Guide | `~/.claude/CLAUDE_SKILLS_GUIDE.md` |
| Installed Skills | `~/.claude/INSTALLED_SKILLS.md` |
| Hook System | `~/.claude/docs/HOOKS-SYSTEM.md` |

---

**META**
- Version: 1.0.0
- Last Updated: 2026-01-30
