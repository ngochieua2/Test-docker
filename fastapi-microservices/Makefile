# Cross-platform Makefile for FastAPI Microservices
# Works on Windows (with make), Mac, and Ubuntu

.DEFAULT_GOAL := help
PYTHON := python3

## help: Show this help message
help:
	@echo "FastAPI Microservices - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install all dependencies"
	@echo "  make install-dev      Install with virtual environment"
	@echo "  make migrate          Run database migrations"
	@echo ""
	@echo "Run Services:"
	@echo "  make hello            Start Hello Service (port 8001)"
	@echo "  make todo             Start Todo Service (port 8002)"
	@echo "  make hello-dev        Start Hello Service with venv"
	@echo "  make todo-dev         Start Todo Service with venv"
	@echo ""
	@echo "Database:"
	@echo "  make create-migration Create new database migration"
	@echo "  make migrate          Apply database migrations"
	@echo ""
	@echo "Development:"
	@echo "  make clean            Clean up temporary files"
	@echo "  make docs             Open API documentation"

## install: Install all dependencies
install:
	pip install -r requirements.txt

## install-dev: Install dependencies in virtual environment
install-dev:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt || venv\Scripts\pip install -r requirements.txt

## hello: Start Hello Service
hello:
	$(PYTHON) run_hello_service.py

## todo: Start Todo Service  
todo:
	$(PYTHON) run_todo_service.py

## hello-dev: Start Hello Service with virtual environment
hello-dev:
	$(PYTHON) run_hello_service.py --venv

## todo-dev: Start Todo Service with virtual environment
todo-dev:
	$(PYTHON) run_todo_service.py --venv

## migrate: Run database migrations
migrate:
	alembic upgrade head

## create-migration: Create new database migration
create-migration:
	alembic revision --autogenerate -m "$(MSG)"

## docs: Open API documentation
docs:
	@echo "Opening API documentation..."
	@echo "Hello Service: http://localhost:8001/docs"
	@echo "Todo Service: http://localhost:8002/docs"

## clean: Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

.PHONY: help install install-dev hello todo hello-dev todo-dev migrate create-migration docs clean