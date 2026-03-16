# Realtime Analysis Architecture

> System design and configuration

---

## Skill Commands

| Command | Description |
|---------|-------------|
| /stream-start [source] | Start stream |
| /stream-stop [source] | Stop stream |
| /stream-status | Check stream status |
| /dashboard [name] | Open dashboard |
| /realtime-alert [condition] | Set real-time alert |

---

## Configuration (config.json)

```json
{
  "server": {
    "port": 8080,
    "maxConnections": 100
  },
  "processing": {
    "workers": 24,
    "bufferSize": 10000,
    "batchInterval": 100
  },
  "storage": {
    "enabled": true,
    "type": "timescaledb",
    "retentionDays": 30
  },
  "alerts": {
    "enabled": true,
    "channels": ["desktop", "sound"]
  }
}
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Binance  │  │  Yahoo   │  │ Twitter  │  │ Custom   │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
└───────┼─────────────┼─────────────┼─────────────┼───────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Stream Manager                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Message Queue (Buffer)                 │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Parallel Processing (24 Workers)                │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ... ┌────┐     │
│  │ W1 │ │ W2 │ │ W3 │ │ W4 │ │ W5 │ │ W6 │     │W24 │     │
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘     └────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Storage    │    │  WebSocket   │    │   Alerts     │
│  TimescaleDB │    │   Server     │    │   System     │
└──────────────┘    └──────────────┘    └──────────────┘
                              │
                              ▼
                    ┌──────────────┐
                    │  Dashboard   │
                    │   Clients    │
                    └──────────────┘
```

---

**Related**: [index.md](index.md) | [features.md](features.md) | [usage.md](usage.md)
