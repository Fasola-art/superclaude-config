# React Low Priority Rules: JS-OPT (1-6)

## JS-OPT: JavaScript Optimization

### JS-OPT-001: Immutability
```typescript
// BAD: Direct mutation
state.items.push(newItem);

// GOOD: Create new array
setState(prev => ({ ...prev, items: [...prev.items, newItem] }));
```

### JS-OPT-002: Conditional Rendering
```typescript
// Early return
if (!data) return <Loading />;
if (error) return <Error />;
return <Content data={data} />;
```

### JS-OPT-003: Event Handlers
```typescript
// BAD: Inline function (new each render)
<button onClick={() => handleClick(id)}>Click</button>

// GOOD: Use data attributes
<button data-id={id} onClick={handleClick}>Click</button>

function handleClick(e) {
  const id = e.currentTarget.dataset.id;
}
```

### JS-OPT-004: Debounce/Throttle
```typescript
const debouncedSearch = useMemo(
  () => debounce((query) => search(query), 300),
  []
);

useEffect(() => {
  debouncedSearch(query);
  return () => debouncedSearch.cancel();
}, [query, debouncedSearch]);
```

### JS-OPT-005: Virtualization
```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }) {
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize() }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div key={virtualRow.key}>{items[virtualRow.index]}</div>
        ))}
      </div>
    </div>
  );
}
```

### JS-OPT-006: Web Workers
```typescript
// heavy-task.worker.ts
self.onmessage = (e) => {
  const result = heavyComputation(e.data);
  self.postMessage(result);
};

// component.tsx
const worker = new Worker(new URL('./heavy-task.worker.ts', import.meta.url));
worker.postMessage(data);
worker.onmessage = (e) => setResult(e.data);
```
