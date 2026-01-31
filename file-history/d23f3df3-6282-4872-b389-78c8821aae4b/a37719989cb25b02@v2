---
name: project-scaffold
description: TypeScript CLI 프로젝트 빠른 생성 (AI 통합 포함)
version: "1.0.0"
triggers:
  - /scaffold
  - /new-project
  - 프로젝트 생성
author: reim
tags:
  - typescript
  - cli
  - project
  - scaffold
---

# Project Scaffold 스킬

> TypeScript + CLI 프로젝트를 빠르게 생성하는 스킬

---

## 사용법

```bash
/scaffold <project-name> [options]
```

### 옵션
- `--cli`: CLI 도구 템플릿 (기본)
- `--api`: API 서버 템플릿
- `--ai`: AI 통합 (Claude API) 포함

### 예시
```bash
/scaffold my-tool --cli --ai
/scaffold api-server --api
```

---

## 실행 지침

<command-name>project-scaffold</command-name>

### 1. 사용자 입력 수집

프로젝트 이름이 없으면 AskUserQuestion으로 물어보세요:
- 프로젝트 이름
- 프로젝트 유형 (CLI / API / Library)
- AI 통합 필요 여부 (Claude / OpenAI / 없음)
- 출력 위치 (현재 디렉토리 / 지정 경로)

### 2. 프로젝트 구조 생성

```
<project-name>/
├── src/
│   ├── cli/
│   │   └── index.ts          # CLI 진입점
│   ├── core/
│   │   └── main.ts           # 핵심 로직
│   ├── integrations/
│   │   └── claude.ts         # AI 연동 (선택)
│   ├── types/
│   │   └── index.ts          # 타입 정의
│   └── utils/
│       └── helpers.ts        # 유틸리티
├── examples/
│   └── sample.txt            # 샘플 입력
├── output/                   # 출력 디렉토리
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
└── README.md
```

### 3. 필수 파일 내용

#### package.json 템플릿
```json
{
  "name": "<project-name>",
  "version": "0.1.0",
  "type": "module",
  "bin": {
    "<cli-name>": "./dist/cli/index.ts"
  },
  "scripts": {
    "dev": "tsx src/cli/index.ts",
    "build": "tsc",
    "start": "node dist/cli/index.js"
  },
  "dependencies": {
    "@anthropic-ai/sdk": "^0.39.0",
    "commander": "^12.1.0",
    "chalk": "^5.3.0",
    "ora": "^8.0.1",
    "dotenv": "^16.4.5"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "typescript": "^5.7.0",
    "tsx": "^4.19.0"
  }
}
```

#### tsconfig.json 템플릿
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

#### CLI 진입점 템플릿 (src/cli/index.ts)
```typescript
#!/usr/bin/env node
import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import { config } from 'dotenv';
config();

const program = new Command();

program
  .name('<cli-name>')
  .description('<description>')
  .version('0.1.0');

program
  .command('run <input>')
  .description('메인 명령어')
  .option('-v, --verbose', '상세 출력')
  .action(async (input, options) => {
    const spinner = ora('처리 중...').start();
    try {
      // 핵심 로직 호출
      spinner.succeed(chalk.green('완료!'));
    } catch (error) {
      spinner.fail(chalk.red('오류 발생'));
    }
  });

program.parse();
```

### 4. 패키지 설치

```bash
cd <project-name> && npm install
```

### 5. 완료 메시지

```markdown
✅ 프로젝트 생성 완료!

📁 위치: <path>
📦 패키지: 설치 완료

시작하기:
  cd <project-name>
  cp .env.example .env
  # ANTHROPIC_API_KEY 설정
  npm run dev run examples/sample.txt
```

---

## 참고

### AI 통합 시 필요한 환경 변수
```
ANTHROPIC_API_KEY=sk-ant-xxx
```

### 확장 가능한 템플릿
- `--notion`: Notion API 통합
- `--clova`: CLOVA Speech STT 통합
- `--supabase`: Supabase 연동

---

**META**
- Created: 2026-01-31
- Last Updated: 2026-01-31
