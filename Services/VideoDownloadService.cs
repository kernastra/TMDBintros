using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
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

            var processInfo = new ProcessStartInfo
            {
                FileName = "yt-dlp",
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
    /// Checks if yt-dlp is available on the system.
    /// </summary>
    /// <returns>True if yt-dlp is available, false otherwise.</returns>
    private async Task<bool> IsYtDlpAvailableAsync()
    {
        try
        {
            var processInfo = new ProcessStartInfo
            {
                FileName = "yt-dlp",
                Arguments = "--version",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using var process = new Process { StartInfo = processInfo };
            process.Start();
            await process.WaitForExitAsync();

            return process.ExitCode == 0;
        }
        catch
        {
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
