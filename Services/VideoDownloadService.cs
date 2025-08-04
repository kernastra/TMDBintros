using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace TMDBintros.Services;

/// <summary>
/// Service for downloading videos from YouTube and other sources.
/// </summary>
public class VideoDownloadService
{
    private readonly ILogger _logger;
    private readonly HttpClient _httpClient;

    /// <summary>
    /// Initializes a new instance of the <see cref="VideoDownloadService"/> class.
    /// </summary>
    /// <param name="httpClient">HTTP client for downloading.</param>
    /// <param name="logger">Logger instance.</param>
    public VideoDownloadService(HttpClient httpClient, ILogger logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    /// <summary>
    /// Downloads a YouTube video using yt-dlp.
    /// </summary>
    /// <param name="videoKey">YouTube video key/ID.</param>
    /// <param name="outputPath">Output file path.</param>
    /// <param name="quality">Preferred quality (480, 720, 1080).</param>
    /// <param name="maxDurationMinutes">Maximum video duration in minutes.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>True if download succeeded, false otherwise.</returns>
    public async Task<bool> DownloadYouTubeVideoAsync(string videoKey, string outputPath, string quality, int maxDurationMinutes, CancellationToken cancellationToken = default)
    {
        try
        {
            // Check if yt-dlp is available
            if (!await IsYtDlpAvailableAsync())
            {
                _logger.LogError("yt-dlp is not available. Please install yt-dlp to download trailers.");
                return false;
            }

            var videoUrl = $"https://www.youtube.com/watch?v={videoKey}";
            var outputDir = Path.GetDirectoryName(outputPath);
            var fileNameWithoutExt = Path.GetFileNameWithoutExtension(outputPath);

            if (!Directory.Exists(outputDir))
            {
                Directory.CreateDirectory(outputDir!);
            }

            // Build yt-dlp command arguments
            var qualitySelector = quality switch
            {
                "1080" => "best[height<=1080]",
                "720" => "best[height<=720]",
                "480" => "best[height<=480]",
                _ => "best[height<=720]"
            };

            var arguments = new List<string>
            {
                "--format", qualitySelector,
                "--output", Path.Combine(outputDir!, $"{fileNameWithoutExt}.%(ext)s"),
                "--no-playlist",
                "--extract-flat", "false"
            };

            // Add duration filter if specified
            if (maxDurationMinutes > 0)
            {
                arguments.AddRange(new[] { "--match-filter", $"duration <= {maxDurationMinutes * 60}" });
            }

            arguments.Add(videoUrl);

            _logger.LogDebug("Starting download of YouTube video: {VideoKey} to {OutputPath}", videoKey, outputPath);

            // Get the correct yt-dlp binary path
            var ytDlpPath = GetYtDlpPath() ?? "yt-dlp";

            var processInfo = new ProcessStartInfo
            {
                FileName = ytDlpPath,
                Arguments = string.Join(" ", arguments.Select(arg => $"\"{arg}\"")),
                WorkingDirectory = outputDir,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = processInfo };
            
            var outputBuilder = new StringBuilder();
            var errorBuilder = new StringBuilder();

            process.OutputDataReceived += (sender, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                {
                    outputBuilder.AppendLine(e.Data);
                    _logger.LogDebug("yt-dlp output: {Output}", e.Data);
                }
            };

            process.ErrorDataReceived += (sender, e) =>
            {
                if (!string.IsNullOrEmpty(e.Data))
                {
                    errorBuilder.AppendLine(e.Data);
                    _logger.LogWarning("yt-dlp error: {Error}", e.Data);
                }
            };

            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            await process.WaitForExitAsync(cancellationToken);

            if (process.ExitCode == 0)
            {
                _logger.LogInformation("Successfully downloaded video: {VideoKey}", videoKey);
                return true;
            }
            else
            {
                _logger.LogError("yt-dlp failed with exit code {ExitCode}. Error: {Error}", 
                    process.ExitCode, errorBuilder.ToString());
                return false;
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error downloading YouTube video: {VideoKey}", videoKey);
            return false;
        }
    }

    /// <summary>
    /// Gets the path to the bundled yt-dlp binary for the current platform.
    /// </summary>
    /// <returns>Path to yt-dlp binary or null if not found.</returns>
    private string? GetYtDlpPath()
    {
        try
        {
            // Get the directory where the plugin assembly is located
            var assemblyLocation = Assembly.GetExecutingAssembly().Location;
            var pluginDirectory = Path.GetDirectoryName(assemblyLocation);
            
            if (string.IsNullOrEmpty(pluginDirectory))
            {
                return null;
            }

            var binariesPath = Path.Combine(pluginDirectory, "Resources", "binaries");
            
            // Determine the correct binary based on the platform
            string binaryName;
            if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
            {
                binaryName = "yt-dlp-windows-x64.exe";
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
            {
                binaryName = "yt-dlp-macos-x64";
            }
            else if (RuntimeInformation.IsOSPlatform(OSPlatform.FreeBSD))
            {
                binaryName = "yt-dlp-freebsd-x64";
            }
            else // Default to Linux
            {
                binaryName = "yt-dlp-linux-x64";
            }

            var ytDlpPath = Path.Combine(binariesPath, binaryName);
            
            if (File.Exists(ytDlpPath))
            {
                // Ensure the binary is executable on Unix systems
                if (!RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
                {
                    try
                    {
                        var chmodProcess = new ProcessStartInfo
                        {
                            FileName = "chmod",
                            Arguments = $"+x \"{ytDlpPath}\"",
                            UseShellExecute = false,
                            CreateNoWindow = true
                        };
                        using var process = Process.Start(chmodProcess);
                        process?.WaitForExit();
                    }
                    catch
                    {
                        // Ignore chmod errors - binary might already be executable
                    }
                }
                
                _logger.LogDebug("Found bundled yt-dlp at: {YtDlpPath}", ytDlpPath);
                return ytDlpPath;
            }
            
            _logger.LogWarning("Bundled yt-dlp binary not found at: {YtDlpPath}", ytDlpPath);
            return null;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting bundled yt-dlp path");
            return null;
        }
    }

    /// <summary>
    /// Checks if yt-dlp is available (either bundled or system-installed).
    /// </summary>
    /// <returns>True if yt-dlp is available, false otherwise.</returns>
    private async Task<bool> IsYtDlpAvailableAsync()
    {
        // First try to get the bundled version
        var ytDlpPath = GetYtDlpPath();
        if (!string.IsNullOrEmpty(ytDlpPath))
        {
            return await TestYtDlpBinary(ytDlpPath);
        }
        
        // Fall back to system-installed yt-dlp
        _logger.LogDebug("Bundled yt-dlp not found, trying system installation");
        return await TestYtDlpBinary("yt-dlp");
    }

    /// <summary>
    /// Tests if a yt-dlp binary is working.
    /// </summary>
    /// <param name="binaryPath">Path to the yt-dlp binary.</param>
    /// <returns>True if the binary works, false otherwise.</returns>
    private async Task<bool> TestYtDlpBinary(string binaryPath)
    {
        try
        {
            var processInfo = new ProcessStartInfo
            {
                FileName = binaryPath,
                Arguments = "--version",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = processInfo };
            process.Start();
            await process.WaitForExitAsync();

            var success = process.ExitCode == 0;
            if (success)
            {
                _logger.LogDebug("yt-dlp binary is working: {BinaryPath}", binaryPath);
            }
            else
            {
                _logger.LogWarning("yt-dlp binary test failed: {BinaryPath}, exit code: {ExitCode}", binaryPath, process.ExitCode);
            }
            
            return success;
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to test yt-dlp binary: {BinaryPath}", binaryPath);
            return false;
        }
    }

    /// <summary>
    /// Gets the final downloaded file path after yt-dlp processing.
    /// </summary>
    /// <param name="basePath">Base path without extension.</param>
    /// <returns>Actual downloaded file path or null if not found.</returns>
    public string? GetDownloadedFilePath(string basePath)
    {
        var directory = Path.GetDirectoryName(basePath);
        var fileName = Path.GetFileNameWithoutExtension(basePath);

        if (string.IsNullOrEmpty(directory) || string.IsNullOrEmpty(fileName))
        {
            return null;
        }

        // Common video extensions yt-dlp might use
        var extensions = new[] { ".mp4", ".webm", ".mkv", ".mov", ".avi" };

        foreach (var ext in extensions)
        {
            var fullPath = Path.Combine(directory, fileName + ext);
            if (File.Exists(fullPath))
            {
                return fullPath;
            }
        }

        return null;
    }
}
