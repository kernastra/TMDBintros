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

class RadarrService:
    """Service for Radarr API integration"""
    
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'X-Api-Key': config.api_key,
            'Content-Type': 'application/json'
        })
    
    def get_wanted_movies(self) -> List[Dict]:
        """Get list of wanted movies from Radarr"""
        if not self.config.enabled:
            return []
            
        try:
            url = f"{self.config.url.rstrip('/')}/api/v3/wanted/missing"
            response = self.session.get(url, params={'pageSize': 1000})
            response.raise_for_status()
            
            data = response.json()
            return data.get('records', [])
            
        except requests.RequestException as e:
            logger.error(f"Error fetching Radarr wanted movies: {e}")
            return []
    
    def get_movie_by_tmdb_id(self, tmdb_id: int) -> Optional[Dict]:
        """Get movie from Radarr by TMDB ID"""
        if not self.config.enabled:
            return None
            
        try:
            url = f"{self.config.url.rstrip('/')}/api/v3/movie"
            response = self.session.get(url, params={'tmdbId': tmdb_id})
            response.raise_for_status()
            
            movies = response.json()
            return movies[0] if movies else None
            
        except requests.RequestException as e:
            logger.error(f"Error fetching movie {tmdb_id} from Radarr: {e}")
            return None

class TMDBUpcomingTrailerDownloader:
    """Download trailers for upcoming movies with Radarr integration"""
    
    def __init__(self, config_manager: ConfigManager):
        main_config = config_manager.load_config()
        self.config = main_config.upcoming  # Use upcoming configuration
        self.radarr_config = main_config.radarr  # Store radarr config for future use
        self.api_key = main_config.tmdb_api_key
        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()
        
        # Initialize Radarr service if enabled
        self.radarr_service = RadarrService(self.radarr_config) if self.radarr_config.enabled else None
        
        # Initialize the main downloader for trailer downloading
        self.trailer_downloader = TMDBTrailerDownloader(
            self.api_key, 
            main_config.jellyfin_movies_path
        )
        
        # Configuration for upcoming movies
        self.upcoming_path = Path(main_config.jellyfin_movies_path) / "_upcoming_trailers"
        self.days_ahead = self.config.days_ahead
        self.popularity_threshold = self.config.popularity_threshold
        self.max_movies_per_run = self.config.max_movies
        
    def get_upcoming_movies(self, pages: int = 5) -> list:
        """
        Fetch upcoming movies from TMDB with comprehensive filtering
        
        Args:
            pages: Number of pages to fetch
            
        Returns:
            List of filtered upcoming movies
        """
        logger.info(f"Fetching upcoming movies for next {self.days_ahead} days...")
        
        # Calculate date range
        today = datetime.now()
        end_date = today + timedelta(days=self.days_ahead)
        
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
            
            # Add filter parameters if configured
            if self.config.filter_countries:
                params['with_origin_country'] = '|'.join(self.config.filter_countries)
            
            if self.config.filter_languages:
                params['with_original_language'] = '|'.join(self.config.filter_languages)
                
            if self.config.filter_genres:
                params['with_genres'] = ','.join(map(str, self.config.filter_genres))
                
            if self.config.exclude_genres:
                params['without_genres'] = ','.join(map(str, self.config.exclude_genres))
                
            if self.config.min_vote_average > 0:
                params['vote_average.gte'] = self.config.min_vote_average
                
            if self.config.min_vote_count > 0:
                params['vote_count.gte'] = self.config.min_vote_count
                
            if self.config.min_runtime > 0:
                params['with_runtime.gte'] = self.config.min_runtime
                
            if self.config.max_runtime > 0:
                params['with_runtime.lte'] = self.config.max_runtime
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                movies = data.get('results', [])
                if not movies:
                    break
                    
                # Apply additional filtering that can't be done via API
                filtered_movies = []
                for movie in movies:
                    if self._passes_all_filters(movie):
                        filtered_movies.append(movie)
                
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
    
    def _passes_all_filters(self, movie: dict) -> bool:
        """
        Check if movie passes all configured filters
        
        Args:
            movie: Movie data from TMDB API
            
        Returns:
            True if movie passes all filters
        """
        # Basic popularity check
        if movie.get('popularity', 0) < self.popularity_threshold:
            return False
            
        # Apply specific filter categories
        if not self._passes_quality_filters(movie):
            return False
            
        if not self._passes_content_filters(movie):
            return False
            
        if not self._passes_production_filters(movie):
            return False
            
        if not self._passes_advanced_filters(movie):
            return False
            
        return True
    
    def _passes_quality_filters(self, movie: dict) -> bool:
        """Check if movie passes quality-based filters"""
        # Already handled in API params for basic vote filtering
        return True
    
    def _passes_content_filters(self, movie: dict) -> bool:
        """Check if movie passes content-based filters"""
        # Rating filters (requires additional API call for detailed info)
        if self.config.filter_ratings or self.config.exclude_ratings:
            # This would require fetching movie details for certification
            # For now, we'll skip this complex filter
            pass
            
        return True
    
    def _passes_production_filters(self, movie: dict) -> bool:
        """Check if movie passes production-based filters (studios, directors, actors)"""
        if not (self.config.filter_studios or self.config.exclude_studios or 
                self.config.filter_directors or self.config.filter_actors):
            return True
            
        # These filters require additional API calls to get credits/production companies
        # For now, we'll implement basic company filtering if available in basic data
        if self.config.filter_studios or self.config.exclude_studios:
            # This would require fetching movie details for production companies
            # For performance, we'll implement this in a future version
            pass
            
        return True
    
    def _passes_advanced_filters(self, movie: dict) -> bool:
        """Check if movie passes advanced filters"""
        # Budget filtering (requires movie details API call)
        if self.config.min_budget > 0:
            # Would require additional API call
            pass
            
        # Franchise/Original filtering
        if self.config.franchise_only:
            # Check if movie is part of a collection
            if not movie.get('belongs_to_collection'):
                return False
                
        if self.config.original_only:
            # Check if movie is original (not a sequel/remake)
            title = movie.get('title', '').lower()
            if any(indicator in title for indicator in ['2', 'ii', 'sequel', 'part', ':']):
                return False
                
        return True
    
    def get_filtered_upcoming_movies(self) -> List[Dict]:
        """
        Get upcoming movies based on Radarr integration mode
        
        Returns:
            List of movies to process for trailers
        """
        if not self.radarr_service or self.radarr_config.integration_mode == 'upcoming':
            # Standard upcoming movies mode - use TMDB discover
            return self.get_upcoming_movies()
            
        elif self.radarr_config.integration_mode == 'radarr_only':
            # Only get trailers for movies in Radarr wanted list
            return self._get_radarr_wanted_movies()
            
        elif self.radarr_config.integration_mode == 'hybrid':
            # Combine upcoming movies with Radarr wanted movies
            upcoming = self.get_upcoming_movies()
            wanted = self._get_radarr_wanted_movies()
            
            # Combine and deduplicate by TMDB ID
            seen_ids = set()
            combined = []
            
            for movie in upcoming + wanted:
                tmdb_id = movie.get('id')
                if tmdb_id and tmdb_id not in seen_ids:
                    seen_ids.add(tmdb_id)
                    combined.append(movie)
                    
            return combined[:self.max_movies_per_run]
            
        return []
    
    def _get_radarr_wanted_movies(self) -> List[Dict]:
        """Get upcoming movies that are in Radarr's wanted list"""
        if not self.radarr_service:
            return []
            
        wanted_movies = self.radarr_service.get_wanted_movies()
        tmdb_movies = []
        
        for radarr_movie in wanted_movies:
            tmdb_id = radarr_movie.get('tmdbId')
            if tmdb_id:
                # Get full movie details from TMDB
                movie_details = self._get_tmdb_movie_details(tmdb_id)
                if movie_details and self._is_upcoming_movie(movie_details):
                    tmdb_movies.append(movie_details)
                    
        logger.info(f"Found {len(tmdb_movies)} upcoming movies in Radarr wanted list")
        return tmdb_movies
    
    def _get_tmdb_movie_details(self, tmdb_id: int) -> Optional[Dict]:
        """Get movie details from TMDB API"""
        try:
            url = f"{self.base_url}/movie/{tmdb_id}"
            params = {'api_key': self.api_key}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Error fetching TMDB details for movie {tmdb_id}: {e}")
            return None
    
    def _is_upcoming_movie(self, movie: Dict) -> bool:
        """Check if movie is upcoming based on release date"""
        release_date = movie.get('release_date')
        if not release_date:
            return False
            
        try:
            movie_date = datetime.strptime(release_date, '%Y-%m-%d')
            today = datetime.now()
            end_date = today + timedelta(days=self.days_ahead)
            
            return today <= movie_date <= end_date
            
        except ValueError:
            return False
    
    def create_upcoming_structure(self):
        """Create directory structure for upcoming trailers"""
        self.upcoming_path.mkdir(parents=True, exist_ok=True)
        
        # Create info file about upcoming trailers
        info_file = self.upcoming_path / "README.md"
        if not info_file.exists():
            info_content = f"""# Upcoming Movie Trailers

This directory contains trailers for upcoming movies downloaded {self.days_ahead} days in advance.

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Monitoring Period:** Next {self.days_ahead} days
**Minimum Popularity:** {self.popularity_threshold}
**Max Trailers per Movie:** {self.config.max_trailers_per_movie}

## Filtering Configuration
- **Countries:** {', '.join(self.config.filter_countries) if self.config.filter_countries else 'All'}
- **Languages:** {', '.join(self.config.filter_languages) if self.config.filter_languages else 'All'}
- **Genres:** {', '.join(map(str, self.config.filter_genres)) if self.config.filter_genres else 'All'}
- **Min Vote Average:** {self.config.min_vote_average if self.config.min_vote_average > 0 else 'No minimum'}
- **Studios:** {', '.join(self.config.filter_studios) if self.config.filter_studios else 'All'}

## Structure
- Each movie has its own folder: `Movie Name (Year)/trailers/`
- Up to {self.config.max_trailers_per_movie} trailers downloaded per movie
- Trailers are ready to be moved to your main library when you add the movie
- Folders are created in Jellyfin Cinema Mode compatible format

## Usage
When you add a movie to your library:
1. Check if it exists in this upcoming folder
2. Copy/move the entire movie folder to your main movies directory
3. Jellyfin Cinema Mode will automatically detect the trailers

## Configuration
Edit your .env file to customize:
- `UPCOMING_DAYS_AHEAD={self.days_ahead}`
- `UPCOMING_POPULARITY_THRESHOLD={self.popularity_threshold}`
- `UPCOMING_MAX_MOVIES={self.max_movies_per_run}`
- `UPCOMING_MAX_TRAILERS_PER_MOVIE={self.config.max_trailers_per_movie}`
"""
            info_file.write_text(info_content)
    
    def get_filtered_upcoming_movies(self) -> List[Dict]:
        """Get upcoming movies based on Radarr integration mode"""
        if not self.radarr_service or self.radarr_config.integration_mode == 'upcoming':
            # Standard upcoming movies mode
            return self.get_upcoming_movies()
            
        elif self.radarr_config.integration_mode == 'radarr_only':
            # Only get movies that are in Radarr's wanted list
            radarr_movies = self.radarr_service.get_wanted_movies()
            upcoming_movies = self.get_upcoming_movies()
            
            # Filter upcoming movies to only include those in Radarr
            filtered_movies = []
            for movie in upcoming_movies:
                tmdb_id = movie.get('id')
                if any(rm.get('tmdbId') == tmdb_id for rm in radarr_movies):
                    filtered_movies.append(movie)
                    
            logger.info(f"Radarr-only mode: {len(filtered_movies)} movies match Radarr wanted list")
            return filtered_movies
            
        elif self.radarr_config.integration_mode == 'hybrid':
            # Get all upcoming movies, but prioritize Radarr movies
            upcoming_movies = self.get_upcoming_movies()
            radarr_movies = self.radarr_service.get_wanted_movies()
            radarr_tmdb_ids = {rm.get('tmdbId') for rm in radarr_movies}
            
            # Sort with Radarr movies first
            prioritized_movies = sorted(
                upcoming_movies,
                key=lambda m: (0 if m.get('id') in radarr_tmdb_ids else 1, -m.get('popularity', 0))
            )
            
            logger.info(f"Hybrid mode: Prioritizing {len(radarr_tmdb_ids)} Radarr movies")
            return prioritized_movies
            
        else:
            logger.warning(f"Unknown integration mode: {self.radarr_config.integration_mode}")
            return self.get_upcoming_movies()
    
    def should_download_to_radarr_folder(self, movie: dict) -> Optional[str]:
        """Check if movie should be downloaded directly to Radarr folder"""
        if not self.radarr_service:
            return None
            
        tmdb_id = movie.get('id')
        radarr_movie = self.radarr_service.get_movie_by_tmdb_id(tmdb_id)
        
        if radarr_movie and radarr_movie.get('hasFile', False):
            # Movie folder exists in Radarr
            folder_path = radarr_movie.get('path')
            if folder_path and Path(folder_path).exists():
                return folder_path
                
        return None
    
    def download_upcoming_trailers(self) -> Dict:
        """
        Download trailers for upcoming movies
        
        Returns:
            Summary statistics
        """
        logger.info("Starting upcoming movies trailer download...")
        logger.info(f"Configuration: {self.days_ahead} days ahead, max {self.config.max_trailers_per_movie} trailers per movie")
        
        # Create directory structure
        self.create_upcoming_structure()
        
        # Get upcoming movies using configured integration mode
        upcoming_movies = self.get_filtered_upcoming_movies()
        
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
            
            # Check if this movie should go directly to Radarr folder
            radarr_path = self.should_download_to_radarr_folder(movie)
            
            if radarr_path:
                # Download directly to Radarr folder
                target_path = Path(radarr_path) / "trailers"
                logger.info(f"Downloading to Radarr folder: {target_path}")
            else:
                # Download to upcoming folder
                movie_folder = self.upcoming_path / f"{title} ({year})"
                target_path = movie_folder / "trailers"
            
            if target_path.exists() and any(target_path.iterdir()):
                logger.info(f"Trailers already exist for {title} ({year}), skipping")
                stats['skipped'] += 1
                continue
            
            try:
                # Create target trailers folder
                target_path.mkdir(parents=True, exist_ok=True)
                
                # Get trailers using existing downloader logic
                movie_id = movie.get('id')
                trailers = self.trailer_downloader.get_movie_trailers(movie_id)
                
                if not trailers:
                    logger.warning(f"No trailers found for {title} ({year})")
                    stats['errors'] += 1
                    continue
                
                # Download trailers
                success_count = 0
                max_trailers = self.config.max_trailers_per_movie
                for j, trailer in enumerate(trailers[:max_trailers]):  # Use configured limit
                    trailer_name = self.trailer_downloader.sanitize_filename(trailer['name'])
                    output_file = target_path / f"{title}-trailer-{j+1}.%(ext)s"
                    
                    video_url = f"https://www.youtube.com/watch?v={trailer['key']}"
                    
                    if self.trailer_downloader.download_trailer(video_url, output_file, 'best'):
                        success_count += 1
                        logger.info(f"Downloaded trailer {j+1}/{max_trailers} for {title}")
                    else:
                        logger.warning(f"Failed to download trailer {j+1} for {title}")
                
                if success_count > 0:
                    # Create movie info file (only for upcoming folder, not Radarr)
                    if not radarr_path:
                        info_file = target_path.parent / "movie_info.json"
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
                    if target_path.exists():
                        target_path.rmdir()
                    if not radarr_path and target_path.parent.exists():
                        target_path.parent.rmdir()
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
