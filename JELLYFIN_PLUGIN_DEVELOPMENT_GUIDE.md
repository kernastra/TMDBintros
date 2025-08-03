# Jellyfin Plugin Development Guide

A comprehensive guide for creating robust Jellyfin plugins with proper structure, packaging, and distribution.

## Table of Contents

- [Project Structure](#project-structure)
- [Core Requirements](#core-requirements)
- [Plugin Architecture](#plugin-architecture)
- [Configuration System](#configuration-system)
- [Dependency Injection](#dependency-injection)
- [Scheduled Tasks](#scheduled-tasks)
- [Packaging & Distribution](#packaging--distribution)
- [GitHub Integration](#github-integration)
- [Testing & Debugging](#testing--debugging)
- [Common Pitfalls](#common-pitfalls)
- [Best Practices](#best-practices)

## Project Structure

### Recommended Directory Layout

```
YourPlugin/
├── .github/
│   └── workflows/
│       └── build-release.yml          # Automated CI/CD
├── Configuration/
│   ├── PluginConfiguration.cs         # Settings model
│   └── configPage.html               # Web configuration UI
├── Models/
│   └── YourModels.cs                 # Data models
├── Services/
│   ├── YourApiService.cs             # External API integration
│   ├── YourProcessingService.cs      # Business logic
│   └── YourFileService.cs            # File operations
├── ScheduledTasks/
│   └── YourTask.cs                   # Background tasks
├── Plugin.cs                         # Main plugin entry point
├── PluginServiceRegistrator.cs       # Dependency injection setup
├── manifest.json                     # Plugin catalog manifest
├── build.yaml                        # Build configuration
├── YourPlugin.csproj                 # Project file
├── README.md                         # Plugin documentation
└── CHANGELOG.md                      # Version history
```

## Core Requirements

### 1. Project File (.csproj)

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <AssemblyVersion>1.0.0.0</AssemblyVersion>
    <FileVersion>1.0.0.0</FileVersion>
    <Nullable>enable</Nullable>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
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

### 2. Build Configuration (build.yaml)

```yaml
guid: "your-unique-guid-here"  # Generate with uuidgen or online tool
name: "Your Plugin Name"
description: "Brief description of your plugin"
overview: "Detailed description with features and benefits"
owner: "YourGitHubUsername"
category: "General"  # or "Metadata", "Channel", etc.
version: "1.0.0.0"
targetAbi: "10.8.13.0"
framework: "net8.0"
changelog: |
  ## 1.0.0
  - Initial release
  - Core functionality
  - Configuration interface
```

## Plugin Architecture

### 1. Main Plugin Class

```csharp
using System;
using System.Collections.Generic;
using System.Globalization;
using Jellyfin.Plugin.YourPlugin.Configuration;
using MediaBrowser.Common.Configuration;
using MediaBrowser.Common.Plugins;
using MediaBrowser.Model.Plugins;
using MediaBrowser.Model.Serialization;

namespace Jellyfin.Plugin.YourPlugin;

public class Plugin : BasePlugin<PluginConfiguration>, IHasWebPages
{
    public override string Name => "Your Plugin Name";
    public override Guid Id => Guid.Parse("your-guid-here");
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

### 2. Service Registration

```csharp
using Microsoft.Extensions.DependencyInjection;
using MediaBrowser.Controller;
using MediaBrowser.Controller.Plugins;
using YourPlugin.Services;

namespace YourPlugin;

public class PluginServiceRegistrator : IPluginServiceRegistrator
{
    public void RegisterServices(IServiceCollection serviceCollection, IServerApplicationHost applicationHost)
    {
        serviceCollection.AddHttpClient();
        serviceCollection.AddScoped<YourApiService>();
        serviceCollection.AddScoped<YourProcessingService>();
        serviceCollection.AddScoped<YourFileService>();
    }
}
```

## Configuration System

### 1. Configuration Model

```csharp
using MediaBrowser.Model.Plugins;

namespace YourPlugin.Configuration;

public class PluginConfiguration : BasePluginConfiguration
{
    // Required settings
    public string ApiKey { get; set; } = string.Empty;
    
    // Feature toggles
    public bool EnableAutomaticProcessing { get; set; } = true;
    public bool EnableDetailedLogging { get; set; } = false;
    
    // Processing settings
    public string OutputDirectory { get; set; } = "output";
    public int ProcessingIntervalHours { get; set; } = 24;
    public int MaxItems { get; set; } = 100;
    
    // Quality/behavior settings
    public string PreferredQuality { get; set; } = "720p";
    public bool OverwriteExisting { get; set; } = false;
}
```

### 2. Configuration Web Page

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
                        <label class="selectLabel" for="ApiKey">API Key (Required):</label>
                        <input id="ApiKey" name="ApiKey" type="password" required />
                        <div class="fieldDescription">Get your API key from the service provider</div>
                    </div>
                    
                    <div class="checkboxContainer checkboxContainer-withDescription">
                        <label>
                            <input id="EnableAutomaticProcessing" name="EnableAutomaticProcessing" type="checkbox" />
                            <span>Enable Automatic Processing</span>
                        </label>
                        <div class="fieldDescription">Automatically process new items</div>
                    </div>
                    
                    <div class="selectContainer">
                        <label class="selectLabel" for="PreferredQuality">Preferred Quality:</label>
                        <select id="PreferredQuality" name="PreferredQuality">
                            <option value="480p">480p</option>
                            <option value="720p">720p</option>
                            <option value="1080p">1080p</option>
                        </select>
                    </div>
                    
                    <div class="inputContainer">
                        <label class="inputLabel inputLabelUnfocused" for="ProcessingIntervalHours">Processing Interval (hours):</label>
                        <input id="ProcessingIntervalHours" name="ProcessingIntervalHours" type="number" min="1" max="168" />
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
            const pluginId = "YourPluginGuidHere";
            
            function loadConfig() {
                Dashboard.showLoadingMsg();
                
                ApiClient.getPluginConfiguration(pluginId).then(function(config) {
                    document.getElementById('ApiKey').value = config.ApiKey || '';
                    document.getElementById('EnableAutomaticProcessing').checked = config.EnableAutomaticProcessing;
                    document.getElementById('PreferredQuality').value = config.PreferredQuality || '720p';
                    document.getElementById('ProcessingIntervalHours').value = config.ProcessingIntervalHours || 24;
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
                    PreferredQuality: document.getElementById('PreferredQuality').value,
                    ProcessingIntervalHours: parseInt(document.getElementById('ProcessingIntervalHours').value),
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

## Dependency Injection

### Service Implementation Example

```csharp
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace YourPlugin.Services;

public class YourApiService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<YourApiService> _logger;

    public YourApiService(HttpClient httpClient, ILogger<YourApiService> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<List<YourModel>> SearchAsync(string query, string apiKey, CancellationToken cancellationToken = default)
    {
        try
        {
            if (string.IsNullOrEmpty(apiKey))
            {
                throw new ArgumentException("API key is required", nameof(apiKey));
            }

            var url = $"https://api.example.com/search?q={Uri.EscapeDataString(query)}&api_key={apiKey}";
            
            _logger.LogDebug("Making API request to: {Url}", url);
            
            var response = await _httpClient.GetStringAsync(url, cancellationToken);
            // Process response...
            
            return new List<YourModel>();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error searching for: {Query}", query);
            throw;
        }
    }
}
```

## Scheduled Tasks

```csharp
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using MediaBrowser.Model.Tasks;
using Microsoft.Extensions.Logging;

namespace YourPlugin.ScheduledTasks;

public class YourTask : IScheduledTask
{
    private readonly ILogger<YourTask> _logger;

    public YourTask(ILogger<YourTask> logger)
    {
        _logger = logger;
    }

    public string Name => "Your Task Name";
    public string Description => "Description of what your task does";
    public string Category => "Your Plugin";
    public string Key => "YourPluginTaskKey";
    public bool IsHidden => false;
    public bool IsEnabled => true;
    public bool IsLogged => true;

    public async Task ExecuteAsync(IProgress<double> progress, CancellationToken cancellationToken)
    {
        try
        {
            _logger.LogInformation("Starting task execution");
            progress?.Report(0);

            var config = Plugin.Instance?.Configuration;
            if (config == null)
            {
                _logger.LogError("Plugin configuration not available");
                return;
            }

            if (!config.EnableAutomaticProcessing)
            {
                _logger.LogInformation("Automatic processing is disabled");
                return;
            }

            // Your task logic here
            progress?.Report(50);
            
            // More processing...
            progress?.Report(100);
            
            _logger.LogInformation("Task completed successfully");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error executing task");
            throw;
        }
    }

    public IEnumerable<TaskTriggerInfo> GetDefaultTriggers()
    {
        var config = Plugin.Instance?.Configuration;
        var intervalHours = config?.ProcessingIntervalHours ?? 24;

        return new[]
        {
            new TaskTriggerInfo
            {
                Type = TaskTriggerInfo.TriggerInterval,
                IntervalTicks = TimeSpan.FromHours(intervalHours).Ticks
            }
        };
    }
}
```

## Packaging & Distribution

### 1. GitHub Actions Workflow

```yaml
name: Build and Release

on:
  push:
    tags: ['v*']
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: 8.0.x
        
    - name: Restore dependencies
      run: dotnet restore
      
    - name: Build
      run: dotnet build --configuration Release --no-restore
      
    - name: Test
      run: dotnet test --no-build --verbosity normal
      continue-on-error: true
      
    - name: Upload build artifacts
      uses: actions/upload-artifact@v4
      with:
        name: plugin-dll
        path: bin/Release/net8.0/YourPlugin.dll
        
  release:
    needs: build
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: 8.0.x
        
    - name: Build Release
      run: |
        dotnet restore
        dotnet build --configuration Release
        
    - name: Create Plugin Package
      run: |
        mkdir -p package
        cp bin/Release/net8.0/YourPlugin.dll package/
        cd package && zip -r ../YourPlugin.zip . && cd ..
        
    - name: Calculate MD5
      id: md5
      run: |
        MD5=$(md5sum YourPlugin.zip | cut -d' ' -f1)
        echo "checksum=$MD5" >> $GITHUB_OUTPUT
        echo "MD5: $MD5"
        
    - name: Create Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body: |
          ## Installation
          
          1. Download `YourPlugin.zip` from assets below
          2. Extract and copy `YourPlugin.dll` to Jellyfin plugins directory
          3. Restart Jellyfin
          4. Configure plugin with your API key
          
          **Or use Custom Repository:**
          Add `https://raw.githubusercontent.com/yourusername/yourplugin/main/manifest.json`
          
          ## MD5 Checksum
          ```
          ${{ steps.md5.outputs.checksum }}
          ```
        
    - name: Upload Release Asset
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: YourPlugin.zip
        asset_name: YourPlugin.zip
        asset_content_type: application/zip
```

### 2. Manifest.json for Plugin Repository

```json
[
  {
    "guid": "your-plugin-guid",
    "name": "Your Plugin Name",
    "description": "Brief description",
    "overview": "Detailed description with features",
    "owner": "yourusername",
    "category": "General",
    "versions": [
      {
        "version": "1.0.0.0",
        "changelog": "Initial release with core features",
        "targetAbi": "10.8.13.0",
        "sourceUrl": "https://github.com/yourusername/yourplugin/releases/download/v1.0.0/YourPlugin.zip",
        "checksum": "your-md5-checksum-here",
        "timestamp": "2025-01-01T00:00:00Z"
      }
    ]
  }
]
```

## Testing & Debugging

### 1. Local Development Setup

```bash
# Build plugin
dotnet build --configuration Release

# Find your Jellyfin plugins directory
# Linux: /var/lib/jellyfin/plugins/
# Windows: C:\ProgramData\Jellyfin\Server\plugins\
# Docker: /config/plugins/

# Copy plugin
cp bin/Release/net8.0/YourPlugin.dll /path/to/jellyfin/plugins/

# Restart Jellyfin
sudo systemctl restart jellyfin
```

### 2. Logging Best Practices

```csharp
// Use appropriate log levels
_logger.LogDebug("Detailed debug information");
_logger.LogInformation("General information about processing");
_logger.LogWarning("Something unexpected but not critical");
_logger.LogError(ex, "Error processing item: {ItemName}", itemName);

// Include context in log messages
_logger.LogInformation("Processing {ItemCount} items with quality {Quality}", 
    items.Count, config.PreferredQuality);

// Use structured logging
_logger.LogInformation("Task completed. Processed: {Processed}, Failed: {Failed}, Duration: {Duration}ms",
    processedCount, failedCount, stopwatch.ElapsedMilliseconds);
```

## Common Pitfalls

### 1. **Package Format Issues**
- ❌ Don't include unnecessary files in ZIP packages
- ✅ Only include the compiled DLL in the ZIP root
- ✅ Use MD5 checksums (not SHA256) for Jellyfin compatibility

### 2. **Configuration Page Problems**
- ❌ Don't use jQuery (compatibility issues)
- ✅ Use vanilla JavaScript with proper error handling
- ✅ Always validate form inputs before saving

### 3. **Resource Management**
- ❌ Don't forget to dispose HttpClient instances
- ✅ Use dependency injection for HttpClient
- ✅ Implement proper cancellation token support

### 4. **File Operations**
- ❌ Don't assume specific file system behaviors
- ✅ Use Path.Combine for cross-platform paths
- ✅ Handle file permissions and access errors gracefully

### 5. **API Integration**
- ❌ Don't make API calls without rate limiting
- ✅ Add delays between requests to respect API limits
- ✅ Implement proper retry logic with exponential backoff

## Best Practices

### 1. **Error Handling**
```csharp
try
{
    // Your code here
}
catch (HttpRequestException ex)
{
    _logger.LogError(ex, "Network error occurred");
    // Handle network-specific errors
}
catch (TaskCanceledException ex)
{
    _logger.LogWarning("Operation was cancelled");
    // Handle cancellation gracefully
}
catch (Exception ex)
{
    _logger.LogError(ex, "Unexpected error occurred");
    // Handle unexpected errors
    throw; // Re-throw if you can't handle it
}
```

### 2. **Async/Await Patterns**
```csharp
// ✅ Good: Proper async method
public async Task<Result> ProcessAsync(CancellationToken cancellationToken = default)
{
    var result = await SomeAsyncOperation(cancellationToken);
    return ProcessResult(result);
}

// ❌ Avoid: Blocking on async methods
public Result Process()
{
    return ProcessAsync().Result; // This can cause deadlocks
}
```

### 3. **Configuration Validation**
```csharp
public bool ValidateConfiguration(PluginConfiguration config, out string error)
{
    error = string.Empty;
    
    if (string.IsNullOrWhiteSpace(config.ApiKey))
    {
        error = "API Key is required";
        return false;
    }
    
    if (config.ProcessingIntervalHours < 1)
    {
        error = "Processing interval must be at least 1 hour";
        return false;
    }
    
    return true;
}
```

### 4. **Performance Considerations**
- Use `ConfigureAwait(false)` in library code
- Implement proper pagination for large datasets
- Cache frequently accessed data when appropriate
- Use streaming for large file operations

### 5. **Version Management**
- Use semantic versioning (MAJOR.MINOR.PATCH.BUILD)
- Maintain backwards compatibility when possible
- Document breaking changes clearly
- Test upgrade scenarios thoroughly

## Quick Start Checklist

- [ ] Create project with proper .csproj file
- [ ] Implement main Plugin class with IHasWebPages
- [ ] Create PluginConfiguration class
- [ ] Build configuration web page with vanilla JS
- [ ] Implement core services with dependency injection
- [ ] Add scheduled task if needed
- [ ] Create manifest.json for distribution
- [ ] Set up GitHub Actions for automated releases
- [ ] Test installation and configuration flow
- [ ] Document usage and troubleshooting

## Additional Resources

- [Jellyfin Plugin Documentation](https://jellyfin.org/docs/general/server/plugins/)
- [Jellyfin Plugin Template](https://github.com/jellyfin/jellyfin-plugin-template)
- [.NET 8 Documentation](https://docs.microsoft.com/en-us/dotnet/core/)
- [ASP.NET Core Dependency Injection](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection)

---

This guide is based on real-world experience building production Jellyfin plugins. Save this as a reference for future plugin development projects!
