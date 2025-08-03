# Plugin Repository Submission Guide

This guide explains how to make the TMDB Trailers plugin available in the official Jellyfin plugin repository.

## Overview

Jellyfin maintains a plugin repository where users can discover and install plugins directly from their Jellyfin dashboard. To get your plugin listed, you need to submit a manifest file to the official repository.

## Required Files

✅ **Already Created:**
- `manifest.json` - Plugin metadata and version information
- `.github/workflows/build-release.yml` - Automated builds and releases
- `CHANGELOG.md` - Version history and changes

## Steps to Submit to Official Repository

### 1. Prepare Your Repository

1. **Upload to GitHub**: Push your plugin to a public GitHub repository
2. **Create Releases**: Use GitHub releases with proper versioning (v1.0.0, v1.0.1, etc.)
3. **Update URLs**: Modify `manifest.json` with your actual GitHub username/repository

### 2. Update Manifest File

Edit `manifest.json` and replace:
- `YourGitHubUsername` with your actual GitHub username
- Update `sourceUrl` to point to your release DLL
- Add actual SHA256 checksum of your DLL
- Update `imageUrl` if you have a logo

### 3. Submit to Jellyfin Repository

1. **Fork the Repository**: 
   ```bash
   # Fork https://github.com/jellyfin/jellyfin-plugin-repository
   ```

2. **Add Your Manifest**:
   ```bash
   git clone https://github.com/YourUsername/jellyfin-plugin-repository
   cd jellyfin-plugin-repository
   cp /path/to/your/manifest.json manifest.json
   ```

3. **Create Pull Request**:
   - Add your `manifest.json` to the repository
   - Follow the PR template and guidelines
   - Include testing information and screenshots

### 4. Official Submission Process

The official Jellyfin plugin repository is located at:
**https://github.com/jellyfin/jellyfin-plugin-repository**

#### Submission Requirements:
- ✅ Plugin must be stable and tested
- ✅ Must follow Jellyfin plugin guidelines
- ✅ Proper documentation (README, changelog)
- ✅ Open source with appropriate license
- ✅ No malicious code or dependencies
- ✅ Proper versioning and release management

#### Review Process:
1. Submit PR to the plugin repository
2. Jellyfin team reviews the plugin
3. Testing on different environments
4. Code quality and security review
5. Approval and merge

## Alternative: Custom Repository

If you don't want to wait for official approval, you can create your own plugin repository:

### 1. Create Repository Structure
```
my-jellyfin-plugins/
├── manifest.json
└── README.md
```

### 2. Host the Manifest
Upload your `manifest.json` to a publicly accessible URL, such as:
- GitHub Pages
- Your own web server
- CDN service

### 3. Add to Jellyfin
Users can add your custom repository in Jellyfin:
1. Go to **Dashboard** → **Plugins** → **Repositories**
2. Add new repository with your manifest URL
3. Save and browse available plugins

## Automated Release Process

The included GitHub Actions workflow automatically:

1. **Builds** the plugin on every tag push
2. **Calculates** SHA256 checksums
3. **Creates** GitHub releases with assets
4. **Updates** version information

### To Create a Release:
```bash
git tag v1.0.0
git push origin v1.0.0
```

This triggers the automated build and release process.

## Manifest File Explanation

```json
{
  "guid": "eb5212ba-b5e0-4aa4-a00c-9ab0cb4d1a5f",  // Unique plugin ID
  "name": "TMDB Trailers",                         // Display name
  "description": "...",                            // Short description
  "overview": "...",                               // Detailed description
  "owner": "YourGitHubUsername",                   // Repository owner
  "category": "General",                           // Plugin category
  "imageUrl": "...",                               // Logo/icon URL
  "versions": [                                    // Version history
    {
      "version": "1.0.0.0",                       // Version number
      "changelog": "...",                          // What's new
      "targetAbi": "10.8.13.0",                   // Jellyfin version
      "sourceUrl": "...",                          // Download URL
      "checksum": "...",                           // SHA256 hash
      "timestamp": "2024-08-03T00:00:00Z"         // Release date
    }
  ]
}
```

## Best Practices

1. **Semantic Versioning**: Use proper version numbering (MAJOR.MINOR.PATCH)
2. **Security**: Never include API keys or secrets in the repository
3. **Documentation**: Maintain clear installation and usage instructions
4. **Testing**: Test on multiple Jellyfin versions when possible
5. **Dependencies**: Document all external dependencies (like yt-dlp)
6. **Backwards Compatibility**: Maintain compatibility when possible

## Resources

- [Jellyfin Plugin Development Guide](https://jellyfin.org/docs/general/server/plugins/)
- [Official Plugin Repository](https://github.com/jellyfin/jellyfin-plugin-repository)
- [Plugin Template](https://github.com/jellyfin/jellyfin-plugin-template)
- [Jellyfin Discord](https://discord.gg/zHBxVSXdBV) - #plugin-dev channel

## Support

For questions about plugin development or repository submission:
1. Check the [Jellyfin documentation](https://jellyfin.org/docs/)
2. Ask in the [Jellyfin Discord](https://discord.gg/zHBxVSXdBV)
3. Open an issue in the [plugin repository](https://github.com/jellyfin/jellyfin-plugin-repository)
