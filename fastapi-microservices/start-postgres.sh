#!/usr/bin/env bash
# Quick PostgreSQL setup for development

echo "🐘 Starting PostgreSQL for Todo Service..."

# Stop and remove existing container if it exists
docker stop todo-postgres 2>/dev/null || true
docker rm todo-postgres 2>/dev/null || true

# Start PostgreSQL container
docker run -d \
  --name todo-postgres \
  -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=todoapp \
  -v todo_postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine

echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Check if container is running
if docker ps | grep -q todo-postgres; then
    echo "✅ PostgreSQL is running!"
    echo "📋 Connection details:"
    echo "   Host: localhost"
    echo "   Port: 5432"
    echo "   Database: todoapp"
    echo "   Username: postgres"
    echo "   Password: password"
    echo ""
    echo "🔗 Connection string: postgresql://postgres:password@localhost:5432/todoapp"
    echo ""
    echo "🛑 To stop: docker stop todo-postgres"
    echo "🗑️  To remove: docker rm todo-postgres"
else
    echo "❌ Failed to start PostgreSQL container"
    exit 1
fi