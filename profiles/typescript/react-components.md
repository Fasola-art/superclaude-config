# React Component Rules

## Component Patterns

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Server Component** | Data fetching, static | Default (no use client) |
| **Client Component** | Interaction, hooks | `'use client'` |
| **Suspense boundary** | Async loading | `<Suspense fallback={...}>` |

## Component Type Patterns

```typescript
// GOOD: Props interface
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
}

// GOOD: Function component
function Button({ variant, size = 'md', children, onClick }: ButtonProps) {
  return (
    <button className={cn(styles[variant], styles[size])} onClick={onClick}>
      {children}
    </button>
  );
}

// GOOD: forwardRef pattern
const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({ label, ...props }, ref) {
    return <input ref={ref} {...props} />;
  }
);
```

## Anti-patterns

```typescript
// BAD: React.FC (implicit children issue)
const Button: React.FC<Props> = ({ ... }) => { ... };

// BAD: Inline objects/functions (re-renders)
<Child style={{ color: 'red' }} onClick={() => handle()} />

// BAD: Barrel import
import { Button, Input, Card } from '@/components';
```

## Exception Handling

| Situation | Solution |
|-----------|----------|
| Complex children type | `React.ReactNode` |
| Event type | `React.MouseEvent<HTMLButtonElement>` |
| Need ref forwarding | `forwardRef` pattern |
