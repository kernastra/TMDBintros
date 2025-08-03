using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using MediaBrowser.Controller.Library;
using MediaBrowser.Model.Tasks;
using Microsoft.Extensions.Logging;
using TMDBintros.Services;

namespace TMDBintros.ScheduledTasks;

/// <summary>
/// Scheduled task for downloading movie trailers.
/// </summary>
public class TrailerDownloadTask : IScheduledTask
{
    private readonly ILibraryManager _libraryManager;
    private readonly ILogger<TrailerDownloadTask> _logger;

    /// <summary>
    /// Initializes a new instance of the <see cref="TrailerDownloadTask"/> class.
    /// </summary>
    /// <param name="libraryManager">Library manager.</param>
    /// <param name="logger">Logger instance.</param>
    public TrailerDownloadTask(ILibraryManager libraryManager, ILogger<TrailerDownloadTask> logger)
    {
        _libraryManager = libraryManager;
        _logger = logger;
    }

    /// <inheritdoc />
    public string Name => "Download Movie Trailers";

    /// <inheritdoc />
    public string Description => "Downloads trailers for movies from TMDB";

    /// <inheritdoc />
    public string Category => "TMDB Trailers";

    /// <inheritdoc />
    public string Key => "TMDBTrailerDownload";

    /// <inheritdoc />
    public bool IsHidden => false;

    /// <inheritdoc />
    public bool IsEnabled => true;

    /// <inheritdoc />
    public bool IsLogged => true;

    /// <inheritdoc />
    public async Task ExecuteAsync(IProgress<double> progress, CancellationToken cancellationToken)
    {
        try
        {
            _logger.LogInformation("Starting trailer download task");
            progress?.Report(0);

            var config = Plugin.Instance?.Configuration;
            if (config == null)
            {
                _logger.LogError("Plugin configuration not available");
                return;
            }

            if (!config.EnableAutomaticDownload)
            {
                _logger.LogInformation("Automatic download is disabled in configuration");
                return;
            }

            if (string.IsNullOrEmpty(config.TmdbApiKey))
            {
                _logger.LogError("TMDB API key is not configured");
                return;
            }

            progress?.Report(10);

            // Create services manually since DI is complex in Jellyfin plugins
            using var httpClient = new HttpClient();
            var tmdbService = new TmdbApiService(httpClient, _logger);
            var downloadService = new VideoDownloadService(httpClient, _logger);
            var fileService = new FileManagementService(_logger);
            var processingService = new TrailerProcessingService(tmdbService, downloadService, fileService, _libraryManager, _logger);

            var result = await processingService.ProcessAllMoviesAsync(config, cancellationToken);

            progress?.Report(90);

            _logger.LogInformation(
                "Trailer download task completed. Processed: {Processed}, Downloaded: {Downloaded}, Skipped: {Skipped}, Failed: {Failed}",
                result.MoviesProcessed,
                result.TrailersDownloaded,
                result.TrailersSkipped,
                result.TrailersFailed);

            if (result.Errors.Any())
            {
                _logger.LogWarning("Task completed with {ErrorCount} errors", result.Errors.Count);
                foreach (var error in result.Errors)
                {
                    _logger.LogWarning("Error: {Error}", error);
                }
            }

            progress?.Report(100);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error executing trailer download task");
            throw;
        }
    }

    /// <inheritdoc />
    public IEnumerable<TaskTriggerInfo> GetDefaultTriggers()
    {
        var config = Plugin.Instance?.Configuration;
        var intervalHours = config?.ProcessingIntervalHours ?? 24.0;

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
