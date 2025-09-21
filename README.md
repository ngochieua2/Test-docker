# Docker Swarm Stack Demo

A comprehensive Docker Swarm stack featuring FastAPI backend, Next.js frontend, PostgreSQL, and SQL Server. Perfect for learning container orchestration and microservices deployment on Ubuntu VPS.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │    │     Backend     │    │   Databases     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│  PostgreSQL     │
│   Port: 3000    │    │   Port: 8000    │    │  SQL Server     │
│   Port: 8080    │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        ▲
                                                        │
┌───────────────────────────────────────────────────────┘
│                 Docker Swarm Cluster
│              (Overlay Networks & Volumes)
└─────────────────────────────────────────────────────────
```

## 📦 Services

- **Frontend**: Next.js app with health monitoring and API integration
- **Backend**: FastAPI with database connections and health checks
- **PostgreSQL**: Primary database with persistent storage
- **SQL Server**: Secondary database for multi-database scenarios

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+ with Swarm mode
- Git
- 8GB+ RAM recommended
- Ubuntu 20.04+ (for VPS deployment)

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <your-repo>
   cd docker-swarm-stack
   ```

2. **Initialize Docker Swarm**:
   ```bash
   docker swarm init
   ```

3. **Deploy the stack**:
   ```bash
   # Linux/Mac
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh deploy
   
   # Windows
   scripts\deploy.bat deploy
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8080
   - API Docs: http://localhost:8080/docs

## 🖥️ Ubuntu VPS Deployment

### Step 1: Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker

# Log out and back in to apply group changes
```

### Step 2: Deploy Application

```bash
# Clone repository
git clone <your-repo-url>
cd docker-swarm-stack

# Initialize Docker Swarm
docker swarm init

# Deploy the stack
chmod +x scripts/deploy.sh
./scripts/deploy.sh deploy
```

### Step 3: Monitor Deployment

```bash
# Check service status
./scripts/monitor.sh health

# Continuous monitoring
./scripts/monitor.sh monitor

# View specific service logs
./scripts/deploy.sh logs backend
```

## � External Database Connections

Both databases are exposed externally and can be accessed from outside the Docker Swarm cluster:

### PostgreSQL Connection
```bash
# Using psql command line
psql -h localhost -p 5432 -U postgres -d postgres

# Connection string
postgresql://postgres:postgres@localhost:5432/postgres
```

### SQL Server Connection
```bash
# Using sqlcmd command line
sqlcmd -S localhost,1433 -U sa -P 'YourStrong@Passw0rd'

# Connection string
Server=localhost,1433;Database=master;User Id=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;
```

### GUI Database Tools
You can connect using popular database management tools:

#### For PostgreSQL:
- **pgAdmin**: http://localhost:5432
- **DBeaver**: PostgreSQL connection
- **DataGrip**: PostgreSQL driver

#### For SQL Server:
- **SQL Server Management Studio (SSMS)**
- **Azure Data Studio**
- **DBeaver**: SQL Server connection
- **DataGrip**: SQL Server driver

### Connection Details
- **PostgreSQL Port**: `5432`
- **SQL Server Port**: `1433`
- **Host**: `localhost` (or your VPS IP address)

## �🛠️ Management Commands

### Deployment Script (`scripts/deploy.sh`)

```bash
# Build images
./scripts/deploy.sh build

# Deploy full stack
./scripts/deploy.sh deploy

# Deploy specific service
./scripts/deploy.sh deploy-service backend

# Scale services
./scripts/deploy.sh scale frontend 3

# View status
./scripts/deploy.sh status

# View logs
./scripts/deploy.sh logs backend

# Remove stack
./scripts/deploy.sh remove
```

### Monitoring Script (`scripts/monitor.sh`)

```bash
# Check all service health
./scripts/monitor.sh health

# Test API endpoints
./scripts/monitor.sh endpoints

# View resource usage
./scripts/monitor.sh resources

# Continuous monitoring (30s interval)
./scripts/monitor.sh monitor

# Monitor specific service
./scripts/monitor.sh service backend
```

## 🔧 Configuration

### Environment Variables

#### Backend (`backend/main.py`)
- `POSTGRES_URL`: PostgreSQL connection string
- `SQLSERVER_URL`: SQL Server connection string

#### Frontend (`frontend/next.config.js`)
- `NEXT_PUBLIC_API_URL`: Backend API URL

### Database Configuration

#### PostgreSQL
- **Host**: localhost (or your VPS IP)
- **Port**: 5432 (exposed externally)
- Default database: `postgres`
- User: `postgres`
- Password: `postgres`

