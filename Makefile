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

# Download upcoming movie trailers
upcoming: ## Download trailers for upcoming movies (3-6 months ahead)
	@echo "Downloading trailers for upcoming movies..."
	docker-compose --profile upcoming run --rm tmdb-upcoming
	@echo "Upcoming trailers download completed"

# List upcoming movies with trailers
upcoming-list: ## List upcoming movies with downloaded trailers
	@echo "Listing upcoming movies..."
	docker-compose --profile upcoming run --rm tmdb-upcoming python3 tmdb_upcoming.py --list

# Clean up old upcoming movies
upcoming-cleanup: ## Clean up old upcoming movies past their release date
	@echo "Cleaning up old upcoming movies..."
	docker-compose --profile upcoming run --rm tmdb-upcoming python3 tmdb_upcoming.py --cleanup

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

# Create release archive
release: ## Create release archive for distribution
	@echo "Creating release archive..."
	@mkdir -p backups logs cache
	@tar -czf backups/tmdb-trailer-downloader-v3.0.0.tar.gz \
		--exclude='.git' \
		--exclude='backups' \
		--exclude='logs/*' \
		--exclude='cache/*' \
		--exclude='.env' \
		--exclude='*.pyc' \
		--exclude='__pycache__' \
		.
	@echo "Release archive created: backups/tmdb-trailer-downloader-v3.0.0.tar.gz"
	@echo "Archive size: $$(du -h backups/tmdb-trailer-downloader-v3.0.0.tar.gz | cut -f1)"

# Show disk usage
disk: ## Show disk usage of Docker resources
	@echo "Docker disk usage:"
	docker system df
	@echo ""
	@echo "Local directory usage:"
	du -sh . logs cache 2>/dev/null || true

# Create GitHub release
github-release: ## Create GitHub release for v3.0.0
	@echo "Creating GitHub release for v3.0.0..."
	@if ! git tag --list | grep -q "v3.0.0"; then \
		echo "Error: v3.0.0 tag not found. Please create the tag first."; \
		exit 1; \
	fi
	@if [ ! -f RELEASE_NOTES_v3.0.0.md ]; then \
		echo "Error: RELEASE_NOTES_v3.0.0.md not found."; \
		exit 1; \
	fi
	@if [ ! -f backups/tmdb-trailer-downloader-v3.0.0.tar.gz ]; then \
		echo "Creating release archive..."; \
		make release; \
	fi
	@echo "Creating GitHub release..."
	gh release create v3.0.0 \
		--title "🚀 TMDB Trailer Downloader v3.0.0 - Complete Container Transformation" \
		--notes-file RELEASE_NOTES_v3.0.0.md \
		backups/tmdb-trailer-downloader-v3.0.0.tar.gz \
		--latest
	@echo "✅ GitHub release v3.0.0 created successfully!"
	@echo "🔗 View at: https://github.com/kernastra/TMDBintros/releases/tag/v3.0.0"

# Push everything and create release
deploy-release: ## Push all changes and create GitHub release
	@echo "Deploying complete v3.0.0 release..."
	@echo "1. Checking git status..."
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "Uncommitted changes found. Committing..."; \
		git add .; \
		git commit -m "🔧 Final v3.0.0 preparations"; \
	fi
	@echo "2. Pushing to GitHub..."
	git push origin main
	git push origin v3.0.0 2>/dev/null || echo "Tag already pushed"
	@echo "3. Creating GitHub release..."
	make github-release
	@echo "🎉 Complete v3.0.0 deployment finished!"
