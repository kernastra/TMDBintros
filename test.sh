#!/bin/bash

# TMDB Trailer Downloader - Testing Setup
# This script helps you quickly test the application without needing a .env file

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}TMDB Trailer Downloader - Testing Mode${NC}"
echo "======================================"

# Check if TMDB API key is provided
if [ "$#" -eq 0 ]; then
    echo -e "${YELLOW}Usage: $0 <TMDB_API_KEY> [command]${NC}"
    echo ""
    echo "Available commands:"
    echo "  up       - Start all services (default)"
    echo "  down     - Stop all services"
    echo "  logs     - Show logs"
    echo "  dashboard - Start only dashboard"
    echo "  scan     - Run one-time library scan"
    echo "  upcoming - Run upcoming movies scan"
    echo ""
    echo "Example:"
    echo "  $0 abc123def456 up"
    echo "  $0 abc123def456 dashboard"
    exit 1
fi

TMDB_API_KEY="$1"
COMMAND="${2:-up}"

# Validate API key format (basic check)
if [[ ! "$TMDB_API_KEY" =~ ^[a-zA-Z0-9]{32}$ ]]; then
    echo -e "${YELLOW}Warning: API key doesn't match expected format (32 alphanumeric characters)${NC}"
    echo "Continuing anyway in case format has changed..."
fi

# Set the API key in the docker-compose file temporarily
export TMDB_API_KEY_TEMP="$TMDB_API_KEY"

# Create a temporary docker-compose file with the API key
sed "s/your_tmdb_api_key_here/$TMDB_API_KEY/g" docker-compose.testing.yml > docker-compose.testing.tmp.yml

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running or not accessible${NC}"
    echo ""
    echo "Please start Docker and try again:"
    echo "  - On Windows/Mac: Start Docker Desktop"
    echo "  - On Linux: sudo systemctl start docker"
    echo "  - In WSL: Make sure Docker Desktop is running on Windows"
    echo ""
    echo "To validate configuration without Docker:"
    echo "  ./validate.sh $TMDB_API_KEY"
    rm -f docker-compose.testing.tmp.yml
    exit 1
fi

case "$COMMAND" in
    "up")
        echo -e "${GREEN}Starting TMDB Trailer Downloader in testing mode...${NC}"
        echo "API Key: ${TMDB_API_KEY:0:8}..."
        echo ""
        docker-compose -f docker-compose.testing.tmp.yml up -d
        echo ""
        echo -e "${GREEN}Services started!${NC}"
        echo "Dashboard: http://localhost:8085"
        echo "Logs: docker-compose -f docker-compose.testing.tmp.yml logs -f"
        ;;
    "down")
        echo -e "${YELLOW}Stopping services...${NC}"
        docker-compose -f docker-compose.testing.tmp.yml down
        echo -e "${GREEN}Services stopped!${NC}"
        ;;
    "logs")
        docker-compose -f docker-compose.testing.tmp.yml logs -f
        ;;
    "dashboard")
        echo -e "${GREEN}Starting dashboard only...${NC}"
        docker-compose -f docker-compose.testing.tmp.yml up -d tmdb-dashboard
        echo "Dashboard: http://localhost:8085"
        ;;
    "scan")
        echo -e "${GREEN}Running library scan...${NC}"
        docker-compose -f docker-compose.testing.tmp.yml run --rm tmdb-trailer-downloader python main.py
        ;;
    "upcoming")
        echo -e "${GREEN}Running upcoming movies scan...${NC}"
        docker-compose -f docker-compose.testing.tmp.yml run --rm tmdb-trailer-downloader python -m tmdb_upcoming
        ;;
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        echo "Available commands: up, down, logs, dashboard, scan, upcoming"
        exit 1
        ;;
esac

# Cleanup function
cleanup() {
    if [ -f "docker-compose.testing.tmp.yml" ]; then
        rm -f docker-compose.testing.tmp.yml
    fi
}

# Set trap to cleanup on exit
trap cleanup EXIT
