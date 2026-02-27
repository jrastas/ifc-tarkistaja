# Makefile for IFC Compliance Checker
# Use with: make <target>

.PHONY: help setup-backend setup-frontend setup dev-backend dev-frontend test-backend test-frontend test build clean

# Default target
help:
	@echo "Available targets:"
	@echo "  setup-backend   - Set up Python virtual environment and install dependencies"
	@echo "  setup-frontend  - Install npm dependencies"
	@echo "  setup           - Set up both backend and frontend"
	@echo "  dev-backend     - Run backend development server"
	@echo "  dev-frontend    - Run frontend development server"
	@echo "  test-backend    - Run backend tests"
	@echo "  test-frontend   - Run frontend tests"
	@echo "  test            - Run all tests"
	@echo "  build           - Build frontend for production"
	@echo "  docker-up       - Start all services with Docker"
	@echo "  docker-down     - Stop all Docker services"
	@echo "  clean           - Remove generated files"

# Backend setup
setup-backend:
	cd backend && python -m venv venv
	cd backend && . venv/bin/activate && pip install -r requirements.txt
	cd backend && . venv/bin/activate && pip install -r requirements-dev.txt
	@echo "Backend setup complete. Activate with: source backend/venv/bin/activate"

# Frontend setup
setup-frontend:
	cd frontend && npm install
	@echo "Frontend setup complete."

# Full setup
setup: setup-backend setup-frontend
	@echo "Full setup complete."

# Development servers
dev-backend:
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# Testing
test-backend:
	cd backend && . venv/bin/activate && pytest -v

test-backend-cov:
	cd backend && . venv/bin/activate && pytest --cov=app --cov-report=html

test-frontend:
	cd frontend && npm test

test-frontend-cov:
	cd frontend && npm test -- --coverage

test: test-backend test-frontend

# Build
build:
	cd frontend && npm run build

# Docker
docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

# Cleanup
clean:
	rm -rf backend/venv
	rm -rf backend/.pytest_cache
	rm -rf backend/htmlcov
	rm -rf backend/__pycache__
	rm -rf backend/app/__pycache__
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	rm -rf frontend/coverage
	@echo "Cleaned up generated files."

# Initialize project structure
init:
	@echo "Creating project structure..."
	@echo "Creating backend directories..."
	mkdir -p backend/app/api
	mkdir -p backend/app/services
	mkdir -p backend/app/schemas
	mkdir -p backend/app/mappings
	mkdir -p backend/app/i18n
	mkdir -p backend/tests/fixtures
	@echo "Creating frontend directories..."
	mkdir -p frontend/src/components
	mkdir -p frontend/src/hooks
	mkdir -p frontend/src/services
	mkdir -p frontend/src/store
	mkdir -p frontend/src/types
	mkdir -p frontend/src/i18n
	@echo "Creating docs directory..."
	mkdir -p docs/phases
	@echo "Creating Python __init__.py files..."
	touch backend/app/__init__.py
	touch backend/app/api/__init__.py
	touch backend/app/services/__init__.py
	touch backend/app/schemas/__init__.py
	@echo "Copying phase documents to docs/phases/..."
	@if [ -f PHASE-1-FOUNDATION.md ]; then cp PHASE-1-FOUNDATION.md docs/phases/; fi
	@if [ -f PHASE-2-BASIC-FUNCTIONALITY.md ]; then cp PHASE-2-BASIC-FUNCTIONALITY.md docs/phases/; fi
	@if [ -f PHASE-3-ADVANCED-FUNCTIONALITY.md ]; then cp PHASE-3-ADVANCED-FUNCTIONALITY.md docs/phases/; fi
	@if [ -f PHASE-4-TESTING.md ]; then cp PHASE-4-TESTING.md docs/phases/; fi
	@echo "Project structure created successfully."
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run 'make setup-backend' after creating requirements.txt"
	@echo "  2. Run 'make setup-frontend' after creating package.json"
