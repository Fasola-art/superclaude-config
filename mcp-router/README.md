# MCP Router

SuperClaude v2.0.9 MCP Router System

## Overview

A system that manages MCP (Model Context Protocol) servers and routes requests.
Supports parallel processing utilizing Mac Studio Ultra M2's 24 CPU cores.

## Components

```
mcp-router/
├── server.py     # Main router server
├── client.py     # Client utility
└── README.md     # This document
```

## Configuration

Configure MCP servers in `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem"],
      "priority": 10,
      "timeout": 30000
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## Usage

### Starting the Server

```bash
python ~/.claude/mcp-router/server.py
```

### Using the Client

```bash
# Check status
python ~/.claude/mcp-router/client.py status

# Call function
python ~/.claude/mcp-router/client.py call filesystem '{"action": "list"}'
```

## Load Balancing Strategies

- **weighted_round_robin**: Priority-based round robin (default)
- **least_latency**: Select server with lowest latency

## Status Codes

| Status | Description |
|--------|-------------|
| HEALTHY | Operating normally |
| DEGRADED | Partial functionality |
| UNHEALTHY | Abnormal state |
| OFFLINE | Offline |
| UNKNOWN | Status unknown |

## Mac Studio Optimization

- Max concurrent servers: 24 (CPU core count)
- Async I/O utilization
- Memory-efficient state management
