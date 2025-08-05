# TMDB Trailer Downloader v3.0.0 - Quick Reference

## 🚀 What's New in v3.0.0

**Complete transformation from simple script to enterprise container application!**

### Key Features
- 🐳 **Full Docker support** with multi-service architecture
- 📊 **Web dashboard** at http://localhost:8080
- 🔄 **Real-time monitoring** for new movies
- ⏰ **Scheduled scanning** at configurable intervals
- 🌐 **Network share support** (SMB/NFS/SSHFS)
- 🔧 **Environment-based config** for security

### Quick Start
```bash
# 1. Setup
cp .env.docker .env
# Edit .env with your TMDB_API_KEY and HOST_MOVIES_PATH

# 2. Test
make test

# 3. Run
make monitor    # Real-time monitoring
make dashboard  # Web interface
```

### Service Commands
```bash
make scan       # One-time library scan
make monitor    # Start real-time monitoring
make schedule   # Start scheduled scanning
make dashboard  # Start web dashboard
make up         # Start all services
make down       # Stop all services
make status     # Check service status
make logs       # View all logs
```

### Access Points
- **Web Dashboard**: http://localhost:8080
- **Service Logs**: `make logs-monitor`, `make logs-schedule`
- **Configuration Test**: `make test`

### File Structure
```
tmdb-trailer-downloader-v3.0.0/
├── 🐳 Docker files (Dockerfile, docker-compose.yml)
├── 🔧 Python apps (monitor, scheduler, dashboard)
├── 📚 Documentation (DOCKER.md, SERVICES.md)
├── ⚙️ Configuration (.env.example, templates)
└── 🛠️ Tools (Makefile, version.py)
```

### Migration from v1.x/v2.x
- **Old**: JSON config files → **New**: Environment variables
- **Old**: Single script → **New**: Multi-service containers
- **Old**: Manual execution → **New**: Automated monitoring
- **Old**: CLI only → **New**: Web dashboard

### Support
- **Documentation**: See README.md, DOCKER.md, SERVICES.md
- **Issues**: https://github.com/kernastra/TMDBintros/issues
- **Releases**: https://github.com/kernastra/TMDBintros/releases

---
**Release Date**: August 4, 2025 | **Docker Tag**: v3.0.0 | **Archive**: 44KB
