# Makefile for TMDB Trailer Downloader Docker operations
# Provides convenient shortcuts for common Docker tasks

.PHONY: help build up down logs clean test scan monitor schedule

# Default target
help: ## Show this help message
	@echo "TMDB Trailer Downloader - Docker Operations"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Build the Docker image
build: ## Build the Docker image
	@echo "Building TMDB Trailer Downloader image..."
	docker-compose build

# Build without cache
build-clean: ## Build the Docker image without cache
	@echo "Building TMDB Trailer Downloader image (no cache)..."
	docker-compose build --no-cache

# Test configuration
test: ## Test configuration and connectivity
	@echo "Testing configuration..."
	docker-compose --profile scanner run --rm tmdb-scanner python3 enhanced_downloader.py --test-config

# One-time scan
scan: ## Run one-time movie scan
	@echo "Running one-time scan..."
	docker-compose --profile scanner up tmdb-scanner

# Start real-time monitoring
monitor: ## Start real-time file system monitoring
	@echo "Starting real-time monitoring..."
	docker-compose --profile monitor up -d tmdb-monitor
	@echo "Monitoring started. View logs with: make logs-monitor"

# Start scheduled scanning
schedule: ## Start scheduled scanning service
	@echo "Starting scheduled scanning..."
	docker-compose --profile scheduler up -d tmdb-scheduler
	@echo "Scheduler started. View logs with: make logs-schedule"

# Start all services
up: ## Start all services
	@echo "Starting all services..."
	docker-compose --profile all up -d
	@echo "All services started. View status with: make status"

# Start web dashboard
dashboard: ## Start web dashboard
	@echo "Starting web dashboard..."
	docker-compose --profile dashboard up -d tmdb-dashboard
	@echo "Dashboard started at http://localhost:${DASHBOARD_PORT:-8080}"
	@echo "View logs with: make logs-dashboard"

# Stop all services
down: ## Stop all services
	@echo "Stopping all services..."
	docker-compose --profile all down

# Show service status
status: ## Show service status
	@echo "Service status:"
	docker-compose ps

# View logs for monitoring service
logs-monitor: ## View real-time monitoring logs
	docker-compose logs -f tmdb-monitor

# View logs for scheduler service
logs-schedule: ## View scheduled scanning logs
	docker-compose logs -f tmdb-scheduler

# View logs for scanner service
logs-scan: ## View one-time scanner logs
	docker-compose logs tmdb-scanner

# View logs for dashboard service
logs-dashboard: ## View dashboard logs
	docker-compose logs -f tmdb-dashboard

# View all logs
logs: ## View logs for all services
	docker-compose logs -f

# Restart monitoring service
restart-monitor: ## Restart monitoring service
	@echo "Restarting monitoring service..."
	docker-compose --profile monitor restart tmdb-monitor

# Restart scheduler service
restart-schedule: ## Restart scheduler service
	@echo "Restarting scheduler service..."
	docker-compose --profile scheduler restart tmdb-scheduler

# Clean up containers and images
clean: ## Clean up stopped containers and unused images
	@echo "Cleaning up Docker resources..."
	docker-compose rm -f
	docker image prune -f

# Complete cleanup (WARNING: removes volumes)
clean-all: ## Complete cleanup including volumes (WARNING: DATA LOSS)
	@echo "WARNING: This will remove all data including logs and cache!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ]
	docker-compose --profile all down -v
	docker image prune -f
	sudo rm -rf ./logs ./cache

# Show environment configuration
env: ## Show current environment configuration
	@echo "Current environment configuration:"
	@if [ -f .env ]; then \
		echo "Environment file: .env"; \
		echo "Key variables:"; \
		grep -E "^(TMDB_API_KEY|HOST_MOVIES_PATH|NETWORK_|SCHEDULE_|LOG_)" .env | head -10; \
	else \
		echo "No .env file found. Copy .env.docker to .env and configure."; \
	fi

# Show version information
version: ## Show version information
	@echo "TMDB Trailer Downloader Version Information:"
	@python3 version.py

# Update and rebuild
update: ## Update base images and rebuild
	@echo "Updating base images..."
	docker pull python:3.11-slim
	@echo "Rebuilding image..."
	docker-compose build --no-cache

# Setup initial configuration
setup: ## Setup initial configuration files
	@echo "Setting up initial configuration..."
	@if [ ! -f .env ]; then \
		cp .env.docker .env; \
		echo "Created .env file from .env.docker template"; \
		echo "Please edit .env with your settings:"; \
		echo "  - TMDB_API_KEY=your_api_key_here"; \
		echo "  - HOST_MOVIES_PATH=/path/to/your/jellyfin/movies"; \
	else \
		echo ".env file already exists"; \
	fi
	@mkdir -p logs cache
	@echo "Created logs and cache directories"

# Development mode (with override)
dev: ## Start in development mode
	@echo "Starting in development mode..."
	@if [ -f docker-compose.dev.yml ]; then \
		docker-compose -f docker-compose.yml -f docker-compose.dev.yml --profile monitor up -d; \
	else \
		echo "Development override not found, using standard configuration"; \
		docker-compose --profile monitor up -d; \
	fi

# Production deployment
prod: ## Deploy in production mode
	@echo "Deploying in production mode..."
	@if [ -f docker-compose.prod.yml ]; then \
		docker-compose -f docker-compose.yml -f docker-compose.prod.yml --profile all up -d; \
	else \
		echo "Production override not found, using standard configuration"; \
		docker-compose --profile all up -d; \
	fi

# Backup logs and cache
backup: ## Backup logs and cache
	@echo "Creating backup..."
	@mkdir -p backups
	@tar -czf backups/tmdb-backup-$(shell date +%Y%m%d-%H%M%S).tar.gz logs cache .env
	@echo "Backup created in backups/ directory"

# Show disk usage
disk: ## Show disk usage of Docker resources
	@echo "Docker disk usage:"
	docker system df
	@echo ""
	@echo "Local directory usage:"
	du -sh . logs cache 2>/dev/null || true
