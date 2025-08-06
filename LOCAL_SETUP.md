# Running TMDB Trailer Downloader Locally with SMB

This guide shows you how to run the TMDB Trailer Downloader directly with Python on your local machine, connecting to your SMB/network shares.

## Prerequisites

### System Requirements
- Python 3.8 or higher
- `cifs-utils` for SMB mounting (Linux)
- Access to your SMB/network share

### Install SMB Support (Linux)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install cifs-utils

# CentOS/RHEL/Fedora
sudo yum install cifs-utils
# or
sudo dnf install cifs-utils
```

## Quick Setup

### 1. Configure Your Environment

Copy the template and edit with your settings:
```bash
cp .env.local .env.local
```

Edit `.env.local` with your details:
```bash
# Required: Your TMDB API key
TMDB_API_KEY=9d6e23004c15bbfb434479fcaac0a844

# SMB Configuration
NETWORK_ENABLED=true
NETWORK_TYPE=smb
NETWORK_SERVER=192.168.1.100       # Your NAS/server IP
NETWORK_SHARE=movies               # SMB share name
NETWORK_USERNAME=your_username
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=WORKGROUP          # Or your domain
NETWORK_MOUNT_POINT=/mnt/jellyfin-movies
```

### 2. Run the Application

```bash
# Setup environment and install dependencies
python3 run_local.py setup

# Scan your existing movie library
python3 run_local.py scan

# Download trailers for upcoming movies
python3 run_local.py upcoming

# Start the web dashboard
python3 run_local.py dashboard

# Start continuous monitoring
python3 run_local.py monitor
```

## Common SMB Configurations

### Synology NAS
```bash
NETWORK_SERVER=192.168.1.100
NETWORK_SHARE=video/movies
NETWORK_USERNAME=your_synology_user
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=WORKGROUP
```

### QNAP NAS
```bash
NETWORK_SERVER=192.168.1.101
NETWORK_SHARE=movies
NETWORK_USERNAME=your_qnap_user
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=WORKGROUP
```

### Windows Share
```bash
NETWORK_SERVER=192.168.1.102
NETWORK_SHARE=Movies
NETWORK_USERNAME=your_windows_user
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=YOUR_DOMAIN
```

### Unraid
```bash
NETWORK_SERVER=192.168.1.103
NETWORK_SHARE=movies
NETWORK_USERNAME=your_unraid_user
NETWORK_PASSWORD=your_password
NETWORK_DOMAIN=WORKGROUP
```

## Advanced Configuration

### Manual SMB Mount

If you prefer to mount SMB manually:

```bash
# Create mount point
sudo mkdir -p /mnt/jellyfin-movies

# Mount SMB share
sudo mount -t cifs //192.168.1.100/movies /mnt/jellyfin-movies \
  -o username=your_user,password=your_pass,domain=WORKGROUP,uid=$UID,gid=$GID

# Set in .env.local
NETWORK_ENABLED=false
JELLYFIN_MOVIES_PATH=/mnt/jellyfin-movies
```

### Alternative: Local Directory for Testing

```bash
# Use local directory (for testing)
NETWORK_ENABLED=false
JELLYFIN_MOVIES_PATH=/home/sean/Movies
```

## Command Reference

### Basic Commands
```bash
# Install dependencies only
python3 run_local.py --no-mount setup

# Skip SMB mounting (if already mounted)
python3 run_local.py --no-mount scan

# Use different config file
python3 run_local.py --env .env.production scan

# Skip dependency check
python3 run_local.py --no-deps scan
```

### Library Scanning
```bash
# Scan existing movies for missing trailers
python3 run_local.py scan

# Force re-download trailers (set OVERWRITE_EXISTING=true in config)
python3 run_local.py scan
```

### Upcoming Movies
```bash
# Download trailers for upcoming movies
python3 run_local.py upcoming

