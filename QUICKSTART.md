# Docker Swarm Stack Demo - Quick Start Guide

## For Ubuntu VPS Deployment

### 1. Server Setup (5 minutes)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Enable Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Log out and back in for group changes to take effect
exit
```

### 2. Deploy Application (5 minutes)

```bash
# Clone repository
git clone <your-repo-url>
cd docker-swarm-stack

# Initialize Docker Swarm
docker swarm init

# Make scripts executable
chmod +x scripts/deploy.sh scripts/monitor.sh

# Deploy the entire stack
./scripts/deploy.sh deploy
```

### 3. Verify Deployment (2 minutes)

```bash
# Check all services
./scripts/monitor.sh health

# Test endpoints
curl http://localhost:3000/health
curl http://localhost:8080/health
```

### 4. Access Your Application

- **Frontend**: http://your-vps-ip:3000
- **Backend**: http://your-vps-ip:8080
- **API Documentation**: http://your-vps-ip:8080/docs

## Common Commands

```bash
# Scale services
./scripts/deploy.sh scale frontend 3
./scripts/deploy.sh scale backend 2

# Monitor services
./scripts/monitor.sh monitor

# View logs
./scripts/deploy.sh logs backend

# Remove everything
./scripts/deploy.sh remove
```

## Service Architecture

- **Frontend** (Next.js): Port 3000 & 8080
- **Backend** (FastAPI): Port 8080 (exposed), 8000 (internal)
- **PostgreSQL**: Internal port 5432
- **SQL Server**: Internal port 1433

Total deployment time: ~10 minutes including server setup!