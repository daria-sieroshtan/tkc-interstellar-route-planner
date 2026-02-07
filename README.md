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

### Run tests

```bash
poetry run pytest              # Run all tests
poetry run pytest -v           # Verbose output
poetry shell                   # Activate venv, then just use: pytest
```
