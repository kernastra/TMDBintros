# TMDB Trailers Plugin for Jellyfin

A Jellyfin plugin that automatically downloads movie trailers from The Movie Database (TMDB) API and organizes them alongside your movie files.

## Features

- **Automatic Trailer Discovery**: Searches TMDB for trailers matching your movie library
- **Quality Selection**: Choose preferred video quality (480p, 720p, 1080p)
- **Smart Organization**: Organizes trailers in configurable folder structures
- **Duration Filtering**: Set maximum trailer length to avoid long videos
- **Scheduled Processing**: Automatically processes new movies at configurable intervals
- **Overwrite Control**: Choose whether to replace existing trailers
- **Detailed Logging**: Optional verbose logging for troubleshooting

## Prerequisites

### System Requirements

- Jellyfin 10.8.13 or later
- .NET 8.0 runtime
- **yt-dlp** (for downloading YouTube videos)

### Installing yt-dlp

The plugin requires `yt-dlp` to download videos from YouTube. Install it using one of these methods:

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install yt-dlp
```

#### CentOS/RHEL/Fedora:
```bash
# Using pip
pip install yt-dlp

# Or using package manager (Fedora)
sudo dnf install yt-dlp
```

#### Windows:
```bash
# Using winget
winget install yt-dlp

# Or using pip
pip install yt-dlp
```

#### macOS:
```bash
# Using Homebrew
brew install yt-dlp

# Or using pip
pip install yt-dlp
```

### TMDB API Key

1. Create a free account at [The Movie Database](https://www.themoviedb.org/)
2. Go to [API Settings](https://www.themoviedb.org/settings/api)
3. Request an API key
4. Copy your API key for use in the plugin configuration

## Installation

### Option 1: Local Installation (Clone & Build)

Perfect for testing, development, or using the latest features:

1. **Quick Installation** (automated):
   ```bash
   git clone https://github.com/kernastra/TMDBintros.git
   cd TMDBintros
   ./local-install.sh
   ```

2. **Manual Installation** (step-by-step):
   - See [LOCAL_INSTALLATION.md](LOCAL_INSTALLATION.md) for detailed instructions
   - Includes troubleshooting and development setup

### Option 2: Manual Installation

1. Download the latest release DLL from the [Releases](https://github.com/kernastra/TMDBintros/releases) page
2. Copy the DLL to your Jellyfin plugins directory (see paths above)
3. Restart Jellyfin

### Option 3: Build from Source

1. Clone this repository:
   ```bash
   git clone https://github.com/kernastra/TMDBintros.git
   cd TMDBintros
   ```

2. Build the plugin:
   ```bash
   dotnet build --configuration Release
   ```

3. Copy the built DLL to your Jellyfin plugins directory:
   ```bash
   # Linux
   cp bin/Release/net8.0/TMDBintros.dll /var/lib/jellyfin/plugins/

   # Windows
   copy bin\Release\net8.0\TMDBintros.dll "C:\ProgramData\Jellyfin\Server\plugins\"

   # Docker
   cp bin/Release/net8.0/TMDBintros.dll /path/to/jellyfin/config/plugins/
   ```

### Option 2: Manual Plugin Installation

1. Download the latest release DLL from the [Releases](https://github.com/kernastra/TMDBintros/releases) page
2. Copy the DLL to your Jellyfin plugins directory (see paths above)
3. Restart Jellyfin

## Configuration

1. Restart Jellyfin after installing the plugin
2. Go to **Dashboard** → **Plugins** → **TMDB Trailers**
3. Configure the following settings:

### Required Settings

- **TMDB API Key**: Your API key from TMDB (required)

### Optional Settings

- **Enable Automatic Download**: Automatically download trailers for new movies (default: enabled)
- **Preferred Video Quality**: 480p, 720p, or 1080p (default: 720p)
- **Maximum Trailer Duration**: Maximum length in minutes (default: 5 minutes)
- **Overwrite Existing Trailers**: Replace existing trailer files (default: disabled)
- **Trailer Folder Name**: Name of subfolder for trailers (default: "trailers")
- **Organize in Subfolders**: Create movie-specific subfolders (default: enabled)
- **Processing Interval**: How often to check for new movies in hours (default: 24 hours)
- **Enable Detailed Logging**: Verbose logging for debugging (default: disabled)

## File Organization

The plugin organizes trailers based on your configuration:

### With Subfolders (default):
```
/Movies/
├── Movie Name (2023)/
│   ├── Movie Name (2023).mkv
│   └── trailers/
│       └── Movie Name (2023)/
│           └── Movie Name (2023) - Official Trailer.mp4
```

### Without Subfolders:
```
/Movies/
├── Movie Name (2023)/
│   ├── Movie Name (2023).mkv
│   └── trailers/
│       └── Movie Name (2023) - Official Trailer.mp4
```

## Manual Processing

You can manually trigger trailer downloads:

1. Go to **Dashboard** → **Scheduled Tasks**
2. Find "Download Movie Trailers" task
3. Click **Run Now**

## Troubleshooting

### Common Issues

1. **"yt-dlp is not available" error**
   - Install yt-dlp using the instructions above
   - Ensure yt-dlp is in your system PATH
   - Restart Jellyfin after installing yt-dlp

2. **"TMDB API key is not configured" error**
   - Ensure you've entered your API key in the plugin configuration
   - Verify the API key is correct and active

3. **No trailers found**
   - Check if the movie exists on TMDB
   - Verify the movie title matches closely with TMDB
   - Enable detailed logging to see search results

4. **Download failures**
   - Check internet connectivity
   - Verify yt-dlp is working: `yt-dlp --version`
   - Check Jellyfin logs for specific error messages

### Logs

Enable detailed logging in the plugin configuration and check Jellyfin logs:

- **Linux**: `/var/log/jellyfin/`
- **Windows**: `C:\ProgramData\Jellyfin\Server\logs\`
- **Docker**: Check container logs

## Development

### Building

```bash
dotnet restore
dotnet build
```

### Testing

```bash
dotnet test
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Plugin Development

Want to create your own Jellyfin plugins? This repository includes comprehensive guides to help you:

### 📚 [Jellyfin Plugin Development Guide](JELLYFIN_PLUGIN_DEVELOPMENT_GUIDE.md)
A complete guide covering:
- Project structure and architecture
- Configuration system best practices
- Dependency injection patterns
- Scheduled task implementation
- Packaging and distribution
- GitHub Actions automation
- Common pitfalls and solutions
- Real-world examples from this TMDB plugin

### ⚡ [Quick Start Template](QUICK_START_TEMPLATE.md)
A minimal template to get started quickly:
- Essential project files with placeholders
- Step-by-step setup instructions
- Quick checklist for new plugins
- Copy-paste ready code snippets

These guides are based on the real-world experience of building this TMDB Trailers plugin and will help you avoid common issues and set up proper CI/CD workflows.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the trailer API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading capabilities
- [Jellyfin](https://jellyfin.org/) for the media server platform

## Support

If you encounter issues or have questions:

1. Check the [troubleshooting section](#troubleshooting)
2. Search existing [GitHub Issues](https://github.com/kernastra/TMDBintros/issues)  
3. Create a new issue with detailed information including:
   - Jellyfin version
   - Plugin version
   - Operating system
   - Relevant log entries
   - Steps to reproduce the issue

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
