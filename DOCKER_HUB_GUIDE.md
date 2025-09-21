# Docker Hub Deployment Guide

This guide explains how to build, push, and deploy three different Docker images to Docker Hub for your docker-swarm-stack project.

## Overview

We provide three different deployment options:

1. **Individual Images**: Separate FastAPI backend and Next.js frontend images
2. **Full Stack Image**: Single container with backend, frontend, and nginx proxy
3. **Microservices**: Using individual images with external databases

## Prerequisites

- Docker Desktop installed and running
- Docker Hub account
- Git repository with your project

## Quick Start

### 1. Build and Push All Images

Replace `your-dockerhub-username` with your actual Docker Hub username:

**Windows (PowerShell):**
```powershell
cd docker-swarm-stack
.\scripts\build-and-push.bat your-dockerhub-username
```

**Linux/Mac:**
```bash
cd docker-swarm-stack
chmod +x scripts/build-and-push.sh
./scripts/build-and-push.sh your-dockerhub-username
```

### 2. Deploy Using Docker Compose

Choose one of the deployment options below:

## Deployment Options

### Option 1: Microservices Architecture (Recommended for Production)

Uses separate containers for each service with external databases.

```bash
# Update docker-compose.hub.yml with your Docker Hub username
# Then deploy:
docker stack deploy -c docker-compose.hub.yml mystack
```

**Services:**
- PostgreSQL: `localhost:5432`
- SQL Server: `localhost:1433`
- FastAPI Backend: `localhost:8000`
- Next.js Frontend: `localhost:3000`, `localhost:8080`

### Option 2: Full Stack Single Container (Recommended for Development)

Everything in one container with nginx proxy.

```bash
# Update docker-compose.fullstack.yml with your Docker Hub username
# Then deploy:
docker stack deploy -c docker-compose.fullstack.yml mystack
```

**Access Points:**
- Main Application: `http://localhost` (port 80)
- Frontend Direct: `http://localhost:3000`
- Backend API Direct: `http://localhost:8000`

### Option 3: Manual Docker Run Commands

**Backend Only:**
```bash
docker run -d \
  --name backend \
  -p 8000:8000 \
  -e POSTGRES_URL="your-postgres-url" \
  -e SQLSERVER_URL="your-sqlserver-url" \
  your-dockerhub-username/docker-swarm-stack-backend:latest
```

**Frontend Only:**
```bash
docker run -d \
  --name frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL="http://localhost:8000" \
  your-dockerhub-username/docker-swarm-stack-frontend:latest
```

**Full Stack:**
```bash
docker run -d \
  --name fullstack \
  -p 80:80 \
  -p 3000:3000 \
  -p 8000:8000 \
  your-dockerhub-username/docker-swarm-stack-fullstack:latest
```

## Image Details

### Backend Image (FastAPI)
- **Size**: ~500MB
- **Base**: python:3.11-slim
- **Includes**: FastAPI app, ODBC drivers for SQL Server
- **Port**: 8000
- **Health Check**: `/health` endpoint

### Frontend Image (Next.js)
- **Size**: ~200MB
- **Base**: node:18-alpine
- **Includes**: Next.js app, optimized production build
- **Port**: 3000
- **Health Check**: `/health` endpoint

### Full Stack Image
- **Size**: ~800MB
- **Base**: python:3.11-slim with Node.js
- **Includes**: FastAPI + Next.js + nginx proxy + PM2 process manager
- **Ports**: 80 (nginx), 3000 (frontend), 8000 (backend)
- **Health Check**: Both frontend and backend endpoints

## Environment Variables

### Backend
```bash
POSTGRES_URL=postgresql://user:pass@host:port/db
SQLSERVER_URL=mssql+pyodbc://user:pass@host:port/db?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
```

### Frontend
```bash
NEXT_PUBLIC_API_URL=http://backend-host:8000
```

### Full Stack
```bash
POSTGRES_URL=postgresql://user:pass@host:port/db
SQLSERVER_URL=mssql+pyodbc://user:pass@host:port/db?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes
```

## Health Checks

All images include health checks:

- **Backend**: `curl -f http://localhost:8000/health`
- **Frontend**: `wget --spider http://localhost:3000/health`
- **Full Stack**: Both frontend and backend health checks

## Troubleshooting

### Build Issues

1. **Docker login fails:**
   ```bash
   docker login
   # Enter your Docker Hub credentials
   ```

2. **Build context too large:**
   - Add `.dockerignore` files
   - Exclude `node_modules`, `.git`, etc.

3. **Multi-platform builds:**
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 -t your-image .
   ```

### Runtime Issues

1. **Cannot connect to database:**
   - Check database connection strings
   - Ensure databases are running and accessible
   - Verify network connectivity

2. **Health checks failing:**
   - Check application logs: `docker logs container-name`
   - Verify ports are correctly exposed
   - Test endpoints manually

### Logs and Debugging

```bash
# View container logs
docker logs container-name

# Interactive shell
docker exec -it container-name /bin/bash

# Check running processes (full stack image)
docker exec -it container-name pm2 list
```

## Production Considerations

### Security
- Use secrets for database passwords
- Enable HTTPS with SSL certificates
- Implement proper authentication and authorization

### Scaling
- Use Docker Swarm or Kubernetes for orchestration
- Configure load balancers
- Implement database clustering

### Monitoring
- Add logging and monitoring solutions
- Configure alerts for health check failures
- Monitor resource usage

## Docker Hub Images

After running the build script, your images will be available at:

- `your-dockerhub-username/docker-swarm-stack-backend:latest`
- `your-dockerhub-username/docker-swarm-stack-frontend:latest`
- `your-dockerhub-username/docker-swarm-stack-fullstack:latest`

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Docker logs for error messages
3. Ensure all prerequisites are met
4. Verify Docker Hub credentials and repository access