# TMDB Trailers Plugin - Bundled yt-dlp Version

## Overview

This version of the TMDB Trailers plugin includes **bundled yt-dlp binaries** for all major platforms, eliminating the need to install yt-dlp separately on your Jellyfin server.

## What's Included

The plugin package (`TMDBintros-bundled.zip`) contains:

- **Plugin DLL**: Core C# .NET 8.0 plugin functionality
- **yt-dlp Binaries** for multiple platforms:
  - `yt-dlp-linux-x64` - Linux x64 systems
  - `yt-dlp-freebsd-x64` - FreeBSD x64 systems (TrueNAS)
  - `yt-dlp-macos-x64` - macOS x64 systems  
  - `yt-dlp-windows-x64.exe` - Windows x64 systems

## How It Works

1. **Automatic Detection**: The plugin automatically detects your server's platform
2. **Binary Selection**: Selects the appropriate yt-dlp binary for your system
3. **Fallback Support**: Falls back to system-installed yt-dlp if bundled version fails
4. **No Installation Required**: No need to install yt-dlp on your server

## Benefits

### ✅ **Works Out of the Box**
- No additional software installation required
- Works on TrueNAS, Docker, and other restricted environments
- Eliminates permission and PATH issues

### ✅ **Cross-Platform Compatible**
- Supports Windows, Linux, macOS, and FreeBSD
- Optimized for TrueNAS Core/SCALE environments
- Works in Docker containers and jails

### ✅ **Version Controlled**
- Uses latest stable yt-dlp version (2025.07.21)
- No version conflicts with system installations
- Consistent behavior across all platforms

## Installation

1. **Download** `TMDBintros-bundled.zip`
2. **Install** via Jellyfin Dashboard → Plugins → Upload Plugin
3. **Configure** your TMDB API key in plugin settings
4. **Enjoy** automatic trailer downloads!

## File Size

- **Package Size**: ~56MB (includes all platform binaries)
- **Runtime Size**: Only one binary (~3-35MB) is used per platform

## Supported Platforms

| Platform | Binary | Size | Status |
|----------|--------|------|--------|
| Linux x64 | `yt-dlp-linux-x64` | ~3MB | ✅ Tested |
| FreeBSD x64 | `yt-dlp-freebsd-x64` | ~3MB | ✅ TrueNAS |
| macOS x64 | `yt-dlp-macos-x64` | ~35MB | ✅ Supported |
| Windows x64 | `yt-dlp-windows-x64.exe` | ~18MB | ✅ Supported |

## Configuration

The plugin automatically:

1. **Detects** your platform at runtime
2. **Locates** the appropriate bundled binary
3. **Sets permissions** (Unix systems)
4. **Downloads trailers** using the bundled yt-dlp

## Troubleshooting

### If bundled yt-dlp fails:
- Plugin will automatically try system-installed yt-dlp
- Check Jellyfin logs for error details
- Ensure TMDB API key is configured

### For permission issues:
- Plugin automatically sets execute permissions on Unix systems
- No manual chmod commands needed

### For TrueNAS users:
- Uses FreeBSD binary optimized for TrueNAS systems
- Works in both jails and direct installations
- No pkg install commands required

## Technical Details

### Binary Selection Logic:
```csharp
if (Windows) → yt-dlp-windows-x64.exe
else if (macOS) → yt-dlp-macos-x64  
else if (FreeBSD) → yt-dlp-freebsd-x64
else → yt-dlp-linux-x64 (default)
```

### Resource Location:
- Binaries stored in: `<plugin-directory>/Resources/binaries/`
- Auto-detected at runtime using `Assembly.GetExecutingAssembly().Location`

## Original vs Bundled Version

| Feature | Original | Bundled |
|---------|----------|---------|
| yt-dlp Installation | ❌ Required | ✅ Included |
| TrueNAS Support | ⚠️ Manual Setup | ✅ Works OOTB |
| Docker Support | ⚠️ Complex | ✅ Simple |
| File Size | ~50KB | ~56MB |
| Dependencies | yt-dlp | None |

## Source Code

This bundled version uses the same C# codebase with enhanced binary detection:

- **VideoDownloadService.cs**: Enhanced with `GetYtDlpPath()` method
- **Platform Detection**: Uses `RuntimeInformation.IsOSPlatform()`
- **Binary Management**: Automatic permissions and fallback logic

## Support

For issues with the bundled version:

1. Check Jellyfin logs for yt-dlp errors
2. Verify TMDB API key configuration  
3. Test with a single movie first
4. Report issues with platform details

---

**Ready to use on TrueNAS and other platforms without any additional setup!**
