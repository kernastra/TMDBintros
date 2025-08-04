#!/bin/bash

# Script to download yt-dlp binaries for different platforms
# Run this during build process or manually

RESOURCES_DIR="Resources/binaries"
mkdir -p "$RESOURCES_DIR"

echo "Downloading yt-dlp binaries..."

# Get the latest release URL
LATEST_URL="https://github.com/yt-dlp/yt-dlp/releases/latest/download"

# Download for different platforms
echo "Downloading Linux x64 binary..."
curl -L "${LATEST_URL}/yt-dlp" -o "${RESOURCES_DIR}/yt-dlp-linux-x64"
chmod +x "${RESOURCES_DIR}/yt-dlp-linux-x64"

echo "Downloading Windows x64 binary..."
curl -L "${LATEST_URL}/yt-dlp.exe" -o "${RESOURCES_DIR}/yt-dlp-windows-x64.exe"

echo "Downloading macOS binary..."
curl -L "${LATEST_URL}/yt-dlp_macos" -o "${RESOURCES_DIR}/yt-dlp-macos-x64"
chmod +x "${RESOURCES_DIR}/yt-dlp-macos-x64"

# Download FreeBSD binary (for TrueNAS)
echo "Downloading FreeBSD binary..."
curl -L "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp" -o "${RESOURCES_DIR}/yt-dlp-freebsd-x64"
chmod +x "${RESOURCES_DIR}/yt-dlp-freebsd-x64"

echo "Download complete! Binaries saved to ${RESOURCES_DIR}/"
ls -la "${RESOURCES_DIR}/"
