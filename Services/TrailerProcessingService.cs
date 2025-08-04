using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using MediaBrowser.Controller.Entities.Movies;
using MediaBrowser.Controller.Library;
using MediaBrowser.Model.Querying;
using Microsoft.Extensions.Logging;
using TMDBintros.Configuration;
using TMDBintros.Models;

namespace TMDBintros.Services;

/// <summary>
/// Main service for processing movie trailers.
/// </summary>
public class TrailerProcessingService
{
    private readonly TmdbApiService _tmdbApiService;
    private readonly VideoDownloadService _downloadService;
    private readonly FileManagementService _fileService;
    private readonly ILibraryManager _libraryManager;
    private readonly ILogger _logger;

    /// <summary>
    /// Initializes a new instance of the <see cref="TrailerProcessingService"/> class.
    /// </summary>
    /// <param name="tmdbApiService">TMDB API service.</param>
    /// <param name="downloadService">Video download service.</param>
    /// <param name="fileService">File management service.</param>
    /// <param name="libraryManager">Jellyfin library manager.</param>
    /// <param name="logger">Logger instance.</param>
    public TrailerProcessingService(
        TmdbApiService tmdbApiService,
        VideoDownloadService downloadService,
        FileManagementService fileService,
        ILibraryManager libraryManager,
        ILogger logger)
    {
        _tmdbApiService = tmdbApiService;
        _downloadService = downloadService;
        _fileService = fileService;
        _libraryManager = libraryManager;
        _logger = logger;
    }

    /// <summary>
    /// Processes all movies in the library to download missing trailers.
    /// </summary>
    /// <param name="config">Plugin configuration.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Processing results.</returns>
    public async Task<ProcessingResult> ProcessAllMoviesAsync(PluginConfiguration config, CancellationToken cancellationToken = default)
    {
        var result = new ProcessingResult();

        if (string.IsNullOrEmpty(config.TmdbApiKey))
        {
            _logger.LogError("TMDB API key is not configured");
            result.Errors.Add("TMDB API key is not configured");
            return result;
        }

        try
        {
            _logger.LogInformation("Starting trailer processing for all movies");

            // Get all movies from all libraries
            var movies = new List<Movie>();
            foreach (var folder in _libraryManager.RootFolder.Children.OfType<MediaBrowser.Controller.Entities.Folder>())
            {
                var folderMovies = folder.GetRecursiveChildren().OfType<Movie>().Where(m => !m.IsVirtualItem);
                movies.AddRange(folderMovies);
            }

            _logger.LogInformation("Found {MovieCount} movies to process", movies.Count);

            foreach (var movie in movies)
            {
                if (cancellationToken.IsCancellationRequested)
                {
                    break;
                }

                try
                {
                    var movieResult = await ProcessSingleMovieAsync(movie, config, cancellationToken);
                    result.MoviesProcessed++;

                    if (movieResult.Success)
                    {
                        result.TrailersDownloaded++;
                        _logger.LogInformation("Successfully processed movie: {MovieTitle}", movie.Name);
                    }
                    else if (movieResult.TrailerExists)
                    {
                        result.TrailersSkipped++;
                        if (config.EnableDetailedLogging)
                        {
                            _logger.LogDebug("Trailer already exists for movie: {MovieTitle}", movie.Name);
                        }
                    }
                    else
                    {
                        result.TrailersFailed++;
                        if (config.EnableDetailedLogging)
                        {
                            _logger.LogWarning("Failed to process movie: {MovieTitle}. Reason: {Reason}", 
                                movie.Name, movieResult.ErrorMessage);
                        }
                    }
                }
                catch (Exception ex)
                {
                    result.TrailersFailed++;
                    _logger.LogError(ex, "Error processing movie: {MovieTitle}", movie.Name);
                    result.Errors.Add($"Error processing {movie.Name}: {ex.Message}");
                }

                // Add a small delay to be respectful to the TMDB API
                await Task.Delay(1000, cancellationToken);
            }

            _logger.LogInformation("Trailer processing completed. Processed: {Processed}, Downloaded: {Downloaded}, Skipped: {Skipped}, Failed: {Failed}",
                result.MoviesProcessed, result.TrailersDownloaded, result.TrailersSkipped, result.TrailersFailed);

            return result;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during trailer processing");
            result.Errors.Add($"Processing error: {ex.Message}");
            return result;
        }
    }

