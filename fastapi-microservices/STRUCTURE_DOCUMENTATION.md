# FastAPI Microservices Project Structure Documentation

## 🏗️ Project Overview

This is a FastAPI-based microservices architecture project that provides a modular, scalable foundation for building distributed applications. The project follows clean architecture principles with shared components, well-organized services, and comprehensive tooling for development and deployment.

## 📁 Complete File Structure

```
fastapi-microservices/
├── 📄 README.md                      # Project overview and setup instructions
├── 📄 requirements.txt               # Main project dependencies
├── 📄 alembic.ini                   # Alembic database migration configuration
├── 🐍 run_hello_service.py          # Cross-platform Hello Service launcher
├── 🐍 run_todo_service.py           # Cross-platform Todo Service launcher
├── 🔧 start-postgres.bat            # Windows PostgreSQL startup script
├── 🔧 start-postgres.sh             # Unix/Linux PostgreSQL startup script
├── 📁 alembic/                      # Database migration management
│   ├── 🐍 env.py                    # Alembic environment configuration
│   ├── 📄 script.py.mako            # Migration script template
│   └── 📁 versions/                 # Database migration versions
├── 📁 services/                     # Individual microservices
│   ├── 📁 hello-service/            # Simple greeting microservice
│   │   ├── 📄 .env                  # Environment variables template
│   │   ├── 🐍 __init__.py           # Package initialization
│   │   ├── 🐍 main.py               # Service entry point
│   │   ├── 📄 requirements.txt      # Service-specific dependencies
│   │   ├── 📄 SERVICE_README.md     # Service documentation
│   │   ├── 📁 app/                  # Application structure
│   │   │   ├── 🐍 __init__.py       # App package initialization
│   │   │   ├── 📁 api/              # API endpoints and routes
│   │   │   ├── 📁 core/             # Core application components
│   │   │   ├── 📁 models/           # Data models and schemas
│       │   ├── 📁 repositories/     # Data access layer
│   │   │   ├── 📁 schemas/          # Pydantic schemas
│   │   │   ├── 📁 services/         # Business logic layer
│   │   │   └── 📁 utils/            # Service-specific utilities
│   │   ├── 📁 tests/                # Unit and integration tests
│   │   │   ├── 🐍 __init__.py       # Test package initialization
│   │   │   ├── 🐍 conftest.py       # Test configuration and fixtures
│   │   │   ├── 🐍 test_services.py  # Service layer tests
│   │   │   └── 📁 api/              # API endpoint tests
│   │   └── 📁 __pycache__/          # Python bytecode cache
│   └── 📁 todo-service/             # CRUD todo management microservice
│       ├── 📄 .env                  # Environment variables template
│       ├── 🐍 __init__.py           # Package initialization
│       ├── 🐍 main.py               # Service entry point
│       ├── 📄 requirements.txt      # Service-specific dependencies
│       ├── 📄 SERVICE_README.md     # Service documentation
│       ├── 📁 app/                  # Application structure
│       │   ├── 🐍 __init__.py       # App package initialization
│       │   ├── 📁 api/              # API endpoints and routes
│       │   ├── 📁 core/             # Core application components
│       │   ├── 📁 models/           # SQLAlchemy data models
│       │   ├── 📁 repositories/     # Data access layer
│       │   ├── 📁 schemas/          # Pydantic schemas
│       │   ├── 📁 services/         # Business logic layer
│       │   └── 📁 utils/            # Service-specific utilities
│       ├── 📁 tests/                # Unit and integration tests
│       │   ├── 🐍 __init__.py       # Test package initialization
│       │   ├── 🐍 conftest.py       # Test configuration and fixtures
│       │   ├── 🐍 test_repositories.py # Repository layer tests
│       │   ├── 🐍 test_services.py  # Service layer tests
│       │   └── 📁 api/              # API endpoint tests
│       └── 📁 __pycache__/          # Python bytecode cache
└── 📁 shared/                       # Shared components across services
    ├── 🐍 __init__.py               # Shared package initialization
    ├── 📄 README.md                 # Shared components documentation
    ├── 🐍 example_integration.py    # Integration example for services
    ├── 📁 auth/                     # Authentication and authorization
    │   ├── 🐍 __init__.py           # Auth package initialization
    │   └── 🐍 manager.py            # Authentication management utilities
    ├── 📁 core/                     # Core shared components
    │   ├── 🐍 __init__.py           # Core package initialization
    │   ├── 🐍 config.py             # Base configuration classes
    │   └── 🐍 schemas.py            # Common response schemas
    ├── 📁 exceptions/               # Exception handling framework
    │   ├── 🐍 __init__.py           # Exceptions package initialization
    │   ├── 🐍 custom.py             # Custom exception classes
    │   └── 🐍 handlers.py           # FastAPI exception handlers
    ├── 📁 legacy/                   # Legacy/deprecated components
    │   ├── 🐍 __init__.py           # Legacy package initialization
    │   ├── 🐍 database.py           # Legacy database configuration
    │   ├── 🐍 models.py             # Legacy SQLAlchemy models
    │   ├── 🐍 schemas.py            # Legacy Pydantic schemas
    │   └── 🐍 services.py           # Legacy business logic services
    ├── 📁 middleware/               # Reusable middleware components
    │   ├── 🐍 __init__.py           # Middleware package initialization
    │   ├── 🐍 logging.py            # Request logging middleware
    │   └── 🐍 security.py           # Security middleware (rate limiting, headers)
    ├── 📁 utils/                    # Utility functions and helpers
    │   ├── 🐍 __init__.py           # Utils package initialization
    │   ├── 🐍 datetime_utils.py     # Date/time manipulation utilities
    │   ├── 🐍 string_utils.py       # String processing utilities
    │   └── 🐍 validators.py         # Data validation utilities
    └── 📁 __pycache__/              # Python bytecode cache
```

