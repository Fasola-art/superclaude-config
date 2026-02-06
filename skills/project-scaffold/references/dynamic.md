# Dynamic Level Template

> Next.js + TypeScript + Supabase

## Structure

```
<project>/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── globals.css
│   │   └── api/
│   │       └── health/route.ts
│   ├── components/
│   │   └── ui/
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts
│   │   │   └── server.ts
│   │   └── utils.ts
│   └── types/
│       └── index.ts
├── public/
├── package.json
├── tsconfig.json
├── next.config.ts
├── tailwind.config.ts
├── .env.example
├── .gitignore
└── README.md
```

## package.json

```json
{
  "name": "{project}",
  "version": "0.1.0",
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "@supabase/supabase-js": "^2.45.0",
    "@supabase/ssr": "^0.5.0"
  },
  "devDependencies": {
    "typescript": "^5.7.0",
    "@types/node": "^22.0.0",
    "@types/react": "^19.0.0",
    "tailwindcss": "^4.0.0",
    "eslint": "^9.0.0",
    "eslint-config-next": "^15.0.0"
  }
}
```

## .env.example

```
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx
SUPABASE_SERVICE_ROLE_KEY=eyJxxx
```

## AI Integration (--ai flag)

```json
{
  "dependencies": {
    "@anthropic-ai/sdk": "^0.39.0"
  }
}
```

```
ANTHROPIC_API_KEY=sk-ant-xxx
```

## Setup Commands

```bash
cd {project} && npm install
cp .env.example .env  # Set Supabase keys
npm run dev
```

## Deploy

```bash
# Vercel
npx vercel --prod
```
