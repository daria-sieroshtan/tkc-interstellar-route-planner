.PHONY: install format lint type-check test check-all fix clean

install:
	poetry install

format:
	poetry run ruff format app tests

lint:
	poetry run ruff check app tests

type-check:
	poetry run mypy app

test:
	poetry run pytest

check-all: format lint type-check test
	@echo "✅ All checks passed!"

fix:
	poetry run ruff check --fix app tests
	poetry run ruff format app tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned up cache and build artifacts"
