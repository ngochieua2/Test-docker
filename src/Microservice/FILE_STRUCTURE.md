# 📁 Microservice Folder Structure & Purpose

This document provides a comprehensive overview of the microservice folder structure and the purpose of each component.

## 📁 Directory Structure

```
📦 Microservice/
├── 📄 alembic.ini                    # Alembic migration configuration
├── 📄 README.md                      # Project documentation and setup guide
├── 📄 run_main_service.py            # Service runner script with environment options
│
├── 📁 alembic/                       # Database Migration Management
│   ├── 📄 env.py                     # Alembic environment configuration
│   ├── 📄 script.py.mako            # Migration script template
│   └── 📁 versions/                  # Auto-generated migration files
│
├── 📁 services/                      # Individual Microservices
│   └── 📁 main-service/              # Primary microservice implementation
│       ├── 📄 .env                   # Environment variables (sensitive config)
│       ├── 📄 __init__.py            # Python package marker
│       ├── 📄 main.py                # Service entry point & FastAPI app lifecycle
│       ├── 📄 requirements.txt       # Service-specific dependencies
│       └── 📁 app/                   # Application logic structure
│           ├── 📄 __init__.py        # Package marker
│           ├── 📁 api/               # API endpoints and routing
│           │   ├── 📄 __init__.py    
│           │   └── 📁 v1/            # API version 1 endpoints
│           ├── 📁 core/              # Core application configuration
│           │   ├── 📄 __init__.py    
│           │   ├── 📄 app.py         # FastAPI application factory
│           │   └── 📄 config.py      # Application settings and configuration
│           ├── 📁 models/            # Oject models
│           ├── 📁 repository/        # Data access layer (Repository pattern)
│           ├── 📁 schemas/           # Request/response schemas
│           └── 📁 services/          # Business logic services
│
└── 📁 shared/                        # Shared Components Across Services
    ├── 📄 __init__.py                # Package marker
    ├── 📄 README.md                  # Shared components documentation
    ├── 📁 constants/                 # Application constants
    │   ├── 📄 __init__.py           
    │   └── 📄 constants.py           # Global constants and enums
    ├── 📁 database/                  # Database abstraction layer
    │   ├── 📄 __init__.py           
    │   ├── 📄 dbContext.py           # Database connection and session management
    │   ├── 📄 models.py              # Database modelss
    └── 📁 utils/                     # Utility functions
        ├── 📄 __init__.py           
        ├── 📄 datetime_utils.py      # Date/time manipulation utilities
        └── 📄 logger.py              # Logging configuration and utilities
```

## 🎯 Component Purposes

### **Root Level Files**
- **`alembic.ini`**: Database migration configuration for version control of database schema changes
- **`README.md`**: Project documentation, setup instructions, and API endpoints description
- **`run_main_service.py`**: Service launcher with options for virtual environments and colored output

### **`alembic/` - Database Migration System**
- **`env.py`**: Alembic environment setup connecting to shared database configuration
- **`script.py.mako`**: Template for generating new migration files
- **`versions/`**: Contains all database migration files (auto-generated)

### **`services/main-service/` - Primary Microservice**
- **`main.py`**: FastAPI application entry point with lifespan management and logging
- **`.env`**: Environment-specific configuration (database URLs, API keys, etc.)
- **`requirements.txt`**: Service-specific Python dependencies
- **`app/`**: Clean architecture implementation:
  - **`api/v1/`**: RESTful API endpoints organized by version
  - **`core/`**: Application configuration and FastAPI factory
  - **`models/`**: SQLAlchemy database models
  - **`repository/`**: Data access layer implementing repository pattern
  - **`schemas/`**: Pydantic models for request/response validation
  - **`services/`**: Business logic and service layer

### **`shared/` - Cross-Service Components**
- **`constants/`**: Global application constants and enumerations
- **`database/`**: Centralized database management:
  - **`dbContext.py`**: Database connection factory and session management
  - **`models.py`**: Shared database models used across services
  - **`schemas.py`**: Common Pydantic schemas
  - **`services.py`**: Shared database operations and queries
- **`utils/`**: Common utilities:
  - **`logger.py`**: Centralized logging configuration
  - **`datetime_utils.py`**: Date/time manipulation functions