## 🎯 Component Purposes and Functions

### 📋 Root Level Files

| File | Purpose |
|------|---------|
| `README.md` | Comprehensive project documentation with setup instructions, service descriptions, and usage examples |
| `requirements.txt` | Core project dependencies including FastAPI, SQLAlchemy, Alembic, and testing frameworks |
| `alembic.ini` | Alembic configuration for database migrations, defining script locations and database connection settings |
| `run_hello_service.py` | Cross-platform Python launcher for the Hello Service with colored output and environment management |
| `run_todo_service.py` | Cross-platform Python launcher for the Todo Service with database setup and configuration validation |
| `start-postgres.bat` | Windows batch script for starting PostgreSQL database container |
| `start-postgres.sh` | Unix/Linux shell script for starting PostgreSQL database container |

### 🗃️ Database Migration System (`alembic/`)

| Component | Purpose |
|-----------|---------|
| `env.py` | Alembic environment configuration that connects to the database and manages migration context |
| `script.py.mako` | Mako template for generating new migration scripts with consistent formatting |
| `versions/` | Directory containing versioned database migration files for schema changes |

### 🔧 Microservices (`services/`)

#### Hello Service (`services/hello-service/`)
A lightweight microservice demonstrating basic FastAPI functionality:

| Component | Purpose |
|-----------|---------|
| `main.py` | Service entry point with application lifespan management and server configuration |
| `.env`    | Template for environment variables configuration |
| `requirements.txt` | Service-specific dependencies if different from main project |
| `SERVICE_README.md` | Detailed service documentation with API endpoints and usage examples |
| `app/api/` | REST API endpoints and route definitions |
| `app/core/` | Core application components (config, app factory, database) |
| `app/models/` | Data models and database schemas |
| `app/schemas/` | Pydantic models for request/response validation |
| `app/services/` | Business logic and service layer implementations |
| `app/utils/` | Service-specific utility functions and helpers |
| `tests/` | Comprehensive test suite with unit and integration tests |

#### Todo Service (`services/todo-service/`)
A full CRUD microservice for todo management:

| Component | Purpose |
|-----------|---------|
| `main.py` | Service entry point with database table creation and application lifecycle |
| `.env`    | Template for environment variables configuration |
| `requirements.txt` | Service-specific dependencies including database drivers |
| `SERVICE_README.md` | Comprehensive service documentation with API specifications |
| `app/api/` | REST API endpoints for todo CRUD operations |
| `app/core/` | Core components including database configuration and app factory |
| `app/models/` | SQLAlchemy models for todo entities |
| `app/repositories/` | Data access layer with repository pattern implementation |
| `app/schemas/` | Pydantic schemas for todo request/response models |
| `app/services/` | Business logic layer for todo operations |
| `app/utils/` | Service-specific utilities and helper functions |
| `tests/` | Complete test suite including repository and service tests |

### 🔄 Shared Components (`shared/`)

The shared folder provides reusable components across all microservices:

#### Core Components (`shared/core/`)
| Component | Purpose |
|-----------|---------|
| `config.py` | Base configuration classes with environment variable management and validation |
| `schemas.py` | Common response schemas and base Pydantic models used across services |

