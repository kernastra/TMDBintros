#!/bin/bash

echo "📦 GitHub Release Asset Upload Helper"
echo "======================================"
echo
echo "Your TMDBintros.zip file is ready for upload!"
echo "File: $(pwd)/TMDBintros.zip"
echo "Size: $(du -h TMDBintros.zip | cut -f1)"
echo "SHA256: $(sha256sum TMDBintros.zip | cut -d' ' -f1)"
echo
echo "🌐 To upload to GitHub release:"
echo "1. Go to: https://github.com/kernastra/TMDBintros/releases"
echo "2. Click on your 'v1' release"
echo "3. Click 'Edit release'"
echo "4. Drag and drop this file: TMDBintros.zip"
echo "5. Click 'Update release'"
echo
echo "✅ After upload, test the URL:"
echo "   https://github.com/kernastra/TMDBintros/releases/download/v1/TMDBintros.zip"
echo
echo "🔄 Then in Jellyfin:"
echo "1. Remove the old custom repository"
echo "2. Add new repository URL:"
echo "   https://raw.githubusercontent.com/kernastra/TMDBintros/main/manifest.json"
echo "3. Check the Catalog for 'TMDB Trailers'"
