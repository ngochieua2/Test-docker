# Docker Run Commands for Local Development

## Build the images first
docker build -t swarm-demo/backend:latest ./backend
docker build -t swarm-demo/frontend:latest ./frontend

## Create a custom network (optional but recommended)
docker network create app-network

## Run PostgreSQL
docker run -d \
  --name postgres \
  --network app-network \
  -p 5432:5432 \
  -e POSTGRES_DB=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine

## Run SQL Server
docker run -d \
  --name sqlserver \
  --network app-network \
  -p 1433:1433 \
  -e SA_PASSWORD="YourStrong@Passw0rd" \
  -e ACCEPT_EULA="Y" \
  -e MSSQL_PID="Express" \
  -v sqlserver_data:/var/opt/mssql \
  mcr.microsoft.com/mssql/server:2022-latest

## Run Backend (FastAPI) - THIS WAS MISSING PORT MAPPING
docker run -d \
  --name backend \
  --network app-network \
  -p 8000:8000 \
  -e POSTGRES_URL="postgresql://postgres:postgres@postgres:5432/postgres" \
  -e SQLSERVER_URL="mssql+pyodbc://sa:YourStrong@Passw0rd@sqlserver:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes" \
  swarm-demo/backend:latest

## Run Frontend (Next.js)
docker run -d \
  --name frontend \
  --network app-network \
  -p 3000:3000 \
  -p 8080:3000 \
  -e NEXT_PUBLIC_API_URL="http://localhost:8000" \
  swarm-demo/frontend:latest

## Access your applications:
# Frontend: http://localhost:3000 or http://localhost:8080
# Backend API: http://localhost:8000
# Backend Health: http://localhost:8000/health
# PostgreSQL: localhost:5432
# SQL Server: localhost:1433