# Interstellar Route Planner API

Technical Challenge for [The Keyholding Company](https://github.com/TheKeyholdingCompany/tech-challenge-backend-dev)

API service for calculating interstellar journey costs through the HSTC (Hyperspace Tunneling Corp) hyperspace gate network.

## Implementation notes
- Transport to the nearest gate cost calculation assumptions
  - All passengers will use one way of transport (i.e. either all will go with the personal transport, or with HSTC, no group splitting)
  - If costs are equal, personal transport is preferred
  - We don't need to return the number of vehicles needed for the journey or any other additinal information
- Hyperspace journey cost calculation
  - Assumptions
    - Calculation per 1 passenger
    - Accept lowercase gate ids
  - Dijkstra's shortest path algorithm is used
  - In production some caching or DB query optimisations could be made, but they were not implemented in the scope of this demo

### Not implemented due to the time boxing
- E2E tests
- Logging, observability

## Running the application locally

Pre-requisite: docker compose installed.

```bash
docker compose -f ops/docker-compose.yml up --build -d
```

Check the logs for any troubleshooting

```bash
docker compose -f ops/docker-compose.yml logs -f api
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
