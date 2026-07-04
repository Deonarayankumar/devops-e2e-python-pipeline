.PHONY: up down test lint

up:
	docker compose up --build -d

down:
	docker compose down -v

test:
	cd services/api && pip install -e ".[dev]" && pytest -v

lint:
	cd services/api && ruff check src tests
