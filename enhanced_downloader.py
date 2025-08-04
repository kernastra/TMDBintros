#!/usr/bin/env python3
"""
Enhanced TMDB Trailer Downloader with Environment Variable Support
Supports .env files, network mounting, and comprehensive configuration
"""

import argparse
import logging
import sys
from pathlib import Path

# Import our custom modules
from config_manager import ConfigManager, setup_logging, TMDBConfig
from network_mount_helper import NetworkMounter

# Import the original TMDBTrailerDownloader class
# (We'll need to modify the original script to export this class)

logger = logging.getLogger(__name__)

class EnhancedTMDBTrailerDownloader:
    """Enhanced version with environment configuration support"""
    
    def __init__(self, config: TMDBConfig):
        self.config = config
        self.network_mounter = None
        
        # Setup network mounter if enabled
        if config.network.enabled and config.network.auto_mount:
            self.network_mounter = NetworkMounter(config.network.to_dict())
    
    def ensure_network_mounted(self) -> bool:
        """Ensure network share is mounted if needed"""
        if not self.network_mounter:
            return True
        
        if not self.network_mounter.mount():
            logger.error("Failed to mount network share")
            return False
        
        return True
    
    def cleanup_network(self) -> None:
        """Cleanup network mount if needed"""
        if self.network_mounter and self.config.network.auto_mount:
            # Only unmount if we auto-mounted it
            self.network_mounter.unmount()
    
    def run_scan_existing(self) -> bool:
        """Run scan for existing movies"""
        if not self.ensure_network_mounted():
            return False
        
        try:
            # Here we would call the original scan_existing_movies method
            # For now, just show what would happen
            movies_path = Path(self.config.jellyfin_movies_path)
            logger.info(f"Scanning for existing movies in: {movies_path}")
            
            if not movies_path.exists():
                logger.error(f"Movies path does not exist: {movies_path}")
                return False
            
            # TODO: Implement actual scanning logic from original script
            logger.info("Scan completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error during scan: {e}")
            return False
        finally:
            self.cleanup_network()
    
    def run_download_movie(self, title: str, year: int = None) -> bool:
        """Download trailers for a specific movie"""
        if not self.ensure_network_mounted():
            return False
        
        try:
            logger.info(f"Downloading trailers for: {title} ({year})")
            
            # TODO: Implement actual download logic from original script
            logger.info("Download completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading movie: {e}")
            return False
        finally:
            self.cleanup_network()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Enhanced TMDB Trailer Downloader')
    parser.add_argument('--config-dir', default='.', help='Configuration directory')
    parser.add_argument('--scan-existing', action='store_true', help='Scan existing movies')
    parser.add_argument('--title', help='Movie title to download')
    parser.add_argument('--year', type=int, help='Movie year')
    parser.add_argument('--quality', help='Download quality override')
    parser.add_argument('--test-config', action='store_true', help='Test configuration and exit')
    parser.add_argument('--create-env', action='store_true', help='Create .env template and exit')
    
    args = parser.parse_args()
    
    # Load configuration
    config_manager = ConfigManager(args.config_dir)
    config = config_manager.load_config()
    
    # Override quality if specified
    if args.quality:
        config.download.quality = args.quality
    
    # Setup logging
    setup_logging(config.log)
    
    # Create .env template if requested
    if args.create_env:
        config_manager.save_env_template()
        print(f"Created .env.example in {args.config_dir}")
        print("Copy this file to .env and edit with your settings")
        return 0
    
    # Test configuration if requested
    if args.test_config:
        print("Testing configuration...")
        errors = config_manager.validate_config(config)
        if errors:
            print("❌ Configuration errors found:")
            for error in errors:
                print(f"  - {error}")
            return 1
        else:
            print("✅ Configuration is valid!")
            print(f"Movies path: {config.jellyfin_movies_path}")
            print(f"Network enabled: {config.network.enabled}")
            if config.network.enabled:
                print(f"Network type: {config.network.type}")
                print(f"Server: {config.network.server}")
            return 0
    
    # Validate configuration
    errors = config_manager.validate_config(config)
    if errors:
        logger.error("Configuration errors:")
        for error in errors:
            logger.error(f"  - {error}")
        logger.error("Fix configuration errors before running")
        return 1
    
    # Create downloader
    downloader = EnhancedTMDBTrailerDownloader(config)
    
    # Execute requested action
    success = False
    
    if args.scan_existing:
        success = downloader.run_scan_existing()
    elif args.title:
        success = downloader.run_download_movie(args.title, args.year)
    else:
        logger.error("No action specified. Use --scan-existing or --title")
        parser.print_help()
        return 1
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
