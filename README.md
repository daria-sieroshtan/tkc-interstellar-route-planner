# Interstellar Route Planner API

API service for calculating interstellar journey costs through the HSTC (Hyperspace Tunneling Corp) hyperspace gate network.

## Running the application locally

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

### Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Database: localhost:5432

### Run tests
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```
