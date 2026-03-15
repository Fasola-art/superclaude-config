# Agent/Skill Mandatory Rules

> **CRITICAL**: 이 규칙 위반 시 작업 거부

## Line Limits (STRICT - NO EXCEPTIONS)

| Type | Max Lines | Violation Action |
|------|-----------|------------------|
| Rules/Guides | **120** | Split or reject |
| Reference | **150** | Split or reject |
| Hook scripts | **150** | Split to _shared/ |
| Index | **50** | Merge or reject |
| Templates | **30** | Simplify |

**MIN 20 lines**: Under 20 → merge with related file

## Before File Creation (MANDATORY)

1. `wc -l` equivalent check → reject if exceeds limit
2. Check existing content → reference instead of duplicate
3. Single topic only → split if multiple topics
4. Extract shared patterns → `_shared/`

## Content Rules

- **No verbose explanations**: Tables over prose
- **No boilerplate**: Skip obvious headers
- **Minimal examples**: 1-2 per concept max
- **Active voice only**: Direct imperatives

## Prohibited

- Stub/placeholder code
- Duplicate content
- Files exceeding line limits
- Multiple topics in one file
