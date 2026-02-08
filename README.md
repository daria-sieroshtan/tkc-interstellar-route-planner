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
    - Calculation per 1 passenger (as suggested by the endpoint spec)
    - Accept lowercase gate ids
  - The brief is inconsistent about the distance CAS -> PRO (table says 120, mermaid diagram says 80). I chose table version.
  - Dijkstra's shortest path algorithm is used
  - Why store normalised nodes and edges instead of adjacency list in the DB? Even though right now it is just static data with the small amount of data points, Hyperspace Tunneling Corp might want ot develop this system in many different ways, so this approach makes it more extensible
    - In production the adjacency list should be cached to avoid runtime computation

### Not implemented due to the time boxing
- E2E tests
- Some more validation and error handling
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
