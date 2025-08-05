#!/usr/bin/env python3
"""
TMDB Upcoming Movies Trailer Downloader
Downloads trailers for upcoming movies (3-6 months ahead)
"""

import requests
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from config_manager import ConfigManager
from tmdb_trailer_downloader import TMDBTrailerDownloader

logger = logging.getLogger(__name__)

class TMDBUpcomingTrailerDownloader:
    """Download trailers for upcoming movies"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager.load_config()
        self.api_key = self.config.tmdb_api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()
        
        # Initialize the main downloader for trailer downloading
        self.trailer_downloader = TMDBTrailerDownloader(
            self.api_key, 
            self.config.jellyfin_movies_path
        )
        
        # Configuration for upcoming movies
        self.upcoming_path = Path(self.config.jellyfin_movies_path) / "_upcoming_trailers"
        self.months_ahead = getattr(self.config, 'upcoming_months_ahead', 6)
        self.min_popularity = getattr(self.config, 'upcoming_min_popularity', 10.0)
        self.max_movies_per_run = getattr(self.config, 'upcoming_max_movies', 50)
        
    def get_upcoming_movies(self, pages: int = 5) -> List[Dict]:
        """
        Get upcoming movies from TMDB API
        
        Args:
            pages: Number of pages to fetch (20 movies per page)
            
        Returns:
            List of upcoming movie data
        """
        logger.info(f"Fetching upcoming movies for next {self.months_ahead} months...")
        
        # Calculate date range
        today = datetime.now()
        end_date = today + timedelta(days=self.months_ahead * 30)
        
        today_str = today.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        all_movies = []
        
        for page in range(1, pages + 1):
            url = f"{self.base_url}/discover/movie"
            params = {
                'api_key': self.api_key,
                'sort_by': 'popularity.desc',
                'primary_release_date.gte': today_str,
                'primary_release_date.lte': end_date_str,
                'page': page,
                'with_release_type': '3|2',  # Theatrical and limited releases
                'vote_count.gte': 10  # At least 10 votes to filter out obscure movies
            }
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                movies = data.get('results', [])
                if not movies:
                    break
                    
                # Filter by popularity
                filtered_movies = [
                    movie for movie in movies 
                    if movie.get('popularity', 0) >= self.min_popularity
                ]
                
                all_movies.extend(filtered_movies)
                logger.info(f"Page {page}: Found {len(filtered_movies)} upcoming movies")
                
            except requests.RequestException as e:
                logger.error(f"Error fetching upcoming movies page {page}: {e}")
                break
        
        # Sort by popularity and limit results
        all_movies.sort(key=lambda x: x.get('popularity', 0), reverse=True)
        final_movies = all_movies[:self.max_movies_per_run]
        
        logger.info(f"Total upcoming movies found: {len(final_movies)}")
        return final_movies
    
    def create_upcoming_structure(self):
        """Create directory structure for upcoming trailers"""
        self.upcoming_path.mkdir(parents=True, exist_ok=True)
        
        # Create info file about upcoming trailers
        info_file = self.upcoming_path / "README.md"
        if not info_file.exists():
            info_content = f"""# Upcoming Movie Trailers

This directory contains trailers for upcoming movies downloaded {self.months_ahead} months in advance.

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Monitoring Period:** Next {self.months_ahead} months
**Minimum Popularity:** {self.min_popularity}

## Structure
- Each movie has its own folder: `Movie Name (Year)/trailers/`
- Trailers are ready to be moved to your main library when you add the movie
- Folders are created in Jellyfin Cinema Mode compatible format

## Usage
When you add a movie to your library:
1. Check if it exists in this upcoming folder
2. Copy/move the entire movie folder to your main movies directory
3. Jellyfin Cinema Mode will automatically detect the trailers

