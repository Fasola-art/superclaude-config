# Enterprise Level Template

> Docker + Microservices + Terraform

## Structure

```
<project>/
├── services/
│   ├── api/
│   │   ├── src/
│   │   │   ├── app.ts
│   │   │   ├── routes/
│   │   │   ├── middleware/
│   │   │   │   └── auth.ts
│   │   │   └── types/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── worker/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   └── package.json
│   └── web/
│       ├── src/
│       ├── Dockerfile
│       └── package.json
├── infra/
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── k8s/
│   │   ├── api-deployment.yaml
│   │   ├── worker-deployment.yaml
│   │   └── ingress.yaml
│   └── docker/
│       └── docker-compose.yml
├── packages/
│   └── shared/
│       ├── src/
│       │   └── types.ts
│       └── package.json
├── scripts/
│   ├── setup.sh
│   └── deploy.sh
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── .env.example
├── turbo.json
├── package.json
└── README.md
```

## docker-compose.yml

```yaml
services:
  api:
    build: ./services/api
    ports: ["3000:3000"]
    env_file: .env
    depends_on: [postgres, redis]
  worker:
    build: ./services/worker
    env_file: .env
    depends_on: [postgres, redis]
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes: ["pgdata:/var/lib/postgresql/data"]
    ports: ["5432:5432"]
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
volumes:
  pgdata:
```

## .env.example

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app
DB_USER=postgres
DB_PASSWORD=postgres
REDIS_URL=redis://localhost:6379
JWT_SECRET=change-me
OAUTH_CLIENT_ID=xxx
OAUTH_CLIENT_SECRET=xxx
```

## Setup Commands

```bash
cd {project}
npm install          # Monorepo dependencies
docker compose up -d # Start infrastructure
npm run db:migrate   # Run migrations
npm run dev          # Start all services
```

## Deploy

```bash
cd infra/terraform && terraform init && terraform plan
# Review → terraform apply
```
