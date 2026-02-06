# Go Rules (38 Rules)

> Go 1.21+ | Idiomatic & Efficient Code

## 파일 구조

| 파일 | 내용 | 규칙 수 |
|------|------|--------|
| [critical.md](critical.md) | ERROR + CONCUR | 12 |
| [high.md](high.md) | STRUCT + IFACE | 10 |
| [medium.md](medium.md) | FUNC + PKG | 10 |
| [low.md](low.md) | PERF + TEST | 6 |
| [QUICK-REFERENCE.md](QUICK-REFERENCE.md) | 빠른 참조 | - |

## 검증

```bash
go fmt ./... && go vet ./... && golangci-lint run && go test -race ./...
```
