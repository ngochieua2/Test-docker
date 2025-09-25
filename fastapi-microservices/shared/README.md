# Shared Components Documentation

This folder contains reusable components that can be shared across all microservices in the FastAPI project.

## 📁 Folder Structure

```
shared/
├── __init__.py                    # Package initialization
├── README.md                      # This documentation
├── core/                         # Core shared components
│   ├── __init__.py
│   ├── config.py                 # Base configuration classes
│   └── schemas.py               # Common response schemas
├── exceptions/                   # Exception handling
│   ├── __init__.py
│   ├── custom.py                # Custom exception classes
│   └── handlers.py              # Exception handlers for FastAPI
├── middleware/                   # Reusable middleware
│   ├── __init__.py
│   ├── logging.py               # Request logging middleware
│   └── security.py             # Security middleware (rate limiting, headers)
├── utils/                       # Utility functions
│   ├── __init__.py
│   ├── datetime_utils.py        # Date/time utilities
│   ├── string_utils.py          # String manipulation utilities
│   └── validators.py            # Validation utilities
├── auth/                        # Authentication & authorization (placeholder)
│   ├── __init__.py
│   └── manager.py               # Auth management utilities
└── legacy/                      # Legacy components (deprecated)
    ├── __init__.py
    ├── database.py              # Legacy database setup
    ├── models.py                # Legacy models
    ├── schemas.py               # Legacy schemas
    └── services.py              # Legacy services
```

## 🎯 Usage Examples

### Core Configuration

```python
# In your service's config.py
from shared.core.config import BaseAppSettings

class ServiceSettings(BaseAppSettings):
    APP_NAME: str = "My Service"
    PORT: int = 8001
    # Add service-specific settings
```

### Exception Handling

```python
# In your service's app.py
from shared.exceptions.handlers import register_exception_handlers
from shared.exceptions.custom import ResourceNotFoundException

app = FastAPI()
register_exception_handlers(app)

# In your service code
if not resource:
    raise ResourceNotFoundException("Resource not found", details={"id": resource_id})
```

### Middleware

```python
# In your service's app.py
from shared.middleware.logging import RequestLoggingMiddleware
from shared.middleware.security import RateLimitMiddleware, SecurityHeadersMiddleware

app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, calls=100, period=60)
app.add_middleware(SecurityHeadersMiddleware)
```

### Utilities

```python
# Using datetime utilities
from shared.utils.datetime_utils import utc_now, time_ago

created_at = utc_now()
time_since = time_ago(created_at)

# Using string utilities
from shared.utils.string_utils import slugify, generate_random_string

slug = slugify("My Blog Post Title")  # "my-blog-post-title"
token = generate_random_string(32)

# Using validators
from shared.utils.validators import validate_email_format, validate_required_fields

email_result = validate_email_format("user@example.com")
if not email_result:
    print(email_result.errors)
```

### Response Schemas

```python
# In your service's endpoints
from shared.core.schemas import SuccessResponse, ErrorResponse, PaginatedResponse

@router.get("/items", response_model=PaginatedResponse)
async def get_items():
    return PaginatedResponse(
        items=[...],
        total=100,
        page=1,
        pages=10,
        per_page=10
    )
```

## 🔧 Integration Guidelines

### Adding New Shared Components

1. **Choose the right folder**: Place components in the most appropriate subfolder
2. **Follow naming conventions**: Use descriptive names and consistent patterns
3. **Add documentation**: Include docstrings and examples
4. **Write tests**: Create corresponding test files
5. **Update this README**: Document new components

### Service Integration

To use shared components in your service:

1. **Import what you need**: Only import specific components to avoid dependencies
2. **Extend base classes**: Use inheritance to customize shared components
3. **Configure appropriately**: Set up middleware and exception handlers in your app factory
4. **Test integration**: Ensure shared components work correctly with your service

## 📋 Best Practices

### Configuration
- Extend `BaseAppSettings` for consistent configuration patterns
- Use environment variables for service-specific settings
- Keep sensitive data in environment variables, not code

### Exception Handling
- Use custom exceptions for business logic errors
- Register global exception handlers for consistent error responses
- Log exceptions appropriately for debugging

### Middleware
- Order middleware carefully (logging should be early, security middleware before business logic)
- Configure rate limiting based on service requirements
- Add custom middleware for service-specific needs

### Utilities
- Use validation utilities for consistent data validation
- Prefer shared datetime utilities for timezone handling
- Use string utilities for consistent text processing

## 🚫 Legacy Components

The `legacy/` folder contains deprecated components from the original shared implementation. These are kept for:

- **Backward compatibility**: Support for existing migrations and old code
- **Reference**: Understanding the evolution of the codebase
- **Migration assistance**: Helping transition to new patterns

**Do not use legacy components in new code.** They will be removed in future versions.

## 🔄 Migration from Legacy

If you're using legacy shared components:

1. **Identify usage**: Find where legacy components are imported
2. **Replace with new patterns**: Use the new organized structure
3. **Update imports**: Change import paths to new locations
4. **Test thoroughly**: Ensure functionality remains the same
5. **Remove legacy dependencies**: Clean up old imports

## 📈 Future Enhancements

Planned additions to the shared components:

- **Caching utilities**: Redis integration and caching decorators
- **Database utilities**: Common database patterns and helpers
- **Monitoring**: Health check utilities and metrics collection
- **Communication**: Inter-service communication helpers
- **Testing**: Common test utilities and fixtures

## 🤝 Contributing

When adding new shared components:

1. Follow the established patterns and structure
2. Add comprehensive documentation and examples
3. Include unit tests for all new functionality
4. Update this README with usage instructions
5. Consider backward compatibility and migration paths

---

**Note**: This shared component structure is designed to promote code reuse while maintaining service independence. Each service should only import what it needs and can extend components as required.