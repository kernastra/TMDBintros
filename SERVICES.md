# Running TMDB Trailer Services

This document explains how to run the TMDB Trailer Downloader monitoring services as system services on Linux.

## Systemd Service Files

### Real-time Monitor Service

Create `/etc/systemd/system/tmdb-monitor.service`:

```ini
[Unit]
Description=TMDB Trailer Monitor - Real-time file system monitoring
After=network.target
Wants=network.target

[Service]
Type=simple
User=jellyfin
Group=jellyfin
WorkingDirectory=/opt/tmdb-trailer-downloader
ExecStart=/usr/bin/python3 /opt/tmdb-trailer-downloader/tmdb_monitor.py --config-dir /etc/tmdb-trailer-downloader
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Environment file
EnvironmentFile=/etc/tmdb-trailer-downloader/.env

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/mnt/jellyfin-movies /var/log/tmdb-trailer-downloader

[Install]
WantedBy=multi-user.target
```

### Scheduled Scanner Service

Create `/etc/systemd/system/tmdb-scheduler.service`:

```ini
[Unit]
Description=TMDB Trailer Scheduler - Periodic scanning service
After=network.target
Wants=network.target

[Service]
Type=simple
User=jellyfin
Group=jellyfin
WorkingDirectory=/opt/tmdb-trailer-downloader
ExecStart=/usr/bin/python3 /opt/tmdb-trailer-downloader/tmdb_scheduler.py --config-dir /etc/tmdb-trailer-downloader --interval 60
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal

# Environment file
EnvironmentFile=/etc/tmdb-trailer-downloader/.env

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/mnt/jellyfin-movies /var/log/tmdb-trailer-downloader

[Install]
WantedBy=multi-user.target
```

## Installation Steps

### 1. Create System User
```bash
sudo useradd -r -s /bin/false -d /opt/tmdb-trailer-downloader tmdb-trailer
sudo usermod -a -G jellyfin tmdb-trailer  # Add to jellyfin group if needed
```

### 2. Install Application
```bash
# Create directories
sudo mkdir -p /opt/tmdb-trailer-downloader
sudo mkdir -p /etc/tmdb-trailer-downloader
sudo mkdir -p /var/log/tmdb-trailer-downloader

# Copy application files
sudo cp -r /path/to/your/TMDBintros/* /opt/tmdb-trailer-downloader/
sudo cp .env.example /etc/tmdb-trailer-downloader/.env

# Set permissions
sudo chown -R tmdb-trailer:tmdb-trailer /opt/tmdb-trailer-downloader
sudo chown -R tmdb-trailer:tmdb-trailer /etc/tmdb-trailer-downloader
sudo chown -R tmdb-trailer:tmdb-trailer /var/log/tmdb-trailer-downloader
sudo chmod 600 /etc/tmdb-trailer-downloader/.env
```

### 3. Configure Environment
Edit `/etc/tmdb-trailer-downloader/.env`:

```bash
sudo nano /etc/tmdb-trailer-downloader/.env
```

Add your configuration:
```bash
TMDB_API_KEY=your_api_key_here
JELLYFIN_MOVIES_PATH=/mnt/jellyfin-movies
LOG_FILE=/var/log/tmdb-trailer-downloader/tmdb.log
# ... other settings
```

### 4. Install Dependencies
```bash
sudo pip3 install -r /opt/tmdb-trailer-downloader/requirements.txt
```

### 5. Enable and Start Services

**For real-time monitoring:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable tmdb-monitor.service
sudo systemctl start tmdb-monitor.service
```

**For scheduled scanning:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable tmdb-scheduler.service
sudo systemctl start tmdb-scheduler.service
```

## Service Management

### Check Status
```bash
sudo systemctl status tmdb-monitor.service
sudo systemctl status tmdb-scheduler.service
```

### View Logs
```bash
sudo journalctl -u tmdb-monitor.service -f
sudo journalctl -u tmdb-scheduler.service -f
```

### Stop/Start Services
```bash
sudo systemctl stop tmdb-monitor.service
sudo systemctl start tmdb-monitor.service
sudo systemctl restart tmdb-monitor.service
```

## Docker Alternative

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cifs-utils \
    nfs-common \
    sshfs \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -r -u 1000 tmdb-trailer

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set permissions
RUN chown -R tmdb-trailer:tmdb-trailer /app
USER tmdb-trailer

# Default command
CMD ["python3", "tmdb_monitor.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  tmdb-monitor:
    build: .
    container_name: tmdb-trailer-monitor
    restart: unless-stopped
    environment:
      - TMDB_API_KEY=${TMDB_API_KEY}
      - JELLYFIN_MOVIES_PATH=/movies
    volumes:
      - /path/to/jellyfin/movies:/movies
      - ./logs:/app/logs
    env_file:
      - .env
    command: python3 tmdb_monitor.py
    
  tmdb-scheduler:
    build: .
    container_name: tmdb-trailer-scheduler
    restart: unless-stopped
    environment:
      - TMDB_API_KEY=${TMDB_API_KEY}
      - JELLYFIN_MOVIES_PATH=/movies
    volumes:
      - /path/to/jellyfin/movies:/movies
      - ./logs:/app/logs
    env_file:
      - .env
    command: python3 tmdb_scheduler.py --interval 120
```

Run with:
```bash
docker-compose up -d
```

## Troubleshooting

### Service Won't Start
1. Check service logs: `sudo journalctl -u tmdb-monitor.service`
2. Verify configuration: `python3 enhanced_downloader.py --test-config`
3. Check file permissions on `/etc/tmdb-trailer-downloader/.env`
4. Ensure Python dependencies are installed

### Network Mount Issues
1. Test manual mount: `sudo mount -t cifs //server/share /mnt/test`
2. Check network connectivity: `ping server-ip`
3. Verify credentials in environment file
4. Check firewall rules (SMB: 445, NFS: 2049, SSH: 22)

### Permission Errors
1. Check ownership: `ls -la /path/to/jellyfin/movies`
2. Verify user is in correct group: `groups tmdb-trailer`
3. Test write access: `sudo -u tmdb-trailer touch /path/to/jellyfin/movies/test`

### Log Files
- Application logs: `/var/log/tmdb-trailer-downloader/`
- System logs: `sudo journalctl -u tmdb-monitor.service`
- File system events: Check `dmesg` for mount/unmount messages