## Configuration
Edit your .env file to customize:
- `UPCOMING_MONTHS_AHEAD={self.months_ahead}`
- `UPCOMING_MIN_POPULARITY={self.min_popularity}`
- `UPCOMING_MAX_MOVIES={self.max_movies_per_run}`
"""
            info_file.write_text(info_content)
    
    def download_upcoming_trailers(self) -> Dict:
        """
        Download trailers for upcoming movies
        
        Returns:
            Summary statistics
        """
        logger.info("Starting upcoming movies trailer download...")
        
        # Create directory structure
        self.create_upcoming_structure()
        
        # Get upcoming movies
        upcoming_movies = self.get_upcoming_movies()
        
        if not upcoming_movies:
            logger.warning("No upcoming movies found")
            return {'total': 0, 'processed': 0, 'skipped': 0, 'errors': 0}
        
        stats = {'total': len(upcoming_movies), 'processed': 0, 'skipped': 0, 'errors': 0}
        
        for i, movie in enumerate(upcoming_movies, 1):
            title = movie.get('title', 'Unknown')
            release_date = movie.get('release_date', '')
            year = release_date[:4] if release_date else 'Unknown'
            popularity = movie.get('popularity', 0)
            
            logger.info(f"[{i}/{len(upcoming_movies)}] Processing: {title} ({year}) - Popularity: {popularity:.1f}")
            
            # Check if we already have this movie
            movie_folder = self.upcoming_path / f"{title} ({year})"
            trailers_folder = movie_folder / "trailers"
            
            if trailers_folder.exists() and any(trailers_folder.iterdir()):
                logger.info(f"Trailers already exist for {title} ({year}), skipping")
                stats['skipped'] += 1
                continue
            
            try:
                # Create movie folder in upcoming directory
                trailers_folder.mkdir(parents=True, exist_ok=True)
                
                # Get trailers using existing downloader logic
                movie_id = movie.get('id')
                trailers = self.trailer_downloader.get_movie_trailers(movie_id)
                
                if not trailers:
                    logger.warning(f"No trailers found for {title} ({year})")
                    stats['errors'] += 1
                    continue
                
                # Download trailers
                success_count = 0
                for j, trailer in enumerate(trailers[:3]):  # Limit to 3 trailers
                    trailer_name = self.trailer_downloader.sanitize_filename(trailer['name'])
                    output_file = trailers_folder / f"{title}-trailer-{j+1}.%(ext)s"
                    
                    video_url = f"https://www.youtube.com/watch?v={trailer['key']}"
                    
                    if self.trailer_downloader.download_trailer(video_url, output_file, 'best'):
                        success_count += 1
                
                if success_count > 0:
                    # Create movie info file
                    info_file = movie_folder / "movie_info.json"
                    movie_info = {
                        'title': title,
                        'year': year,
                        'release_date': release_date,
                        'popularity': popularity,
                        'overview': movie.get('overview', ''),
                        'tmdb_id': movie_id,
                        'downloaded_at': datetime.now().isoformat(),
                        'trailers_count': success_count
                    }
                    info_file.write_text(json.dumps(movie_info, indent=2))
                    
                    logger.info(f"Successfully downloaded {success_count} trailers for {title} ({year})")
                    stats['processed'] += 1
                else:
                    logger.error(f"Failed to download any trailers for {title} ({year})")
                    # Clean up empty folder
                    if trailers_folder.exists():
                        trailers_folder.rmdir()
                    if movie_folder.exists():
                        movie_folder.rmdir()
                    stats['errors'] += 1
                    
            except Exception as e:
                logger.error(f"Error processing {title} ({year}): {e}")
                stats['errors'] += 1
        
        logger.info(f"Upcoming trailers download completed: {stats}")
        return stats
    
    def list_upcoming_movies(self) -> List[Dict]:
        """List movies with downloaded upcoming trailers"""
        if not self.upcoming_path.exists():
            return []
        
        movies = []
        for movie_dir in self.upcoming_path.iterdir():
            if movie_dir.is_dir() and movie_dir.name != "README.md":
                info_file = movie_dir / "movie_info.json"
                trailers_dir = movie_dir / "trailers"
                
                movie_info = {
                    'folder_name': movie_dir.name,
                    'trailers_count': 0,
                    'download_date': None
                }
                
                # Load movie info if available
                if info_file.exists():
                    try:
                        with open(info_file) as f:
                            file_info = json.load(f)
                            movie_info.update(file_info)
                    except Exception as e:
                        logger.warning(f"Error reading info file for {movie_dir.name}: {e}")
                
                # Count trailers
                if trailers_dir.exists():
                    movie_info['trailers_count'] = len([
                        f for f in trailers_dir.iterdir() 
                        if f.suffix.lower() in ['.mp4', '.mkv', '.avi', '.webm']
                    ])
                
                movies.append(movie_info)
        
        return sorted(movies, key=lambda x: x.get('popularity', 0), reverse=True)
    
    def cleanup_old_upcoming(self, days_old: int = 30):
        """
        Clean up upcoming movies that are now past their release date
        
        Args:
            days_old: Remove movies older than this many days past release
        """
        if not self.upcoming_path.exists():
            return
        
        logger.info(f"Cleaning up upcoming movies older than {days_old} days past release...")
        
        today = datetime.now()
        cleanup_count = 0
        
        for movie_dir in self.upcoming_path.iterdir():
            if not movie_dir.is_dir() or movie_dir.name == "README.md":
                continue
                
            info_file = movie_dir / "movie_info.json"
            if not info_file.exists():
                continue
                
            try:
                with open(info_file) as f:
                    movie_info = json.load(f)
                
                release_date_str = movie_info.get('release_date', '')
                if not release_date_str:
                    continue
                
                release_date = datetime.strptime(release_date_str, '%Y-%m-%d')
                days_since_release = (today - release_date).days
                
                if days_since_release > days_old:
                    logger.info(f"Removing old upcoming movie: {movie_info.get('title', movie_dir.name)} (released {days_since_release} days ago)")
                    
                    # Remove the entire movie directory
                    import shutil
                    shutil.rmtree(movie_dir)
                    cleanup_count += 1
                    
            except Exception as e:
                logger.warning(f"Error checking release date for {movie_dir.name}: {e}")
        
        logger.info(f"Cleaned up {cleanup_count} old upcoming movies")


def main():
    """Main entry point for upcoming trailers downloader"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Download trailers for upcoming movies')
    parser.add_argument('--config-dir', default='.', help='Configuration directory path')
    parser.add_argument('--list', action='store_true', help='List downloaded upcoming trailers')
    parser.add_argument('--cleanup', action='store_true', help='Clean up old upcoming movies')
    parser.add_argument('--cleanup-days', type=int, default=30, help='Days after release to cleanup')
    parser.add_argument('--log-level', default='INFO', help='Set logging level')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('tmdb_upcoming.log'),
            logging.StreamHandler()
        ]
    )
    
    try:
        # Load configuration
        config_manager = ConfigManager(config_dir=args.config_dir)
        downloader = TMDBUpcomingTrailerDownloader(config_manager)
        
        if args.list:
            movies = downloader.list_upcoming_movies()
            print(f"\n📽️  Upcoming Movies with Trailers ({len(movies)} total):\n")
            for movie in movies:
                release_date = movie.get('release_date', 'Unknown')
                trailers = movie.get('trailers_count', 0)
                popularity = movie.get('popularity', 0)
                print(f"  🎬 {movie['folder_name']}")
                print(f"     Release: {release_date}")
                print(f"     Trailers: {trailers}")
                print(f"     Popularity: {popularity:.1f}")
                print()
        
        elif args.cleanup:
            downloader.cleanup_old_upcoming(args.cleanup_days)
        
        else:
            # Download upcoming trailers
            stats = downloader.download_upcoming_trailers()
            print(f"\n✅ Upcoming trailers download completed!")
            print(f"   📊 Total movies: {stats['total']}")
            print(f"   ✅ Successfully processed: {stats['processed']}")
            print(f"   ⏭️  Skipped (already exist): {stats['skipped']}")
            print(f"   ❌ Errors: {stats['errors']}")
            
            if stats['processed'] > 0:
                print(f"\n📂 Trailers saved to: {downloader.upcoming_path}")
                print("💡 When you add these movies to your library, copy the folders to your main movies directory")
    
    except KeyboardInterrupt:
        logger.info("Upcoming trailers download interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
