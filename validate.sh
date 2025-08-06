#!/bin/bash

# TMDB Trailer Downloader - Configuration Validator
# This script validates the docker-compose configuration without requiring Docker to be running

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}TMDB Trailer Downloader - Configuration Validator${NC}"
echo "=================================================="

# Check if TMDB API key is provided
if [ "$#" -eq 0 ]; then
    echo -e "${YELLOW}Usage: $0 <TMDB_API_KEY>${NC}"
    echo ""
    echo "This script validates the testing configuration syntax."
    echo ""
    echo "Example:"
    echo "  $0 abc123def456"
    exit 1
fi

TMDB_API_KEY="$1"

# Validate API key format (basic check)
if [[ ! "$TMDB_API_KEY" =~ ^[a-zA-Z0-9]{32}$ ]]; then
    echo -e "${YELLOW}Warning: API key doesn't match expected format (32 alphanumeric characters)${NC}"
    echo "Expected format: 32 alphanumeric characters"
    echo "Your key length: ${#TMDB_API_KEY}"
    echo "Continuing validation anyway..."
    echo ""
fi

# Create a temporary docker-compose file with the API key
echo -e "${BLUE}Creating temporary configuration...${NC}"
sed "s/your_tmdb_api_key_here/$TMDB_API_KEY/g" docker-compose.testing.yml > docker-compose.testing.tmp.yml

# Validate docker-compose syntax
echo -e "${BLUE}Validating docker-compose syntax...${NC}"
if command -v docker-compose >/dev/null 2>&1; then
    if docker-compose -f docker-compose.testing.tmp.yml config >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Docker Compose syntax is valid${NC}"
    else
        echo -e "${RED}✗ Docker Compose syntax validation failed:${NC}"
        docker-compose -f docker-compose.testing.tmp.yml config
        rm -f docker-compose.testing.tmp.yml
        exit 1
    fi
else
    echo -e "${YELLOW}⚠ docker-compose not found, skipping syntax validation${NC}"
fi

# Validate environment variables
echo -e "${BLUE}Validating environment variables...${NC}"

# Check for required variables
REQUIRED_VARS=(
    "TMDB_API_KEY"
    "JELLYFIN_MOVIES_PATH" 
    "UPCOMING_ENABLED"
    "DASHBOARD_ENABLED"
    "DASHBOARD_PORT"
)

CONFIG_VALID=true
for var in "${REQUIRED_VARS[@]}"; do
    if grep -q "${var}:" docker-compose.testing.tmp.yml; then
        echo -e "${GREEN}✓ $var is configured${NC}"
    else
        echo -e "${RED}✗ $var is missing${NC}"
        CONFIG_VALID=false
    fi
done

# Check API key substitution
if grep -q "your_tmdb_api_key_here" docker-compose.testing.tmp.yml; then
    echo -e "${RED}✗ API key substitution failed${NC}"
    CONFIG_VALID=false
else
    echo -e "${GREEN}✓ API key properly substituted${NC}"
fi

# Validate port configuration
if grep -q "8085:8085" docker-compose.testing.tmp.yml; then
    echo -e "${GREEN}✓ Dashboard port 8085 configured${NC}"
else
    echo -e "${RED}✗ Dashboard port configuration missing${NC}"
    CONFIG_VALID=false
fi

# Check for common issues
echo -e "${BLUE}Checking for common configuration issues...${NC}"

# Check regex pattern escaping
if grep -q "MOVIE_FOLDER_PATTERN" docker-compose.testing.tmp.yml; then
    PATTERN=$(grep "MOVIE_FOLDER_PATTERN" docker-compose.testing.tmp.yml | cut -d'"' -f4)
    echo -e "${GREEN}✓ Movie folder pattern: $PATTERN${NC}"
else
    echo -e "${YELLOW}⚠ Movie folder pattern not found${NC}"
fi

# Check volume mounts
if grep -q "./movies:/app/movies" docker-compose.testing.tmp.yml && grep -q "./logs:/app/logs" docker-compose.testing.tmp.yml; then
    echo -e "${GREEN}✓ Volume mounts configured${NC}"
else
    echo -e "${RED}✗ Volume mounts missing or incorrect${NC}"
    CONFIG_VALID=false
fi

# Summary
echo ""
echo "=================================================="
if [ "$CONFIG_VALID" = true ]; then
    echo -e "${GREEN}✓ Configuration validation passed!${NC}"
    echo ""
    echo "Your configuration is ready for testing."
    echo "To run when Docker is available:"
    echo "  ./test.sh $TMDB_API_KEY dashboard"
    echo ""
    echo "Dashboard will be available at: http://localhost:8085"
else
    echo -e "${RED}✗ Configuration validation failed!${NC}"
    echo ""
    echo "Please check the errors above and fix the configuration."
fi

# Cleanup
rm -f docker-compose.testing.tmp.yml
