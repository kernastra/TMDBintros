# Changelog

All notable changes to the TMDB Trailers plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2024-08-03

### Added
- Initial release of TMDB Trailers plugin
- TMDB API integration for movie and trailer search
- YouTube trailer downloading using yt-dlp
- Configurable video quality selection (480p, 720p, 1080p)
- Smart file organization with customizable folder structures
- Automatic scheduled processing of new movies
- Web-based configuration interface
- Support for trailer duration filtering
- Overwrite control for existing trailers
- Detailed logging options for troubleshooting
- Cross-platform compatibility (Linux, Windows, macOS)

### Features
- **Automatic Discovery**: Scans movie library for files
- **Quality Control**: Preferred video quality selection
- **Organization**: Configurable folder structures and naming
- **Scheduling**: Automatic processing at configurable intervals
- **Safety**: File existence checks and overwrite protection
- **Logging**: Comprehensive logging with debug options

### Requirements
- Jellyfin 10.8.13 or later
- .NET 8.0 runtime
- yt-dlp for video downloading
- TMDB API key (free registration required)

### Known Issues
- None at initial release

[Unreleased]: https://github.com/YourGitHubUsername/TMDBintros/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/YourGitHubUsername/TMDBintros/releases/tag/v1.0.0
