# Docker Deployment Guide

This document explains how to run the TMDB Trailer Downloader using Docker and Docker Compose.

## Quick Start

### 1. Copy the Docker Environment File
```bash
cp .env.docker .env
```

### 2. Edit Configuration
```bash
nano .env
```

**Required settings:**
```bash
TMDB_API_KEY=your_tmdb_api_key_here
HOST_MOVIES_PATH=/path/to/your/jellyfin/movies
```

### 3. Choose Your Deployment Mode

**One-time scan:**
```bash
docker-compose --profile scanner up tmdb-scanner
```

**Real-time monitoring:**
```bash
docker-compose --profile monitor up -d tmdb-monitor
```

**Scheduled scanning:**
```bash
docker-compose --profile scheduler up -d tmdb-scheduler
```

## Deployment Options

### Option 1: One-Time Scanning

Perfect for **manual execution** or **cron jobs**:

```bash
# Run once and exit
docker-compose --profile scanner up tmdb-scanner

# Check logs
docker-compose logs tmdb-scanner
```

### Option 2: Real-Time Monitoring

Best for **continuous operation** with instant detection:

```bash
# Start real-time monitoring
docker-compose --profile monitor up -d tmdb-monitor

# View logs
docker-compose logs -f tmdb-monitor

# Stop monitoring
docker-compose --profile monitor down
```

### Option 3: Scheduled Scanning

Ideal for **periodic operations** with lower resource usage:

```bash
# Start scheduled scanner (every 60 minutes by default)
docker-compose --profile scheduler up -d tmdb-scheduler

# Custom interval (every 30 minutes)
SCHEDULE_INTERVAL=30 docker-compose --profile scheduler up -d tmdb-scheduler

# View logs
docker-compose logs -f tmdb-scheduler
```

### Option 4: All Services

Run **everything** (not recommended unless needed):

```bash
# Start all services
docker-compose --profile all up -d

# Stop all services
docker-compose --profile all down
```

## Configuration Examples

### Local Movies Directory

```bash
# .env file
TMDB_API_KEY=your_api_key_here
HOST_MOVIES_PATH=/home/user/jellyfin/movies
NETWORK_ENABLED=false
```

### Network Share (SMB/CIFS)

```bash
# .env file
TMDB_API_KEY=your_api_key_here
HOST_MOVIES_PATH=/mnt/movies  # Mount point in container
NETWORK_ENABLED=true
NETWORK_TYPE=smb
NETWORK_SERVER=192.168.1.100
NETWORK_SHARE=movies
NETWORK_USERNAME=jellyfin
NETWORK_PASSWORD=secure_password
NETWORK_DOMAIN=WORKGROUP
PRIVILEGED_MODE=true  # Required for network mounting
```

### NFS Share

```bash
# .env file
TMDB_API_KEY=your_api_key_here
HOST_MOVIES_PATH=/mnt/movies
NETWORK_ENABLED=true
NETWORK_TYPE=nfs
NETWORK_SERVER=192.168.1.100
NETWORK_SHARE=/volume1/movies
PRIVILEGED_MODE=true
```

### SSH/SFTP Share

```bash
# .env file
TMDB_API_KEY=your_api_key_here
HOST_MOVIES_PATH=/mnt/movies
NETWORK_ENABLED=true
NETWORK_TYPE=sshfs
NETWORK_SERVER=user@192.168.1.100
NETWORK_SHARE=/path/to/movies
PRIVILEGED_MODE=true
```

## Building the Image

### Build Locally
```bash
# Build with default tag
docker build -t tmdb-trailer-downloader:latest .

# Build with custom tag
docker build -t tmdb-trailer-downloader:v1.0.0 .

# Build with build args
docker build \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VERSION=v1.0.0 \
  -t tmdb-trailer-downloader:v1.0.0 .
```

### Build via Docker Compose
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build tmdb-monitor

# Build with no cache
docker-compose build --no-cache
```

## Volume Management

### Important Volumes

```yaml
volumes:
  # Your Jellyfin movies (READ/WRITE)
  - ${HOST_MOVIES_PATH}:/movies
  
  # Application logs (PERSISTENT)
  - ./logs:/app/logs
  
  # Download cache (PERSISTENT) 
  - ./cache:/app/cache
  
  # Environment config (READ-ONLY)
  - ./.env:/app/.env:ro
```

### Volume Permissions

**Fix permission issues:**
```bash
# Create directories with correct permissions
sudo mkdir -p ./logs ./cache
sudo chown -R 1000:1000 ./logs ./cache

# For movies directory
sudo chown -R 1000:1000 /path/to/jellyfin/movies
# OR add your user to group 1000
sudo usermod -a -G 1000 $USER
```

## Network Configuration

### Internal Network
All services use the `tmdb-network` bridge network for internal communication.

### External Access
The dashboard service exposes a web interface:
```bash
DASHBOARD_PORT=8080 docker-compose --profile dashboard up -d tmdb-dashboard
```

**Web Dashboard Features:**
- 📊 **Real-time statistics** (movies, trailers, disk usage)
- 🔄 **Service status monitoring** (monitor, scheduler, API)
- 📁 **Movie library overview** with trailer counts
- 📝 **Live activity logs** with filtering
- 🔄 **Auto-refresh** every 30 seconds

Access at: http://localhost:8080

## Security Considerations

### Privileged Mode
Network mounting requires privileged mode:
```bash
PRIVILEGED_MODE=true
```

**Security implications:**
- ⚠️ **Full system access** within container
- ✅ **Required** for SMB/NFS/SSHFS mounting
- ✅ **Isolated** in container environment

### Environment File Security
```bash
# Secure the environment file
chmod 600 .env

