using System;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using Microsoft.Extensions.Logging;

namespace TMDBintros.Services;

/// <summary>
/// Service for managing trailer files and organization.
/// </summary>
public class FileManagementService
{
    private readonly ILogger _logger;

    /// <summary>
    /// Initializes a new instance of the <see cref="FileManagementService"/> class.
    /// </summary>
    /// <param name="logger">Logger instance.</param>
    public FileManagementService(ILogger logger)
    {
        _logger = logger;
    }

    /// <summary>
    /// Generates a safe file name for a trailer.
    /// </summary>
    /// <param name="movieTitle">Movie title.</param>
    /// <param name="year">Release year.</param>
    /// <param name="trailerName">Trailer name from TMDB.</param>
    /// <returns>Safe file name without extension.</returns>
    public string GenerateTrailerFileName(string movieTitle, int? year, string trailerName)
    {
        // Clean up the movie title and trailer name
        var cleanTitle = SanitizeFileName(movieTitle);
        var cleanTrailerName = SanitizeFileName(trailerName);

        // Create a descriptive file name
        var fileName = year.HasValue 
            ? $"{cleanTitle} ({year}) - {cleanTrailerName}" 
            : $"{cleanTitle} - {cleanTrailerName}";

        // Ensure the filename isn't too long (most filesystems have a 255 character limit)
        if (fileName.Length > 200)
        {
            fileName = fileName.Substring(0, 200);
        }

        return fileName;
    }

    /// <summary>
    /// Gets the appropriate directory for storing trailers.
    /// </summary>
    /// <param name="moviePath">Path to the movie file.</param>
    /// <param name="trailerFolderName">Name of the trailer subfolder.</param>
    /// <param name="organizeInSubfolders">Whether to organize in movie-specific subfolders.</param>
    /// <param name="movieTitle">Movie title (used if organizing in subfolders).</param>
    /// <param name="year">Release year (used if organizing in subfolders).</param>
    /// <returns>Directory path for storing trailers.</returns>
    public string GetTrailerDirectory(string moviePath, string trailerFolderName, bool organizeInSubfolders, string movieTitle, int? year)
    {
        var movieDirectory = Path.GetDirectoryName(moviePath);
        if (string.IsNullOrEmpty(movieDirectory))
        {
            throw new ArgumentException("Invalid movie path", nameof(moviePath));
        }

        var baseTrailerDir = Path.Combine(movieDirectory, trailerFolderName);

        if (!organizeInSubfolders)
        {
            return baseTrailerDir;
        }

        // Create a subfolder for this specific movie
        var movieFolderName = year.HasValue 
            ? $"{SanitizeFileName(movieTitle)} ({year})" 
            : SanitizeFileName(movieTitle);

        return Path.Combine(baseTrailerDir, movieFolderName);
    }

    /// <summary>
    /// Moves and renames a downloaded trailer file to its final location.
    /// </summary>
    /// <param name="sourcePath">Source file path.</param>
    /// <param name="destinationDirectory">Destination directory.</param>
    /// <param name="fileName">Desired file name without extension.</param>
    /// <param name="overwriteExisting">Whether to overwrite existing files.</param>
    /// <returns>Final file path or null if operation failed.</returns>
    public string? MoveAndRenameTrailer(string sourcePath, string destinationDirectory, string fileName, bool overwriteExisting)
    {
        try
        {
            if (!File.Exists(sourcePath))
            {
                _logger.LogError("Source file does not exist: {SourcePath}", sourcePath);
                return null;
            }

            var extension = Path.GetExtension(sourcePath);
            var finalFileName = fileName + extension;
            var destinationPath = Path.Combine(destinationDirectory, finalFileName);

            // Create destination directory if it doesn't exist
            Directory.CreateDirectory(destinationDirectory);

            // Check if destination file already exists
            if (File.Exists(destinationPath))
            {
                if (!overwriteExisting)
                {
                    _logger.LogInformation("Trailer already exists and overwrite is disabled: {DestinationPath}", destinationPath);
                    return destinationPath; // Consider this a success
                }

                _logger.LogInformation("Overwriting existing trailer: {DestinationPath}", destinationPath);
                File.Delete(destinationPath);
            }

            // Move and rename the file
            File.Move(sourcePath, destinationPath);
            _logger.LogInformation("Trailer moved to: {DestinationPath}", destinationPath);

            return destinationPath;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error moving trailer from {SourcePath} to {DestinationDirectory}", sourcePath, destinationDirectory);
            return null;
        }
    }

    /// <summary>
    /// Checks if a trailer already exists for a movie.
    /// </summary>
    /// <param name="moviePath">Path to the movie file.</param>
    /// <param name="trailerFolderName">Name of the trailer subfolder.</param>
    /// <param name="organizeInSubfolders">Whether trailers are organized in subfolders.</param>
    /// <param name="movieTitle">Movie title.</param>
    /// <param name="year">Release year.</param>
    /// <returns>True if a trailer exists, false otherwise.</returns>
    public bool TrailerExists(string moviePath, string trailerFolderName, bool organizeInSubfolders, string movieTitle, int? year)
    {
        try
        {
            var trailerDirectory = GetTrailerDirectory(moviePath, trailerFolderName, organizeInSubfolders, movieTitle, year);
            
            if (!Directory.Exists(trailerDirectory))
            {
                return false;
            }

            // Look for video files in the trailer directory
            var videoExtensions = new[] { ".mp4", ".webm", ".mkv", ".mov", ".avi" };
            var files = Directory.GetFiles(trailerDirectory)
                .Where(f => videoExtensions.Contains(Path.GetExtension(f).ToLowerInvariant()))
                .ToArray();

            return files.Length > 0;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error checking if trailer exists for movie: {MoviePath}", moviePath);
            return false;
        }
    }

    /// <summary>
    /// Sanitizes a file name by removing invalid characters.
    /// </summary>
    /// <param name="fileName">File name to sanitize.</param>
    /// <returns>Sanitized file name.</returns>
    private static string SanitizeFileName(string fileName)
    {
        if (string.IsNullOrEmpty(fileName))
        {
            return "Unknown";
        }

        // Remove invalid file name characters
        var invalidChars = Path.GetInvalidFileNameChars();
        var sanitized = string.Join("", fileName.Where(c => !invalidChars.Contains(c)));

        // Replace multiple spaces with single space
        sanitized = Regex.Replace(sanitized, @"\s+", " ");

        // Trim and handle empty result
        sanitized = sanitized.Trim();
        if (string.IsNullOrEmpty(sanitized))
        {
            sanitized = "Unknown";
        }

        return sanitized;
    }

    /// <summary>
    /// Cleans up temporary files and empty directories.
    /// </summary>
    /// <param name="tempDirectory">Temporary directory to clean up.</param>
    public void CleanupTempFiles(string tempDirectory)
    {
        try
        {
            if (Directory.Exists(tempDirectory))
            {
                Directory.Delete(tempDirectory, true);
                _logger.LogDebug("Cleaned up temporary directory: {TempDirectory}", tempDirectory);
            }
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to clean up temporary directory: {TempDirectory}", tempDirectory);
        }
    }
}
