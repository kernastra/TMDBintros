# Environment Configuration Guide

This enhanced version of the TMDB Trailer Downloader supports comprehensive configuration through environment variables and `.env` files.

## Quick Start

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your settings:**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Test your configuration:**
   ```bash
   python3 enhanced_downloader.py --test-config
   ```

4. **Run the downloader:**
   ```bash
   python3 enhanced_downloader.py --scan-existing
   ```

## Configuration Options

### Required Settings

| Variable | Description | Example |
|----------|-------------|---------|
| `TMDB_API_KEY` | Your TMDB API key | `9d6e23004c15bbfb434479fcaac0a844` |
| `JELLYFIN_MOVIES_PATH` | Path to Jellyfin movies library | `/mnt/jellyfin-movies` |

### Network Share Settings (Optional)

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `NETWORK_ENABLED` | Enable automatic network mounting | `false` | `true` |
| `NETWORK_TYPE` | Share type (smb, nfs, sshfs) | `smb` | `smb` |
| `NETWORK_SERVER` | Server IP or hostname | - | `192.168.1.10` |
| `NETWORK_SHARE` | Share name/path | - | `movies` |
| `NETWORK_USERNAME` | Username for authentication | - | `myuser` |
| `NETWORK_PASSWORD` | Password for authentication | - | `mypass` |
| `NETWORK_DOMAIN` | Windows domain | `WORKGROUP` | `MYDOMAIN` |
| `NETWORK_MOUNT_POINT` | Local mount point | `/mnt/jellyfin-movies` | `/mnt/nas` |
| `NETWORK_AUTO_MOUNT` | Auto mount/unmount | `true` | `true` |

### Download Settings

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DOWNLOAD_QUALITY` | Video quality preference | `best` | `720p` |
| `MAX_TRAILERS_PER_MOVIE` | Maximum trailers per movie | `5` | `3` |
| `SKIP_EXISTING` | Skip if trailers exist | `true` | `false` |
| `OVERWRITE_EXISTING` | Overwrite existing files | `false` | `true` |
| `DOWNLOAD_TIMEOUT` | Download timeout (seconds) | `300` | `600` |
| `MAX_CONCURRENT_DOWNLOADS` | Parallel downloads | `3` | `5` |
| `RETRY_ATTEMPTS` | Retry failed downloads | `3` | `5` |
| `RETRY_DELAY` | Delay between retries (seconds) | `5` | `10` |

### Advanced Settings

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `LOG_LEVEL` | Logging level | `INFO` | `DEBUG` |
| `LOG_FILE` | Log file path | - | `/var/log/tmdb-downloader.log` |
| `SCAN_RECURSIVE` | Recursive directory scanning | `true` | `false` |
| `MOVIE_FOLDER_PATTERN` | Regex for movie folders | `^(.+?)\\s*\\((\\d{4})\\).*$` | Custom regex |

## Network Share Examples

### Synology NAS (SMB)
```bash
NETWORK_ENABLED=true
NETWORK_TYPE=smb
NETWORK_SERVER=192.168.1.10
NETWORK_SHARE=movies
NETWORK_USERNAME=myuser
NETWORK_PASSWORD=mypassword
NETWORK_DOMAIN=WORKGROUP
```

### TrueNAS Scale (NFS)
```bash
NETWORK_ENABLED=true
NETWORK_TYPE=nfs
NETWORK_SERVER=192.168.1.20
NETWORK_SHARE=/mnt/tank/movies
NETWORK_NFS_VERSION=4
```

### Remote Server (SSH/SFTP)
```bash
NETWORK_ENABLED=true
NETWORK_TYPE=sshfs
NETWORK_SERVER=192.168.1.30
NETWORK_USERNAME=mediauser
NETWORK_SSH_KEY=/home/user/.ssh/id_rsa
NETWORK_REMOTE_PATH=/volume1/movies
```

### Windows Server (SMB with Domain)
```bash
NETWORK_ENABLED=true
NETWORK_TYPE=smb
NETWORK_SERVER=mediaserver.company.com
NETWORK_SHARE=movies
NETWORK_USERNAME=mediauser
NETWORK_PASSWORD=complexpassword
NETWORK_DOMAIN=COMPANY
```

## Usage Examples

### Basic Usage
```bash
# Test configuration
python3 enhanced_downloader.py --test-config

# Scan existing movies
python3 enhanced_downloader.py --scan-existing

# Download specific movie
python3 enhanced_downloader.py --title "The Matrix" --year 1999
```

### Advanced Usage
```bash
# Override quality for single download
python3 enhanced_downloader.py --title "Inception" --quality 1080p

# Use different config directory
python3 enhanced_downloader.py --config-dir /etc/tmdb-downloader --scan-existing

# Create environment template in different location
python3 enhanced_downloader.py --config-dir /path/to/config --create-env
```

## Security Best Practices

1. **Protect your `.env` file:**
   ```bash
   chmod 600 .env
   ```

2. **Never commit `.env` to version control:**
   - The `.gitignore` file already excludes `.env` files
   - Use `.env.example` for sharing configuration templates

3. **Use SSH keys instead of passwords when possible:**
   ```bash
   NETWORK_TYPE=sshfs
   NETWORK_SSH_KEY=/home/user/.ssh/id_rsa
   # Don't set NETWORK_PASSWORD
   ```

4. **Consider using a dedicated service account:**
   - Create a specific user for media access
   - Grant minimal required permissions

## Troubleshooting

### Configuration Issues
```bash
# Validate configuration
python3 enhanced_downloader.py --test-config

# Check environment loading
python3 config_manager.py
```

### Network Mount Issues
```bash
# Test manual mounting
sudo mount -t cifs //server/share /mnt/test -o username=user,password=pass

# Check mount status
mount | grep jellyfin
df -h /mnt/jellyfin-movies
```

### Permission Issues
```bash
# Check file permissions
ls -la .env

# Fix permissions
chmod 600 .env
```

## Migration from JSON Config

The system automatically falls back to `config.json` if environment variables aren't set:

1. **Keep using JSON:** Just don't create a `.env` file
2. **Migrate gradually:** Set some variables in `.env`, keep others in JSON
3. **Full migration:** Move all settings to `.env` and remove `config.json`

## Environment Variable Precedence

1. **System environment variables** (highest priority)
2. **`.env` file variables**
3. **JSON configuration file** (fallback)
4. **Default values** (lowest priority)

This allows for flexible deployment scenarios where you can override specific settings without changing the base configuration.
