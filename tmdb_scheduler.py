#!/usr/bin/env python3
"""
TMDB Trailer Scheduler - Periodic scanning for new movies
"""

import time
import logging
import schedule
from datetime import datetime
from pathlib import Path
from config_manager import ConfigManager
from enhanced_downloader import EnhancedTMDBTrailerDownloader

logger = logging.getLogger(__name__)

class TMDBTrailerScheduler:
    """Scheduled scanning service for automatic trailer downloads"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager.load_config()
        self.downloader = EnhancedTMDBTrailerDownloader(config_manager)
        self.last_scan = None
        
    def scan_for_new_movies(self):
        """Perform a scan for new movies"""
        try:
            logger.info(f"Starting scheduled scan at {datetime.now()}")
            
            # Run the existing scan functionality
            success = self.downloader.run_scan_existing()
            
            if success:
                logger.info("Scheduled scan completed successfully")
            else:
                logger.warning("Scheduled scan completed with warnings")
                
            self.last_scan = datetime.now()
            
        except Exception as e:
            logger.error(f"Error during scheduled scan: {e}")
    
    def start_scheduler(self, interval_minutes: int = 60):
        """Start the scheduled scanning service"""
        logger.info(f"Starting TMDB Trailer Scheduler")
        logger.info(f"Scanning every {interval_minutes} minutes")
        logger.info(f"Monitoring: {self.config.jellyfin_movies_path}")
        logger.info("Press Ctrl+C to stop scheduler")
        
        # Schedule the scan
        schedule.every(interval_minutes).minutes.do(self.scan_for_new_movies)
        
        # Run an initial scan
        logger.info("Running initial scan...")
        self.scan_for_new_movies()
        
        try:
            # Keep the scheduler running
            while True:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Scheduler stopped by user")
        except Exception as e:
            logger.error(f"Error in scheduler: {e}")

def main():
    """Main entry point for the scheduler service"""
    import argparse
    
    parser = argparse.ArgumentParser(description='TMDB Trailer Scheduler - Periodic scanning service')
    parser.add_argument('--config-dir', help='Configuration directory path')
    parser.add_argument('--interval', type=int, default=60, 
                       help='Scan interval in minutes (default: 60)')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Set the logging level')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('tmdb_scheduler.log'),
            logging.StreamHandler()
        ]
    )
    
    try:
        # Load configuration
        config_manager = ConfigManager(config_dir=args.config_dir)
        
        # Create and start scheduler
        scheduler = TMDBTrailerScheduler(config_manager)
        scheduler.start_scheduler(args.interval)
        
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
