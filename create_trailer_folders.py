#!/usr/bin/env python3
"""
Create trailer folders for all movies in the library
This prevents permission issues during trailer downloads
"""

import os
import re
import logging
from pathlib import Path
from dotenv import load_dotenv

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )

def scan_and_create_trailer_folders(movies_path: str) -> tuple:
    """
    Scan movie library and create trailer folders where missing
    
    Returns:
        tuple: (total_movies, folders_created, errors)
    """
    logger = logging.getLogger(__name__)
    
    movies_path = Path(movies_path)
    if not movies_path.exists():
        logger.error(f"Movies path does not exist: {movies_path}")
        return 0, 0, 1
    
    logger.info(f"Scanning movie library: {movies_path}")
    
    # Pattern to match movie folders: "Movie Title (YYYY)"
    movie_pattern = re.compile(r'^(.+)\s+\((\d{4})\)$')
    
    total_movies = 0
    folders_created = 0
    errors = 0
    
    try:
        # Get all directories in movies path
        for item in movies_path.iterdir():
            if not item.is_dir():
                continue
                
            # Skip special folders
            if item.name.startswith('_') or item.name.startswith('.'):
                continue
                
            # Check if it matches movie pattern
            if not movie_pattern.match(item.name):
                logger.debug(f"Skipping non-movie folder: {item.name}")
                continue
                
            total_movies += 1
            
            # Check if trailers folder exists
            trailers_folder = item / "trailers"
            
            if trailers_folder.exists():
                logger.debug(f"Trailers folder already exists: {item.name}")
                continue
                
            # Create trailers folder
            try:
                trailers_folder.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created trailers folder: {item.name}/trailers")
                folders_created += 1
                
            except PermissionError as e:
                logger.error(f"Permission denied creating trailers folder for {item.name}: {e}")
                errors += 1
            except Exception as e:
                logger.error(f"Error creating trailers folder for {item.name}: {e}")
                errors += 1
                
    except Exception as e:
        logger.error(f"Error scanning movies directory: {e}")
        errors += 1
        
    return total_movies, folders_created, errors

def main():
    """Main entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Load environment variables
    load_dotenv('.env.local')  # Load from .env.local first
    load_dotenv()              # Then from .env if it exists
    
    # Get movies path from environment
    movies_path = os.getenv('JELLYFIN_MOVIES_PATH')
    if not movies_path:
        logger.error("JELLYFIN_MOVIES_PATH not set in environment variables")
        return 1
    
    logger.info("Starting trailer folder creation process...")
    
    total_movies, folders_created, errors = scan_and_create_trailer_folders(movies_path)
    
    # Summary
    logger.info("=" * 50)
    logger.info("TRAILER FOLDER CREATION SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Total movie folders found: {total_movies}")
    logger.info(f"Trailer folders created: {folders_created}")
    logger.info(f"Errors encountered: {errors}")
    
    if folders_created > 0:
        logger.info("✅ Trailer folders created successfully!")
        logger.info("Your movie library is now ready for trailer downloads.")
    elif total_movies > 0 and folders_created == 0:
        logger.info("ℹ️  All movies already have trailer folders.")
    else:
        logger.warning("⚠️  No movie folders found or processed.")
        
    if errors > 0:
        logger.warning(f"⚠️  {errors} errors occurred during processing.")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
