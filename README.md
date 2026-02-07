# Interstellar Route Planner API

API service for calculating interstellar journey costs through the HSTC (Hyperspace Tunneling Corp) hyperspace gate network.

## Quick Start

Pre-requisite: docker compose installed.

```bash
docker compose up --build -d
docker compose exec api alembic upgrade head
docker compose logs -f api
```

Check the logs for any troubleshooting

```bash
docker compose logs -f api
```

Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Database: localhost:5432

