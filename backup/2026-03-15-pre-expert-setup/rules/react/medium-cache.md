# React Medium Rules: Cache + Image

## CACHE: Caching Strategies

### CACHE-001: fetch Cache Options
```typescript
fetch(url, { cache: 'force-cache' });        // Default
fetch(url, { cache: 'no-store' });           // No cache
fetch(url, { next: { revalidate: 3600 } });  // Time-based
fetch(url, { next: { tags: ['posts'] } });   // Tag-based
```

### CACHE-002: unstable_cache
```typescript
import { unstable_cache } from 'next/cache';

const getCachedUser = unstable_cache(
  async (id: string) => await db.user.findUnique({ where: { id } }),
  ['user'],
  { revalidate: 3600, tags: ['user'] }
);
```

### CACHE-003: Tag-Based Revalidation
```typescript
const posts = await fetch('/api/posts', { next: { tags: ['posts'] } });

// Trigger
import { revalidateTag } from 'next/cache';
revalidateTag('posts');
```

### CACHE-004: Path Revalidation
```typescript
import { revalidatePath } from 'next/cache';
revalidatePath('/posts');
revalidatePath('/posts', 'layout');
```

### CACHE-005: React cache()
```typescript
import { cache } from 'react';
const getUser = cache(async (id: string) => {
  return await db.user.findUnique({ where: { id } });
});
// Multiple calls → single execution
```

---

## IMAGE: Image Optimization

### IMAGE-001: next/image
```typescript
import Image from 'next/image';
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />
```

### IMAGE-002: Responsive Images
```typescript
<Image
  src="/photo.jpg" alt="Photo" fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="object-cover"
/>
```

### IMAGE-003: Lazy Loading
```typescript
// Default: lazy
<Image src="/below.jpg" alt="..." width={800} height={600} />

// LCP: priority
<Image src="/hero.jpg" alt="..." width={1200} height={600} priority />
```

### IMAGE-004: Format Config
```typescript
// next.config.js
images: {
  formats: ['image/avif', 'image/webp'],
  deviceSizes: [640, 750, 828, 1080, 1200, 1920],
}
```

### IMAGE-005: Placeholder
```typescript
<Image
  src="/photo.jpg" alt="Photo" width={800} height={600}
  placeholder="blur" blurDataURL="data:image/jpeg;base64,..."
/>
```
