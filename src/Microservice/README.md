# FastAPI Microservices Project

This project contains two independent FastAPI microservices with a shared database configuration and Alembic migrations.

## Project Structure

```
fastapi-microservices/
├── shared/                     # Shared/common modules
│   ├── __init__.py
│   ├── database.py            # Database configuration
│   ├── models.py              # SQLAlchemy models
│   ├── schemas.py             # Pydantic schemas
│   └── services.py            # Business logic services
├── services/
│   ├── hello-service/         # Hello World service
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── requirements.txt
│   └── todo-service/          # Todo CRUD service
│       ├── __init__.py
│       ├── main.py
│       └── requirements.txt
├── alembic/                   # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Project dependencies
└── run scripts              # Various run scripts
```

## Services

### Hello Service (Port 8001)
- **Endpoint**: `GET /hello` → Returns `"Hello World"`
- **Health Check**: `GET /health`

### Todo Service (Port 8002)
- **GET /todos** → List all todos (with pagination)
- **GET /todos/{id}** → Get todo by ID
- **POST /todos** → Create new todo
- **PUT /todos/{id}** → Update todo
- **DELETE /todos/{id}** → Delete todo
- **Health Check**: `GET /health`

## Database Configuration

- **Database**: PostgreSQL
- **Connection String**: `postgresql+psycopg2://admin:admin1@localhost:15432/appdb`
- **Migration Tool**: Alembic (shared across all services)

## Setup and Installation

### Prerequisites
- Python 3.8+
- PostgreSQL database running on `localhost:15432`
  - Database: `appdb`
  - Username: `admin`
  - Password: `admin1`

### Installation Steps

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run database migrations**:
   ```bash
   # Create initial migration (if needed)
   alembic revision --autogenerate -m "Initial migration"
   
   # Apply migrations
   alembic upgrade head
   ```

3. **Run services**:

   ## 🚀 **Recommended Method**
   
   **Python Scripts (Cross-platform: Windows, Mac, Ubuntu)**
   ```bash
   # Hello Service
   python run_hello_service.py
   python run_hello_service.py --venv     # With virtual environment (recommended)
   python run_hello_service.py --help     # Show help and options
   
   # Todo Service (in another terminal)
   python run_todo_service.py
   python run_todo_service.py --venv      # With virtual environment (recommended)
   python run_todo_service.py --help      # Show help and options
   ```

   ## 🛠️ **Alternative Method**
   
   **Using Make (if you have make installed)**
   ```bash
   # Install dependencies
   make install
   
   # Run services
   make hello     # Start Hello Service
   make todo      # Start Todo Service
   
   # Or with virtual environment
   make hello-dev
   make todo-dev
   
   # See all available commands
   make help
   ```

   **Manual Run (Any Platform)**:
   ```bash
   # Hello Service
   cd services/hello-service
   python main.py
   
   # Todo Service
   cd services/todo-service  
   python main.py
   ```

## API Documentation

Once services are running, you can access the interactive API documentation:

- **Hello Service**: http://localhost:8001/docs
- **Todo Service**: http://localhost:8002/docs

## Example API Usage

### Hello Service
```bash
curl http://localhost:8001/hello
# Returns: "Hello World"
```

### Todo Service
```bash
# Create a todo
curl -X POST "http://localhost:8002/todos" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Complete FastAPI tutorial", "completed": false}'

# Get all todos
curl http://localhost:8002/todos

# Get specific todo
curl http://localhost:8002/todos/1

# Update todo
curl -X PUT "http://localhost:8002/todos/1" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'

# Delete todo
curl -X DELETE http://localhost:8002/todos/1
```

## Database Management

### Create Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

## Development Notes

- Each service runs independently with its own port
- Shared modules are in the `shared/` directory
- Database models and schemas are centralized for consistency
- Alembic migrations are shared across all services
- Services can be deployed separately as microservices

## Health Checks

Both services include health check endpoints:
- Hello Service: http://localhost:8001/health
- Todo Service: http://localhost:8002/health