#### Authentication System (`shared/auth/`)
| Component | Purpose |
|-----------|---------|
| `manager.py` | Authentication and authorization management utilities (placeholder for future implementation) |

#### Exception Handling (`shared/exceptions/`)
| Component | Purpose |
|-----------|---------|
| `custom.py` | Custom exception classes for business logic errors and API-specific exceptions |
| `handlers.py` | FastAPI exception handlers for consistent error responses across services |

#### Middleware Framework (`shared/middleware/`)
| Component | Purpose |
|-----------|---------|
| `logging.py` | Request/response logging middleware for observability and debugging |
| `security.py` | Security middleware including rate limiting, CORS handling, and security headers |

#### Utility Library (`shared/utils/`)
| Component | Purpose |
|-----------|---------|
| `datetime_utils.py` | Date and time manipulation utilities with timezone handling |
| `string_utils.py` | String processing functions including slugification and validation |
| `validators.py` | Data validation utilities and custom validators for Pydantic models |

#### Legacy Components (`shared/legacy/`)
| Component | Purpose |
|-----------|---------|
| `database.py` | Legacy database configuration (maintained for backward compatibility) |
| `models.py` | Legacy SQLAlchemy models (being phased out in favor of service-specific models) |
| `schemas.py` | Legacy Pydantic schemas (superseded by service-specific schemas) |
| `services.py` | Legacy business logic services (replaced by service-specific implementations) |

#### Integration Example (`shared/example_integration.py`)
Comprehensive example demonstrating how to integrate shared components into a new microservice, including:
- Configuration management
- Exception handling setup
- Middleware integration
- Utility usage patterns

## 🏛️ Architecture Patterns

### 1. **Microservices Architecture**
- **Separation of Concerns**: Each service handles a specific domain (Hello, Todo)
- **Independent Deployment**: Services can be deployed and scaled independently
- **Technology Flexibility**: Services can use different tech stacks if needed

### 2. **Clean Architecture**
- **Layered Structure**: API → Services → Repositories → Models
- **Dependency Inversion**: Higher layers depend on abstractions, not implementations
- **Testability**: Each layer can be tested in isolation

### 3. **Shared Kernel Pattern**
- **Common Components**: Shared utilities reduce code duplication
- **Consistent Standards**: Uniform error handling and configuration across services
- **Rapid Development**: New services can leverage existing components

### 4. **Repository Pattern**
- **Data Access Abstraction**: Repository layer abstracts database operations
- **Testability**: Easy to mock data access for unit testing
- **Flexibility**: Can switch between different data storage solutions

## 🚀 Key Features

### ✅ Development Experience
- **Cross-platform Support**: Works on Windows, macOS, and Linux
- **Hot Reload**: Development servers with automatic reload on file changes
- **Comprehensive Logging**: Structured logging with colored output
- **Environment Management**: Flexible configuration with environment variables

### ✅ Production Ready
- **Database Migrations**: Alembic for version-controlled schema changes
- **Exception Handling**: Comprehensive error handling with custom exceptions
- **Security Middleware**: Rate limiting, CORS, and security headers
- **Health Checks**: Built-in health endpoints for monitoring

### ✅ Testing & Quality
- **Test Structure**: Organized test suites for each service
- **Test Fixtures**: Reusable test configuration and data
- **API Testing**: HTTP client testing for endpoints
- **Service Testing**: Business logic and repository testing

### ✅ Scalability & Maintenance
- **Modular Design**: Easy to add new services and features
- **Shared Components**: Reusable utilities and middleware
- **Documentation**: Comprehensive README files and code documentation
- **Legacy Support**: Graceful handling of deprecated components

## 🔧 Getting Started

1. **Prerequisites**: Python 3.8+, PostgreSQL
2. **Installation**: `pip install -r requirements.txt`
3. **Database Setup**: Run `start-postgres.sh` or `start-postgres.bat`
4. **Run Services**: 
   - Hello Service: `python run_hello_service.py`
   - Todo Service: `python run_todo_service.py`
5. **API Documentation**: Visit `http://localhost:8001/docs` or `http://localhost:8002/docs`

## 📚 Additional Resources

- **Service Documentation**: Check individual `SERVICE_README.md` files
- **Shared Components**: See `shared/README.md` for detailed component documentation
- **Integration Examples**: Reference `shared/example_integration.py` for implementation patterns
- **API Documentation**: Interactive docs available at `/docs` endpoint for each service

This architecture provides a solid foundation for building scalable, maintainable microservices with FastAPI while promoting code reuse and consistent development practices across the entire project.