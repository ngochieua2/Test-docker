# Todo Service

A comprehensive FastAPI microservice for todo management with CRUD operations, filtering, search, and statistics.

## 🏗️ Project Structure

```
todo-service/
├── app/                          # Main application package
│   ├── api/                      # API layer
│   │   └── v1/                   # API version 1
│   │       ├── api.py           # Main API router
│   │       ├── todos.py         # Todo CRUD endpoints
│   │       └── health.py        # Health check endpoints
│   ├── core/                     # Core application components
│   │   ├── app.py               # FastAPI app factory
│   │   ├── config.py            # Configuration settings
│   │   └── database.py          # Database configuration
│   ├── models/                   # Database models
│   │   └── todo.py              # Todo SQLAlchemy model
│   ├── schemas/                  # Pydantic schemas
│   │   ├── todo.py              # Todo request/response schemas
│   │   └── health.py            # Health check schemas
│   ├── services/                 # Business logic layer
│   │   ├── todo_service.py      # Todo business logic
│   │   └── health_service.py    # Health check business logic
│   └── utils/                    # Utility functions
│       ├── helpers.py           # Common helper functions
│       └── logger.py            # Logging utilities
├── tests/                        # Test suite
│   ├── api/                      # API endpoint tests
│   │   ├── test_todos.py        # Todo endpoint tests
│   │   └── test_health.py       # Health endpoint tests
│   ├── conftest.py              # Test configuration
│   └── test_services.py         # Service layer tests
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
└── .env.example                 # Environment variables template
```

## 🚀 Features

### Todo Management
- **CRUD Operations**: Create, read, update, delete todos
- **Filtering**: Filter by completion status
- **Search**: Search in title and description
- **Pagination**: Efficient data loading
- **Statistics**: Get todo completion metrics
- **Bulk Operations**: Delete all completed todos
- **Toggle Completion**: Quick status toggle

### API Endpoints

#### Todo Endpoints (`/api/v1/todos`)
- `GET /` - List todos with filtering and pagination
- `POST /` - Create new todo
- `GET /{id}` - Get specific todo
- `PUT /{id}` - Update todo
- `PATCH /{id}/toggle` - Toggle completion status
- `DELETE /{id}` - Delete todo
- `DELETE /` - Delete all completed todos
- `GET /stats` - Get todo statistics

#### Health Check (`/api/v1/health`)
- `GET /` - Comprehensive health status with database check

### Advanced Features
- **Data Validation**: Comprehensive input validation
- **Error Handling**: Proper HTTP error responses
- **Logging**: Structured logging throughout
- **Database Health**: Database connectivity monitoring
- **System Metrics**: CPU, memory, disk usage monitoring

## 🛠️ Setup & Development

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- pip

### Installation

1. **Navigate to the service:**
   ```bash
   cd fastapi-microservices/services/todo-service
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env file with your database settings
   ```

5. **Set up database:**
   ```bash
   # For PostgreSQL, create database first
   createdb todoapp
   
   # Tables will be created automatically on first run
   ```

### Running the Service

#### Development Mode
```bash
python main.py
```

#### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8002
```

### Testing

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```

Run specific test file:
```bash
pytest tests/api/test_todos.py -v
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8002/docs
- **ReDoc:** http://localhost:8002/redoc

## 🔍 API Examples

### Create Todo
```bash
curl -X POST "http://localhost:8002/api/v1/todos/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Build awesome APIs", "completed": false}'
```

### Get Todos with Filters
```bash
# Get all todos
curl "http://localhost:8002/api/v1/todos/"

# Get completed todos only
curl "http://localhost:8002/api/v1/todos/?completed=true"

# Search todos
curl "http://localhost:8002/api/v1/todos/?search=FastAPI"

# Pagination
curl "http://localhost:8002/api/v1/todos/?skip=0&limit=10"
```

### Update Todo
```bash
curl -X PUT "http://localhost:8002/api/v1/todos/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Title", "completed": true}'
```

### Toggle Completion
```bash
curl -X PATCH "http://localhost:8002/api/v1/todos/1/toggle"
```

### Get Statistics
```bash
curl "http://localhost:8002/api/v1/todos/stats"
```

## 🏗️ Architecture Benefits

### 1. **Separation of Concerns**
- **API Layer**: HTTP request/response handling
- **Service Layer**: Business logic and operations
- **Model Layer**: Database entities
- **Schema Layer**: Data validation and serialization

### 2. **Advanced Features**
- **Search & Filtering**: Powerful query capabilities
- **Statistics**: Real-time todo metrics
- **Bulk Operations**: Efficient batch processing
- **Health Monitoring**: Database and system monitoring

### 3. **Production Ready**
- **Comprehensive Testing**: Unit and integration tests
- **Error Handling**: Proper HTTP status codes
- **Input Validation**: Pydantic schema validation
- **Logging**: Structured logging throughout
- **Database Management**: Connection pooling and health checks

### 4. **Easy to Extend**
- **Modular Structure**: Add new features easily
- **Service Pattern**: Business logic separation
- **Configuration Management**: Environment-based settings
- **API Versioning**: Future-proof API design

## 🔧 Adding New Features

### Adding Todo Categories
1. **Update Model**: Add category field to `Todo` model
2. **Update Schemas**: Add category to request/response schemas
3. **Update Service**: Add category filtering logic
4. **Update API**: Add category endpoints
5. **Add Tests**: Test category functionality

### Adding User Authentication
1. **Create User Model**: Add user authentication models
2. **Add Auth Service**: Implement authentication logic
3. **Update Todo Model**: Add user relationship
4. **Add Middleware**: JWT authentication middleware
5. **Update Tests**: Test authenticated endpoints

## 📊 Monitoring

### Health Endpoint Features
- Service status and version
- Database connectivity check
- System metrics (CPU, memory, disk)
- Response time monitoring
- Uptime tracking

### Logging
- Request/response logging
- Business operation logging
- Error logging with context
- Performance monitoring

## 🐳 Docker

The service is designed to work with the existing Docker setup in the parent directory.

## 🤝 Contributing

1. Follow the established code structure
2. Add comprehensive tests for new features
3. Update documentation
4. Use proper logging
5. Follow Python best practices
6. Validate all inputs
7. Handle errors gracefully