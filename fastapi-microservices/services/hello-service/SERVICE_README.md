# Hello Service

A well-structured FastAPI microservice with proper separation of concerns and easy expandability.

## 🏗️ Project Structure

```
hello-service/
├── app/                          # Main application package
│   ├── api/                      # API layer
│   │   └── v1/                   # API version 1
│   │       ├── api.py           # Main API router
│   │       ├── hello.py         # Hello endpoints
│   │       └── health.py        # Health check endpoints
│   ├── core/                     # Core application components
│   │   ├── app.py               # FastAPI app factory
│   │   └── config.py            # Configuration settings
│   ├── models/                   # Database models (SQLAlchemy)
│   ├── schemas/                  # Pydantic schemas (request/response)
│   │   ├── hello.py             # Hello-related schemas
│   │   └── health.py            # Health check schemas
│   ├── services/                 # Business logic layer
│   │   ├── hello_service.py     # Hello business logic
│   │   └── health_service.py    # Health check business logic
│   └── utils/                    # Utility functions
│       ├── helpers.py           # Common helper functions
│       └── logger.py            # Logging utilities
├── tests/                        # Test suite
│   ├── api/                      # API endpoint tests
│   │   ├── test_hello.py        # Hello endpoint tests
│   │   └── test_health.py       # Health endpoint tests
│   ├── conftest.py              # Test configuration
│   └── test_services.py         # Service layer tests
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
└── .env.example                 # Environment variables template
```

## 🚀 Features

### API Endpoints

#### Hello Endpoints (`/api/v1/hello`)
- `GET /` - Simple hello message
- `POST /` - Personalized hello message
- `GET /greetings/{language}` - Hello in different languages

#### Health Check (`/api/v1/health`)
- `GET /` - Comprehensive health status with system metrics

### Supported Languages
- English, Spanish, French, German, Italian
- Portuguese, Russian, Japanese, Chinese, Korean

## 🛠️ Setup & Development

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone and navigate to the service:**
   ```bash
   cd fastapi-microservices/services/hello-service
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
   # Edit .env file as needed
   ```

### Running the Service

#### Development Mode
```bash
python main.py
```

#### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8001
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
pytest tests/api/test_hello.py -v
```

## 📚 API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc

## 🏗️ Architecture Benefits

### 1. **Separation of Concerns**
- **API Layer:** Handle HTTP requests/responses
- **Service Layer:** Business logic and operations
- **Schema Layer:** Data validation and serialization
- **Utils Layer:** Common utilities and helpers

### 2. **Easy to Expand**
- Add new endpoints by creating new route files
- Add new business logic in service modules
- Add new data models and schemas
- Modular structure supports team development

### 3. **Configuration Management**
- Environment-based configuration
- Easy to deploy across different environments
- Feature flags for enabling/disabling features

### 4. **Testing Ready**
- Comprehensive test structure
- API tests and service tests
- Easy to add new tests

### 5. **Production Ready**
- Proper logging configuration
- Health check with system metrics
- CORS support
- Error handling
- Documentation generation

## 🔧 Adding New Features

### Adding a New Endpoint

1. **Create route file:** `app/api/v1/new_endpoint.py`
2. **Create service:** `app/services/new_service.py`
3. **Create schemas:** `app/schemas/new_schema.py`
4. **Add to API router:** Update `app/api/v1/api.py`
5. **Add tests:** Create `tests/api/test_new_endpoint.py`

### Adding Database Models

1. **Create model:** `app/models/new_model.py`
2. **Create migration:** Use Alembic for database changes
3. **Update services:** Modify service layer to use new models

## 📊 Monitoring

The health endpoint provides:
- Service status and version
- System metrics (CPU, memory, disk usage)
- Service uptime
- Timestamp information

## 🐳 Docker

The service is designed to work with the existing Docker setup in the parent directory.

## 🤝 Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Use proper logging
5. Follow Python best practices