#!/bin/bash

# Quick test script to verify local installation
# Run this after installing the plugin to check everything is working

echo "🧪 TMDB Trailers Plugin - Installation Test"
echo "==========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_pass() {
    echo -e "✅ ${GREEN}$1${NC}"
}

print_fail() {
    echo -e "❌ ${RED}$1${NC}"
}

print_warn() {
    echo -e "⚠️  ${YELLOW}$1${NC}"
}

ERRORS=0

# Test 1: Check if DLL exists in common Jellyfin locations
echo "🔍 Checking plugin installation..."

FOUND_PLUGIN=false
PLUGIN_PATHS=(
    "/var/lib/jellyfin/plugins/TMDBintros.dll"
    "$HOME/.local/share/jellyfin/plugins/TMDBintros.dll"
    "/usr/local/var/jellyfin/plugins/TMDBintros.dll"
    "$HOME/Library/Application Support/jellyfin/plugins/TMDBintros.dll"
)

for path in "${PLUGIN_PATHS[@]}"; do
    if [ -f "$path" ]; then
        print_pass "Plugin found at: $path"
        FOUND_PLUGIN=true
        
        # Check file size
        SIZE=$(ls -lh "$path" | awk '{print $5}')
        echo "   File size: $SIZE"
        
        # Check permissions
        PERMS=$(ls -l "$path" | awk '{print $1}')
        echo "   Permissions: $PERMS"
        break
    fi
done

if [ "$FOUND_PLUGIN" = false ]; then
    print_fail "Plugin DLL not found in common locations"
    echo "   Checked:"
    for path in "${PLUGIN_PATHS[@]}"; do
        echo "   - $path"
    done
    ERRORS=$((ERRORS + 1))
fi

echo ""

# Test 2: Check prerequisites
echo "🔧 Checking prerequisites..."

# Check .NET
if command -v dotnet &> /dev/null; then
    DOTNET_VERSION=$(dotnet --version)
    print_pass ".NET installed: $DOTNET_VERSION"
else
    print_fail ".NET not found"
    ERRORS=$((ERRORS + 1))
fi

# Check yt-dlp
if command -v yt-dlp &> /dev/null; then
    YTDLP_VERSION=$(yt-dlp --version)
    print_pass "yt-dlp installed: $YTDLP_VERSION"
else
    print_warn "yt-dlp not found (required for downloading videos)"
    echo "   Install with: sudo apt install yt-dlp"
fi

echo ""

# Test 3: Check if Jellyfin is running
echo "🖥️  Checking Jellyfin status..."

JELLYFIN_RUNNING=false

# Check systemd service
if command -v systemctl &> /dev/null; then
    if systemctl is-active --quiet jellyfin 2>/dev/null; then
        print_pass "Jellyfin service is running (systemd)"
        JELLYFIN_RUNNING=true
    elif systemctl --user is-active --quiet jellyfin 2>/dev/null; then
        print_pass "Jellyfin user service is running (systemd)"
        JELLYFIN_RUNNING=true
    fi
fi

# Check Docker
if command -v docker &> /dev/null; then
    if docker ps --format "table {{.Names}}" 2>/dev/null | grep -q jellyfin; then
        print_pass "Jellyfin Docker container is running"
        JELLYFIN_RUNNING=true
    fi
fi

# Check if Jellyfin web interface is accessible
if command -v curl &> /dev/null; then
    if curl -s --max-time 5 http://localhost:8096 &>/dev/null; then
        print_pass "Jellyfin web interface accessible at http://localhost:8096"
        JELLYFIN_RUNNING=true
    fi
fi

if [ "$JELLYFIN_RUNNING" = false ]; then
    print_warn "Jellyfin does not appear to be running"
    echo "   • Check if Jellyfin is started"
    echo "   • Try: sudo systemctl start jellyfin"
    echo "   • Or: docker start jellyfin"
fi

echo ""

# Test 4: Test yt-dlp functionality
echo "🎥 Testing yt-dlp functionality..."

if command -v yt-dlp &> /dev/null; then
    # Test with a very short video and just get info (no download)
    TEST_URL="https://www.youtube.com/watch?v=jNQXAC9IVRw"  # Short "Me at the zoo" video
    
    if yt-dlp --quiet --no-download --print "%(title)s" "$TEST_URL" &>/dev/null; then
        print_pass "yt-dlp can access YouTube"
    else
        print_warn "yt-dlp cannot access YouTube (may be network/region issue)"
    fi
else
    print_warn "yt-dlp not available for testing"
fi

echo ""

# Test 5: Check TMDB API accessibility
echo "🌐 Testing TMDB API accessibility..."

if command -v curl &> /dev/null; then
    # Test TMDB API without API key (should get auth error, proving API is accessible)
    if curl -s --max-time 10 "https://api.themoviedb.org/3/search/movie?query=test" | grep -q "api_key"; then
        print_pass "TMDB API is accessible"
    else
        print_warn "TMDB API may not be accessible (network issue?)"
    fi
else
    print_warn "curl not available for testing TMDB API"
fi

echo ""

# Summary
echo "📋 Test Summary"
echo "==============="

if [ $ERRORS -eq 0 ]; then
    print_pass "All critical tests passed!"
    echo ""
    echo "🎉 Your installation looks good! Next steps:"
    echo "1. Open Jellyfin web interface: http://localhost:8096"
    echo "2. Go to Dashboard → Plugins → TMDB Trailers"
    echo "3. Configure with your TMDB API key"
    echo "4. Run 'Download Movie Trailers' scheduled task"
    echo ""
else
    print_fail "$ERRORS critical issue(s) found"
    echo ""
    echo "🔧 Please fix the issues above before using the plugin"
    echo ""
fi

# Additional helpful information
echo "💡 Helpful Commands:"
echo "   • Check Jellyfin logs: sudo journalctl -u jellyfin -f"
echo "   • Restart Jellyfin: sudo systemctl restart jellyfin"
echo "   • Plugin location: find /var/lib/jellyfin -name 'TMDBintros.dll'"
echo "   • Test yt-dlp: yt-dlp --version"
echo ""

echo "📚 Documentation:"
echo "   • Local Installation: $(pwd)/LOCAL_INSTALLATION.md"
echo "   • Main README: $(pwd)/README.md"
echo "   • Plugin Submission: $(pwd)/PLUGIN_SUBMISSION.md"
