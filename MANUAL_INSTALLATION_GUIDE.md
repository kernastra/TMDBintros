# TMDB Trailers Plugin - Manual Installation Guide

This guide covers all manual installation methods for the TMDB Trailers plugin across different versions and environments.

## 📋 **Available Versions**

### **v2.0.5 - Automatic Python Installation (Recommended)**
- **Best for**: Any environment, automatically installs Python if missing
- **Size**: ~15MB
- **Requirements**: None (auto-installs Python)

### **v2.0.4 - Standalone Binaries**
- **Best for**: Environments where you can't install Python
- **Size**: ~56MB
- **Requirements**: None (true standalone executables)

### **v2.0.2 - Enhanced Bundled**
- **Best for**: Systems with Python 3 already installed
- **Size**: ~56MB
- **Requirements**: Python 3 must be pre-installed

---

## 🚀 **Method 1: Direct ZIP Download (Easiest)**

### **Step 1: Download the Plugin**

Choose your preferred version:

**v2.0.5 (Auto Python Install) - RECOMMENDED:**
```bash
wget https://github.com/kernastra/TMDBintros/releases/download/v2.0.5/TMDBintros-auto-python-v2.0.5.zip
```

**v2.0.4 (Standalone Binaries):**
```bash
wget https://github.com/kernastra/TMDBintros/releases/download/v2.0.4-standalone/TMDBintros-bundled-standalone.zip
```

**v2.0.2 (Enhanced Bundled):**
```bash
wget https://github.com/kernastra/TMDBintros/releases/download/v2.0.2-bundled-fixed/TMDBintros-bundled-v2.0.2.zip
```

### **Step 2: Install via Jellyfin Admin**

1. **Access Jellyfin Admin Panel**
   - Open your Jellyfin server (e.g., `http://your-server:8096`)
   - Login as admin
   - Go to **Dashboard** → **Plugins**

2. **Upload Plugin**
   - Click **"Add Local Plugin"** or **"Upload Plugin"**
   - Select the downloaded ZIP file
   - Click **"Upload"**

3. **Restart Jellyfin**
   - The plugin will show as "Pending Restart"
   - Restart your Jellyfin server
   - The plugin should appear in the **Installed Plugins** list

---

## 🐧 **Method 2: Manual File Placement**

### **For Docker/Container Deployments:**

1. **Download and Extract:**
```bash
# Download (choose your version)
wget https://github.com/kernastra/TMDBintros/releases/download/v2.0.5/TMDBintros-auto-python-v2.0.5.zip

# Extract
unzip TMDBintros-auto-python-v2.0.5.zip -d tmdb-plugin
```

2. **Copy to Jellyfin Plugins Directory:**
```bash
# For Docker with mounted config
docker cp tmdb-plugin/ jellyfin-container:/config/plugins/TMDB_Trailers/

# Or if you have direct access to the volume
cp -r tmdb-plugin/* /path/to/jellyfin/config/plugins/TMDB_Trailers/
```

3. **Restart Container:**
```bash
docker restart jellyfin-container
```

### **For TrueNAS SCALE:**

1. **Access TrueNAS Shell:**
   - Go to **System** → **Shell** in TrueNAS web interface

2. **Navigate to Jellyfin Plugins Directory:**
```bash
# Find your Jellyfin app dataset
cd /mnt/your-pool/ix-applications/releases/jellyfin/volumes/ix_data/config/plugins/

# Create plugin directory
mkdir -p TMDB_Trailers
cd TMDB_Trailers
```

3. **Download and Extract:**
```bash
# Download
wget https://github.com/kernastra/TMDBintros/releases/download/v2.0.5/TMDBintros-auto-python-v2.0.5.zip

# Extract
unzip TMDBintros-auto-python-v2.0.5.zip
rm TMDBintros-auto-python-v2.0.5.zip
```

4. **Restart Jellyfin App:**
   - Go to **Apps** in TrueNAS
   - Click the **⋮** menu next to Jellyfin
   - Select **Restart**

### **For TrueNAS Core:**

1. **SSH into TrueNAS:**
```bash
ssh root@your-truenas-ip
```

2. **Navigate to Jail:**
```bash
# List jails to find Jellyfin
jls

# Enter Jellyfin jail (replace X with jail number)
jexec X csh
```

