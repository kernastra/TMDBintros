# Upcoming Movies Feature - Usage Guide

## Overview

The upcoming movies feature automatically downloads trailers for movies releasing in the next 3-6 months, with comprehensive filtering options and optional Radarr integration.

## Quick Start

1. **Configure your environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Enable upcoming movies:**
   ```bash
   UPCOMING_ENABLED=true
   UPCOMING_DAYS_AHEAD=90
   UPCOMING_MAX_MOVIES=50
   ```

3. **Run upcoming movies:**
   ```bash
   # List upcoming movies (no download)
   make upcoming-list
   
   # Download trailers for upcoming movies
   make upcoming
   
   # Clean up old trailers
   make upcoming-cleanup
   ```

## Configuration Options

### Basic Settings
```bash
# Enable/disable upcoming movies feature
UPCOMING_ENABLED=true

# How far ahead to look (days)
UPCOMING_DAYS_AHEAD=90

# Maximum movies to process per run
UPCOMING_MAX_MOVIES=50

# Maximum trailers to download per movie (1-5 recommended)
UPCOMING_MAX_TRAILERS_PER_MOVIE=3

# Minimum popularity threshold (0-100+)
UPCOMING_POPULARITY_THRESHOLD=10.0

# Days to keep old upcoming trailers
UPCOMING_CLEANUP_DAYS=30
```

### Content Filters
```bash
# Filter by country (ISO codes)
UPCOMING_FILTER_COUNTRIES=US,GB,CA,AU

# Filter by language (ISO codes)
UPCOMING_FILTER_LANGUAGES=en,en-US

# Include specific genres (TMDB genre IDs)
UPCOMING_FILTER_GENRES=28,12,878,53
# 28=Action, 12=Adventure, 878=Sci-Fi, 53=Thriller

# Exclude specific genres
UPCOMING_EXCLUDE_GENRES=27,99
# 27=Horror, 99=Documentary
```

### Production Filters
```bash
# Filter by studios/production companies
UPCOMING_FILTER_STUDIOS=Marvel,Warner,Disney,Universal,Sony

# Exclude specific studios
UPCOMING_EXCLUDE_STUDIOS=Asylum,Troma

# Filter by directors (partial name matching)
UPCOMING_FILTER_DIRECTORS=Christopher Nolan,Denis Villeneuve

# Filter by actors (partial name matching)
UPCOMING_FILTER_ACTORS=Tom Hanks,Meryl Streep
```

### Quality Filters
```bash
# Minimum vote average (0.0-10.0)
UPCOMING_MIN_VOTE_AVERAGE=6.0

# Minimum vote count
UPCOMING_MIN_VOTE_COUNT=100

# Runtime filters (minutes)
UPCOMING_MIN_RUNTIME=90
UPCOMING_MAX_RUNTIME=180

# Budget filter (USD)
UPCOMING_MIN_BUDGET=10000000

# Only franchise movies (part of collection)
UPCOMING_FRANCHISE_ONLY=false

# Only original movies (not sequels)
UPCOMING_ORIGINAL_ONLY=false
```

### Content Rating Filters
```bash
# Include specific ratings
UPCOMING_FILTER_RATINGS=PG,PG-13,R

# Exclude specific ratings
UPCOMING_EXCLUDE_RATINGS=NC-17,NR
```

## Radarr Integration

### Configuration
```bash
# Enable Radarr integration
RADARR_ENABLED=true
RADARR_URL=http://localhost:7878
RADARR_API_KEY=your_radarr_api_key

# Integration mode: upcoming, radarr_only, or hybrid
RADARR_INTEGRATION_MODE=hybrid
```

### Integration Modes

#### 1. `upcoming` (Default)
- Download trailers for all popular upcoming movies
- Store in `_upcoming_trailers/` folder
- Manual copy when you add movies to your library

#### 2. `radarr_only`
- Only download trailers for movies in your Radarr wanted list
- Wait for Radarr to create movie folders
- Place trailers directly in Radarr movie folders

#### 3. `hybrid`
- Download all popular upcoming trailers to `_upcoming_trailers/`
- Prioritize movies that are already in Radarr
- Auto-move trailers when Radarr creates movie folders

## Usage Examples

### Example 1: Marvel/Disney Fan
```bash
# Focus on big studio releases
UPCOMING_FILTER_COUNTRIES=US
UPCOMING_FILTER_STUDIOS=Marvel,Disney,Pixar,Lucasfilm
UPCOMING_FILTER_GENRES=28,12,878,16
UPCOMING_MIN_VOTE_AVERAGE=6.5
UPCOMING_MIN_BUDGET=50000000
```

