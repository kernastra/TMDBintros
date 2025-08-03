#!/bin/bash

# Simple HTTP server for hosting manifest.json
# Run this on a machine accessible by your Jellyfin server

echo "🌐 Starting local manifest server..."
echo "Manifest will be available at: http://$(hostname -I | awk '{print $1}'):8000/manifest.json"
echo "Add this URL to Jellyfin as a custom repository"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Python 3 server
if command -v python3 &> /dev/null; then
    python3 -m http.server 8000
# Python 2 fallback
elif command -v python &> /dev/null; then
    python -m SimpleHTTPServer 8000
else
    echo "❌ Python not found. Please install Python to run the server."
    exit 1
fi