# This will:
# - Query TMDB for upcoming movies
# - Apply your filters (country, genre, rating, etc.)
# - Download trailers for matching movies
# - Organize them in your movie library
```

### Web Dashboard
```bash
# Start dashboard (access at http://localhost:8085)
python3 run_local.py dashboard

# The dashboard provides:
# - Real-time status monitoring
# - Configuration management
# - Manual scan triggers
# - Download progress tracking
```

### File System Monitoring
```bash
# Monitor for new movies and auto-download trailers
python3 run_local.py monitor

# This will:
# - Watch your movie directory for new folders
# - Automatically download trailers for new movies
# - Run continuously in background
```

## Directory Structure

Your movie library should follow this structure:
```
/mnt/jellyfin-movies/
├── Movie Name (2024)/
│   ├── Movie Name (2024).mkv
│   ├── trailer_1.mp4          # Downloaded by this tool
│   └── trailer_2.mp4
├── Another Movie (2023)/
│   ├── Another Movie (2023).mp4
│   └── trailer_1.mp4
└── Upcoming Movie (2025)/     # Created by upcoming feature
    ├── trailer_1.mp4          # Downloaded before movie release
    ├── trailer_2.mp4
    └── trailer_3.mp4
```

## Troubleshooting

### SMB Mount Issues

**Permission Denied:**
```bash
# Add yourself to necessary groups
sudo usermod -a -G users $USER
sudo usermod -a -G sambashare $USER

# Log out and back in, then try again
```

**Mount Failed:**
```bash
# Test SMB connection manually
smbclient -L //192.168.1.100 -U your_username

# Check if cifs-utils is installed
dpkg -l | grep cifs-utils

# Try different SMB version
sudo mount -t cifs //192.168.1.100/movies /mnt/jellyfin-movies \
  -o username=your_user,password=your_pass,vers=2.0
```

### Python Dependencies

**Missing Modules:**
```bash
# Install in virtual environment
python3 -m venv tmdb_env
source tmdb_env/bin/activate
pip install -r requirements.txt
python3 run_local.py scan
```

### Network Issues

**Can't Reach Server:**
```bash
# Test network connectivity
ping 192.168.1.100

# Test SMB port
telnet 192.168.1.100 445

# Check firewall
sudo ufw status
```

### File Permissions

**Can't Write Files:**
```bash
# Check mount options include your UID/GID
mount | grep cifs

# Remount with correct permissions
sudo umount /mnt/jellyfin-movies
sudo mount -t cifs //server/share /mnt/jellyfin-movies \
  -o username=user,password=pass,uid=$UID,gid=$GID
```

## Performance Tips

### Large Libraries
- Set `MAX_CONCURRENT_DOWNLOADS=1` for stability
- Use `SCAN_RECURSIVE=false` if movies aren't in subdirectories
- Enable `SKIP_EXISTING=true` to avoid re-processing

### Network Performance
- Mount SMB with `cache=strict` for better performance
- Use wired connection for large downloads
- Consider running during off-peak hours

### Filtering for Efficiency
- Use specific genre filters to reduce API calls
- Set higher `UPCOMING_MIN_VOTE_COUNT` for popular movies only
- Limit `UPCOMING_MAX_MOVIES` for faster processing

## Integration with Media Servers

### Jellyfin
The tool creates trailers in the same directory as movies, which Jellyfin automatically detects.

### Plex
Trailers are named `trailer_1.mp4`, `trailer_2.mp4` which Plex recognizes.

### Emby
Similar to Jellyfin, trailers are auto-detected in movie folders.

## Security Notes

- Store credentials securely in `.env.local`
- Don't commit `.env.local` to version control
- Consider using SMB key-based authentication
- Run with minimal required permissions

## Next Steps

Once running locally:
1. Monitor logs in `tmdb_local.log`
2. Check web dashboard at http://localhost:8085
3. Set up automated scanning with cron
4. Consider migrating to Docker for production
