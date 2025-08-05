# 🎬 Upcoming Movies Feature

The TMDB Trailer Downloader v3.0.0+ includes a powerful **Upcoming Movies** feature that proactively downloads trailers for movies releasing in the next 3-6 months. This allows you to have trailers ready before you add the movies to your library!

## 🌟 Overview

This feature:
- 📅 **Fetches upcoming movies** from TMDB (next 3-6 months)
- 🎯 **Filters by popularity** to avoid obscure releases
- 📥 **Downloads trailers proactively** in Jellyfin-compatible format
- 📂 **Organizes in separate folder** (`_upcoming_trailers/`)
- 🔄 **Auto-cleanup** old movies past their release date
- 📊 **Tracks movie metadata** for easy management

## 📁 Directory Structure

```
/your/jellyfin/movies/
├── Existing Movie (2024)/
│   └── trailers/
│       ├── Existing Movie-trailer-1.mp4
│       └── Existing Movie-trailer-2.mp4
├── _upcoming_trailers/           ← New upcoming trailers folder
│   ├── README.md                ← Information about upcoming trailers
│   ├── The Batman 2 (2025)/
│   │   ├── movie_info.json      ← Movie metadata
│   │   └── trailers/
│   │       ├── The Batman 2-trailer-1.mp4
│   │       └── The Batman 2-trailer-2.mp4
│   └── Avengers 5 (2025)/
│       ├── movie_info.json
│       └── trailers/
│           ├── Avengers 5-trailer-1.mp4
│           └── Avengers 5-trailer-2.mp4
```

## ⚙️ Configuration

Add these settings to your `.env` file:

```bash
# Upcoming Movies Configuration
UPCOMING_ENABLED=true
UPCOMING_MONTHS_AHEAD=6          # Download trailers 6 months ahead
UPCOMING_MIN_POPULARITY=15.0     # Minimum TMDB popularity score
UPCOMING_MAX_MOVIES=50          # Maximum movies per run
UPCOMING_CLEANUP_DAYS=30        # Days after release to cleanup
```

### Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `UPCOMING_ENABLED` | `false` | Enable upcoming movies feature |
| `UPCOMING_MONTHS_AHEAD` | `6` | How many months ahead to search |
| `UPCOMING_MIN_POPULARITY` | `10.0` | Minimum TMDB popularity score (filters out obscure movies) |
| `UPCOMING_MAX_MOVIES` | `50` | Maximum movies to process per run |
| `UPCOMING_CLEANUP_DAYS` | `30` | Days after release date to remove old upcoming movies |

## 🚀 Usage

### Docker Commands (Recommended)

```bash
# Download upcoming movie trailers
make upcoming

# List downloaded upcoming trailers
make upcoming-list

# Clean up old upcoming movies
make upcoming-cleanup

# Or use docker-compose directly
docker-compose --profile upcoming run --rm tmdb-upcoming
docker-compose --profile upcoming run --rm tmdb-upcoming python3 tmdb_upcoming.py --list
docker-compose --profile upcoming run --rm tmdb-upcoming python3 tmdb_upcoming.py --cleanup
```

### Native Python Commands

```bash
# Download upcoming trailers
python3 tmdb_upcoming.py

# List upcoming movies with trailers
python3 tmdb_upcoming.py --list

# Clean up old movies
python3 tmdb_upcoming.py --cleanup --cleanup-days 45

# Custom configuration
python3 tmdb_upcoming.py --config-dir /etc/tmdb --log-level DEBUG
```

## 📊 Example Output

### Download Run
```
📽️  Fetching upcoming movies for next 6 months...
Page 1: Found 18 upcoming movies
Page 2: Found 15 upcoming movies
Total upcoming movies found: 33

[1/33] Processing: Dune: Part Three (2026) - Popularity: 145.2
✅ Successfully downloaded 3 trailers for Dune: Part Three (2026)

[2/33] Processing: Avatar 3 (2025) - Popularity: 89.4
✅ Successfully downloaded 2 trailers for Avatar 3 (2025)

✅ Upcoming trailers download completed!
   📊 Total movies: 33
   ✅ Successfully processed: 25
   ⏭️  Skipped (already exist): 5
   ❌ Errors: 3

📂 Trailers saved to: /movies/_upcoming_trailers
💡 When you add these movies to your library, copy the folders to your main movies directory
```

