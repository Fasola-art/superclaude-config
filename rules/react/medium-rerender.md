# React Medium Rules: Prevent Rerenders

## RERENDER: Optimization Techniques

### RERENDER-001: React.memo
```typescript
const ExpensiveComponent = React.memo(function ExpensiveComponent({ data }) {
  return <div>{/* Complex rendering */}</div>;
});
```

### RERENDER-002: useMemo
```typescript
const sortedItems = useMemo(() => {
  return items.sort((a, b) => a.price - b.price);
}, [items]);
```

### RERENDER-003: useCallback
```typescript
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []);

<List items={items} onItemClick={handleClick} />
```

### RERENDER-004: Separate State
```typescript
// BAD: One large state
const [state, setState] = useState({ user: null, posts: [], settings: {} });

// GOOD: Separate
const [user, setUser] = useState(null);
const [posts, setPosts] = useState([]);
const [settings, setSettings] = useState({});
```

### RERENDER-005: Separate Context
```typescript
// BAD: One Context
const AppContext = createContext({ user, theme, settings });

// GOOD: Separate by purpose
const UserContext = createContext(null);
const ThemeContext = createContext(null);
const SettingsContext = createContext(null);
```

### RERENDER-006: Children Pattern
```typescript
function Parent({ children }) {
  const [count, setCount] = useState(0);
  return (
    <div>
      <button onClick={() => setCount(c => c + 1)}>{count}</button>
      {children} {/* No rerender */}
    </div>
  );
}
```

### RERENDER-007: State Colocation
```typescript
// BAD: Parent manages input state → ExpensiveList rerenders
function Parent() {
  const [inputValue, setInputValue] = useState('');
  return (
    <>
      <Input value={inputValue} onChange={setInputValue} />
      <ExpensiveList />
    </>
  );
}

// GOOD: State managed internally
function Parent() {
  return (
    <>
      <InputWithState />
      <ExpensiveList /> {/* No rerender */}
    </>
  );
}
```
