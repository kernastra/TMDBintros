# Jellyfin Plugin Quick Start Template

This is a minimal template to get started quickly with a new Jellyfin plugin.

## 1. Create Project Structure

```bash
mkdir YourPlugin
cd YourPlugin
```

## 2. Create YourPlugin.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <AssemblyVersion>1.0.0.0</AssemblyVersion>
    <FileVersion>1.0.0.0</FileVersion>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Jellyfin.Controller" Version="10.8.13" />
    <PackageReference Include="Jellyfin.Model" Version="10.8.13" />
    <PackageReference Include="Microsoft.Extensions.DependencyInjection.Abstractions" Version="8.0.0" />
    <PackageReference Include="Microsoft.Extensions.Http" Version="8.0.0" />
    <PackageReference Include="Microsoft.Extensions.Logging.Abstractions" Version="8.0.0" />
  </ItemGroup>

  <ItemGroup>
    <EmbeddedResource Include="Configuration\configPage.html" />
  </ItemGroup>
</Project>
```

## 3. Create Plugin.cs

```csharp
using System;
using System.Collections.Generic;
using System.Globalization;
using YourPlugin.Configuration;
using MediaBrowser.Common.Configuration;
using MediaBrowser.Common.Plugins;
using MediaBrowser.Model.Plugins;
using MediaBrowser.Model.Serialization;

namespace YourPlugin;

public class Plugin : BasePlugin<PluginConfiguration>, IHasWebPages
{
    public override string Name => "Your Plugin Name";
    public override Guid Id => Guid.Parse("TODO-GENERATE-GUID-HERE");
    public static Plugin? Instance { get; private set; }

    public Plugin(IApplicationPaths applicationPaths, IXmlSerializer xmlSerializer)
        : base(applicationPaths, xmlSerializer)
    {
        Instance = this;
    }

    public IEnumerable<PluginPageInfo> GetPages()
    {
        return new[]
        {
            new PluginPageInfo
            {
                Name = this.Name,
                EmbeddedResourcePath = string.Format(CultureInfo.InvariantCulture, "{0}.Configuration.configPage.html", GetType().Namespace)
            }
        };
    }
}
```

## 4. Create Configuration/PluginConfiguration.cs

```csharp
using MediaBrowser.Model.Plugins;

namespace YourPlugin.Configuration;

public class PluginConfiguration : BasePluginConfiguration
{
    public string ApiKey { get; set; } = string.Empty;
    public bool EnableAutomaticProcessing { get; set; } = true;
    public bool EnableDetailedLogging { get; set; } = false;
    public int ProcessingIntervalHours { get; set; } = 24;
}
```

## 5. Create Configuration/configPage.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Your Plugin Configuration</title>
</head>
<body>
    <div id="YourPluginConfigPage" data-role="page" class="page type-interior pluginConfigurationPage">
        <div data-role="content">
            <div class="content-primary">
                <form id="YourPluginConfigForm">
                    <div class="selectContainer">
                        <label class="selectLabel" for="ApiKey">API Key:</label>
                        <input id="ApiKey" name="ApiKey" type="password" />
                    </div>
                    
                    <div class="checkboxContainer">
                        <label>
                            <input id="EnableAutomaticProcessing" name="EnableAutomaticProcessing" type="checkbox" />
                            <span>Enable Automatic Processing</span>
                        </label>
                    </div>
                    
                    <div class="checkboxContainer">
                        <label>
                            <input id="EnableDetailedLogging" name="EnableDetailedLogging" type="checkbox" />
                            <span>Enable Detailed Logging</span>
                        </label>
                    </div>
                    
                    <button id="saveConfig" type="submit">Save</button>
                </form>
            </div>
        </div>
    </div>

    <script type="text/javascript">
        (function() {
            const pluginId = "TODO-SAME-GUID-AS-PLUGIN-CS";
            
            function loadConfig() {
                Dashboard.showLoadingMsg();
                
                ApiClient.getPluginConfiguration(pluginId).then(function(config) {
                    document.getElementById('ApiKey').value = config.ApiKey || '';
                    document.getElementById('EnableAutomaticProcessing').checked = config.EnableAutomaticProcessing;
                    document.getElementById('EnableDetailedLogging').checked = config.EnableDetailedLogging;
                    
                    Dashboard.hideLoadingMsg();
                }).catch(function(error) {
                    console.error('Error loading configuration:', error);
                    Dashboard.hideLoadingMsg();
                    Dashboard.alert('Error loading configuration');
                });
            }
            
            function saveConfig(e) {
                e.preventDefault();
                Dashboard.showLoadingMsg();
                
                const config = {
                    ApiKey: document.getElementById('ApiKey').value,
                    EnableAutomaticProcessing: document.getElementById('EnableAutomaticProcessing').checked,
                    EnableDetailedLogging: document.getElementById('EnableDetailedLogging').checked
                };
                
                ApiClient.updatePluginConfiguration(pluginId, config).then(function() {
                    Dashboard.hideLoadingMsg();
                    Dashboard.processPluginConfigurationUpdateResult();
                }).catch(function(error) {
                    console.error('Error saving configuration:', error);
                    Dashboard.hideLoadingMsg();
                    Dashboard.alert('Error saving configuration');
                });
            }
            
            document.getElementById('YourPluginConfigPage').addEventListener('pageshow', loadConfig);
            document.getElementById('YourPluginConfigForm').addEventListener('submit', saveConfig);
        })();
    </script>
</body>
</html>
```

