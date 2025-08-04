# 🎬 TMDB Trailers Plugin for Jellyfin

[![Release](https://img.shields.io/github/v/release/kernastra/TMDBintros)](https://github.com/kernastra/TMDBintros/releases)
[![License](https://img.shields.io/github/license/kernastra/TMDBintros)](LICENSE)
[![Issues](https://img.shields.io/github/issues/kernastra/TMDBintros)](https://github.com/kernastra/TMDBintros/issues)

A powerful Jellyfin plugin that automatically downloads movie trailers from The Movie Database (TMDB) API and organizes them alongside your movie files. **Now available with zero external dependencies!**

## 🚀 **NEW: Bundled Version Available!**

**No more yt-dlp installation hassles!** Choose the version that works best for you:

| Version | Best For | Dependencies | Installation |
|---------|----------|--------------|--------------|
| **🎯 Bundled** | TrueNAS, Docker, Easy Setup | ✅ **None** | Repository or ZIP |
| 📦 Standard | Advanced Users | yt-dlp required | Build from source |

---

## ✨ Features

- 🎬 **Automatic Trailer Discovery**: Searches TMDB for trailers matching your movie library
- 🎯 **Quality Selection**: Choose preferred video quality (480p, 720p, 1080p)
- 📁 **Smart Organization**: Organizes trailers in configurable folder structures
- ⏱️ **Duration Filtering**: Set maximum trailer length to avoid long videos
- 📅 **Scheduled Processing**: Automatically processes new movies at configurable intervals
- 🔄 **Overwrite Control**: Choose whether to replace existing trailers
- 📊 **Detailed Logging**: Optional verbose logging for troubleshooting
- 🌍 **Cross-Platform**: Linux, FreeBSD, macOS, Windows support
- 🐳 **Container Ready**: Perfect for Docker and TrueNAS deployments

---

## 📦 Installation Options

### 🎯 **Option 1: Bundled Version (Recommended)**

**Perfect for TrueNAS, Docker, and hassle-free installation!**

#### **🔗 Repository Installation (Easiest)**
1. **Add Repository to Jellyfin**:
   - Go to **Dashboard** → **Plugins** → **Repositories**
   - Click **Add Repository**
   - **Repository URL**: 
     ```
     https://raw.githubusercontent.com/kernastra/TMDBintros/main/repository-manifest.json
     ```
   - **Repository Name**: `TMDB Trailers Bundled`

2. **Install Plugin**:
   - Go to **Plugins** → **Catalog**
   - Find **"TMDB Trailers (Bundled yt-dlp)"**
   - Click **Install**
   - **Restart Jellyfin**

3. **Configure**: Add your TMDB API key and enjoy!

#### **📥 Manual ZIP Installation**
1. **Download**: [TMDBintros-bundled.zip](https://github.com/kernastra/TMDBintros/releases/download/v2.0.0-bundled/TMDBintros-bundled.zip) (~56MB)
2. **Upload**: Dashboard → Plugins → Upload Plugin
3. **Restart**: Restart Jellyfin
4. **Configure**: Add your TMDB API key

📖 **Detailed Guide**: [EASY_INSTALL_GUIDE.md](EASY_INSTALL_GUIDE.md)

---

### 📦 **Option 2: Standard Version**

**For advanced users who prefer managing dependencies:**

#### **🛠️ Prerequisites**
- Jellyfin 10.8.13 or later
- .NET 8.0 runtime
- **yt-dlp** (must be installed separately)

#### **Installing yt-dlp**

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install yt-dlp

# CentOS/RHEL/Fedora
sudo dnf install yt-dlp
# or: pip install yt-dlp

# Windows
winget install yt-dlp
# or: pip install yt-dlp

# macOS
brew install yt-dlp
# or: pip install yt-dlp
```

#### **🔧 Build from Source**
1. **Clone & Build**:
   ```bash
   git clone https://github.com/kernastra/TMDBintros.git
   cd TMDBintros
   dotnet build --configuration Release
   ```

2. **Install DLL**:
   ```bash
   # Linux
   cp bin/Release/net8.0/TMDBintros.dll /var/lib/jellyfin/plugins/
   
   # Windows
   copy bin\Release\net8.0\TMDBintros.dll "C:\ProgramData\Jellyfin\Server\plugins\"
   
   # Docker
   cp bin/Release/net8.0/TMDBintros.dll /path/to/jellyfin/config/plugins/
   ```

---

## 🔑 TMDB API Key Setup

**Required for both versions:**

1. Create account at [The Movie Database](https://www.themoviedb.org/)
2. Go to [API Settings](https://www.themoviedb.org/settings/api)
3. Request an API key (free)
4. Copy your API key for plugin configuration

---

## ⚙️ Configuration

1. **Restart Jellyfin** after installing the plugin
2. Go to **Dashboard** → **Plugins** → **TMDB Trailers**
3. Configure your settings:

### 🔑 Required Settings
- **TMDB API Key**: Your API key from TMDB *(required)*

### 🎛️ Optional Settings
| Setting | Options | Default | Description |
|---------|---------|---------|-------------|
| **Auto Download** | On/Off | ✅ On | Automatically download trailers for new movies |
| **Video Quality** | 480p/720p/1080p | 720p | Preferred download quality |
| **Max Duration** | 1-10 minutes | 5 min | Maximum trailer length |
| **Overwrite** | Yes/No | No | Replace existing trailers |
| **Trailer Folder** | Custom name | "trailers" | Subfolder name for trailers |
| **Subfolders** | Yes/No | Yes | Create movie-specific folders |
| **Process Interval** | 1-168 hours | 24 hours | Auto-check frequency |
| **Detailed Logging** | On/Off | Off | Verbose logging for debugging |

---

## 📁 File Organization

### 📂 With Subfolders (Default):
```
/Movies/
├── Movie Name (2023)/
│   ├── Movie Name (2023).mkv
│   └── trailers/
│       └── Movie Name (2023)/
│           └── Movie Name (2023) - Official Trailer.mp4
```

### 📂 Without Subfolders:
```
/Movies/
├── Movie Name (2023)/
│   ├── Movie Name (2023).mkv
│   └── trailers/
│       └── Movie Name (2023) - Official Trailer.mp4
```

---

## 🎯 Manual Processing

Trigger trailer downloads manually:

1. **Dashboard** → **Scheduled Tasks**
2. Find **"Download Movie Trailers"**
3. Click **▶️ Run Now**

---

## 🛠️ Troubleshooting

### 🔧 Common Issues

| Issue | Solution |
|-------|----------|
| **"yt-dlp not available"** | Use bundled version OR install yt-dlp manually |
| **"TMDB API key not configured"** | Add valid API key in plugin settings |
| **No trailers found** | Check movie exists on TMDB, enable detailed logging |
| **Download failures** | Check internet, verify yt-dlp: `yt-dlp --version` |
| **Permission errors** | Bundled version handles this automatically |

### 📊 Logs Location
- **Linux**: `/var/log/jellyfin/`
- **Windows**: `C:\ProgramData\Jellyfin\Server\logs`
- **Docker**: Container logs

**💡 Tip**: Enable "Detailed Logging" in plugin settings for troubleshooting.

---

## 📚 Documentation

### 📖 **User Guides**
- **[📥 Easy Install Guide](EASY_INSTALL_GUIDE.md)** - Step-by-step installation with screenshots
- **[🔧 Bundled Version README](BUNDLED_VERSION_README.md)** - Technical details about the bundled version

### 👩‍💻 **Developer Resources**
- **[🚀 Plugin Development Guide](JELLYFIN_PLUGIN_DEVELOPMENT_GUIDE.md)** - Complete Jellyfin plugin development tutorial
- **[⚡ Quick Start Template](QUICK_START_TEMPLATE.md)** - Minimal template for new plugins
- **[📋 Plugin Submission Guide](PLUGIN_SUBMISSION.md)** - How to submit to official Jellyfin repository

### 🏗️ **Project Files**
- **[🔨 Build Scripts](download-yt-dlp.sh)** - Automated binary download script
- **[📦 Installation Script](install-bundled.sh)** - Automated installation helper

---

## 🌟 Perfect For

### 🏠 **Home Users**
- ✅ TrueNAS Core/SCALE servers
- ✅ Unraid systems
- ✅ Raspberry Pi setups
- ✅ Docker deployments

### 🏢 **Professional**
- ✅ Corporate networks
- ✅ Air-gapped systems
- ✅ Compliance environments
- ✅ Managed containers

### 🎮 **Media Enthusiasts**
- ✅ Large movie collections
- ✅ Automated workflows
- ✅ Quality-focused setups
- ✅ Set-and-forget operation

---

## 🔧 Development

### Building
```bash
git clone https://github.com/kernastra/TMDBintros.git
cd TMDBintros
dotnet restore
dotnet build --configuration Release
```

### Testing
```bash
dotnet test
```

### Contributing
1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. ✏️ Make your changes
4. 🧪 Add tests if applicable
5. 📤 Submit a pull request

---

## 📈 Version History

| Version | Release | Highlights |
|---------|---------|------------|
| **v2.0.0** | 🎯 Latest | **Bundled yt-dlp**, zero dependencies, TrueNAS ready |
| v1.0.2 | 🔧 Stable | Configuration fixes, improved UI |
| v1.0.1 | 📦 Initial | Core functionality, manual yt-dlp required |

---

## 🤝 Support

### 💬 Getting Help
1. 📖 Check [troubleshooting section](#🛠️-troubleshooting)
2. 🔍 Search [GitHub Issues](https://github.com/kernastra/TMDBintros/issues)
3. 🆕 Create new issue with:
   - Jellyfin version
   - Plugin version  
   - Operating system
   - Log entries
   - Reproduction steps

### 🔗 Quick Links
- **[📥 Releases](https://github.com/kernastra/TMDBintros/releases)** - Download latest versions
- **[🐛 Issues](https://github.com/kernastra/TMDBintros/issues)** - Report bugs or request features
- **[📊 TMDB API](https://www.themoviedb.org/settings/api)** - Get your free API key

---

## 🙏 Acknowledgments

- **[🎬 The Movie Database (TMDB)](https://www.themoviedb.org/)** - Trailer metadata API
- **[📹 yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Video downloading engine
- **[🖥️ Jellyfin](https://jellyfin.org/)** - Open-source media server platform

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🚀 Ready to Get Started?

### 🎯 **Recommended Quick Start**:
1. **Copy repository URL**: `https://raw.githubusercontent.com/kernastra/TMDBintros/main/repository-manifest.json`
2. **Add to Jellyfin**: Dashboard → Plugins → Repositories → Add Repository
3. **Install plugin**: Plugins → Catalog → "TMDB Trailers (Bundled yt-dlp)" → Install
4. **Get API key**: [TMDB API Settings](https://www.themoviedb.org/settings/api)
5. **Configure**: Dashboard → Plugins → TMDB Trailers → Add API key
6. **Enjoy**: Automatic trailers for your entire movie library! 🍿

**🎬 Transform your movie library with cinematic trailers - zero setup required!**

## Manual Processing

You can manually trigger trailer downloads:

1. Go to **Dashboard** → **Scheduled Tasks**
2. Find "Download Movie Trailers" task
3. Click **Run Now**

## Troubleshooting

### Common Issues

1. **"yt-dlp is not available" error**
   - Install yt-dlp using the instructions above
   - Ensure yt-dlp is in your system PATH
   - Restart Jellyfin after installing yt-dlp

2. **"TMDB API key is not configured" error**
   - Ensure you've entered your API key in the plugin configuration
   - Verify the API key is correct and active

3. **No trailers found**
   - Check if the movie exists on TMDB
   - Verify the movie title matches closely with TMDB
   - Enable detailed logging to see search results

4. **Download failures**
   - Check internet connectivity
   - Verify yt-dlp is working: `yt-dlp --version`
   - Check Jellyfin logs for specific error messages

### Logs

Enable detailed logging in the plugin configuration and check Jellyfin logs:

- **Linux**: `/var/log/jellyfin/`
- **Windows**: `C:\ProgramData\Jellyfin\Server\logs\`
- **Docker**: Check container logs

## Development

### Building

```bash
dotnet restore
dotnet build
```

### Testing

```bash
dotnet test
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Plugin Development

Want to create your own Jellyfin plugins? This repository includes comprehensive guides to help you:

### 📚 [Jellyfin Plugin Development Guide](JELLYFIN_PLUGIN_DEVELOPMENT_GUIDE.md)
A complete guide covering:
- Project structure and architecture
- Configuration system best practices
- Dependency injection patterns
- Scheduled task implementation
- Packaging and distribution
- GitHub Actions automation
- Common pitfalls and solutions
- Real-world examples from this TMDB plugin

### ⚡ [Quick Start Template](QUICK_START_TEMPLATE.md)
A minimal template to get started quickly:
- Essential project files with placeholders
- Step-by-step setup instructions
- Quick checklist for new plugins
- Copy-paste ready code snippets

These guides are based on the real-world experience of building this TMDB Trailers plugin and will help you avoid common issues and set up proper CI/CD workflows.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the trailer API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for video downloading capabilities
- [Jellyfin](https://jellyfin.org/) for the media server platform

## Support

If you encounter issues or have questions:

1. Check the [troubleshooting section](#troubleshooting)
2. Search existing [GitHub Issues](https://github.com/kernastra/TMDBintros/issues)  
3. Create a new issue with detailed information including:
   - Jellyfin version
   - Plugin version
   - Operating system
   - Relevant log entries
   - Steps to reproduce the issue

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
