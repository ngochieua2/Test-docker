# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create a non-root user for security first
RUN useradd --create-home --shell /bin/bash --uid 1001 app

# Copy requirements first for better layer caching
COPY services/main-service/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the main-service application code
COPY services/main-service /app/services/main-service

# Copy shared modules
COPY shared /app/shared

# Copy alembic configuration if present
COPY alembic* /app/

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the port
EXPOSE 8001

# Health check with proper URL
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Command to run the application
CMD ["python", "services/main-service/main.py"]