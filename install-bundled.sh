#!/bin/bash

# TMDB Trailers Plugin - Installation Script for Bundled Version
# This script helps install the bundled version on your Jellyfin server

echo "🎬 TMDB Trailers Plugin - Bundled yt-dlp Installation"
echo "=================================================="
echo ""

# Check if we're running on the correct system
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PLATFORM="Linux"
    BINARY="yt-dlp-linux-x64"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macOS"
    BINARY="yt-dlp-macos-x64"
elif [[ "$OSTYPE" == "freebsd"* ]]; then
    PLATFORM="FreeBSD (TrueNAS)"
    BINARY="yt-dlp-freebsd-x64"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    PLATFORM="Windows"
    BINARY="yt-dlp-windows-x64.exe"
else
    PLATFORM="Unknown"
    BINARY="yt-dlp-linux-x64 (default)"
fi

echo "🖥️  Detected Platform: $PLATFORM"
echo "📦 Bundled Binary: $BINARY"
echo ""

echo "✅ This bundled version includes:"
echo "   • TMDB Trailers Plugin (C# .NET 8.0)"
echo "   • yt-dlp binaries for all platforms"
echo "   • Automatic platform detection"
echo "   • No external dependencies"
echo ""

echo "📋 Installation Steps:"
echo "   1. Upload TMDBintros-bundled.zip to Jellyfin"
echo "   2. Go to Dashboard → Plugins → Upload Plugin"
echo "   3. Select the bundled ZIP file"
echo "   4. Restart Jellyfin"
echo "   5. Configure TMDB API key in plugin settings"
echo ""

echo "🔧 Configuration Required:"
echo "   • TMDB API Key (get free at https://www.themoviedb.org/settings/api)"
echo "   • Set preferred video quality (480p/720p/1080p)"
echo "   • Configure trailer folder location"
echo ""

echo "🚀 Benefits of Bundled Version:"
echo "   ✅ Works on TrueNAS without additional setup"
echo "   ✅ No yt-dlp installation required"
echo "   ✅ Cross-platform compatibility"
echo "   ✅ Automatic fallback to system yt-dlp if needed"
echo ""

echo "📊 Package Info:"
echo "   • Size: ~56MB (includes all platform binaries)"
echo "   • Runtime: Only appropriate binary is used"
echo "   • Version: yt-dlp 2025.07.21"
echo ""

if [ -f "TMDBintros-bundled.zip" ]; then
    echo "✅ Found TMDBintros-bundled.zip in current directory"
    echo "   File size: $(du -h TMDBintros-bundled.zip | cut -f1)"
    echo ""
    echo "🔗 Ready to install! Upload this file to Jellyfin."
else
    echo "❌ TMDBintros-bundled.zip not found in current directory"
    echo "   Make sure you're running this script from the plugin directory"
fi

echo ""
echo "🎯 Ready to download trailers automatically!"
echo "=================================================="
