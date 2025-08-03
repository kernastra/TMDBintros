# Local Installation Guide

This guide explains how to clone, build, and install the TMDB Trailers plugin locally on your system.

## Prerequisites

### Required Software

1. **Git** - For cloning the repository
   ```bash
   # Ubuntu/Debian
   sudo apt install git
   
   # Windows
   # Download from https://git-scm.com/
   
   # macOS
   brew install git
   ```

2. **.NET 8.0 SDK** - For building the plugin
   ```bash
   # Ubuntu/Debian
   wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
   sudo dpkg -i packages-microsoft-prod.deb
   sudo apt update
   sudo apt install dotnet-sdk-8.0
   
   # Windows
   # Download from https://dotnet.microsoft.com/download/dotnet/8.0
   
   # macOS
   brew install dotnet
   ```

3. **yt-dlp** - For downloading YouTube videos
   ```bash
   # Ubuntu/Debian
   sudo apt install yt-dlp
   
   # Windows
   winget install yt-dlp
   # or: pip install yt-dlp
   
   # macOS
   brew install yt-dlp
   ```

4. **Jellyfin Server** - Running locally or accessible
   - Download from [jellyfin.org](https://jellyfin.org/downloads/)

### TMDB API Key

1. Create a free account at [The Movie Database](https://www.themoviedb.org/)
2. Go to [API Settings](https://www.themoviedb.org/settings/api)
3. Request an API key (it's free and instant)
4. Save your API key for later configuration

## Step-by-Step Installation

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/YourGitHubUsername/TMDBintros.git
cd TMDBintros

# Optional: Check available branches/tags
git branch -a
git tag -l
```

### Step 2: Build the Plugin

```bash
# Restore dependencies and build
dotnet restore
dotnet build --configuration Release

# Verify the build was successful
ls -la bin/Release/net8.0/TMDBintros.dll
```

**Expected output:**
```
-rw-r--r-- 1 user user 49152 Aug  3 07:32 bin/Release/net8.0/TMDBintros.dll
```

### Step 3: Find Your Jellyfin Plugins Directory

The location depends on your Jellyfin installation:

#### Linux (Standard Installation)
```bash
# System-wide installation
sudo mkdir -p /var/lib/jellyfin/plugins
JELLYFIN_PLUGINS="/var/lib/jellyfin/plugins"

# User installation (if running as user)
mkdir -p ~/.local/share/jellyfin/plugins
JELLYFIN_PLUGINS="$HOME/.local/share/jellyfin/plugins"
```

#### Windows
```powershell
# Standard installation
$JELLYFIN_PLUGINS = "C:\ProgramData\Jellyfin\Server\plugins"

# Create directory if it doesn't exist
New-Item -ItemType Directory -Force -Path $JELLYFIN_PLUGINS
```

#### macOS
```bash
# Standard installation
mkdir -p /usr/local/var/jellyfin/plugins
JELLYFIN_PLUGINS="/usr/local/var/jellyfin/plugins"

# Homebrew installation
mkdir -p ~/Library/Application\ Support/jellyfin/plugins
JELLYFIN_PLUGINS="$HOME/Library/Application Support/jellyfin/plugins"
```

#### Docker Installation
```bash
# Find your Jellyfin config volume
docker inspect jellyfin | grep -A 5 "Mounts"

# Typical paths:
# /path/to/jellyfin/config/plugins
# ./jellyfin/config/plugins (if using relative paths)
```

### Step 4: Install the Plugin

```bash
# Copy the built DLL to Jellyfin plugins directory
# Linux/macOS
cp bin/Release/net8.0/TMDBintros.dll "$JELLYFIN_PLUGINS/"

# Windows (PowerShell)
Copy-Item "bin\Release\net8.0\TMDBintros.dll" "$JELLYFIN_PLUGINS\"

# Docker (from host)
cp bin/Release/net8.0/TMDBintros.dll /path/to/jellyfin/config/plugins/

# Verify installation
ls -la "$JELLYFIN_PLUGINS/TMDBintros.dll"
```

### Step 5: Restart Jellyfin

```bash
# Linux (systemd)
sudo systemctl restart jellyfin

# Linux (if running as user service)
systemctl --user restart jellyfin

# Docker
docker restart jellyfin

# Windows (if running as service)
# Go to Services app and restart "Jellyfin Server"

# macOS (if using launchd)
launchctl stop org.jellyfin.jellyfin
launchctl start org.jellyfin.jellyfin
```

### Step 6: Verify Plugin Installation

1. **Open Jellyfin Web Interface**
   - Usually at `http://localhost:8096` or your server IP

2. **Check Plugin is Loaded**
   - Go to **Dashboard** → **Plugins**
   - Look for "TMDB Trailers" in the installed plugins list

3. **Check Logs** (if plugin doesn't appear)
   ```bash
   # Linux
   tail -f /var/log/jellyfin/jellyfin.log
   
   # Docker
   docker logs jellyfin
   
   # Windows
   # Check: C:\ProgramData\Jellyfin\Server\logs\
   ```

### Step 7: Configure the Plugin

1. **Go to Plugin Settings**
   - **Dashboard** → **Plugins** → **TMDB Trailers** → **Settings**

2. **Enter Required Configuration**
   - **TMDB API Key**: Enter your API key from Step 1
   - **Enable Automatic Download**: ✅ (recommended)
   - **Preferred Quality**: 720p (or your preference)
   - **Max Trailer Duration**: 5 minutes
   - **Trailer Folder Name**: "trailers"
   - **Organize in Subfolders**: ✅ (recommended)

3. **Save Configuration**
   - Click **Save**

### Step 8: Test the Plugin

#### Option A: Manual Test
1. **Go to Scheduled Tasks**
   - **Dashboard** → **Scheduled Tasks**
   - Find "Download Movie Trailers"
   - Click **Run Now**

2. **Monitor Progress**
   - Watch the task progress
   - Check logs for any errors

#### Option B: Add a Test Movie
1. **Add a popular movie** to your library (e.g., "The Matrix")
2. **Scan Library** to detect the new movie
3. **Wait for automatic processing** (or run manual task)
4. **Check for trailers** in the movie folder

## Troubleshooting

### Common Issues

#### 1. Plugin Not Appearing in Dashboard

**Symptoms**: Plugin not visible in Jellyfin plugins list

**Solutions**:
```bash
# Check file permissions
chmod 644 "$JELLYFIN_PLUGINS/TMDBintros.dll"

# Check Jellyfin can read the file
sudo -u jellyfin ls -la "$JELLYFIN_PLUGINS/TMDBintros.dll"

# Check Jellyfin logs for errors
tail -f /var/log/jellyfin/jellyfin.log | grep -i tmdb
```

#### 2. Build Failures

**Symptoms**: `dotnet build` fails

**Solutions**:
```bash
# Clean and rebuild
dotnet clean
dotnet restore
dotnet build --configuration Release

# Check .NET version
dotnet --version  # Should be 8.0.x

# Install missing dependencies
dotnet restore --force
```

#### 3. yt-dlp Not Found

**Symptoms**: "yt-dlp is not available" error in logs

**Solutions**:
```bash
# Test yt-dlp installation
yt-dlp --version

# Add to PATH if needed (Linux/macOS)
export PATH="$PATH:/usr/local/bin"

# Reinstall yt-dlp
pip install --upgrade yt-dlp
```

#### 4. TMDB API Errors

**Symptoms**: "Movie not found on TMDB" or API errors

**Solutions**:
- Verify your TMDB API key is correct
- Check internet connectivity
- Test API key manually:
  ```bash
  curl "https://api.themoviedb.org/3/search/movie?api_key=YOUR_API_KEY&query=matrix"
  ```

#### 5. Permission Issues

**Symptoms**: Cannot write to trailer directories

**Solutions**:
```bash
# Fix Jellyfin user permissions
sudo chown -R jellyfin:jellyfin /var/lib/jellyfin/
sudo chmod -R 755 /var/lib/jellyfin/

# For media directories
sudo chown -R jellyfin:jellyfin /path/to/your/movies/
sudo chmod -R 755 /path/to/your/movies/
```

### Development Mode

If you're developing or testing changes:

#### 1. Enable Debug Logging
```bash
# Edit Jellyfin logging configuration
# Add this to your logging.json:
{
  "Jellyfin.Plugins.TMDBintros": "Debug"
}
```

#### 2. Quick Rebuild and Deploy
```bash
# Create a quick deploy script
cat > deploy.sh << 'EOF'
#!/bin/bash
dotnet build --configuration Release
sudo systemctl stop jellyfin
cp bin/Release/net8.0/TMDBintros.dll /var/lib/jellyfin/plugins/
sudo systemctl start jellyfin
echo "Plugin deployed and Jellyfin restarted"
EOF

chmod +x deploy.sh
./deploy.sh
```

#### 3. Live Development
```bash
# Use file watching for automatic rebuilds
dotnet watch build --configuration Release
```

## File Structure After Installation

After successful installation, your file structure will look like:

```
/var/lib/jellyfin/plugins/
└── TMDBintros.dll

/path/to/your/movies/
└── Movie Name (2023)/
    ├── Movie Name (2023).mkv
    └── trailers/
        └── Movie Name (2023)/
            └── Movie Name (2023) - Official Trailer.mp4
```

## Updating the Plugin

To update to a newer version:

```bash
# Pull latest changes
git pull origin main

# Rebuild
dotnet build --configuration Release

# Stop Jellyfin
sudo systemctl stop jellyfin

# Replace the DLL
cp bin/Release/net8.0/TMDBintros.dll /var/lib/jellyfin/plugins/

# Start Jellyfin
sudo systemctl start jellyfin
```

## Uninstalling

To remove the plugin:

```bash
# Remove the DLL
rm /var/lib/jellyfin/plugins/TMDBintros.dll

# Restart Jellyfin
sudo systemctl restart jellyfin

# Optional: Remove trailer files
# find /path/to/movies -name "trailers" -type d -exec rm -rf {} +
```

## Support

If you encounter issues:

1. **Check the logs** first
2. **Enable detailed logging** in plugin configuration
3. **Search existing issues** on GitHub
4. **Create a new issue** with:
   - Your OS and Jellyfin version
   - Build output and error messages
   - Relevant log excerpts
   - Steps to reproduce

## Contributing

If you want to contribute to development:

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YourUsername/TMDBintros.git
cd TMDBintros

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and test
dotnet build
./deploy.sh  # Your local deploy script

# Commit and push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

This local installation method gives you full control over the plugin and allows you to customize it for your specific needs!
