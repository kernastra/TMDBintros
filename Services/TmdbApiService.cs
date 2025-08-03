using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using TMDBintros.Models;

namespace TMDBintros.Services;

/// <summary>
/// Service for interacting with the TMDB API.
/// </summary>
public class TmdbApiService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger _logger;
    private const string BaseUrl = "https://api.themoviedb.org/3";

    /// <summary>
    /// Initializes a new instance of the <see cref="TmdbApiService"/> class.
    /// </summary>
    /// <param name="httpClient">HTTP client for API requests.</param>
    /// <param name="logger">Logger instance.</param>
    public TmdbApiService(HttpClient httpClient, ILogger logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    /// <summary>
    /// Searches for movies by title and year.
    /// </summary>
    /// <param name="title">Movie title.</param>
    /// <param name="year">Release year (optional).</param>
    /// <param name="apiKey">TMDB API key.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>List of matching movies.</returns>
    public async Task<List<TmdbMovie>> SearchMoviesAsync(string title, int? year, string apiKey, CancellationToken cancellationToken = default)
    {
        try
        {
            var query = Uri.EscapeDataString(title);
            var url = $"{BaseUrl}/search/movie?api_key={apiKey}&query={query}";
            
            if (year.HasValue)
            {
                url += $"&year={year}";
            }

            _logger.LogDebug("Searching TMDB for movie: {Title} ({Year})", title, year);

            var response = await _httpClient.GetAsync(url, cancellationToken);
            response.EnsureSuccessStatusCode();

            var content = await response.Content.ReadAsStringAsync(cancellationToken);
            var searchResponse = JsonSerializer.Deserialize<TmdbSearchResponse>(content);

            return searchResponse?.Results ?? new List<TmdbMovie>();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error searching for movie: {Title}", title);
            return new List<TmdbMovie>();
        }
    }

    /// <summary>
    /// Gets videos (trailers) for a specific movie.
    /// </summary>
    /// <param name="movieId">TMDB movie ID.</param>
    /// <param name="apiKey">TMDB API key.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>List of videos for the movie.</returns>
    public async Task<List<TmdbVideo>> GetMovieVideosAsync(int movieId, string apiKey, CancellationToken cancellationToken = default)
    {
        try
        {
            var url = $"{BaseUrl}/movie/{movieId}/videos?api_key={apiKey}";

            _logger.LogDebug("Getting videos for TMDB movie ID: {MovieId}", movieId);

            var response = await _httpClient.GetAsync(url, cancellationToken);
            response.EnsureSuccessStatusCode();

            var content = await response.Content.ReadAsStringAsync(cancellationToken);
            var videosResponse = JsonSerializer.Deserialize<TmdbVideosResponse>(content);

            return videosResponse?.Results ?? new List<TmdbVideo>();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting videos for movie ID: {MovieId}", movieId);
            return new List<TmdbVideo>();
        }
    }

    /// <summary>
    /// Finds the best trailer for a movie based on preferences.
    /// </summary>
    /// <param name="videos">List of videos to search through.</param>
    /// <param name="preferredQuality">Preferred video quality (480, 720, 1080).</param>
    /// <returns>The best matching trailer or null if none found.</returns>
    public TmdbVideo? FindBestTrailer(List<TmdbVideo> videos, string preferredQuality)
    {
        if (!videos.Any())
        {
            return null;
        }

        // Filter for YouTube trailers only
        var trailers = videos
            .Where(v => v.Site.Equals("YouTube", StringComparison.OrdinalIgnoreCase) && 
                       v.Type.Equals("Trailer", StringComparison.OrdinalIgnoreCase))
            .ToList();

        if (!trailers.Any())
        {
            _logger.LogDebug("No YouTube trailers found");
            return null;
        }

        // Priority order: Official trailers first, then by quality preference
        var qualitySize = preferredQuality switch
        {
            "1080" => 1080,
            "720" => 720,
            "480" => 480,
            _ => 720
        };

        var bestTrailer = trailers
            .OrderByDescending(t => t.Official)
            .ThenBy(t => Math.Abs(t.Size - qualitySize))
            .ThenByDescending(t => t.PublishedAt)
            .FirstOrDefault();

        if (bestTrailer != null)
        {
            _logger.LogDebug("Selected trailer: {Name} (Quality: {Size}, Official: {Official})", 
                bestTrailer.Name, bestTrailer.Size, bestTrailer.Official);
        }

        return bestTrailer;
    }
}
