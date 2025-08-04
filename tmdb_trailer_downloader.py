#!/usr/bin/env python3
"""
TMDB Trailer Downloader
A simple self-hosted script to download movie trailers from TMDB and organize them.
"""

import os
import sys
import json
import requests
import subprocess
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tmdb_downloader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class TMDBTrailerDownloader:
    def __init__(self, api_key: str, remote_share_path: str):
        """
        Initialize the TMDB Trailer Downloader.
        
        Args:
            api_key: TMDB API key
            remote_share_path: Path to remote share where trailers will be stored
        """
        self.api_key = api_key
        self.remote_share_path = Path(remote_share_path)
        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()
        
        # Ensure remote share path exists
        self.remote_share_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized TMDB Downloader - Remote share: {self.remote_share_path}")
    
    def search_movie(self, title: str, year: Optional[int] = None) -> Optional[Dict]:
        """
        Search for a movie on TMDB.
        
        Args:
            title: Movie title
            year: Optional release year for better matching
            
        Returns:
            Movie data dict or None if not found
        """
        url = f"{self.base_url}/search/movie"
        params = {
            'api_key': self.api_key,
            'query': title
        }
        
        if year:
            params['year'] = year
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['results']:
                movie = data['results'][0]  # Take first result
                logger.info(f"Found movie: {movie['title']} ({movie.get('release_date', 'Unknown')[:4]})")
                return movie
            else:
                logger.warning(f"No results found for: {title}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Error searching for movie '{title}': {e}")
            return None
    
    def get_movie_trailers(self, movie_id: int) -> List[Dict]:
        """
        Get trailers for a specific movie.
        
        Args:
            movie_id: TMDB movie ID
            
        Returns:
            List of trailer data dicts
        """
        url = f"{self.base_url}/movie/{movie_id}/videos"
        params = {'api_key': self.api_key}
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Filter for trailers on YouTube
            trailers = [
                video for video in data['results']
                if video['type'] == 'Trailer' and video['site'] == 'YouTube'
            ]
            
            logger.info(f"Found {len(trailers)} trailers for movie ID {movie_id}")
            return trailers
            
        except requests.RequestException as e:
            logger.error(f"Error getting trailers for movie ID {movie_id}: {e}")
            return []
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for filesystem compatibility.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\s+', ' ', filename).strip()
        return filename
    
    def download_trailer(self, video_url: str, output_path: Path, quality: str = 'best') -> bool:
        """
        Download a trailer using yt-dlp.
        
        Args:
            video_url: YouTube video URL
            output_path: Path where the video should be saved
            quality: Video quality preference
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cmd = [
                'yt-dlp',
                '--format', f'{quality}[ext=mp4]/best[ext=mp4]/best',
                '--output', str(output_path),
                '--no-playlist',
                '--write-info-json',
                video_url
            ]
            
            logger.info(f"Downloading trailer: {video_url}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            logger.info(f"Successfully downloaded trailer to: {output_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading trailer: {e.stderr}")
            return False
        except FileNotFoundError:
            logger.error("yt-dlp not found. Please install yt-dlp: pip install yt-dlp")
            return False
    
    def process_movie(self, title: str, year: Optional[int] = None, quality: str = 'best') -> bool:
        """
        Process a single movie: search, get trailers, and download.
        
        Args:
            title: Movie title
            year: Optional release year
            quality: Video quality preference
            
        Returns:
            True if at least one trailer was downloaded successfully
        """
        logger.info(f"Processing movie: {title}" + (f" ({year})" if year else ""))
        
        # Search for movie
        movie = self.search_movie(title, year)
        if not movie:
            return False
        
        # Get trailers
        trailers = self.get_movie_trailers(movie['id'])
        if not trailers:
            logger.warning(f"No trailers found for: {movie['title']}")
            return False
        
        # Create Jellyfin-compatible movie directory structure
        movie_title = self.sanitize_filename(movie['title'])
        movie_year = movie.get('release_date', '')[:4] if movie.get('release_date') else 'Unknown'
        movie_dir = self.remote_share_path / f"{movie_title} ({movie_year})"
        
        # Create trailers subdirectory (Jellyfin Cinema Mode compatibility)
        trailers_dir = movie_dir / "trailers"
        trailers_dir.mkdir(parents=True, exist_ok=True)
        
        success_count = 0
        
        # Download trailers into the trailers subfolder
        for i, trailer in enumerate(trailers[:3]):  # Limit to first 3 trailers
            trailer_name = self.sanitize_filename(trailer['name'])
            # Use simple naming for Jellyfin compatibility
            output_file = trailers_dir / f"{movie_title}-trailer-{i+1}.%(ext)s"
            
            video_url = f"https://www.youtube.com/watch?v={trailer['key']}"
            
            if self.download_trailer(video_url, output_file, quality):
                success_count += 1
        
        logger.info(f"Downloaded {success_count}/{len(trailers)} trailers for {movie['title']} in Jellyfin-compatible structure")
        return success_count > 0
    
    def scan_existing_movies(self) -> List[Dict]:
        """
        Scan the remote share path for existing movie folders.
        
        Returns:
            List of dicts with detected movie info
        """
        logger.info(f"Scanning for existing movies in: {self.remote_share_path}")
        
        if not self.remote_share_path.exists():
            logger.warning(f"Remote share path does not exist: {self.remote_share_path}")
            return []
        
        movies = []
        
        # Look for movie folders with pattern "Movie Name (Year)"
        for item in self.remote_share_path.iterdir():
            if item.is_dir():
                # Try to parse movie name and year from folder name
                match = re.match(r'^(.+?)\s*\((\d{4})\).*$', item.name)
                if match:
                    title = match.group(1).strip()
                    year = int(match.group(2))
                    
                    # Check if trailers directory already exists
                    trailers_dir = item / "trailers"
                    has_trailers = trailers_dir.exists() and any(trailers_dir.iterdir())
                    
                    movies.append({
                        'title': title,
                        'year': year,
                        'folder': str(item),
                        'has_trailers': has_trailers
                    })
                    
                    if has_trailers:
                        logger.info(f"Found movie with existing trailers: {title} ({year})")
                    else:
                        logger.info(f"Found movie without trailers: {title} ({year})")
        
        logger.info(f"Found {len(movies)} movie folders")
        return movies
    
    def process_existing_movies(self, quality: str = 'best', skip_existing: bool = True):
        """
        Process all movies found in the existing directory structure.
        
        Args:
            quality: Video quality preference
            skip_existing: Skip movies that already have trailers
        """
        existing_movies = self.scan_existing_movies()
        
        if not existing_movies:
            logger.warning("No existing movie folders found")
            return
        
        movies_to_process = []
        for movie in existing_movies:
            if skip_existing and movie['has_trailers']:
                logger.info(f"Skipping {movie['title']} ({movie['year']}) - already has trailers")
                continue
            movies_to_process.append(movie)
        
        if not movies_to_process:
            logger.info("No movies need trailer downloads")
            return
        
        logger.info(f"Processing {len(movies_to_process)} movies for trailer downloads...")
        
        success_count = 0
        for movie in movies_to_process:
            if self.process_movie(movie['title'], movie['year'], quality):
                success_count += 1
        
        logger.info(f"Successfully processed {success_count}/{len(movies_to_process)} movies")
    
    def process_movie_list(self, movie_list: List[Dict], quality: str = 'best'):
        """
        Process a list of movies.
        
        Args:
            movie_list: List of dicts with 'title' and optional 'year' keys
            quality: Video quality preference
        """
        total_movies = len(movie_list)
        successful_movies = 0
        
        logger.info(f"Processing {total_movies} movies...")
        
        for i, movie_info in enumerate(movie_list, 1):
            title = movie_info.get('title', '')
            year = movie_info.get('year')
            
            logger.info(f"[{i}/{total_movies}] Processing: {title}")
            
            if self.process_movie(title, year, quality):
                successful_movies += 1
        
        logger.info(f"Completed processing: {successful_movies}/{total_movies} movies successful")
        """
        Process a list of movies.
        
        Args:
            movie_list: List of dicts with 'title' and optional 'year' keys
            quality: Video quality preference
        """
        total_movies = len(movie_list)
        successful_movies = 0
        
        logger.info(f"Processing {total_movies} movies...")
        
        for i, movie_info in enumerate(movie_list, 1):
            title = movie_info.get('title', '')
            year = movie_info.get('year')
            
            logger.info(f"[{i}/{total_movies}] Processing: {title}")
            
            if self.process_movie(title, year, quality):
                successful_movies += 1
        
        logger.info(f"Completed processing: {successful_movies}/{total_movies} movies successful")


def load_config(config_path: str = 'config.json') -> Dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        return {}


def create_sample_config():
    """Create a sample configuration file."""
    sample_config = {
        "tmdb_api_key": "your_tmdb_api_key_here",
        "remote_share_path": "/path/to/your/jellyfin/movies/library",
        "quality": "best",
        "movies": [
            {"title": "The Matrix", "year": 1999},
            {"title": "Inception", "year": 2010},
            {"title": "Interstellar", "year": 2014}
        ]
    }
    
    with open('config.json', 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    logger.info("Created sample config.json file. Please edit it with your settings.")
    logger.info("TIP: Use --scan-existing to automatically find movies in your Jellyfin library!")


def main():
    parser = argparse.ArgumentParser(description='TMDB Trailer Downloader for Jellyfin Cinema Mode')
    parser.add_argument('--config', default='config.json', help='Config file path')
    parser.add_argument('--title', help='Single movie title to process')
    parser.add_argument('--year', type=int, help='Movie year (for single movie)')
    parser.add_argument('--quality', default='best', help='Video quality (best, 1080p, 720p, etc.)')
    parser.add_argument('--create-config', action='store_true', help='Create sample config file')
    parser.add_argument('--scan-existing', action='store_true', help='Scan for existing movies and download missing trailers')
    parser.add_argument('--include-existing', action='store_true', help='Include movies that already have trailers (use with --scan-existing)')
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config()
        return
    
    # Load configuration
    config = load_config(args.config)
    if not config:
        logger.error("Please create a config file. Use --create-config to generate a sample.")
        return
    
    # Validate required config
    api_key = config.get('tmdb_api_key')
    remote_share_path = config.get('remote_share_path')
    
    if not api_key or api_key == 'your_tmdb_api_key_here':
        logger.error("Please set your TMDB API key in the config file")
        return
    
    if not remote_share_path:
        logger.error("Please set your remote share path in the config file")
        return
    
    # Initialize downloader
    downloader = TMDBTrailerDownloader(api_key, remote_share_path)
    
    # Process movies
    quality = args.quality or config.get('quality', 'best')
    
    if args.scan_existing:
        # Scan existing movie folders and download missing trailers
        skip_existing = not args.include_existing
        downloader.process_existing_movies(quality, skip_existing)
    elif args.title:
        # Process single movie from command line
        downloader.process_movie(args.title, args.year, quality)
    else:
        # Process movies from config file
        movie_list = config.get('movies', [])
        if not movie_list:
            logger.warning("No movies found in config file. Use --scan-existing to scan for existing movies.")
            return
        
        downloader.process_movie_list(movie_list, quality)


if __name__ == "__main__":
    main()
