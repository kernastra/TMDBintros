# Changelog

All notable changes to the TMDB Trailer Downloader project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2025-08-04

### Added - Major Release: Enterprise & Container Support
- 🐳 **Full Docker containerization** with Docker Compose
- 📊 **Web dashboard** with real-time monitoring and statistics
- 🔄 **Real-time file system monitoring** service (`tmdb_monitor.py`)
- ⏰ **Scheduled scanning service** (`tmdb_scheduler.py`) 
- 🌐 **Multi-service architecture** with profiles (scanner/monitor/scheduler/dashboard)
- 📱 **Responsive web interface** for system monitoring
- 🔧 **Makefile** with 20+ convenient Docker operations
- 📚 **Comprehensive documentation** (DOCKER.md, SERVICES.md)
- 🔒 **Enhanced security** with non-root containers and privilege management
- 📈 **Live statistics** and service health monitoring
- 🏢 **Enterprise deployment** support (Docker Swarm, Kubernetes)
- 🛡️ **Production-ready** systemd service files
- 📊 **Performance monitoring** and resource usage tracking

### Enhanced
- 🌐 **Network share support** expanded with automatic mounting/unmounting
- 🔧 **Environment variable configuration** system overhauled
- 📝 **Logging system** enhanced with structured output and multiple levels
- 🔐 **Security improvements** with credential isolation and .dockerignore
- 📱 **Cross-platform compatibility** via containers
- 🎯 **Cinema Mode compatibility** validated against official Jellyfin plugin

### Changed - Breaking Changes
- **Configuration method**: Environment variables now preferred over JSON
- **Deployment model**: Container-first with Docker Compose
- **Service architecture**: Monolithic script split into specialized services
- **Versioning**: Adopted semantic versioning (v3.0.0)

### Technical Improvements
- **Container optimization**: Multi-stage builds, layer caching, security hardening
- **Service orchestration**: Profile-based deployment with dependency management
- **Monitoring capabilities**: Real-time logs, health checks, auto-restart policies
- **Network architecture**: Isolated container networking with bridge configuration
- **Volume management**: Persistent data handling for logs, cache, and configuration

## [2.x] - Previous Development

### Added
- 🔧 **Environment variable configuration** system
- 🌐 **Network share mounting** (SMB/CIFS, NFS, SSHFS)
- 📝 **Enhanced logging** and error handling
- 🔒 **Security-focused** credential management
- 🎯 **Batch processing** and library scanning
- 📁 **Automatic folder structure** creation

### Enhanced
- **Configuration management** with fallback system
- **Network credential** handling and validation
- **Error recovery** and retry mechanisms
- **Cinema Mode compatibility** verification

## [1.x] - Initial Release

### Added
- 🎬 **Basic TMDB trailer downloading**
- 📁 **Jellyfin folder structure** creation
- 📝 **JSON-based configuration**
- 🔧 **Command-line interface**
- 📥 **yt-dlp integration** for video downloads

### Features
- Single movie and batch processing
- Basic error handling and logging
- Cinema Mode plugin compatibility
- Configurable video quality settings

---

## Migration Guide

### From v1.x to v3.0.0

**Configuration Migration:**
```bash
# Old way (v1.x)
cp config.json.example config.json
# Edit config.json

# New way (v3.0.0)
cp .env.docker .env
# Edit .env with environment variables
```

**Execution Migration:**
```bash
# Old way (v1.x)
python3 tmdb_trailer_downloader.py --scan-existing

# New way (v3.0.0)
docker-compose --profile scanner up tmdb-scanner
# OR for continuous monitoring
docker-compose --profile monitor up -d tmdb-monitor
```

**Feature Additions in v3.0.0:**
- ✅ **Web dashboard**: Access at http://localhost:8080
- ✅ **Real-time monitoring**: Automatically detects new movies
- ✅ **Scheduled scanning**: Runs at configurable intervals
- ✅ **Container deployment**: Production-ready with Docker
- ✅ **Service management**: Start/stop individual components

## Compatibility

### Jellyfin Cinema Mode
- ✅ **Fully compatible** with Cinema Mode plugin v1.x
- ✅ **Folder structure** matches official requirements
- ✅ **Trailer detection** verified with plugin source code

### System Requirements
- **v3.0.0**: Docker & Docker Compose OR Python 3.7+
- **v2.x**: Python 3.7+, network mounting tools (optional)
- **v1.x**: Python 3.7+, basic dependencies

### Upgrade Path
- **v1.x → v3.0.0**: Configuration migration required
- **v2.x → v3.0.0**: Environment variables compatible, add Docker
- **All versions**: Existing trailer files remain unchanged

## Support

- 📖 **Documentation**: See README.md, DOCKER.md, SERVICES.md
- 🐛 **Issues**: Report via GitHub Issues
- 💬 **Discussions**: GitHub Discussions for questions
- 🔧 **Enterprise Support**: Contact for production deployments