    /// <summary>
    /// Processes a single movie to download its trailer.
    /// </summary>
    /// <param name="movie">Movie to process.</param>
    /// <param name="config">Plugin configuration.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Processing result for the movie.</returns>
    public async Task<MovieProcessingResult> ProcessSingleMovieAsync(Movie movie, PluginConfiguration config, CancellationToken cancellationToken = default)
    {
        var result = new MovieProcessingResult { MovieTitle = movie.Name };

        try
        {
            if (string.IsNullOrEmpty(movie.Path) || !File.Exists(movie.Path))
            {
                result.ErrorMessage = "Movie file not found";
                return result;
            }

            // Check if trailer already exists
            var year = movie.ProductionYear;
            if (!config.OverwriteExistingTrailers && 
                _fileService.TrailerExists(movie.Path, config.TrailerFolderName, config.OrganizeInSubfolders, movie.Name, year))
            {
                result.TrailerExists = true;
                return result;
            }

            // Search for movie on TMDB
            var tmdbMovies = await _tmdbApiService.SearchMoviesAsync(movie.Name, year, config.TmdbApiKey, cancellationToken);
            if (!tmdbMovies.Any())
            {
                result.ErrorMessage = "Movie not found on TMDB";
                return result;
            }

            // Use the first (best) match
            var tmdbMovie = tmdbMovies.First();
            
            // Get trailers for the movie
            var videos = await _tmdbApiService.GetMovieVideosAsync(tmdbMovie.Id, config.TmdbApiKey, cancellationToken);
            if (!videos.Any())
            {
                result.ErrorMessage = "No videos found on TMDB";
                return result;
            }

            // Find the best trailer
            var bestTrailer = _tmdbApiService.FindBestTrailer(videos, config.PreferredQuality);
            if (bestTrailer == null)
            {
                result.ErrorMessage = "No suitable trailer found";
                return result;
            }

            // Download the trailer
            var success = await DownloadTrailerAsync(movie, bestTrailer, config, cancellationToken);
            if (success)
            {
                result.Success = true;
                result.TrailerUrl = $"https://www.youtube.com/watch?v={bestTrailer.Key}";
            }
            else
            {
                result.ErrorMessage = "Failed to download trailer";
            }

            return result;
        }
        catch (Exception ex)
        {
            result.ErrorMessage = ex.Message;
            _logger.LogError(ex, "Error processing movie: {MovieTitle}", movie.Name);
            return result;
        }
    }

    /// <summary>
    /// Downloads a trailer for a specific movie.
    /// </summary>
    /// <param name="movie">Movie entity.</param>
    /// <param name="trailer">Trailer to download.</param>
    /// <param name="config">Plugin configuration.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>True if successful, false otherwise.</returns>
    private async Task<bool> DownloadTrailerAsync(Movie movie, TmdbVideo trailer, PluginConfiguration config, CancellationToken cancellationToken)
    {
        string? tempFilePath = null;
        string? tempDirectory = null;

        try
        {
            // Create temporary directory for download
            tempDirectory = Path.Combine(Path.GetTempPath(), $"jellyfin_trailer_{Guid.NewGuid()}");
            Directory.CreateDirectory(tempDirectory);

            // Generate temporary file name
            var tempFileName = _fileService.GenerateTrailerFileName(movie.Name, movie.ProductionYear, trailer.Name);
            tempFilePath = Path.Combine(tempDirectory, tempFileName);

            // Download the trailer
            var downloadSuccess = await _downloadService.DownloadYouTubeVideoAsync(
                trailer.Key, 
                tempFilePath, 
                config.PreferredQuality, 
                config.MaxTrailerDurationMinutes, 
                cancellationToken);

            if (!downloadSuccess)
            {
                return false;
            }

            // Find the actual downloaded file (yt-dlp may have used a different extension)
            var actualFilePath = _downloadService.GetDownloadedFilePath(tempFilePath);
            if (actualFilePath == null || !File.Exists(actualFilePath))
            {
                _logger.LogError("Downloaded file not found for movie: {MovieTitle}", movie.Name);
                return false;
            }

            // Get destination directory
            var destinationDir = _fileService.GetTrailerDirectory(
                movie.Path, 
                config.TrailerFolderName, 
                config.OrganizeInSubfolders, 
                movie.Name, 
                movie.ProductionYear);

            // Move trailer to final location
            var finalFileName = _fileService.GenerateTrailerFileName(movie.Name, movie.ProductionYear, trailer.Name);
            var finalPath = _fileService.MoveAndRenameTrailer(
                actualFilePath, 
                destinationDir, 
                finalFileName, 
                config.OverwriteExistingTrailers);

            return finalPath != null;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error downloading trailer for movie: {MovieTitle}", movie.Name);
            return false;
        }
        finally
        {
            // Cleanup temporary files
            if (!string.IsNullOrEmpty(tempDirectory))
            {
                _fileService.CleanupTempFiles(tempDirectory);
            }
        }
    }
}

/// <summary>
/// Result of processing all movies.
/// </summary>
public class ProcessingResult
{
    public int MoviesProcessed { get; set; }
    public int TrailersDownloaded { get; set; }
    public int TrailersSkipped { get; set; }
    public int TrailersFailed { get; set; }
    public List<string> Errors { get; set; } = new();
}

/// <summary>
/// Result of processing a single movie.
/// </summary>
public class MovieProcessingResult
{
    public string MovieTitle { get; set; } = string.Empty;
    public bool Success { get; set; }
    public bool TrailerExists { get; set; }
    public string? ErrorMessage { get; set; }
    public string? TrailerUrl { get; set; }
}
