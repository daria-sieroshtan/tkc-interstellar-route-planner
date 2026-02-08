#!/bin/bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

# Install Docker, Docker Compose, and Git
apt-get update
apt-get install -y docker.io docker-compose-v2 git

systemctl enable docker
systemctl start docker

# Read metadata
APP_REPO_URL=$(curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/attributes/app-repo-url)
DB_PASSWORD=$(curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/attributes/db-password)
ENVIRONMENT=$(curl -s -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/attributes/environment)

# Clone repo
git clone "$APP_REPO_URL" /opt/app

# Write .env
cat > /opt/app/.env <<EOF
POSTGRES_USER=hstc
POSTGRES_PASSWORD=${DB_PASSWORD}
POSTGRES_DB=hstc_routes
DATABASE_URL=postgresql://hstc:${DB_PASSWORD}@db:5432/hstc_routes
ENVIRONMENT=${ENVIRONMENT}
EOF

# Build and start services
cd /opt/app
docker compose -f ops/docker-compose.yml build
docker compose -f ops/docker-compose.yml up -d