3. **Install Plugin:**
```bash
# Navigate to plugins directory
cd /config/plugins

# Create plugin directory
mkdir -p TMDB_Trailers
cd TMDB_Trailers

# Download and extract
fetch https://github.com/kernastra/TMDBintros/releases/download/v2.0.5/TMDBintros-auto-python-v2.0.5.zip
unzip TMDBintros-auto-python-v2.0.5.zip
rm TMDBintros-auto-python-v2.0.5.zip
```

4. **Restart Jellyfin Service:**
```bash
service jellyfin restart
exit  # Exit jail
```

---

## 🔧 **Method 3: Build from Source**

### **Prerequisites:**
- .NET 8.0 SDK
- Git

### **Steps:**

1. **Clone Repository:**
```bash
git clone https://github.com/kernastra/TMDBintros.git
cd TMDBintros
```

2. **Build Plugin:**
```bash
dotnet build --configuration Release
```

3. **Package Plugin:**
```bash
cd bin/Release/net8.0
zip -r ../../../TMDBintros-custom.zip .
cd ../../..
```

4. **Install Built Plugin:**
   - Use the generated `TMDBintros-custom.zip` file
   - Follow Method 1 steps for installation

---

## ⚙️ **Configuration**

### **Required Settings:**

1. **TMDB API Key:**
   - Go to **Dashboard** → **Plugins** → **TMDB Trailers** → **Settings**
   - Get API key from [TMDB](https://www.themoviedb.org/settings/api)
   - Enter your API key and save

2. **File Paths:**
   - **Movies Directory**: Path to your movies (e.g., `/media/movies`)
   - **Trailers Directory**: Where to save trailers (e.g., `/media/trailers`)

3. **Quality Settings:**
   - Choose preferred video quality (480p/720p/1080p)
   - Set maximum file size if needed

---

## 🔍 **Verification**

### **Check Plugin Installation:**

1. **Via Jellyfin UI:**
   - Go to **Dashboard** → **Plugins**
   - Look for **"TMDB Trailers"** in installed plugins

2. **Via Logs:**
   - Go to **Dashboard** → **Logs**
   - Look for TMDB plugin initialization messages

3. **Via File System:**
```bash
# Check if plugin files exist
ls /config/plugins/TMDB_Trailers/

# Should show files like:
# TMDBintros.dll
# manifest.json
# Resources/ (directory with binaries)
```

### **Test Functionality:**

1. **Manual Scan:**
   - Go to **Dashboard** → **Scheduled Tasks**
   - Find **"Download Movie Trailers"**
   - Click **"Run Now"**

2. **Check Logs:**
   - Monitor logs for Python installation (v2.0.5)
   - Look for yt-dlp detection messages
   - Verify trailer download attempts

---

## 🆘 **Troubleshooting**

### **Plugin Not Appearing:**
- Ensure ZIP file was extracted properly
- Check file permissions (should be readable by Jellyfin user)
- Restart Jellyfin service/container
- Check logs for error messages

### **Python Dependency Issues (v2.0.5):**
- Plugin automatically installs Python - check logs
- For containers without package manager access, use v2.0.4 instead

### **Permission Issues:**
```bash
# Fix permissions (adjust path as needed)
chown -R jellyfin:jellyfin /config/plugins/TMDB_Trailers/
chmod -R 755 /config/plugins/TMDB_Trailers/
```

### **TrueNAS Specific Issues:**
- Ensure plugin directory is on persistent storage
- Check that Jellyfin app has access to the plugins directory
- Verify dataset permissions

---

## 📞 **Support**

If you encounter issues:

1. **Check Logs**: Always check Jellyfin logs first
2. **GitHub Issues**: Report bugs at [GitHub Issues](https://github.com/kernastra/TMDBintros/issues)
3. **Version Compatibility**: Ensure you're using the right version for your environment

---

## 📦 **Version Comparison**

| Version | Size | Dependencies | Best For |
|---------|------|-------------|----------|
| v2.0.5 | 15MB | Auto-installs Python | Any environment |
| v2.0.4 | 56MB | None | No Python access |
| v2.0.2 | 56MB | Python 3 required | Pre-existing Python |

**Recommendation**: Start with v2.0.5 for automatic dependency management!
