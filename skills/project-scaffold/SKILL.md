---
name: project-scaffold
description: Quick TypeScript CLI project generation with AI integration support.
version: "1.0.0"
triggers:
  - /scaffold
  - /new-project
  - create project
author: reim
tags:
  - typescript
  - cli
  - project
  - scaffold
---

# Project Scaffold Skill

> Quickly generate TypeScript + CLI projects

---

## Usage

```bash
/scaffold <project-name> [options]
```

### Options
- `--cli`: CLI tool template (default)
- `--api`: API server template
- `--ai`: Include AI integration (Claude API)

### Examples
```bash
/scaffold my-tool --cli --ai
/scaffold api-server --api
```

---

## Execution Instructions

<command-name>project-scaffold</command-name>

### 1. Collect User Input

If project name is not provided, ask using AskUserQuestion:
- Project name
- Project type (CLI / API / Library)
- AI integration needed (Claude / OpenAI / None)
- Output location (current directory / specified path)

### 2. Generate Project Structure

```
<project-name>/
├── src/
│   ├── cli/
│   │   └── index.ts          # CLI entry point
│   ├── core/
│   │   └── main.ts           # Core logic
│   ├── integrations/
│   │   └── claude.ts         # AI integration (optional)
│   ├── types/
│   │   └── index.ts          # Type definitions
│   └── utils/
│       └── helpers.ts        # Utilities
├── examples/
│   └── sample.txt            # Sample input
├── output/                   # Output directory
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
└── README.md
```

### 3. Required File Contents

#### package.json Template
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

#### tsconfig.json Template
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

#### CLI Entry Point Template (src/cli/index.ts)
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
  .description('Main command')
  .option('-v, --verbose', 'Verbose output')
  .action(async (input, options) => {
    const spinner = ora('Processing...').start();
    try {
      // Call core logic
      spinner.succeed(chalk.green('Complete!'));
    } catch (error) {
      spinner.fail(chalk.red('Error occurred'));
    }
  });

program.parse();
```

### 4. Install Packages

```bash
cd <project-name> && npm install
```

### 5. Completion Message

```markdown
Project created successfully!

Location: <path>
Packages: Installed

Getting started:
  cd <project-name>
  cp .env.example .env
  # Set ANTHROPIC_API_KEY
  npm run dev run examples/sample.txt
```

---

## Reference

### Environment Variables for AI Integration
```
ANTHROPIC_API_KEY=sk-ant-xxx
```

### Extensible Templates
- `--notion`: Notion API integration
- `--clova`: CLOVA Speech STT integration
- `--supabase`: Supabase integration

---

**META**
- Created: 2026-01-31
- Last Updated: 2026-01-31
