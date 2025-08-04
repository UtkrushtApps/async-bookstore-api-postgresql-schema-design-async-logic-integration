#!/bin/bash
set -e
cd /root/task/
echo "Starting containers..."
docker-compose up -d
# Wait for Postgres
until docker exec bookstore_postgres pg_isready -U bookstore_user -d bookstore_db > /dev/null 2>&1; do
  sleep 2
done
echo "Postgres is ready. Applying schema..."
docker exec -i bookstore_postgres psql -U bookstore_user -d bookstore_db < /root/task/schema.sql
echo "Loading sample data..."
docker exec -i bookstore_postgres psql -U bookstore_user -d bookstore_db < /root/task/data/sample_data.sql
echo "Validating FastAPI connectivity..."
sleep 4
curl -f http://localhost:8000/docs || { echo "FastAPI API is not healthy!"; exit 1; }
echo "Setup complete."