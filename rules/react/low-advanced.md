# React Low Priority Rules: JS-OPT (7-12)

## JS-OPT: Advanced Patterns

### JS-OPT-007: Lazy Initialization
```typescript
// BAD: Computed every render
const [state, setState] = useState(expensiveComputation());

// GOOD: Computed once
const [state, setState] = useState(() => expensiveComputation());
```

### JS-OPT-008: No Conditional Hooks
```typescript
// BAD: Conditional Hook (error!)
if (condition) {
  useEffect(() => {}, []);
}

// GOOD: Condition inside Hook
useEffect(() => {
  if (condition) {
    // Logic
  }
}, [condition]);
```

### JS-OPT-009: Unique Keys
```typescript
// BAD: Index as key
{items.map((item, index) => <Item key={index} />)}

// GOOD: Unique ID
{items.map(item => <Item key={item.id} />)}
```

### JS-OPT-010: Fragment
```typescript
// BAD: Unnecessary div
return (<div><Header /><Content /></div>);

// GOOD: Fragment
return (<><Header /><Content /></>);
```

### JS-OPT-011: Optional Chaining
```typescript
// BAD
const name = user && user.profile && user.profile.name;

// GOOD
const name = user?.profile?.name;
```

### JS-OPT-012: Nullish Coalescing
```typescript
// BAD
const value = data !== null && data !== undefined ? data : defaultValue;

// GOOD
const value = data ?? defaultValue;
```

---

## Checklist

### Setup
- [ ] Server Components default
- [ ] Minimize 'use client'
- [ ] Configure next/image
- [ ] Bundle analyzer

### Review
- [ ] Promise.all used
- [ ] No barrel imports
- [ ] Cache strategy
- [ ] memo/useMemo/useCallback

### Deploy
- [ ] Bundle size
- [ ] Lighthouse score
- [ ] Core Web Vitals
