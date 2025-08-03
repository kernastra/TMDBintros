#!/bin/bash

# TMDB Trailers Plugin - Local Installation Script
# This script automates the local installation process

set -e  # Exit on any error

echo "🎬 TMDB Trailers Plugin - Local Installation"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running as root (not recommended)
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root. This may cause permission issues."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Git
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install git first."
    exit 1
fi
print_status "Git found: $(git --version)"

# Check .NET
if ! command -v dotnet &> /dev/null; then
    print_error ".NET is not installed. Please install .NET 8.0 SDK first."
    echo "Visit: https://dotnet.microsoft.com/download/dotnet/8.0"
    exit 1
fi

DOTNET_VERSION=$(dotnet --version)
print_status ".NET found: $DOTNET_VERSION"

# Check if .NET version is 8.x
if [[ ! $DOTNET_VERSION =~ ^8\. ]]; then
    print_warning ".NET version $DOTNET_VERSION found. This plugin requires .NET 8.0+"
fi

# Check yt-dlp
if ! command -v yt-dlp &> /dev/null; then
    print_warning "yt-dlp not found. The plugin needs this to download videos."
    echo "Install with: sudo apt install yt-dlp (Linux) or winget install yt-dlp (Windows)"
    read -p "Continue without yt-dlp? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_status "yt-dlp found: $(yt-dlp --version)"
fi

echo ""

# Step 2: Build the plugin
echo "🔨 Building the plugin..."

if [ ! -f "TMDBintros.csproj" ]; then
    print_error "TMDBintros.csproj not found. Are you in the correct directory?"
    exit 1
fi

# Clean and restore
print_info "Cleaning previous builds..."
dotnet clean > /dev/null 2>&1 || true

print_info "Restoring dependencies..."
if ! dotnet restore > /dev/null 2>&1; then
    print_error "Failed to restore dependencies"
    exit 1
fi

# Build
print_info "Building release version..."
if ! dotnet build --configuration Release > /dev/null 2>&1; then
    print_error "Build failed. Run 'dotnet build --configuration Release' to see errors."
    exit 1
fi

# Check if DLL was created
DLL_PATH="bin/Release/net8.0/TMDBintros.dll"
if [ ! -f "$DLL_PATH" ]; then
    print_error "Build succeeded but DLL not found at $DLL_PATH"
    exit 1
fi

DLL_SIZE=$(ls -lh "$DLL_PATH" | awk '{print $5}')
print_status "Plugin built successfully! Size: $DLL_SIZE"

echo ""

# Step 3: Find Jellyfin plugins directory
echo "📂 Finding Jellyfin plugins directory..."

JELLYFIN_PLUGINS=""

# Common Jellyfin plugin paths
POSSIBLE_PATHS=(
    "/var/lib/jellyfin/plugins"
    "$HOME/.local/share/jellyfin/plugins"
    "/usr/local/var/jellyfin/plugins"
    "$HOME/Library/Application Support/jellyfin/plugins"
    "/opt/jellyfin/plugins"
)

# Check for existing Jellyfin plugins directory
for path in "${POSSIBLE_PATHS[@]}"; do
    if [ -d "$path" ]; then
        JELLYFIN_PLUGINS="$path"
        print_status "Found Jellyfin plugins directory: $JELLYFIN_PLUGINS"
        break
    fi
done

# If not found, prompt user
if [ -z "$JELLYFIN_PLUGINS" ]; then
    print_warning "Jellyfin plugins directory not found automatically."
    echo "Common locations:"
    echo "  - Linux (system): /var/lib/jellyfin/plugins"
    echo "  - Linux (user): ~/.local/share/jellyfin/plugins"
    echo "  - macOS: ~/Library/Application Support/jellyfin/plugins"
    echo "  - Docker: /config/plugins (in container)"
    echo ""
    read -p "Enter your Jellyfin plugins directory path: " JELLYFIN_PLUGINS
    
    if [ -z "$JELLYFIN_PLUGINS" ]; then
        print_error "No plugins directory specified"
        exit 1
    fi
fi

# Create plugins directory if it doesn't exist
if [ ! -d "$JELLYFIN_PLUGINS" ]; then
    print_info "Creating plugins directory: $JELLYFIN_PLUGINS"
    if ! mkdir -p "$JELLYFIN_PLUGINS" 2>/dev/null; then
        print_error "Cannot create directory: $JELLYFIN_PLUGINS"
        print_info "You may need to run: sudo mkdir -p '$JELLYFIN_PLUGINS'"
        exit 1
    fi