#### SQL Server
- **Host**: localhost (or your VPS IP)  
- **Port**: 1433 (exposed externally)
- Database: `master`
- User: `sa`
- Password: `YourStrong@Passw0rd`

## 🌐 Networking

### Networks
- `frontend_network`: Frontend ↔ Backend communication
- `backend_network`: Backend ↔ Database communication

### Ports
- `3000`: Frontend (Next.js)
- `8080`: Backend (FastAPI) - exposed externally
- `8000`: Backend API (internal)
- `5432`: PostgreSQL (exposed externally)
- `1433`: SQL Server (exposed externally)

## 📊 Scaling and High Availability

### Horizontal Scaling

```bash
# Scale frontend replicas
./scripts/deploy.sh scale frontend 5

# Scale backend replicas
./scripts/deploy.sh scale backend 3

# Check current scaling
docker stack services swarm-demo
```

### Placement Constraints

- **Databases**: Manager nodes only (data persistence)
- **Applications**: Any available node

### Health Checks

All services include comprehensive health checks:
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3 attempts
- **Start Period**: 30-60 seconds

## 🔍 Troubleshooting

### Common Issues

1. **Services not starting**:
   ```bash
   # Check service logs
   docker service logs swarm-demo_backend
   
   # Check service details
   docker service inspect swarm-demo_backend
   ```

2. **Database connection issues**:
   ```bash
   # Test database connectivity
   docker exec -it $(docker ps -q -f name=swarm-demo_postgresql) psql -U postgres -d testdb
   ```

3. **Network connectivity**:
   ```bash
   # List networks
   docker network ls
   
   # Inspect network
   docker network inspect swarm-demo_backend_network
   ```

4. **Resource constraints**:
   ```bash
   # Check resource usage
   ./scripts/monitor.sh resources
   
   # Check node resources
   docker node ls
   docker system df
   ```

### Log Analysis

```bash
# All service logs
docker stack services swarm-demo

# Specific service logs
docker service logs -f swarm-demo_backend

# Container logs
docker logs <container_id>
```

## 🔒 Security Considerations

### Production Checklist

- [ ] Change default database passwords
- [ ] Use environment variables for secrets
- [ ] Configure SSL/TLS certificates
- [ ] Set up proper firewall rules
- [ ] Enable Docker secrets management
- [ ] Implement proper authentication
- [ ] Regular security updates

### Docker Secrets (Production)

```bash
# Create secrets
echo "new_postgres_password" | docker secret create postgres_password -
echo "new_sqlserver_password" | docker secret create sqlserver_password -

# Update docker-compose.yml to use secrets
# See: https://docs.docker.com/engine/swarm/secrets/
```

## 📈 Performance Optimization

### Resource Limits

Current settings in `docker-compose.yml`:

- **Frontend/Backend**: 512MB RAM, 0.5 CPU
- **PostgreSQL**: 512MB RAM, 0.5 CPU  
- **SQL Server**: 2GB RAM, 1.0 CPU

### Optimization Tips

1. **Adjust resource limits** based on actual usage
2. **Use multi-stage builds** for smaller images
3. **Implement caching strategies** in application
4. **Use read replicas** for databases under high load
5. **Configure connection pooling** in applications

## 🧪 Testing

### API Testing

```bash
# Health checks
curl http://localhost:8080/health
curl http://localhost:8080/health/postgres
curl http://localhost:8080/health/sqlserver

# Create user (PostgreSQL)
curl -X POST "http://localhost:8080/users/postgres" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'

# Get users
curl http://localhost:8080/users/postgres
```

### Load Testing

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test frontend
ab -n 1000 -c 10 http://localhost:3000/

# Test API
ab -n 1000 -c 10 http://localhost:8080/health
```

## 📚 Learning Resources

### Docker Swarm
- [Docker Swarm Documentation](https://docs.docker.com/engine/swarm/)
- [Swarm Mode Tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/)

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI with Databases](https://fastapi.tiangolo.com/tutorial/databases/)

### Next.js
- [Next.js Documentation](https://nextjs.org/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section
2. Review service logs: `./scripts/deploy.sh logs <service>`
3. Monitor service health: `./scripts/monitor.sh health`
4. Create an issue with detailed logs and environment info

---

**Happy Learning! 🚀**

This stack provides a solid foundation for understanding Docker Swarm, microservices architecture, and container orchestration. Experiment with scaling, updates, and different deployment strategies to deepen your knowledge.