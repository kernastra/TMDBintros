using MediaBrowser.Model.Plugins;

namespace TMDBintros.Configuration;

/// <summary>
/// Plugin configuration.
/// </summary>
public class PluginConfiguration : BasePluginConfiguration
{
    /// <summary>
    /// Gets or sets the TMDB API key.
    /// </summary>
    public string TmdbApiKey { get; set; } = string.Empty;

    /// <summary>
    /// Gets or sets a value indicating whether to download trailers automatically.
    /// </summary>
    public bool EnableAutomaticDownload { get; set; } = true;

    /// <summary>
    /// Gets or sets the preferred video quality for trailers.
    /// </summary>
    public string PreferredQuality { get; set; } = "1080";

    /// <summary>
    /// Gets or sets the maximum trailer duration in minutes.
    /// </summary>
    public int MaxTrailerDurationMinutes { get; set; } = 5;

    /// <summary>
    /// Gets or sets a value indicating whether to overwrite existing trailers.
    /// </summary>
    public bool OverwriteExistingTrailers { get; set; } = false;

    /// <summary>
    /// Gets or sets the custom trailer folder name.
    /// </summary>
    public string TrailerFolderName { get; set; } = "trailers";

    /// <summary>
    /// Gets or sets a value indicating whether to organize trailers in subfolders.
    /// </summary>
    public bool OrganizeInSubfolders { get; set; } = true;

    /// <summary>
    /// Gets or sets the interval in hours for automatic processing.
    /// </summary>
    public double ProcessingIntervalHours { get; set; } = 24.0;

    /// <summary>
    /// Gets or sets a value indicating whether to log detailed processing information.
    /// </summary>
    public bool EnableDetailedLogging { get; set; } = false;
}
