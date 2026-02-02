# Claude Agent SDK (TypeScript)

> TypeScript Claude Agent SDK Reference Documentation

## Overview

The Claude Agent SDK is the official SDK for building AI agents.

## Installation

```bash
npm install @anthropic-ai/sdk
```

## Basic Usage

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const message = await client.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude!' }
  ]
});
```

## Reference Links

- [Official Documentation](https://docs.anthropic.com/claude/reference)
- [GitHub](https://github.com/anthropics/anthropic-sdk-typescript)
