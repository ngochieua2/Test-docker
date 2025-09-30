#!/bin/sh
# Wait for DB (optional: install 'wait-for-it' or similar if needed)
echo "Running migrations..."
alembic upgrade head

echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 5002 --reload