fi

echo ""

# Step 4: Install the plugin
echo "📦 Installing plugin..."

# Check if plugin already exists
if [ -f "$JELLYFIN_PLUGINS/TMDBintros.dll" ]; then
    print_warning "Plugin already exists in $JELLYFIN_PLUGINS"
    read -p "Overwrite existing plugin? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Installation cancelled"
        exit 0
    fi
fi

# Copy the plugin
if ! cp "$DLL_PATH" "$JELLYFIN_PLUGINS/" 2>/dev/null; then
    print_error "Cannot copy plugin. You may need sudo privileges."
    print_info "Try running: sudo cp '$DLL_PATH' '$JELLYFIN_PLUGINS/'"
    exit 1
fi

print_status "Plugin installed to: $JELLYFIN_PLUGINS/TMDBintros.dll"

# Set appropriate permissions
if command -v chown &> /dev/null; then
    # Try to set jellyfin user ownership (may fail if not root)
    chown jellyfin:jellyfin "$JELLYFIN_PLUGINS/TMDBintros.dll" 2>/dev/null || true
fi
chmod 644 "$JELLYFIN_PLUGINS/TMDBintros.dll" 2>/dev/null || true

echo ""

# Step 5: Restart Jellyfin
echo "🔄 Restarting Jellyfin..."

JELLYFIN_RESTARTED=false

# Try different restart methods
if command -v systemctl &> /dev/null; then
    if systemctl is-active --quiet jellyfin; then
        print_info "Restarting Jellyfin service..."
        if sudo systemctl restart jellyfin 2>/dev/null; then
            print_status "Jellyfin service restarted"
            JELLYFIN_RESTARTED=true
        fi
    elif systemctl --user is-active --quiet jellyfin 2>/dev/null; then
        print_info "Restarting user Jellyfin service..."
        if systemctl --user restart jellyfin 2>/dev/null; then
            print_status "Jellyfin user service restarted"
            JELLYFIN_RESTARTED=true
        fi
    fi
fi

# Check for Docker
if command -v docker &> /dev/null && docker ps --format "table {{.Names}}" | grep -q jellyfin; then
    print_info "Restarting Jellyfin Docker container..."
    if docker restart jellyfin 2>/dev/null; then
        print_status "Jellyfin Docker container restarted"
        JELLYFIN_RESTARTED=true
    fi
fi

if [ "$JELLYFIN_RESTARTED" = false ]; then
    print_warning "Could not automatically restart Jellyfin"
    print_info "Please restart Jellyfin manually:"
    echo "  - Systemd: sudo systemctl restart jellyfin"
    echo "  - Docker: docker restart jellyfin"
    echo "  - Windows: Restart Jellyfin Server service"
    echo "  - Manual: Stop and start Jellyfin application"
fi

echo ""

# Step 6: Final instructions
echo "🎉 Installation Complete!"
echo "======================="
echo ""
print_status "Plugin successfully installed!"
echo ""
echo "📋 Next Steps:"
echo "1. 🌐 Open Jellyfin Web Interface (usually http://localhost:8096)"
echo "2. 🔧 Go to Dashboard → Plugins → TMDB Trailers"
echo "3. 🔑 Enter your TMDB API key (get free key from themoviedb.org)"
echo "4. ⚙️  Configure plugin settings (quality, folder names, etc.)"
echo "5. 💾 Save configuration"
echo "6. 🎬 Go to Dashboard → Scheduled Tasks → 'Download Movie Trailers' → Run Now"
echo ""
echo "🔗 Important Links:"
echo "   • TMDB API Key: https://www.themoviedb.org/settings/api"
echo "   • Documentation: $(pwd)/README.md"
echo "   • Local Install Guide: $(pwd)/LOCAL_INSTALLATION.md"
echo ""

if [ "$JELLYFIN_RESTARTED" = false ]; then
    print_warning "Remember to restart Jellyfin before using the plugin!"
fi

# Show file locations
echo "📍 File Locations:"
echo "   • Plugin DLL: $JELLYFIN_PLUGINS/TMDBintros.dll"
echo "   • Source Code: $(pwd)"
echo "   • Build Output: $(pwd)/$DLL_PATH"
echo ""

print_status "Enjoy your automatically downloaded movie trailers! 🍿"
