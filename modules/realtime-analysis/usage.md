# Realtime Analysis Usage

> Usage examples and performance optimization

---

## Usage Examples

```bash
# Start BTC real-time stream
/stream-start binance:btcusdt

# Open dashboard
/dashboard market_overview

# Set price alert
/realtime-alert "BTCUSDT > 50000"

# Check stream status
/stream-status
```

---

## Performance Optimization

```yaml
optimization:
  m2_ultra:
    cpu_affinity: true
    numa_aware: true
    memory_mapping: true

  buffering:
    ring_buffer: true
    zero_copy: true

  networking:
    tcp_nodelay: true
    keep_alive: true

  storage:
    batch_insert: true
    compression: "lz4"
```

---

## Roadmap

- [ ] GPU-accelerated analysis (Metal)
- [ ] Distributed processing support
- [ ] Real-time ML prediction
- [ ] Advanced anomaly detection
- [ ] Multi-exchange aggregation

---

**Related**: [index.md](index.md) | [features.md](features.md) | [architecture.md](architecture.md)
