<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# TMDB Trailers Jellyfin Plugin Development Instructions

This is a Jellyfin plugin project written in C# targeting .NET 8.0. The plugin integrates with The Movie Database (TMDB) API to automatically download movie trailers.

## Project Structure

- **Plugin.cs**: Main plugin entry point implementing IPlugin and IHasWebPages
- **Configuration/**: Plugin configuration classes and HTML configuration page
- **Models/**: TMDB API response models with JSON serialization
- **Services/**: Core business logic services
  - **TmdbApiService**: TMDB API integration for searching movies and trailers
  - **VideoDownloadService**: YouTube video downloading using yt-dlp
  - **FileManagementService**: File organization and naming
  - **TrailerProcessingService**: Main orchestration service
- **ScheduledTasks/**: Jellyfin scheduled task for automatic processing

## Key Technologies

- **Jellyfin Plugin Framework**: Uses Jellyfin.Controller and Jellyfin.Model packages
- **TMDB API**: RESTful API for movie and trailer metadata
- **yt-dlp**: External tool for downloading YouTube videos
- **Dependency Injection**: Microsoft.Extensions.DependencyInjection
- **System.Text.Json**: JSON serialization for API responses

## Development Guidelines

1. **Error Handling**: Always use try-catch blocks and log errors appropriately
2. **Async/Await**: Use async patterns for I/O operations (API calls, file operations)
3. **Cancellation Tokens**: Support cancellation in long-running operations
4. **Logging**: Use ILogger for debugging and operational logging
5. **Configuration**: Make features configurable through PluginConfiguration
6. **File Safety**: Sanitize file names and handle path operations safely
7. **API Rate Limiting**: Add delays between TMDB API calls to respect rate limits

## Common Patterns

- Services are registered in PluginServiceRegistrator for dependency injection
- Configuration is accessed via Plugin.Instance?.Configuration
- File operations should handle cross-platform path differences
- External process execution (yt-dlp) should capture output and handle errors
- TMDB API responses should be deserialized using System.Text.Json attributes

## Testing Considerations

- Mock external dependencies (HttpClient, file system, processes)
- Test with various movie titles and edge cases
- Verify file organization logic with different configuration options
- Test error scenarios (missing API key, network failures, etc.)

When making changes, ensure compatibility with Jellyfin 10.8.13+ and maintain backwards compatibility where possible.