### Example 2: Quality Cinema
```bash
# Focus on critically acclaimed films
UPCOMING_FILTER_COUNTRIES=US,GB,FR,DE
UPCOMING_FILTER_DIRECTORS=Christopher Nolan,Denis Villeneuve,Greta Gerwig
UPCOMING_MIN_VOTE_AVERAGE=7.0
UPCOMING_MIN_VOTE_COUNT=200
UPCOMING_EXCLUDE_GENRES=27,99,10770
```

### Example 3: Action Enthusiast
```bash
# Focus on action and thriller movies
UPCOMING_FILTER_GENRES=28,53,80
UPCOMING_EXCLUDE_GENRES=35,10749,99
UPCOMING_MIN_RUNTIME=90
UPCOMING_MAX_RUNTIME=150
UPCOMING_MIN_VOTE_AVERAGE=6.0
UPCOMING_MAX_TRAILERS_PER_MOVIE=5     # Get more trailers for action movies
```

### Example 4: Minimalist Setup
```bash
# Conservative setup - only 1 trailer per movie to save storage
UPCOMING_FILTER_COUNTRIES=US,GB
UPCOMING_MIN_VOTE_AVERAGE=7.0
UPCOMING_MAX_TRAILERS_PER_MOVIE=1     # Only the best trailer per movie
UPCOMING_MAX_MOVIES=25                # Fewer movies, higher quality
```

### Example 5: Comprehensive Collection
```bash
# Maximum trailers for comprehensive preview experience
UPCOMING_FILTER_COUNTRIES=US,GB,CA,AU
UPCOMING_MAX_TRAILERS_PER_MOVIE=5     # Download up to 5 trailers per movie
UPCOMING_MAX_MOVIES=100               # Process more movies
UPCOMING_MIN_VOTE_AVERAGE=5.0         # Lower threshold for more variety
```

## Commands

### Make Commands
```bash
# List upcoming movies without downloading
make upcoming-list

# Download upcoming movie trailers
make upcoming

# Clean up old upcoming trailers
make upcoming-cleanup
```

### Direct Python Commands
```bash
# List only
python tmdb_upcoming.py --list-only

# Download with custom cleanup days
python tmdb_upcoming.py --cleanup-days 45

# Cleanup old trailers
python tmdb_upcoming.py --cleanup
```

## File Structure

```
jellyfin_movies/
├── _upcoming_trailers/          # Upcoming movies storage
│   ├── README.md               # Auto-generated info
│   ├── Movie Name (2025)/
│   │   └── trailers/
│   │       ├── trailer_1.mp4
│   │       └── trailer_2.mp4
│   └── Another Movie (2025)/
│       └── trailers/
└── Regular Movie (2024)/       # Your existing library
    ├── movie.mkv
    └── trailers/
```

## Docker Usage

```bash
# Run upcoming movies service
docker-compose --profile upcoming up tmdb-upcoming

# One-time run
docker-compose run --rm tmdb-upcoming python tmdb_upcoming.py --list-only
```

## Troubleshooting

### Common Issues

1. **No movies found**
   - Check your filters aren't too restrictive
   - Verify TMDB API key is valid
   - Increase `UPCOMING_DAYS_AHEAD`

2. **Too many movies**
   - Increase filter thresholds
   - Add genre exclusions
   - Reduce `UPCOMING_MAX_MOVIES`

3. **Radarr integration not working**
   - Verify Radarr URL and API key
   - Check Radarr is accessible from container
   - Review Radarr logs for API calls

### Debug Mode
```bash
# Enable debug logging
LOG_LEVEL=DEBUG

# Check what movies would be processed
python tmdb_upcoming.py --list-only
```

## Tips

1. **Start Conservative**: Begin with restrictive filters and gradually expand
2. **Monitor Storage**: Upcoming trailers can use significant disk space
3. **Regular Cleanup**: Run cleanup regularly to remove old trailers
4. **Test Filters**: Use `--list-only` to test filter combinations
5. **Radarr Integration**: Start with `hybrid` mode for best of both worlds

## Advanced Features

### Custom Genre IDs
Common TMDB genre IDs:
- 28: Action
- 12: Adventure  
- 16: Animation
- 35: Comedy
- 80: Crime
- 99: Documentary
- 18: Drama
- 10751: Family
- 14: Fantasy
- 36: History
- 27: Horror
- 10402: Music
- 9648: Mystery
- 10749: Romance
- 878: Science Fiction
- 10770: TV Movie
- 53: Thriller
- 10752: War
- 37: Western

### Production Company Examples
- Marvel Studios
- Walt Disney Pictures
- Warner Bros.
- Universal Pictures
- Sony Pictures
- Paramount Pictures
- 20th Century Studios
- MGM
- Lionsgate
- A24
- Focus Features
