#!/bin/bash
set -e

echo "Waiting for database..."
retries=10
until alembic upgrade head; do
  retries=$((retries - 1))
  if [ "$retries" -le 0 ]; then
    echo "Failed to run migrations after multiple attempts"
    exit 1
  fi
  echo "Migration failed, retrying in 2s... ($retries attempts left)"
  sleep 2
done

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
