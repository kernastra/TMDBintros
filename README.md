# TMDB Trailer Downloader v3.2.0 for Jellyfin Cinema Mode

A production-ready Python application that downloads movie trailers from The Movie Database (TMDB) API and organizes them for the [Jellyfin Cinema Mode plugin](https://github.com/CherryFloors/jellyfin-plugin-cinemamode).

## ✨ Key Features

### 🎬 Core Functionality
- **Smart trailer downloading** from TMDB API using yt-dlp
- **Jellyfin Cinema Mode compatible** folder structure  
- **Batch processing** of existing movie libraries
- **Configurable trailer limits** (1-5 trailers per movie)
- **Quality control** with multiple resolution options

### 🌐 Network Storage Support
- **SMB/CIFS shares** (TrueNAS, Synology, QNAP, Windows)
- **NFS shares** (Linux/Unix systems)  
- **SSH/SFTP** remote access
- **Automatic mounting/unmounting** with credential management
- **Multi-platform compatibility** (Linux, macOS, Windows)

### 🎭 Upcoming Movies (NEW!)
- **Proactive trailer downloading** 3-6 months ahead of release
- **Advanced filtering system** with 25+ options:
  - 🌍 Geographic (countries, languages)
  - 🎯 Content (genres, ratings, runtime)
  - � Production (studios, directors, actors)
  - ⭐ Quality (TMDB ratings, vote counts, budgets)
- **Configurable trailer counts** per upcoming movie
- **Smart cleanup** of expired upcoming trailers

### 🔗 Radarr Integration (STABLE!)
- **Three operation modes:**
  - `upcoming` - Download popular upcoming movie trailers
  - `radarr_only` - Only download trailers for Radarr wanted movies
  - `hybrid` - Smart combination of both approaches
- **Seamless workflow** with existing media management
- **Automatic folder placement** in Radarr movie directories

### �️ Web Dashboard & Monitoring
- **Web interface** on port 8085 (avoids media stack conflicts)
- **Real-time monitoring** with filesystem watching
- **Scheduled scanning** with customizable intervals
- **Background service mode** for continuous operation
- **Comprehensive logging** with configurable levels

### 🐳 Deployment Options
- **Docker containerization** with multi-service architecture
- **Native Python execution** for direct control
- **Standalone testing** with docker-compose.testing.yml
- **Environment-based configuration** for security

## 🚀 Quick Start Guide

### Method 1: Local Python Execution (Recommended for Testing)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up configuration:**
```bash
cp .env.example .env
nano .env  # Add your TMDB_API_KEY and paths
```

3. **Test your setup:**
```bash
python3 enhanced_downloader.py --test-config
```

4. **Scan existing library:**
```bash
python3 enhanced_downloader.py --scan-existing
```

5. **Enable upcoming movies (optional):**
```bash
# Edit .env file:
UPCOMING_ENABLED=true
UPCOMING_DAYS_AHEAD=90
UPCOMING_MAX_TRAILERS_PER_MOVIE=3

# Run upcoming movies download:
python3 tmdb_upcoming.py
```

### Method 2: Docker Deployment (Recommended for Production)

1. **Quick Docker setup:**
```bash
cp .env.example .env
nano .env  # Configure your settings

# One-time scan
docker-compose --profile scanner up tmdb-scanner

# Enable web dashboard (port 8085)
docker-compose --profile dashboard up -d tmdb-dashboard

# Start monitoring services
docker-compose --profile monitor up -d tmdb-monitor
```

📖 **Complete Docker guide**: See [DOCKER.md](DOCKER.md)

### Method 3: Standalone Testing
```bash
# Use testing environment without .env dependency
docker-compose -f docker-compose.testing.yml up tmdb-scanner-test
```
## 🎭 Upcoming Movies Feature

Download trailers for movies releasing in the next 3-6 months with sophisticated filtering:

### Basic Configuration
```bash
# Enable in .env file
UPCOMING_ENABLED=true
UPCOMING_DAYS_AHEAD=90               # Look 90 days ahead
UPCOMING_MAX_MOVIES=50               # Process up to 50 movies
UPCOMING_MAX_TRAILERS_PER_MOVIE=3    # Download 1-5 trailers per movie
```

### Advanced Filtering System
```bash
# Geographic filtering
UPCOMING_FILTER_COUNTRIES=US,GB,CA,AU          # ISO country codes
UPCOMING_FILTER_LANGUAGES=en,en-US             # Language preferences

# Content filtering  
UPCOMING_FILTER_GENRES=28,12,878,53            # Action, Adventure, Sci-Fi, Thriller
UPCOMING_EXCLUDE_GENRES=27,9648,99             # Exclude Horror, Mystery, Documentary

# Production filtering
UPCOMING_FILTER_STUDIOS=Marvel,Disney,Warner,Universal
UPCOMING_FILTER_DIRECTORS=Christopher Nolan,Denis Villeneuve
UPCOMING_FILTER_ACTORS=                        # Optional actor filtering

# Quality filtering
UPCOMING_MIN_VOTE_AVERAGE=6.0                  # Minimum TMDB rating
UPCOMING_MIN_VOTE_COUNT=100                    # Minimum votes required
UPCOMING_MIN_BUDGET=10000000                   # Minimum budget ($10M+)
UPCOMING_MIN_RUNTIME=90                        # Minimum runtime (minutes)
UPCOMING_MAX_RUNTIME=180                       # Maximum runtime (minutes)

# Content rating filtering
UPCOMING_FILTER_RATINGS=G,PG,PG-13,R          # Include these ratings
UPCOMING_EXCLUDE_RATINGS=NC-17                # Exclude these ratings
```

### Genre Reference
```bash
# Complete TMDB Genre ID Reference:
# 28=Action, 12=Adventure, 16=Animation, 35=Comedy, 80=Crime, 99=Documentary,
# 18=Drama, 10751=Family, 14=Fantasy, 36=History, 27=Horror, 10402=Music,
# 9648=Mystery, 10749=Romance, 878=Science Fiction, 10770=TV Movie,
# 53=Thriller, 10752=War, 37=Western
```

### Usage Examples
```bash
# List upcoming movies (no download)
python3 tmdb_upcoming.py --list-only

# Download trailers for upcoming movies
python3 tmdb_upcoming.py

# Clean up expired upcoming trailers
python3 tmdb_upcoming.py --cleanup
```

📖 **Complete filtering guide**: See [UPCOMING_MOVIES_USAGE.md](UPCOMING_MOVIES_USAGE.md)

## � Radarr Integration

Seamlessly integrate with your Radarr media management workflow:

### Configuration
```bash
# Enable in .env file
RADARR_ENABLED=true
RADARR_URL=http://localhost:7878
RADARR_API_KEY=your_radarr_api_key_here
RADARR_SYNC_MODE=hybrid                        # upcoming, radarr_only, or hybrid
```

### Operation Modes
- **`upcoming`** - Download trailers for popular upcoming movies (standard mode)
- **`radarr_only`** - Only download trailers for movies in your Radarr wanted list  
- **`hybrid`** - Smart combination: upcoming movies + prioritized Radarr content

### Benefits
- ✅ **Seamless workflow** - Integrates with existing Radarr setup
- ✅ **Intelligent placement** - Trailers placed in correct Radarr movie folders
- ✅ **Focused downloads** - Only relevant content based on your preferences
- ✅ **API synchronization** - Monitors Radarr for new wanted movies

📖 **Complete Radarr guide**: See [RADARR_INTEGRATION.md](RADARR_INTEGRATION.md)

## 🌐 Network Storage Support

Seamlessly work with movies stored on network shares:

### Supported Protocols
- **SMB/CIFS** - Windows shares, TrueNAS, Synology, QNAP
- **NFS** - Linux/Unix network file systems
- **SSH/SFTP** - Secure remote access

### Configuration Examples

**TrueNAS/FreeNAS (SMB):**
```bash
NETWORK_ENABLED=true
NETWORK_TYPE=smb
NETWORK_SERVER=192.168.1.100
NETWORK_SHARE=movies
NETWORK_USERNAME=your_truenas_username
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=WORKGROUP
NETWORK_MOUNT_POINT=/mnt/jellyfin-movies
```

**Synology DiskStation:**
```bash
NETWORK_ENABLED=true
NETWORK_TYPE=smb
NETWORK_SERVER=diskstation.local
NETWORK_SHARE=movies
NETWORK_USERNAME=your_synology_username
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=WORKGROUP
```

**Linux NFS:**
```bash
NETWORK_ENABLED=true
NETWORK_TYPE=nfs
NETWORK_SERVER=192.168.1.100
NETWORK_SHARE=/export/movies
NETWORK_NFS_VERSION=4
```

### Automatic Management
- ✅ **Automatic mounting** when needed
- ✅ **Credential validation** before operations
- ✅ **Clean unmounting** after completion
- ✅ **Error handling** for network issues

## 📁 Jellyfin Cinema Mode Integration

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

## 🖥️ Web Dashboard & Monitoring

### Web Dashboard (Port 8085)
Access your trailer management interface at `http://localhost:8085`:
- 📊 **Download statistics** and progress tracking
- 🎬 **Movie library overview** with trailer status
- ⚙️ **Configuration management** through web interface
- 📈 **Performance metrics** and system health

### Real-Time Monitoring
```bash
# Enable monitoring in .env
ENABLE_MONITORING=true
MONITOR_TYPE=filesystem              # Real-time file system watching
MONITOR_DELAY=5                      # Seconds to wait after detecting changes

# Start monitoring service
python3 tmdb_monitor.py              # Native execution
# or
docker-compose --profile monitor up -d tmdb-monitor  # Docker
```

### Scheduled Operations
```bash
# Configure automatic scanning
SCHEDULE_ENABLED=true
SCHEDULE_INTERVAL=60                 # Minutes between scans
SCHEDULE_TIME=02:00                  # Daily scan time (HH:MM)

# Start scheduler service
python3 tmdb_scheduler.py
```

### Background Service Mode
```bash
# Run as background service
SERVICE_MODE=true
SERVICE_PID_FILE=/var/run/tmdb-monitor.pid

# Service will run continuously and handle:
# - Automatic library scanning
# - Upcoming movie updates
# - Network share management
# - Error recovery and logging
```

## ⚙️ Configuration Options

### Environment Configuration (.env file)
The recommended secure method for all settings:

```bash
# ================================
# TMDB API Configuration  
# ================================
TMDB_API_KEY=your_tmdb_api_key_here

# ================================
# Jellyfin Movies Path
# ================================
JELLYFIN_MOVIES_PATH=/path/to/your/jellyfin/movies/library

# ================================
# Download Settings
# ================================
DOWNLOAD_QUALITY=best                           # best, 1080p, 720p, 480p
MAX_TRAILERS_PER_MOVIE=5                       # Max trailers for library scanning
SKIP_EXISTING=true                             # Skip movies that already have trailers
OVERWRITE_EXISTING=false                       # Overwrite existing trailers

# ================================
# Network Share Configuration
# ================================
NETWORK_ENABLED=false                          # Enable network mounting
NETWORK_TYPE=smb                               # smb, nfs, ssh/sftp
NETWORK_SERVER=192.168.1.100                  # Server IP or hostname
NETWORK_SHARE=movies                           # Share name
NETWORK_USERNAME=your_username                 # Authentication
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=WORKGROUP                       # SMB domain
NETWORK_MOUNT_POINT=/mnt/jellyfin-movies      # Local mount point
NETWORK_AUTO_MOUNT=true                        # Auto mount/unmount

# ================================
# Upcoming Movies Configuration
# ================================
UPCOMING_ENABLED=false                         # Enable upcoming movies feature
UPCOMING_DAYS_AHEAD=90                         # Days to look ahead
UPCOMING_MAX_MOVIES=50                         # Max movies to process
UPCOMING_MAX_TRAILERS_PER_MOVIE=3             # Trailers per upcoming movie
UPCOMING_POPULARITY_THRESHOLD=10.0            # Minimum popularity score
UPCOMING_CLEANUP_DAYS=30                      # Days before cleaning old trailers

# Filtering options (see UPCOMING_MOVIES_USAGE.md for complete list)
UPCOMING_FILTER_COUNTRIES=US,GB,CA,AU
UPCOMING_FILTER_GENRES=28,12,878,53           # Action, Adventure, Sci-Fi, Thriller  
UPCOMING_EXCLUDE_GENRES=27,9648,99            # Exclude Horror, Mystery, Documentary
UPCOMING_MIN_VOTE_AVERAGE=6.0
UPCOMING_MIN_VOTE_COUNT=100

# ================================
# Radarr Integration
# ================================
RADARR_ENABLED=false
RADARR_URL=http://localhost:7878
RADARR_API_KEY=your_radarr_api_key_here
RADARR_SYNC_MODE=upcoming                     # upcoming, radarr_only, or hybrid

# ================================
# Web Dashboard  
# ================================
DASHBOARD_ENABLED=false
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8085                           # Port 8085 (avoids media stack conflicts)
DASHBOARD_DEBUG=false

# ================================
# Monitoring & Automation
# ================================
ENABLE_MONITORING=false                       # Real-time monitoring
MONITOR_TYPE=filesystem                       # filesystem, scheduled, disabled
MONITOR_DELAY=5                               # Seconds after file changes

SCHEDULE_ENABLED=false                        # Scheduled scanning
SCHEDULE_INTERVAL=60                          # Minutes between scans
SCHEDULE_TIME=02:00                           # Daily scan time

SERVICE_MODE=false                            # Background service mode
SERVICE_PID_FILE=/var/run/tmdb-monitor.pid

# ================================
# Performance & Logging
# ================================
MAX_CONCURRENT_DOWNLOADS=3
DOWNLOAD_TIMEOUT=300
RETRY_ATTEMPTS=3
RETRY_DELAY=5

LOG_LEVEL=INFO                                # DEBUG, INFO, WARNING, ERROR
LOG_FILE=                                     # Leave empty for console only
```

📖 **Complete configuration guide**: See [ENV_CONFIG.md](ENV_CONFIG.md)

## 📋 Requirements

- **Python 3.7+** (Python 3.9+ recommended)
- **yt-dlp** - Video downloading (`pip install yt-dlp`)
- **python-dotenv** - Environment configuration (`pip install python-dotenv`)
- **TMDB API key** - Free from https://www.themoviedb.org/settings/api
- **Network tools** (for network shares):
  - `cifs-utils` (SMB/CIFS support)
  - `nfs-common` (NFS support)  
  - `sshfs` (SSH/SFTP support)

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install system dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install cifs-utils nfs-common sshfs

# Install system dependencies (CentOS/RHEL)
sudo yum install cifs-utils nfs-utils fuse-sshfs
```

## 📖 Usage Examples

### Library Scanning
```bash
# Scan existing library for missing trailers
python3 enhanced_downloader.py --scan-existing

# Include movies that already have trailers  
python3 enhanced_downloader.py --scan-existing --include-existing

# Custom quality setting
python3 enhanced_downloader.py --scan-existing --quality 1080p

# Test configuration without downloading
python3 enhanced_downloader.py --test-config
```

### Single Movie Processing
```bash
# Download trailers for specific movie
python3 enhanced_downloader.py --title "The Matrix" --year 1999

# Specify custom trailer count
python3 enhanced_downloader.py --title "Inception" --year 2010 --max-trailers 5
```

### Upcoming Movies
```bash
# List upcoming movies (no download)
python3 tmdb_upcoming.py --list-only

# Download trailers for upcoming movies
python3 tmdb_upcoming.py

# Clean up expired upcoming trailers (older than UPCOMING_CLEANUP_DAYS)
python3 tmdb_upcoming.py --cleanup
```

### Monitoring & Services
```bash
# Real-time filesystem monitoring
python3 tmdb_monitor.py

# Scheduled scanning every 60 minutes  
python3 tmdb_scheduler.py --interval 60

# Web dashboard on port 8085
python3 tmdb_dashboard.py

# Background service mode
python3 tmdb_monitor.py --service
```

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
## 🐳 Docker Deployment

### Production Docker Setup
```bash
# Quick start with Docker
cp .env.example .env
nano .env  # Configure your settings

# One-time library scan
docker-compose --profile scanner up tmdb-scanner

# Enable web dashboard (port 8085)
docker-compose --profile dashboard up -d tmdb-dashboard

# Start background monitoring
docker-compose --profile monitor up -d tmdb-monitor

# Upcoming movies service
docker-compose --profile upcoming up -d tmdb-upcoming
```

### Docker Profiles
- **`scanner`** - One-time library scanning
- **`dashboard`** - Web management interface (port 8085)
- **`monitor`** - Real-time filesystem monitoring
- **`upcoming`** - Upcoming movies processing
- **`scheduler`** - Scheduled scanning operations

### Standalone Testing
```bash
# Test without .env file dependency
docker-compose -f docker-compose.testing.yml up tmdb-scanner-test
```

📖 **Complete Docker guide**: See [DOCKER.md](DOCKER.md)

## 🚨 Troubleshooting

### Configuration Validation
```bash
# Test your configuration
python3 enhanced_downloader.py --test-config

# Validate network connectivity
python3 -c "from network_mount_helper import NetworkMounter; NetworkMounter().test_connection()"
```

### Network Share Issues
```bash
# Check if share is mounted
mount | grep jellyfin

# Test manual SMB mount
sudo mount -t cifs //server/movies /mnt/test -o username=user,password=pass

# Test NFS mount
sudo mount -t nfs server:/export/movies /mnt/test

# Check network connectivity
ping your-nas-server
telnet your-nas-server 445  # SMB port
telnet your-nas-server 2049 # NFS port
```

### Permission Problems
- Ensure user has **read/write access** to Jellyfin movies directory
- Verify **network credentials** are correct
- Check **firewall settings** for required ports:
  - SMB/CIFS: Port 445
  - NFS: Port 2049  
  - SSH/SFTP: Port 22

### Common Issues
1. **TMDB API rate limits** - Script includes automatic retry logic
2. **yt-dlp failures** - Update yt-dlp: `pip install --upgrade yt-dlp`
3. **Network timeouts** - Increase `DOWNLOAD_TIMEOUT` in .env
4. **Disk space** - Monitor available space, enable cleanup

## 🔑 Getting a TMDB API Key

1. Visit https://www.themoviedb.org/
2. Create a free account
3. Go to **Settings → API**  
4. Request an API key (choose "Developer" option)
5. Copy the API key to your `.env` file as `TMDB_API_KEY`

## 📊 Logging & Monitoring

### Log Configuration
```bash
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR
LOG_FILE=/var/log/tmdb.log       # File path or empty for console only
```

### Log Locations
- **Console output** - Real-time colored formatting
- **Log files** - Persistent storage with rotation
- **Docker logs** - `docker-compose logs tmdb-scanner`
- **Service logs** - systemd integration available

### What Gets Logged
- ✅ **Download progress** and completion status
- ✅ **Network operations** (mount/unmount activities)  
- ✅ **API interactions** with TMDB
- ✅ **Error details** with retry information
- ✅ **Performance metrics** and timing data

## 📁 Output Structure

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

### Upcoming Movies Structure
```
/your/jellyfin/movies/
└── _upcoming/                         ← Upcoming movies folder
    ├── Weapons (2025)/
    │   └── trailers/
    │       ├── Weapons-trailer-1.mp4
    │       └── Weapons-trailer-2.mp4
    └── Freakier Friday (2025)/
        └── trailers/
            └── Freakier Friday-trailer-1.mp4
```

After running this script, the [Jellyfin Cinema Mode plugin](https://github.com/CherryFloors/jellyfin-plugin-cinemamode) will automatically find and play these trailers before your movies!

## 📚 Documentation

### Complete Guides
- 📖 **[UPCOMING_MOVIES_USAGE.md](UPCOMING_MOVIES_USAGE.md)** - Complete upcoming movies configuration
- 🔗 **[RADARR_INTEGRATION.md](RADARR_INTEGRATION.md)** - Radarr workflow integration  
- 🐳 **[DOCKER.md](DOCKER.md)** - Docker deployment guide
- ⚙️ **[ENV_CONFIG.md](ENV_CONFIG.md)** - Environment configuration reference
- 🔧 **[LOCAL_SETUP.md](LOCAL_SETUP.md)** - Local Python installation
- 🧪 **[TESTING.md](TESTING.md)** - Testing and validation

### Quick References
- 📋 **[PORT_REFERENCE.md](PORT_REFERENCE.md)** - Port usage and conflicts
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

## 🤝 Contributing & Support

### Reporting Issues
- 🐛 **Bug reports** - Include logs and configuration details
- 💡 **Feature requests** - Describe your use case
- 📚 **Documentation** - Help improve guides and examples

### Development
- **Python 3.9+** recommended for development
- **Testing environment** available with `docker-compose.testing.yml`
- **Code formatting** with Black and isort
- **Type hints** encouraged for new code

### Community
- ⭐ **Star this repo** if it's helpful!
- 📢 **Share your setup** - Help others learn from your configuration
- 🔗 **Integration stories** - Show us your Jellyfin + Radarr workflows

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[TMDB](https://www.themoviedb.org/)** - The Movie Database for comprehensive movie data
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Robust video downloading capabilities  
- **[Jellyfin](https://jellyfin.org/)** - Open-source media server platform
- **[Cinema Mode Plugin](https://github.com/CherryFloors/jellyfin-plugin-cinemamode)** - Seamless trailer integration
- **[Radarr](https://radarr.video/)** - Automated movie collection management

---

**Version**: 3.2.0 | **Status**: Production Ready ✅ | **Last Updated**: August 2025
