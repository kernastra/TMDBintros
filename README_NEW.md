# TMDB Trailer Downloader

A simple Python script to download movie trailers from The Movie Database (TMDB) API and organize them on your remote share.

## Features

- 🎬 Search movies on TMDB by title and year
- 📥 Download trailers using yt-dlp
- 📁 Organize trailers in movie-specific folders
- 🔧 Configurable video quality
- 📝 Comprehensive logging
- 🎯 Support for batch processing or single movies

## Requirements

- Python 3.7+
- yt-dlp installed (`pip install yt-dlp`)
- TMDB API key (free from https://www.themoviedb.org/settings/api)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create your configuration file:
```bash
cp config.json.example config.json
```

3. Edit `config.json` with your settings:
   - Add your TMDB API key
   - Set your remote share path
   - Add movies you want trailers for

## Usage

### Process movies from config file:
```bash
python tmdb_trailer_downloader.py
```

### Process a single movie:
```bash
python tmdb_trailer_downloader.py --title "The Matrix" --year 1999
```

### Custom quality setting:
```bash
python tmdb_trailer_downloader.py --quality 1080p
```

### Create sample config:
```bash
python tmdb_trailer_downloader.py --create-config
```

## Configuration

The `config.json` file contains:

- `tmdb_api_key`: Your TMDB API key
- `remote_share_path`: Path to where trailers should be stored
- `quality`: Video quality preference (best, 1080p, 720p, 480p, etc.)
- `movies`: List of movies with title and optional year

## Output Structure

Trailers are organized as:
```
/your/remote/share/
├── The Matrix (1999)/
│   ├── The Matrix-trailer-1-Official Trailer.mp4
│   └── The Matrix-trailer-2-Trailer #2.mp4
└── Inception (2010)/
    └── Inception-trailer-1-Official Trailer.mp4
```

## Logging

All operations are logged to:
- Console output
- `tmdb_downloader.log` file

## Command Line Options

- `--config PATH`: Custom config file path
- `--title TITLE`: Single movie title
- `--year YEAR`: Movie year (for single movie)
- `--quality QUALITY`: Video quality override
- `--create-config`: Generate sample config file

## Getting a TMDB API Key

1. Go to https://www.themoviedb.org/
2. Create a free account
3. Go to Settings → API
4. Request an API key (choose "Developer" option)
5. Copy the API key to your config.json file
