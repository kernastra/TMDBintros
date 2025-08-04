# TMDB Trailer Downloader v3.0.0 for Jellyfin Cinema Mode

A production-ready Python application that downloads movie trailers from The Movie Database (TMDB) API and organizes them for the [Jellyfin Cinema Mode plugin](https://github.com/CherryFloors/jellyfin-plugin-cinemamode).

## Features

- 🎬 Search movies on TMDB by title and year
- 📥 Download trailers using yt-dlp
- 📁 **Jellyfin Cinema Mode compatible** folder structure
- 🌐 **Network share support** (SMB/CIFS, NFS, SSHFS)
- 🔧 **Environment-based configuration** for enterprise deployment
- 🔒 **Security-focused** credential management
- 📝 Comprehensive logging and validation
- 🎯 Support for batch processing or single movies
- 🚀 **Production-ready** with automatic mounting and cleanup
- 🐳 **Full Docker support** with multi-service architecture
- 📊 **Web dashboard** for monitoring and management
- 🔄 **Real-time monitoring** and scheduled scanning

## Jellyfin Integration

This script creates the **exact folder structure** required by the Jellyfin Cinema Mode plugin:

```
/your/media/share/
├── The Matrix (1999)/
│   ├── The Matrix (1999).mkv          ← Your movie file
│   └── trailers/                      ← Trailers subfolder (Cinema Mode compatible)
│       ├── The Matrix-trailer-1.mp4
│       └── The Matrix-trailer-2.mp4
└── Inception (2010)/
    ├── Inception (2010).mkv
    └── trailers/
        └── Inception-trailer-1.mp4
```

The Cinema Mode plugin will automatically discover these trailers and play them before your movies!

## Requirements

- Python 3.7+
- yt-dlp (`pip install yt-dlp`)
- python-dotenv (`pip install python-dotenv`)
- TMDB API key (free from https://www.themoviedb.org/settings/api)
- **Network share access** (SMB/CIFS, NFS, or SSHFS for remote storage)

## Quick Start

### Option 1: Docker (Recommended for Production)

**Easy deployment with Docker Compose:**

```bash
# 1. Copy Docker environment template
cp .env.docker .env

# 2. Edit configuration
nano .env
# Add your TMDB_API_KEY and HOST_MOVIES_PATH

# 3. Run one-time scan
docker-compose --profile scanner up tmdb-scanner

# 4. Or start real-time monitoring
docker-compose --profile monitor up -d tmdb-monitor
```

📖 **Full Docker guide**: See [DOCKER.md](DOCKER.md) for complete instructions.

### Option 2: Native Python Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create your environment configuration:**
```bash
cp .env.example .env
```

3. **Edit `.env` with your settings:**
```bash
# TMDB API Configuration
TMDB_API_KEY=your_api_key_here

# Jellyfin Configuration
JELLYFIN_MOVIES_PATH=/path/to/jellyfin/movies

# Network Share (if using remote storage)
NETWORK_SHARE_TYPE=smb  # or nfs, sshfs
NETWORK_SHARE_PATH=//server/movies
NETWORK_USERNAME=your_username
NETWORK_PASSWORD=your_password
```

4. **Test your configuration:**
```bash
python3 enhanced_downloader.py --test-config
```

5. **Scan and download trailers:**
```bash
python3 enhanced_downloader.py --scan-existing
```

## Usage

### Automatic Library Scanning (Recommended):
Scan your existing Jellyfin movie library and download trailers for movies missing them:
```bash
python3 enhanced_downloader.py --scan-existing
```

### Continuous Monitoring (New!):
Automatically monitor your movies folder and download trailers when new movies are added:

**Real-time monitoring** (watches for file system changes):
```bash
python3 tmdb_monitor.py
```

**Scheduled scanning** (runs at regular intervals):
```bash
python3 tmdb_scheduler.py --interval 60  # Scan every 60 minutes
```

### Test Configuration:
Validate your environment settings before downloading:
```bash
python3 enhanced_downloader.py --test-config
```

### Process movies from legacy config file:
```bash
python3 tmdb_trailer_downloader.py  # Uses old JSON config system
```

### Process a single movie:
```bash
python3 enhanced_downloader.py --title "The Matrix" --year 1999
```

### Custom quality setting:
```bash
python3 enhanced_downloader.py --scan-existing --quality 1080p
```

### Include movies that already have trailers:
```bash
python3 enhanced_downloader.py --scan-existing --include-existing
```

## Configuration

### Environment-Based Configuration (Recommended)

Create a `.env` file with your settings. This is the **secure, production-ready** method:

```bash
# ================================
# TMDB API Configuration
# ================================
TMDB_API_KEY=your_tmdb_api_key_here

# ================================
# Jellyfin Configuration
# ================================
JELLYFIN_MOVIES_PATH=/path/to/jellyfin/movies
# For network shares, this will be the mount point

# ================================
# Network Share Configuration
# ================================
# Set these if your Jellyfin movies are on a network share
NETWORK_SHARE_TYPE=smb          # smb, nfs, or sshfs
NETWORK_SHARE_PATH=//server/movies
NETWORK_USERNAME=your_username
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=your_domain      # For SMB shares (optional)

# For SSH-based shares (SSHFS)
# SSH_KEY_PATH=/path/to/private/key
# SSH_PORT=22

# ================================
# Download Configuration
# ================================
DOWNLOAD_QUALITY=best           # best, 1080p, 720p, 480p
MAX_TRAILERS_PER_MOVIE=3
DOWNLOAD_TIMEOUT=300

# ================================
# Scanning Configuration
# ================================
ENABLE_PARALLEL_DOWNLOADS=true
MAX_CONCURRENT_DOWNLOADS=3
SKIP_EXISTING_TRAILERS=true

# ================================
# Logging Configuration
# ================================
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=tmdb_downloader.log
```

### Legacy JSON Configuration

The old `config.json` system is still supported but **not recommended** for production:

```json
{
  "tmdb_api_key": "your_api_key_here",
  "remote_share_path": "/path/to/jellyfin/movies",
  "quality": "best",
  "movies": [
    {"title": "The Matrix", "year": 1999},
    {"title": "Inception", "year": 2010}
  ]
}
```

**⚠️ Security Note**: Environment variables are more secure than JSON files for production deployments.

## Automatic Monitoring & Continuous Operation

The application now supports **automatic monitoring** of your movie library to detect and download trailers for newly added movies:

### Real-Time File System Monitoring

**Watches for new movie folders** and immediately downloads trailers:

```bash
# Install monitoring dependencies
pip install watchdog

# Start real-time monitoring
python3 tmdb_monitor.py

# With custom configuration
python3 tmdb_monitor.py --config-dir /etc/tmdb --log-level DEBUG
```

**How it works:**
- 📁 Monitors your Jellyfin movies directory for new folders
- 🎬 Detects folders matching `Movie Name (YYYY)` pattern
- ⚡ Automatically downloads trailers within seconds of detection
- 🔄 Runs continuously until stopped (Ctrl+C)
- 📝 Logs all activity to `tmdb_monitor.log`

### Scheduled Scanning

**Periodically scans** for new movies at regular intervals:

```bash
# Install scheduling dependencies  
pip install schedule

# Scan every hour (default)
python3 tmdb_scheduler.py

# Custom interval (every 30 minutes)
python3 tmdb_scheduler.py --interval 30

# Run with custom configuration
python3 tmdb_scheduler.py --config-dir /etc/tmdb --interval 120
```

**Perfect for:**
- 🕒 **Scheduled operations** (run via cron/systemd)
- 🏢 **Enterprise environments** with regular media additions
- 🔋 **Lower resource usage** than real-time monitoring
- 📊 **Predictable scanning windows**

### Monitoring Configuration

Add to your `.env` file:

```bash
# Monitoring Options
ENABLE_MONITORING=true
MONITOR_TYPE=filesystem        # or scheduled
MONITOR_DELAY=5               # Seconds to wait after detecting new folder
SCHEDULE_INTERVAL=60          # Minutes between scheduled scans
```

## Network Share Support

This application supports automatic mounting of network shares for enterprise deployments:

### SMB/CIFS Shares
```bash
NETWORK_SHARE_TYPE=smb
NETWORK_SHARE_PATH=//server.domain.com/movies
NETWORK_USERNAME=your_username
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=your_domain
```

### NFS Shares
```bash
NETWORK_SHARE_TYPE=nfs
NETWORK_SHARE_PATH=server.domain.com:/path/to/movies
```

### SSHFS Shares
```bash
NETWORK_SHARE_TYPE=sshfs
NETWORK_SHARE_PATH=user@server.domain.com:/path/to/movies
SSH_KEY_PATH=/path/to/private/key
SSH_PORT=22
```

The application will automatically:
1. **Mount** the network share before downloading
2. **Validate** the mount is accessible
3. **Download** trailers to the correct location
4. **Unmount** the share when complete

## Command Line Options

### Enhanced Downloader (Recommended)
```bash
python3 enhanced_downloader.py [OPTIONS]
```

Options:
- `--scan-existing`: **Automatically scan Jellyfin library** for movies missing trailers
- `--test-config`: Validate configuration and network connectivity
- `--title TITLE`: Single movie title
- `--year YEAR`: Movie year (for single movie)
- `--quality QUALITY`: Video quality override
- `--include-existing`: Include movies that already have trailers
- `--help`: Show all available options

### Monitoring Services (New!)

**Real-time File System Monitor:**
```bash
python3 tmdb_monitor.py [OPTIONS]
```

Options:
- `--config-dir PATH`: Configuration directory path
- `--log-level LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

**Scheduled Scanner:**
```bash
python3 tmdb_scheduler.py [OPTIONS]
```

Options:
- `--config-dir PATH`: Configuration directory path
- `--interval MINUTES`: Scan interval in minutes (default: 60)
- `--log-level LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

### Legacy Downloader
```bash
python3 tmdb_trailer_downloader.py [OPTIONS]
```

Options:
- `--config PATH`: Custom config file path  
- `--create-config`: Generate sample config file
- (Plus all options from enhanced downloader)

## Jellyfin Cinema Mode Setup

1. **Configure this application** with your TMDB API key and Jellyfin path
2. **Test your setup**: `python3 enhanced_downloader.py --test-config`
3. **Download trailers**: `python3 enhanced_downloader.py --scan-existing`
4. **Install the [Cinema Mode plugin](https://github.com/CherryFloors/jellyfin-plugin-cinemamode)** in Jellyfin
5. **Enable Cinema Mode** in user playback settings
6. **Enjoy automatic trailers** before your movies!

## Security Best Practices

- **Use environment variables** instead of JSON files for credentials
- **Store `.env` files securely** and never commit them to version control
- **Use SSH keys** instead of passwords for SSHFS when possible
- **Regularly rotate** API keys and network credentials
- **Monitor logs** for unauthorized access attempts

## Deployment Examples

### Docker Deployment (Recommended)

**Local movies with Docker:**
```bash
# .env file
TMDB_API_KEY=your_key
HOST_MOVIES_PATH=/home/user/jellyfin/movies
NETWORK_ENABLED=false

# Run real-time monitoring
docker-compose --profile monitor up -d tmdb-monitor
```

**Network share with Docker:**
```bash
# .env file
TMDB_API_KEY=your_key
HOST_MOVIES_PATH=/mnt/movies
NETWORK_ENABLED=true
NETWORK_TYPE=smb
NETWORK_SERVER=192.168.1.100
NETWORK_SHARE=movies
NETWORK_USERNAME=jellyfin
NETWORK_PASSWORD=secure_password
PRIVILEGED_MODE=true

# Run scheduled scanning
docker-compose --profile scheduler up -d tmdb-scheduler
```

### Native Python Deployment

**Local Development:**
```bash
# Simple local setup
TMDB_API_KEY=your_key
JELLYFIN_MOVIES_PATH=/home/user/jellyfin/movies
```

**Network Share (SMB):**
```bash
# Corporate SMB share
TMDB_API_KEY=your_key
JELLYFIN_MOVIES_PATH=/mnt/jellyfin_movies
NETWORK_SHARE_TYPE=smb
NETWORK_SHARE_PATH=//media-server.company.com/movies
NETWORK_USERNAME=jellyfin_service
NETWORK_PASSWORD=secure_password
NETWORK_DOMAIN=COMPANY
```

**SSH-Based Remote Storage:**
```bash
# Remote server with SSH key authentication
TMDB_API_KEY=your_key
JELLYFIN_MOVIES_PATH=/mnt/remote_movies
NETWORK_SHARE_TYPE=sshfs
NETWORK_SHARE_PATH=admin@media-server.example.com:/media/movies
SSH_KEY_PATH=/home/user/.ssh/media_server_key
```

## Troubleshooting

### Configuration Issues
```bash
# Test your configuration
python3 enhanced_downloader.py --test-config
```

### Network Mount Problems
```bash
# Check mount status
mount | grep jellyfin

# Manual mount test (SMB example)
sudo mount -t cifs //server/movies /mnt/test -o username=user
```

### Permission Issues
- Ensure your user has **read/write access** to the Jellyfin movies directory
- For network shares, verify **network credentials** are correct
- Check **firewall settings** for SMB (445), NFS (2049), or SSH (22) ports

## Getting a TMDB API Key

1. Go to https://www.themoviedb.org/
2. Create a free account
3. Go to Settings → API
4. Request an API key (choose "Developer" option)
5. Copy the API key to your `.env` file

## Output Structure

Trailers are organized in **Jellyfin Cinema Mode compatible** structure:
```
/your/jellyfin/movies/
├── The Matrix (1999)/
│   ├── The Matrix (1999).mkv          ← Your existing movie
│   └── trailers/                      ← Created by this script
│       ├── The Matrix-trailer-1.mp4
│       └── The Matrix-trailer-2.mp4
└── Inception (2010)/
    ├── Inception (2010).mkv
    └── trailers/
        └── Inception-trailer-1.mp4
```

After running this script, the [Jellyfin Cinema Mode plugin](https://github.com/CherryFloors/jellyfin-plugin-cinemamode) will automatically find and play these trailers before your movies!

## Logging

All operations are logged with configurable levels:
- **Console output** with colored formatting
- **Log file** (`tmdb_downloader.log` by default)
- **Network operations** (mount/unmount activities)
- **Download progress** and error details
