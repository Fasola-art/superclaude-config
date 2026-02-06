# 공통 검증 명령어

## 전체 검증

```bash
# 모든 언어 린트
npm run lint && ruff check . && golangci-lint run

# 모든 테스트
npm test && pytest && go test ./...
```

## 언어별 빠른 검증

```bash
# TypeScript/JavaScript
npm run lint && npm test

# Python
ruff check . && ruff format --check . && pytest -v

# Go
go fmt ./... && go vet ./... && go test -race ./...
```

## CI 필수 체크

```bash
# Pre-commit 필수
lint → test → build
```