### List Command
```
📽️  Upcoming Movies with Trailers (25 total):

  🎬 Dune: Part Three (2026)
     Release: 2026-07-17
     Trailers: 3
     Popularity: 145.2

  🎬 Avatar 3 (2025)
     Release: 2025-12-20
     Trailers: 2
     Popularity: 89.4

  🎬 The Batman 2 (2025)
     Release: 2025-10-03
     Trailers: 2
     Popularity: 78.1
```

## 🔄 Workflow Integration

### When Adding Movies to Your Library

1. **Check upcoming folder** first: `/movies/_upcoming_trailers/`
2. **Look for your movie**: `Movie Name (Year)/`
3. **Copy the entire folder** to your main movies directory
4. **Jellyfin Cinema Mode** will automatically detect trailers

### Automated Workflow

```bash
# Schedule this to run weekly
0 2 * * 0 cd /path/to/tmdb && make upcoming

# Schedule cleanup monthly  
0 3 1 * * cd /path/to/tmdb && make upcoming-cleanup
```

## 🎯 Movie Selection Criteria

The system automatically filters movies based on:

- ✅ **Release window**: Next 3-6 months (configurable)
- ✅ **Popularity threshold**: TMDB popularity ≥ 10.0 (configurable)
- ✅ **Vote count**: At least 10 votes on TMDB
- ✅ **Release type**: Theatrical and limited releases
- ✅ **Trailer availability**: Must have trailers on YouTube

## 📋 Movie Metadata

Each upcoming movie includes a `movie_info.json` file:

```json
{
  "title": "Dune: Part Three",
  "year": "2026",
  "release_date": "2026-07-17",
  "popularity": 145.2,
  "overview": "The third installment in the new Dune film series...",
  "tmdb_id": 438631,
  "downloaded_at": "2025-08-04T16:30:00",
  "trailers_count": 3
}
```

## 🧹 Automatic Cleanup

The system automatically removes upcoming movies that:
- Are past their release date + cleanup days
- Have been released for more than 30 days (configurable)
- Helps keep the upcoming folder manageable

## 📈 Benefits

### For Home Users
- 🎬 **Always ready**: Trailers available before you get the movie
- 🔍 **Discovery**: Find new movies you might want to add
- ⚡ **Instant setup**: Just copy the folder when you add the movie

### For Enterprise/Media Centers
- 📅 **Planning**: Know what's coming and prepare storage
- 🎯 **Curated content**: Only popular movies, not obscure releases
- 🔄 **Automated workflow**: Integrate with your media acquisition pipeline

## 🔧 Advanced Configuration

### Custom Popularity Thresholds

```bash
# Only very popular movies
UPCOMING_MIN_POPULARITY=50.0

# Include more indie/niche films
UPCOMING_MIN_POPULARITY=5.0

# Blockbusters only
UPCOMING_MIN_POPULARITY=100.0
```

### Time Window Adjustment

```bash
# Shorter window (next 3 months)
UPCOMING_MONTHS_AHEAD=3

# Longer window (next 12 months)
UPCOMING_MONTHS_AHEAD=12
```

### Volume Control

```bash
# Conservative (top 20 movies)
UPCOMING_MAX_MOVIES=20

# Extensive (top 100 movies)
UPCOMING_MAX_MOVIES=100
```

## 🚨 Troubleshooting

### No Movies Found
- Check your `UPCOMING_MIN_POPULARITY` setting (might be too high)
- Verify your TMDB API key is working
- Check network connectivity

### Too Many Movies
- Increase `UPCOMING_MIN_POPULARITY` to be more selective
- Decrease `UPCOMING_MAX_MOVIES` limit
- Reduce `UPCOMING_MONTHS_AHEAD` window

### Storage Space
- Enable automatic cleanup: regular `make upcoming-cleanup`
- Reduce `UPCOMING_MAX_MOVIES` limit
- Monitor the `_upcoming_trailers` folder size

## 🔗 Integration with Other Features

The upcoming movies feature works seamlessly with:
- **Real-time monitoring**: Monitors the main movies folder only
- **Scheduled scanning**: Separate from upcoming downloads
- **Web dashboard**: Shows upcoming trailers statistics
- **Network shares**: Works with SMB/NFS/SSHFS configurations

## 💡 Pro Tips

1. **Run weekly**: Schedule upcoming downloads weekly for fresh content
2. **Monitor releases**: Use `upcoming-list` to see what's coming
3. **Adjust popularity**: Tune the popularity threshold for your taste
4. **Cleanup regularly**: Monthly cleanup keeps storage manageable
5. **Copy efficiently**: Use `rsync` or similar for large trailer folders

---

**Ready to get started?** Enable the feature in your `.env` file and run `make upcoming`! 🚀
