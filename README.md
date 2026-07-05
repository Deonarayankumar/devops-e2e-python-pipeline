# DevOps E2E Python Pipeline

End-to-end CI/CD lab for a FastAPI order API and background worker. Demonstrates multi-stage pipelines across Jenkins and Azure DevOps with quality gates and artifact promotion.

## Architecture

```
┌─────────┐     ┌─────────┐     ┌──────────┐
│  API    │────▶│  Redis  │◀────│  Worker  │
│ FastAPI │     │  queue  │     │  Python  │
└─────────┘     └─────────┘     └──────────┘
```

See [docs/architecture.md](docs/architecture.md) for pipeline flow and integration points.

## Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Jenkins (optional) with shared library configured
- Azure DevOps project (optional)
- SonarQube, Trivy, JFrog CLI (for pipeline scripts)

## Quick start

```bash
docker compose up --build
curl http://localhost:8000/health
curl -X POST http://localhost:8000/orders -H "Content-Type: application/json" \
  -d '{"sku":"WIDGET-01","quantity":2}'
```

## Run tests

```bash
cd services/api
pip install -e ".[dev]"
pytest -v
```

## Pipeline scripts

| Script | Purpose |
|--------|---------|
| `scripts/trivy-scan.sh` | Container vulnerability scan |
| `scripts/smoke-test.sh` | Post-deploy HTTP smoke tests |
| `scripts/jfrog-promote.sh` | Promote image between JFrog repos |

## Learnings

- Shared Jenkins library for artifact promotion
- Parallel quality gates: unit tests, SonarQube, Trivy
- Azure DevOps YAML mirroring Jenkins stages for portability
