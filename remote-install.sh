#!/bin/bash

# TMDB Trailers Plugin - Remote Installation Script
# Usage: ./remote-install.sh [jellyfin-plugins-directory]

set -e

echo "🎬 TMDB Trailers Plugin - Remote Installation"
echo "============================================="

# Default plugin directories to try
PLUGIN_DIRS=(
    "/var/lib/jellyfin/plugins"
    "/usr/share/jellyfin/plugins" 
    "/etc/jellyfin/plugins"
    "/opt/jellyfin/plugins"
    "/config/plugins"  # Docker
    "$HOME/.local/share/jellyfin/plugins"
)

# Custom directory from command line
if [ "$1" ]; then
    PLUGIN_DIRS=("$1")
fi

# Find TMDBintros.dll
DLL_FILE=""
if [ -f "TMDBintros.dll" ]; then
    DLL_FILE="TMDBintros.dll"
elif [ -f "/tmp/TMDBintros.dll" ]; then
    DLL_FILE="/tmp/TMDBintros.dll"
else
    echo "❌ Error: TMDBintros.dll not found in current directory or /tmp"
    echo "Please copy the DLL file to this location first:"
    echo "   scp TMDBintros.dll user@server:/tmp/"
    exit 1
fi

echo "📁 Found plugin DLL: $DLL_FILE"

# Find Jellyfin plugins directory
JELLYFIN_PLUGINS_DIR=""
for dir in "${PLUGIN_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        JELLYFIN_PLUGINS_DIR="$dir"
        echo "✅ Found Jellyfin plugins directory: $dir"
        break
    fi
done

if [ -z "$JELLYFIN_PLUGINS_DIR" ]; then
    echo "❌ Error: Could not find Jellyfin plugins directory"
    echo "Common locations:"
    for dir in "${PLUGIN_DIRS[@]}"; do
        echo "   $dir"
    done
    echo ""
    echo "Please specify the correct path:"
    echo "   ./remote-install.sh /path/to/jellyfin/plugins"
    exit 1
fi

# Create plugins directory if it doesn't exist
if [ ! -d "$JELLYFIN_PLUGINS_DIR" ]; then
    echo "📁 Creating plugins directory: $JELLYFIN_PLUGINS_DIR"
    sudo mkdir -p "$JELLYFIN_PLUGINS_DIR"
fi

# Copy plugin
echo "📦 Installing plugin..."
if [ -w "$JELLYFIN_PLUGINS_DIR" ]; then
    cp "$DLL_FILE" "$JELLYFIN_PLUGINS_DIR/"
else
    sudo cp "$DLL_FILE" "$JELLYFIN_PLUGINS_DIR/"
fi

# Set permissions
echo "🔐 Setting permissions..."
sudo chown jellyfin:jellyfin "$JELLYFIN_PLUGINS_DIR/TMDBintros.dll" 2>/dev/null || true
sudo chmod 644 "$JELLYFIN_PLUGINS_DIR/TMDBintros.dll"

# Verify installation
if [ -f "$JELLYFIN_PLUGINS_DIR/TMDBintros.dll" ]; then
    echo "✅ Plugin installed successfully!"
    echo "📍 Location: $JELLYFIN_PLUGINS_DIR/TMDBintros.dll"
    echo "📊 Size: $(du -h "$JELLYFIN_PLUGINS_DIR/TMDBintros.dll" | cut -f1)"
else
    echo "❌ Installation failed - plugin file not found"
    exit 1
fi

echo ""
echo "🔄 Next Steps:"
echo "1. Restart Jellyfin service:"
echo "   sudo systemctl restart jellyfin"
echo "   # or if using Docker:"
echo "   docker restart jellyfin"
echo ""
echo "2. Check Jellyfin web interface:"
echo "   Dashboard → Plugins → TMDB Trailers"
echo ""
echo "3. Configure the plugin:"
echo "   - Add your TMDB API key"
echo "   - Configure download settings"
echo ""
echo "4. Install yt-dlp if not already installed:"
echo "   sudo apt install yt-dlp"
echo ""
echo "🎉 Installation complete!"
