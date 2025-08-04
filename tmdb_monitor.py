#!/usr/bin/env python3
"""
TMDB Trailer Monitor - Continuous file system monitoring for new movies
"""

import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from config_manager import ConfigManager
from tmdb_trailer_downloader import TMDBTrailerDownloader
import re

logger = logging.getLogger(__name__)

class MovieFolderHandler(FileSystemEventHandler):
    """Handle file system events for movie folder monitoring"""
    
    def __init__(self, downloader: TMDBTrailerDownloader):
        self.downloader = downloader
        self.processed_movies = set()  # Track processed movies to avoid duplicates
    
    def on_created(self, event):
        """Handle new directory creation"""
        if event.is_directory:
            self.check_new_movie(Path(event.src_path))
    
    def on_moved(self, event):
        """Handle directory moves/renames"""
        if event.is_directory:
            self.check_new_movie(Path(event.dest_path))
    
    def check_new_movie(self, movie_path: Path):
        """Check if a new directory is a movie and download trailers"""
        try:
            # Parse movie name and year from folder name
            match = re.match(r'^(.+?)\s*\((\d{4})\).*$', movie_path.name)
            if not match:
                logger.debug(f"Directory doesn't match movie pattern: {movie_path.name}")
                return
            
            title = match.group(1).strip()
            year = int(match.group(2))
            movie_key = f"{title}_{year}"
            
            # Avoid processing the same movie multiple times
            if movie_key in self.processed_movies:
                return
            
            # Check if trailers directory already exists
            trailers_dir = movie_path / "trailers"
            if trailers_dir.exists() and any(trailers_dir.iterdir()):
                logger.info(f"Movie already has trailers: {movie_path.name}")
                self.processed_movies.add(movie_key)
                return
            
            logger.info(f"New movie detected: {title} ({year})")
            
            # Small delay to ensure directory is fully created
            time.sleep(2)
            
            # Download trailers for the new movie
            success = self.downloader.process_single_movie(title, year)
            if success:
                logger.info(f"Successfully downloaded trailers for: {title} ({year})")
                self.processed_movies.add(movie_key)
            else:
                logger.warning(f"Failed to download trailers for: {title} ({year})")
                
        except Exception as e:
            logger.error(f"Error processing new movie {movie_path}: {e}")

class TMDBTrailerMonitor:
    """Continuous monitoring service for automatic trailer downloads"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager.load_config()
        self.downloader = TMDBTrailerDownloader(str(self.config.jellyfin_movies_path))
        self.observer = None
        
    def start_monitoring(self):
        """Start continuous monitoring of the movies directory"""
        movies_path = Path(self.config.jellyfin_movies_path)
        
        if not movies_path.exists():
            logger.error(f"Movies directory does not exist: {movies_path}")
            return False
        
        logger.info(f"Starting continuous monitoring of: {movies_path}")
        logger.info("Monitoring for new movie folders matching pattern: 'Movie Name (YYYY)'")
        logger.info("Press Ctrl+C to stop monitoring")
        
        # Create event handler
        handler = MovieFolderHandler(self.downloader)
        
        # Create observer
        self.observer = Observer()
        self.observer.schedule(handler, str(movies_path), recursive=False)
        
        try:
            self.observer.start()
            
            # Keep the monitor running
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error during monitoring: {e}")
        finally:
            if self.observer:
                self.observer.stop()
                self.observer.join()
        
        return True
    
    def stop_monitoring(self):
        """Stop the monitoring service"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Monitoring stopped")

def main():
    """Main entry point for the monitoring service"""
    import argparse
    
    parser = argparse.ArgumentParser(description='TMDB Trailer Monitor - Continuous monitoring service')
    parser.add_argument('--config-dir', help='Configuration directory path')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Set the logging level')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('tmdb_monitor.log'),
            logging.StreamHandler()
        ]
    )
    
    try:
        # Load configuration
        config_manager = ConfigManager(config_dir=args.config_dir)
        
        # Create and start monitor
        monitor = TMDBTrailerMonitor(config_manager)
        monitor.start_monitoring()
        
    except Exception as e:
        logger.error(f"Failed to start monitoring: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
