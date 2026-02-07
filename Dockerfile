FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.3.2

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
