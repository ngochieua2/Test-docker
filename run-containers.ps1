# PowerShell script to build and run containers with proper port mapping
# Save as run-containers.ps1

Write-Host "Building Docker images..." -ForegroundColor Green

# Build images
docker build -t swarm-demo/backend:latest ./backend
docker build -t swarm-demo/frontend:latest ./frontend

Write-Host "Creating network..." -ForegroundColor Green
# Create network
docker network create app-network 2>$null

Write-Host "Starting containers..." -ForegroundColor Green

# Stop and remove existing containers
docker stop postgres sqlserver backend frontend 2>$null
docker rm postgres sqlserver backend frontend 2>$null

# Run PostgreSQL
docker run -d `
  --name postgres `
  --network app-network `
  -p 5432:5432 `
  -e POSTGRES_DB=postgres `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=postgres `
  postgres:15-alpine

# Run SQL Server
docker run -d `
  --name sqlserver `
  --network app-network `
  -p 1433:1433 `
  -e "SA_PASSWORD=YourStrong@Passw0rd" `
  -e "ACCEPT_EULA=Y" `
  -e "MSSQL_PID=Express" `
  mcr.microsoft.com/mssql/server:2022-latest

# Wait a bit for databases to start
Start-Sleep -Seconds 10

# Run Backend with proper port mapping
docker run -d `
  --name backend `
  --network app-network `
  -p 8000:8000 `
  -e "POSTGRES_URL=postgresql://postgres:postgres@postgres:5432/postgres" `
  -e "SQLSERVER_URL=mssql+pyodbc://sa:YourStrong@Passw0rd@sqlserver:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes" `
  swarm-demo/backend:latest

# Run Frontend
docker run -d `
  --name frontend `
  --network app-network `
  -p 3000:3000 `
  -p 8080:3000 `
  -e "NEXT_PUBLIC_API_URL=http://localhost:8000" `
  swarm-demo/frontend:latest

Write-Host "Containers started successfully!" -ForegroundColor Green
Write-Host "Access your applications at:" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:3000 or http://localhost:8080" -ForegroundColor Cyan
Write-Host "  Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Backend Health: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "  PostgreSQL: localhost:5432" -ForegroundColor Cyan
Write-Host "  SQL Server: localhost:1433" -ForegroundColor Cyan