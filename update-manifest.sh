#!/bin/bash

# Script to update manifest.json with current build information
# Run this after building a release version

echo "🔧 Updating manifest.json with build information..."

# Build the release version
echo "Building release version..."
dotnet build --configuration Release

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

DLL_PATH="bin/Release/net8.0/TMDBintros.dll"

if [ ! -f "$DLL_PATH" ]; then
    echo "❌ DLL not found at $DLL_PATH"
    exit 1
fi

# Calculate SHA256 checksum
echo "Calculating SHA256 checksum..."
CHECKSUM=$(sha256sum "$DLL_PATH" | cut -d' ' -f1)
echo "SHA256: $CHECKSUM"

# Get current timestamp in ISO format
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Timestamp: $TIMESTAMP"

# Get version from project file
VERSION=$(grep -oP '<AssemblyVersion>\K[^<]+' TMDBintros.csproj || echo "1.0.0.0")
echo "Version: $VERSION"

echo ""
echo "📝 Manual steps to complete manifest.json:"
echo "1. Replace 'YourGitHubUsername' with your actual GitHub username"
echo "2. Replace 'SHA256-CHECKSUM-PLACEHOLDER' with: $CHECKSUM"
echo "3. Update timestamp to: $TIMESTAMP"
echo "4. Verify version is: $VERSION"
echo "5. Update sourceUrl to point to your GitHub release"
echo ""
echo "📋 Example sourceUrl format:"
echo "https://github.com/YourGitHubUsername/TMDBintros/releases/download/v${VERSION}/TMDBintros.dll"
echo ""
echo "✅ Build complete! DLL ready for release at: $DLL_PATH"

# Optional: Show file size
FILE_SIZE=$(ls -lh "$DLL_PATH" | cut -d' ' -f5)
echo "📦 DLL size: $FILE_SIZE"
