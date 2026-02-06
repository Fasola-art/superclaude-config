# Import/Export Rules

## Import Order

```typescript
// 1. React/Next.js
import { useState } from 'react';
import Link from 'next/link';

// 2. External libraries
import { clsx } from 'clsx';
import { format } from 'date-fns';

// 3. Internal modules (absolute)
import { Button } from '@/components/Button';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/lib/utils';

// 4. Relative path (same folder)
import { helpers } from './helpers';

// 5. Types (type-only)
import type { User } from '@/types';

// 6. Styles
import styles from './styles.module.css';
```

## Export Patterns

```typescript
// GOOD: Named export (tree-shakable)
export function Button() { ... }
export function Input() { ... }

// GOOD: Separate type export
export type { ButtonProps, InputProps };

// GOOD: Constant export
export const BUTTON_VARIANTS = ['primary', 'secondary'] as const;
```

## Anti-patterns

```typescript
// BAD: Barrel import (bundle size)
import { Button, Input, Card, Modal } from '@/components';

// BAD: Import entire library
import _ from 'lodash';
import * as R from 'ramda';

// BAD: default export (refactoring difficult)
export default function Button() { ... }
```
