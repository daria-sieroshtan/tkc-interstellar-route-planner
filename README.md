# Interstellar Route Planner API

API service for calculating interstellar journey costs through the HSTC (Hyperspace Tunneling Corp) hyperspace gate network.

## Running the application locally

Pre-requisite: docker compose installed.

```bash
docker compose up --build -d
docker compose exec api alembic upgrade head
```

Check the logs for any troubleshooting

```bash
docker compose logs -f api
```

### Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Database: localhost:5432

## Local development

Pre-requisite: poetry installed

```bash
# Install dependencies (creates and manages venv automatically)
poetry install
```

### Development Commands

Use the Makefile for convenience:

```bash
make install       # Install dependencies
make test          # Run tests
make format        # Format code with Ruff
make lint          # Lint code with Ruff
make type-check    # Type check with mypy
make check-all     # Run all checks (CI pipeline)
make fix           # Auto-fix linting issues
make clean         # Clean cache files
```

Or use Poetry directly:

```bash
poetry run pytest              # Run all tests
poetry run pytest -v           # Verbose output
poetry run ruff format app     # Format code
poetry run ruff check app      # Lint code
poetry run mypy app            # Type check
```