# Never commit to version control
echo ".env" >> .gitignore
```

### Network Credentials
```bash
# Use strong passwords
NETWORK_PASSWORD=Very$ecure!Pa$$w0rd

# Consider SSH keys for SSHFS
# (mount SSH key into container)
```

## Monitoring and Logs

### View Live Logs
```bash
# Single service
docker-compose logs -f tmdb-monitor

# All services
docker-compose logs -f

# With timestamps
docker-compose logs -f -t tmdb-monitor
```

### Log Files Location
```bash
# Host location
./logs/tmdb-monitor.log
./logs/tmdb-scheduler.log
./logs/tmdb-scanner.log

# Container location
/app/logs/
```

### Health Checks
```bash
# Check service health
docker-compose ps

# Check specific container
docker inspect tmdb-monitor --format='{{json .State.Health}}'
```

## Troubleshooting

### Container Won't Start
```bash
# Check configuration
docker-compose config

# View startup logs
docker-compose logs tmdb-monitor

# Check environment
docker-compose exec tmdb-monitor env
```

### Permission Errors
```bash
# Check volume ownership
ls -la ./logs ./cache

# Fix permissions
sudo chown -R 1000:1000 ./logs ./cache

# Check movies directory
ls -la ${HOST_MOVIES_PATH}
```

### Network Mount Issues
```bash
# Test network connectivity
docker-compose exec tmdb-monitor ping ${NETWORK_SERVER}

# Check mount inside container
docker-compose exec tmdb-monitor mount | grep movies

# Manual network test
docker-compose exec tmdb-monitor mount -t cifs //${NETWORK_SERVER}/${NETWORK_SHARE} /mnt/test
```

### API Issues
```bash
# Test TMDB API
docker-compose exec tmdb-monitor python3 -c "
import os, requests
api_key = os.getenv('TMDB_API_KEY')
response = requests.get(f'https://api.themoviedb.org/3/movie/550?api_key={api_key}')
print(f'Status: {response.status_code}')
print(f'Movie: {response.json().get(\"title\", \"API Error\")}')
"
```

## Maintenance

### Update Image
```bash
# Pull latest base image
docker pull python:3.11-slim

# Rebuild
docker-compose build --no-cache

# Restart services
docker-compose --profile monitor down
docker-compose --profile monitor up -d
```

### Clean Up
```bash
# Remove stopped containers
docker-compose rm

# Remove unused images
docker image prune

# Remove all data (DANGEROUS)
docker-compose down -v
rm -rf ./logs ./cache
```

### Backup Configuration
```bash
# Backup environment
cp .env .env.backup

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz ./logs/

# Backup cache
tar -czf cache-backup-$(date +%Y%m%d).tar.gz ./cache/
```

## Production Deployment

### Docker Swarm
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  tmdb-monitor:
    image: tmdb-trailer-downloader:latest
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
        max_attempts: 3
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    # ... rest of configuration
```

Deploy:
```bash
docker stack deploy -c docker-compose.prod.yml tmdb-stack
```

### Kubernetes
```yaml
# k8s-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tmdb-monitor
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tmdb-monitor
  template:
    metadata:
      labels:
        app: tmdb-monitor
    spec:
      containers:
      - name: tmdb-monitor
        image: tmdb-trailer-downloader:latest
        env:
        - name: TMDB_API_KEY
          valueFrom:
            secretKeyRef:
              name: tmdb-secret
              key: api-key
        volumeMounts:
        - name: movies
          mountPath: /movies
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: movies
        hostPath:
          path: /path/to/jellyfin/movies
      - name: logs
        persistentVolumeClaim:
          claimName: tmdb-logs
```

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TMDB_API_KEY` | TMDB API key | - | ✅ |
| `HOST_MOVIES_PATH` | Host movies directory | - | ✅ |
| `NETWORK_ENABLED` | Enable network mounting | `false` | ❌ |
| `NETWORK_TYPE` | Share type (smb/nfs/sshfs) | `smb` | ❌ |
| `NETWORK_SERVER` | Server IP/hostname | - | ❌ |
| `NETWORK_SHARE` | Share name/path | - | ❌ |
| `NETWORK_USERNAME` | Network username | - | ❌ |
| `NETWORK_PASSWORD` | Network password | - | ❌ |
| `DOWNLOAD_QUALITY` | Video quality | `best` | ❌ |
| `MAX_TRAILERS_PER_MOVIE` | Max trailers per movie | `3` | ❌ |
| `SCHEDULE_INTERVAL` | Scan interval (minutes) | `60` | ❌ |
| `LOG_LEVEL` | Logging level | `INFO` | ❌ |
| `PRIVILEGED_MODE` | Enable privileged mode | `false` | ❌ |
