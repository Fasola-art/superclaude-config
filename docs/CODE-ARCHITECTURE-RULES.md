# Code Architecture Rules (Required)

> Mandatory rules for code architecture design

---

## UI/Hook Separation

| Principle        | Description              |
|------------------|--------------------------|
| Component role   | Handle UI rendering only |
| State management | Extract to Custom Hook   |
| API calls        | Extract to Custom Hook   |
| Hook filename    | `use-[feature-name].ts`  |

### Example

```typescript
// BAD: Logic mixed in component
function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/user').then(res => res.json()).then(setUser);
  }, []);

  return <div>{user?.name}</div>;
}

// GOOD: Extracted to Hook
function UserProfile() {
  const { user, loading } = useUser();
  return <div>{user?.name}</div>;
}

// hooks/use-user.ts
function useUser() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/user').then(res => res.json()).then(setUser);
  }, []);

  return { user, loading };
}
```

---

## Common Function Extraction

| Principle           | Description                                   |
|---------------------|-----------------------------------------------|
| Repeated patterns   | 2+ repetitions → Extract to shared component  |
| Props consolidation | Similar Props → Unify with BaseProps type     |
| Related components  | Apply Compound Component pattern              |

### Compound Component Example

```typescript
// GOOD: Compound Component pattern
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
  <Card.Footer>Footer</Card.Footer>
</Card>
```

---

## SSOT (Single Source of Truth)

| Principle        | Description                                              |
|------------------|----------------------------------------------------------|
| Data source      | All data/state must have single source                   |
| Derived values   | Compute instead of storing in state                      |
| Validation logic | Consolidate duplicate validation into single function    |
| Constants/config | Manage duplicates in single file                         |

### Example

```typescript
// BAD: Derived value stored in state
const [items, setItems] = useState([]);
const [total, setTotal] = useState(0); // Derived value

// GOOD: Compute derived value
const [items, setItems] = useState([]);
const total = useMemo(() => items.reduce((sum, i) => sum + i.price, 0), [items]);
```

---

## Database Normalization Rules (Required)

### Apply 3 Normal Forms

| Normal Form | Rule                       | Checklist                                                     |
|-------------|----------------------------|---------------------------------------------------------------|
| 1NF         | Atomic values              | Use separate table instead of arrays/nested objects in columns |
| 2NF         | Full functional dependency | All columns depend on entire composite key                    |
| 3NF         | Remove transitive dependency | No dependencies between non-key columns                       |

### Example

```sql
-- BAD: 1NF violation (storing arrays)
CREATE TABLE orders (
  id INT,
  items TEXT  -- Stored as 'item1,item2,item3'
);

-- GOOD: Separate table
CREATE TABLE orders (
  id INT PRIMARY KEY
);

CREATE TABLE order_items (
  id INT PRIMARY KEY,
  order_id INT REFERENCES orders(id),
  item_name TEXT
);
```

---

## Checklist

### When Writing Components
- [ ] Is state management logic extracted to Hook?
- [ ] Are API calls extracted to Hook?
- [ ] Are patterns repeated 2+ times extracted to shared components?

### When Designing Data
- [ ] Does all state have single source?
- [ ] Are derivable values not stored in state?
- [ ] Does database comply with 3NF?
