#!/bin/bash

# TMDB Trailers Plugin Installation Script
# This script builds the plugin and provides installation instructions

echo "Building TMDB Trailers Plugin..."

# Build the plugin
dotnet build --configuration Release

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "Plugin DLL location: $(pwd)/bin/Release/net8.0/TMDBintros.dll"
    echo ""
    echo "📋 Installation Instructions:"
    echo "1. Stop your Jellyfin server"
    echo "2. Copy the DLL to your Jellyfin plugins directory:"
    echo "   - Linux: /var/lib/jellyfin/plugins/"
    echo "   - Windows: C:\\ProgramData\\Jellyfin\\Server\\plugins\\"
    echo "   - Docker: /config/plugins/ (in your mapped volume)"
    echo "3. Install yt-dlp if not already installed:"
    echo "   - Ubuntu/Debian: sudo apt install yt-dlp"
    echo "   - Windows: winget install yt-dlp"
    echo "   - macOS: brew install yt-dlp"
    echo "4. Start your Jellyfin server"
    echo "5. Go to Dashboard → Plugins → TMDB Trailers to configure"
    echo ""
    echo "📝 Required Configuration:"
    echo "- Get a free TMDB API key from: https://www.themoviedb.org/settings/api"
    echo "- Enter the API key in the plugin configuration"
    echo ""
    echo "🎬 The plugin will then automatically download trailers for your movies!"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi
