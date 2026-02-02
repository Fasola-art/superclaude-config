# React Error Patterns

> **Category**: react
> **Updated**: 2026-01-30

---

## 🔴 Critical Errors

### Hydration Mismatch

**Message**: `Text content does not match server-rendered HTML`

**Cause**: Server/client rendering mismatch

**Solutions**:
```typescript
// ❌ Cause: Client-only values
function Component() {
  return <div>{new Date().toLocaleString()}</div>;  // Different on server/client
}

// ✅ Fix 1: useEffect
function Component() {
  const [time, setTime] = useState<string>();
  useEffect(() => {
    setTime(new Date().toLocaleString());
  }, []);
  return <div>{time}</div>;
}

// ✅ Fix 2: suppressHydrationWarning
<time suppressHydrationWarning>
  {new Date().toLocaleString()}
</time>

// ✅ Fix 3: dynamic import (ssr: false)
const ClientOnly = dynamic(() => import('./ClientComponent'), {
  ssr: false
});
```

**Prevention**: Clearly separate server/client logic

---

### Invalid Hook Call

**Message**: `Hooks can only be called inside of the body of a function component`

**Cause**: Hook rules violation

**Solutions**:
```typescript
// ❌ Cause 1: Hook inside conditional
if (condition) {
  const [state, setState] = useState();  // Error
}

// ✅ Fix: Call at top level
const [state, setState] = useState();
if (condition) {
  // use state
}

// ❌ Cause 2: Hook in regular function
function helper() {
  const [state, setState] = useState();  // Error
}

// ✅ Fix: Convert to custom hook (use prefix)
function useHelper() {
  const [state, setState] = useState();
  return state;
}
```

**Prevention**: Enable ESLint `react-hooks/rules-of-hooks`

---

### Too Many Re-renders

**Message**: `Too many re-renders. React limits the number of renders`

**Cause**: setState called during render

**Solutions**:
```typescript
// ❌ Cause: State change during render
function Component() {
  const [count, setCount] = useState(0);
  setCount(count + 1);  // Infinite loop
  return <div>{count}</div>;
}

// ✅ Fix 1: Use useEffect
useEffect(() => {
  setCount(c => c + 1);
}, [dependency]);

// ✅ Fix 2: Move to event handler
<button onClick={() => setCount(c => c + 1)}>Increment</button>

// ❌ Cause 2: Inline function changes state
<Child onChange={setData(newData)} />  // Executes immediately

// ✅ Fix: Wrap in arrow function
<Child onChange={() => setData(newData)} />
```

---

## 🟠 Common Errors

### Cannot update unmounted component

**Message**: `Can't perform a React state update on an unmounted component`

**Cause**: setState called after unmount

**Solutions**:
```typescript
// ❌ Cause: No cleanup
useEffect(() => {
  fetchData().then(data => setData(data));
}, []);

// ✅ Fix 1: AbortController
useEffect(() => {
  const controller = new AbortController();

  fetchData({ signal: controller.signal })
    .then(data => setData(data))
    .catch(err => {
      if (err.name !== 'AbortError') throw err;
    });

  return () => controller.abort();
}, []);

// ✅ Fix 2: isMounted flag (less recommended)
useEffect(() => {
  let isMounted = true;
  fetchData().then(data => {
    if (isMounted) setData(data);
  });
  return () => { isMounted = false; };
}, []);
```

---

### Each child should have a unique key

**Cause**: Missing key in list rendering

**Solutions**:
```typescript
// ❌ Error
{items.map(item => <Item {...item} />)}

// ❌ Anti-pattern: index as key
{items.map((item, index) => <Item key={index} {...item} />)}

// ✅ Fix: Use unique ID
{items.map(item => <Item key={item.id} {...item} />)}
```

---

### Cannot read property of undefined

**Cause**: Accessing data before loaded

**Solutions**:
```typescript
// ❌ Error
function Component({ user }) {
  return <div>{user.name}</div>;  // user may be undefined
}

// ✅ Fix 1: Optional chaining
return <div>{user?.name}</div>;

// ✅ Fix 2: Early return
if (!user) return <Loading />;
return <div>{user.name}</div>;

// ✅ Fix 3: Default value
function Component({ user = { name: 'Guest' } }) {
  return <div>{user.name}</div>;
}
```

---

## 🟡 Warnings

### React does not recognize the X prop

**Cause**: Custom prop passed to DOM element

**Solutions**:
```typescript
// ❌ Warning
<div isActive={true}>...</div>  // isActive is not a DOM attribute

// ✅ Fix 1: data- prefix
<div data-active={true}>...</div>

// ✅ Fix 2: Filter with destructuring
const { isActive, ...domProps } = props;
<div {...domProps}>...</div>
```

---

### useEffect has missing dependencies

**Cause**: Missing dependency array items

**Solutions**:
```typescript
// ⚠️ Warning
useEffect(() => {
  fetchUser(userId);
}, []);  // userId missing

// ✅ Fix 1: Add dependency
useEffect(() => {
  fetchUser(userId);
}, [userId]);

// ✅ Fix 2: Intentional omission (comment required)
useEffect(() => {
  fetchUser(userId);
  // eslint-disable-next-line react-hooks/exhaustive-deps
}, []);  // Intentional: initial load only
```

---

## 📊 Error Frequency

| Error | Frequency | Severity |
|-------|-----------|----------|
| Hydration Mismatch | High | High |
| Invalid Hook Call | Medium | High |
| Too Many Re-renders | Medium | High |
| Missing Key | High | Low |
| Missing Dependencies | High | Low |

---

## 🔧 Debugging Tools

```bash
# React DevTools
# Install Chrome extension

# Strict Mode (detects bugs via double rendering)
<StrictMode>
  <App />
</StrictMode>

# Profiler
# React DevTools > Profiler tab
```

---

**META**
- Category: react
- Last Updated: 2026-01-30
