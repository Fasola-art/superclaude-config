# TypeScript/React/Next.js Language Profile

> **Version**: 1.0.0
> **Target**: TypeScript 5.x, React 18+, Next.js 14+
> **Auto-detect**: `package.json` or `tsconfig.json`

---

## Goal

**Primary Outcome**: Generate type-safe and performance-optimized code

**Success Criteria**:
- [ ] Comply with `strict: true` mode
- [ ] Zero `any` types
- [ ] Bundle size optimized (no barrel imports)
- [ ] Proper Server/Client component separation

**Failure Cases**:
- `@ts-ignore` usage → Requires type fix
- Runtime type error → Add type guard

---

## Quick Reference

### Required Rules

| Rule | Description | Example |
|------|-------------|---------|
| **strict mode** | tsconfig.json strict: true | No implicit any |
| **explicit return** | Explicit function return types | `fn(): string` |
| **null check** | Optional chaining | `user?.name` |
| **no barrel** | Direct import | `from '@/Button'` |

### Recommended Rules

| Rule | Reason | Alternative |
|------|--------|-------------|
| `unknown` > `any` | Type safety | Narrow with guard |
| `const assertion` | Preserve literals | `as const` |
| `satisfies` | Type validation | TS 4.9+ |

---

## Files

| File | Content |
|------|---------|
| [type-system.md](type-system.md) | Type definition patterns |
| [react-components.md](react-components.md) | Component patterns |
| [nextjs-app-router.md](nextjs-app-router.md) | App Router rules |
| [imports-exports.md](imports-exports.md) | Import/Export rules |
| [error-handling.md](error-handling.md) | Error handling |
| [performance.md](performance.md) | Performance + Testing |

---

## Self-Diagnosis Checklist

### Critical (Must Complete)
- [ ] `tsconfig.json` has `strict: true`
- [ ] Zero `any` type usage
- [ ] Zero barrel import usage
- [ ] Proper Server/Client separation

### Important (80%+)
- [ ] Explicit return types
- [ ] Unified error handling
- [ ] No unnecessary re-renders
- [ ] Image optimization

**Pass Criteria**: Critical 100% + Important 80%+

---

## References

| Document | Link |
|----------|------|
| TypeScript | https://www.typescriptlang.org/docs/ |
| React | https://react.dev/ |
| Next.js | https://nextjs.org/docs |
| Vercel Rules | `~/.claude/rules/react/` |