## 6. Create build.yaml

```yaml
guid: "TODO-SAME-GUID-AS-PLUGIN-CS"
name: "Your Plugin Name"
description: "Brief description"
overview: "Detailed description"
owner: "YourGitHubUsername"
category: "General"
version: "1.0.0.0"
targetAbi: "10.8.13.0"
framework: "net8.0"
changelog: |
  ## 1.0.0
  - Initial release
```

## 7. Create manifest.json

```json
[
  {
    "guid": "TODO-SAME-GUID-AS-PLUGIN-CS",
    "name": "Your Plugin Name",
    "description": "Brief description",
    "overview": "Detailed description",
    "owner": "yourusername",
    "category": "General",
    "versions": [
      {
        "version": "1.0.0.0",
        "changelog": "Initial release",
        "targetAbi": "10.8.13.0",
        "sourceUrl": "https://github.com/yourusername/yourplugin/releases/download/v1.0.0/YourPlugin.zip",
        "checksum": "will-be-generated-by-github-actions",
        "timestamp": "2025-01-01T00:00:00Z"
      }
    ]
  }
]
```

## 8. Setup Commands

```bash
# Generate GUID
uuidgen

# Build and test
dotnet restore
dotnet build --configuration Release

# Create local install script
echo '#!/bin/bash
dotnet build --configuration Release
sudo cp bin/Release/net8.0/YourPlugin.dll /var/lib/jellyfin/plugins/
sudo systemctl restart jellyfin
echo "Plugin installed. Check Jellyfin Dashboard → Plugins"' > install-local.sh
chmod +x install-local.sh
```

## 9. Quick Checklist

- [ ] Replace all "YourPlugin" with your actual plugin name
- [ ] Replace all "TODO-GENERATE-GUID-HERE" with the same GUID (use `uuidgen`)
- [ ] Replace "yourusername" with your GitHub username
- [ ] Update descriptions and names
- [ ] Add your actual plugin logic
- [ ] Test locally before releasing

## 10. GitHub Actions (Optional)

Copy the GitHub Actions workflow from the full development guide to automate building and releasing.

---

This template gives you a working Jellyfin plugin structure in minutes. For more advanced features, refer to the complete [Jellyfin Plugin Development Guide](JELLYFIN_PLUGIN_DEVELOPMENT_GUIDE.md).
