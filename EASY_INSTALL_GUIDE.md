# 🎬 TMDB Trailers Plugin - Easy Installation Guide

## Option 1: Add Custom Repository (Recommended)

### Step 1: Add Repository to Jellyfin
1. Open **Jellyfin Dashboard**
2. Go to **Plugins** → **Repositories**
3. Click **Add Repository**
4. Enter the following details:
   - **Repository Name**: `TMDB Trailers Bundled`
   - **Repository URL**: `https://raw.githubusercontent.com/kernastra/TMDBintros/main/repository-manifest.json`

### Step 2: Install Plugin
1. Go to **Plugins** → **Catalog**
2. Look for **"TMDB Trailers (Bundled yt-dlp)"**
3. Click **Install**
4. **Restart Jellyfin** when prompted

### Step 3: Configure
1. Go to **Dashboard** → **Plugins** → **TMDB Trailers**
2. Enter your **TMDB API Key** (get free at [themoviedb.org](https://www.themoviedb.org/settings/api))
3. Configure settings as desired
4. Save and enjoy automatic trailer downloads!

---

## Option 2: Manual Installation

### Download and Upload
1. **Download**: [TMDBintros-bundled.zip](https://github.com/kernastra/TMDBintros/releases/download/v2.0.0-bundled/TMDBintros-bundled.zip)
2. **Upload**: Dashboard → Plugins → Upload Plugin
3. **Select**: Choose the downloaded ZIP file
4. **Restart**: Restart Jellyfin
5. **Configure**: Add your TMDB API key

---

## 🚀 What Makes This Special?

### ✅ **Zero Dependencies**
- **No yt-dlp installation required**
- **No command-line setup needed**
- **No package manager commands**

### ✅ **Universal Compatibility**
- **TrueNAS Core/SCALE**: Works out-of-the-box
- **Docker**: No external mounts needed
- **Linux**: Any distribution
- **Windows**: Native support
- **macOS**: Full compatibility
- **FreeBSD**: Optimized binaries

### ✅ **Smart Technology**
```
🖥️ Platform Detection → 📦 Binary Selection → 🎬 Download Trailers
```

### ✅ **Intelligent Fallback**
```
Bundled yt-dlp → System yt-dlp → Clear Error Messages
```

---

## 📊 Technical Details

| Feature | Value |
|---------|-------|
| **Package Size** | ~56MB |
| **Runtime Memory** | ~3-35MB (one binary) |
| **Supported Platforms** | Linux, FreeBSD, macOS, Windows |
| **yt-dlp Version** | 2025.07.21 (latest) |
| **Jellyfin Compatibility** | 10.8.13+ |
| **Dependencies** | None |

---

## 🔧 Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| **TMDB API Key** | Required for trailer search | *(none)* |
| **Video Quality** | 480p, 720p, 1080p | 720p |
| **Max Duration** | Maximum trailer length | 5 minutes |
| **Trailer Folder** | Subfolder name | "trailers" |
| **Organize Subfolders** | Movie-specific folders | Yes |
| **Overwrite Existing** | Replace existing trailers | No |
| **Processing Interval** | Auto-download frequency | 24 hours |

---

## 🎯 Perfect For

### 🏠 **Home Server Users**
- TrueNAS Core/SCALE users
- Unraid users  
- Docker enthusiasts
- Raspberry Pi setups

### 🏢 **Professional Environments**
- Restricted corporate networks
- Air-gapped systems
- Controlled environments
- Compliance-required setups

### 🎮 **Media Enthusiasts**
- Large movie collections
- Automated media management
- Quality-focused users
- Set-and-forget solutions

---

## ❓ Troubleshooting

### Repository Not Loading?
- Verify URL: `https://raw.githubusercontent.com/kernastra/TMDBintros/main/repository-manifest.json`
- Check internet connectivity
- Try manual installation instead

### Plugin Not Installing?
- Ensure Jellyfin 10.8.13+
- Check available disk space (60MB needed)
- Restart Jellyfin after adding repository

### No Trailers Downloading?
1. **Check TMDB API Key**: Must be valid and configured
2. **Check Logs**: Dashboard → Logs for error details
3. **Test Single Movie**: Try with one movie first
4. **Verify Movie Names**: Plugin uses movie titles for search

### Permission Issues?
- Plugin handles permissions automatically
- No manual chmod needed
- Works in all container environments

---

## 🆕 Version History

### v2.0.0 - Bundled Release (Latest)
- ✅ Bundled yt-dlp for all platforms
- ✅ Zero external dependencies
- ✅ TrueNAS/Docker ready
- ✅ Automatic platform detection

### v1.0.2 - Configuration Fix
- ✅ Fixed JavaScript configuration page
- ✅ Resolved save/load issues

### v1.0.1 - Package Fix
- ✅ Fixed ZIP package structure
- ✅ Improved installation compatibility

---

## 🔗 Repository URL (Copy This)

```
https://raw.githubusercontent.com/kernastra/TMDBintros/main/repository-manifest.json
```

**Just copy this URL and paste it into Jellyfin's "Add Repository" dialog!**

---

## 📞 Support

- **GitHub Issues**: [Report problems](https://github.com/kernastra/TMDBintros/issues)
- **Documentation**: [Full plugin guide](https://github.com/kernastra/TMDBintros)
- **TMDB API**: [Get your free key](https://www.themoviedb.org/settings/api)

---

🎬 **Ready to enhance your movie library with automatic trailers!**
