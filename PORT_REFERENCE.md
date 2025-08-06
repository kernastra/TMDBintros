# Port Configuration Reference

## 🚢 TMDB Trailer Downloader Ports

### **Web Dashboard**: Port 8085
- **URL**: http://localhost:8085
- **Purpose**: Web interface for monitoring and management
- **Configuration**: `DASHBOARD_PORT=8085` in .env file

---

## 🎬 Common Media Server Stack Ports

This reference helps avoid port conflicts when setting up your media server environment.

### **Download Clients**
- **qBittorrent**: 8080 (Web UI)
- **Deluge**: 8112 (Web UI)
- **Transmission**: 9091 (Web UI)
- **SABnzbd**: 8080 (Web UI)
- **NZBGet**: 6789 (Web UI)

### **Media Management (Arr Stack)**
- **Radarr**: 7878 (Movies)
- **Sonarr**: 8989 (TV Shows)
- **Prowlarr**: 9696 (Indexer Management)
- **Lidarr**: 8686 (Music)
- **Readarr**: 8787 (Books)
- **Bazarr**: 6767 (Subtitles)

### **Media Servers**
- **Jellyfin**: 8096 (Main interface)
- **Plex**: 32400 (Main interface)
- **Emby**: 8096 (Main interface)

### **Request Management**
- **Jellyseerr**: 5055 (Jellyfin requests)
- **Overseerr**: 5055 (Plex requests)
- **Ombi**: 3579 (Multi-platform requests)

### **Monitoring & Analytics**
- **Tautulli**: 8181 (Plex monitoring)
- **Varken**: 3000 (Grafana dashboard)
- **Netdata**: 19999 (System monitoring)

### **Other Common Services**
- **Portainer**: 9000 (Docker management)
- **Traefik**: 8080/80/443 (Reverse proxy)
- **Nginx Proxy Manager**: 8080/80/443
- **Homer Dashboard**: 8080
- **Heimdall Dashboard**: 80/443

---

## 🔧 Port Selection Strategy

### **Safe Port Ranges for Custom Applications**
- **8001-8009**: Generally safe for custom apps
- **8081-8089**: Alternative to 8080 range
- **3001-3009**: Node.js application range
- **4001-4009**: Alternative application range
- **8501-8509**: Streamlit/data apps range

### **TMDB Trailer Downloader Port Choice**
We chose **port 8085** because:
- ✅ **Avoids qBittorrent**: Common conflict with 8080
- ✅ **Safe from Arr stack**: No conflicts with 7878, 8989, etc.
- ✅ **Not used by Jellyfin**: Avoids 8096
- ✅ **Easy to remember**: Close to 8080 but unique
- ✅ **Standard range**: Within common web application ports

### **How to Change the Dashboard Port**
```bash
# In your .env file
DASHBOARD_PORT=8085              # Default
DASHBOARD_PORT=8087              # Alternative
DASHBOARD_PORT=3005              # Node.js style
DASHBOARD_PORT=8501              # Data app style
```

### **Testing Port Availability**
```bash
# Check if port is in use (Linux/Mac)
netstat -an | grep :8085
lsof -i :8085

# Check if port is in use (Windows)
netstat -an | findstr :8085
```

---

## 🐳 Docker Port Mapping

### **Basic Port Mapping**
```yaml
ports:
  - "8085:8085"          # host:container
  - "8087:8085"          # custom host port
```

### **Environment Variable Port Mapping**
```yaml
ports:
  - "${DASHBOARD_PORT:-8085}:${DASHBOARD_PORT:-8085}"
```

### **Multiple Service Ports**
```yaml
services:
  tmdb-dashboard:
    ports:
      - "${DASHBOARD_PORT:-8085}:${DASHBOARD_PORT:-8085}"
  
  other-service:
    ports:
      - "8086:8080"      # Avoid conflict with dashboard
```

---

## 🔍 Troubleshooting Port Conflicts

### **Common Symptoms**
- 🚫 "Port already in use" error
- 🌐 Can't access web interface
- 🔄 Service fails to start
- 📱 Browser shows "connection refused"

### **Quick Fixes**
1. **Check what's using the port**:
   ```bash
   # Linux/Mac
   sudo lsof -i :8085
   
   # Windows
   netstat -ano | findstr :8085
   ```

2. **Change the port**:
   ```bash
   # In .env file
   DASHBOARD_PORT=8087
   ```

3. **Restart the service**:
   ```bash
   docker-compose restart tmdb-dashboard
   ```

4. **Use a different port range**:
   ```bash
   # Try ports in 8001-8009 range
   DASHBOARD_PORT=8003
   ```

### **Advanced Solutions**
- **Use reverse proxy** (Traefik, Nginx) for subdomain routing
- **Set up VLANs** for service isolation
- **Use Docker networks** for internal communication
- **Implement service discovery** for dynamic port allocation

---

## 📋 Quick Reference Commands

```bash
# Start dashboard on default port (8085)
make dashboard

# Start dashboard on custom port
DASHBOARD_PORT=8087 make dashboard

# Check dashboard status
docker-compose ps tmdb-dashboard

# View dashboard logs
make logs-dashboard

# Access dashboard
open http://localhost:8085
```

This port configuration ensures your TMDB Trailer Downloader dashboard won't conflict with your existing media server setup! 🎬
