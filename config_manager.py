#!/usr/bin/env python3
"""
Configuration management for TMDB Trailer Downloader
Supports environment variables, .env files, and JSON configuration
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

@dataclass
class NetworkConfig:
    """Network share configuration"""
    enabled: bool = False
    type: str = "smb"  # smb, nfs, sshfs
    server: str = ""
    share: str = ""
    username: str = ""
    password: str = ""
    domain: str = "WORKGROUP"
    mount_point: str = "/mnt/jellyfin-movies"
    auto_mount: bool = True
    
    # NFS specific
    nfs_version: Optional[str] = None
    
    # SSH specific
    ssh_key: Optional[str] = None
    remote_path: str = "/movies"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for compatibility"""
        return {
            'enabled': self.enabled,
            'type': self.type,
            'server': self.server,
            'share': self.share,
            'username': self.username,
            'password': self.password,
            'domain': self.domain,
            'mount_point': self.mount_point,
            'auto_mount': self.auto_mount,
            'nfs_version': self.nfs_version,
            'ssh_key': self.ssh_key,
            'remote_path': self.remote_path
        }

@dataclass
class DownloadConfig:
    """Download configuration options"""
    quality: str = "best"
    max_trailers_per_movie: int = 5
    skip_existing: bool = True
    trailer_naming_pattern: str = "trailer_{index}"
    overwrite_existing: bool = False
    download_timeout: int = 300
    max_concurrent_downloads: int = 3
    retry_attempts: int = 3
    retry_delay: int = 5

@dataclass
class ScanConfig:
    """Library scanning configuration"""
    recursive: bool = True
    movie_folder_pattern: str = r"^(.+?)\s*\((\d{4})\).*$"

@dataclass
class UpcomingConfig:
    """Upcoming movies configuration"""
    enabled: bool = False
    months_ahead: int = 6
    min_popularity: float = 10.0
    max_movies: int = 50
    cleanup_days: int = 30

@dataclass
class LogConfig:
    """Logging configuration"""
    level: str = "INFO"
    file: Optional[str] = None

@dataclass
class TMDBConfig:
    """Complete TMDB Trailer Downloader configuration"""
    tmdb_api_key: str = ""
    jellyfin_movies_path: str = "/path/to/your/jellyfin/movies/library"
    network: NetworkConfig = field(default_factory=NetworkConfig)
    download: DownloadConfig = field(default_factory=DownloadConfig)
    scan: ScanConfig = field(default_factory=ScanConfig)
    upcoming: UpcomingConfig = field(default_factory=UpcomingConfig)
    log: LogConfig = field(default_factory=LogConfig)
    movies: list = field(default_factory=list)

class ConfigManager:
    """Manage configuration from multiple sources"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else Path.cwd()
        self.env_file = self.config_dir / ".env"
        self.json_file = self.config_dir / "config.json"
        
    def load_env_file(self) -> None:
        """Load environment variables from .env file"""
        if self.env_file.exists():
            logger.info(f"Loading environment variables from {self.env_file}")
            load_dotenv(self.env_file)
        else:
            logger.info("No .env file found, using system environment variables only")
    
    def get_env_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean value from environment variable"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_env_int(self, key: str, default: int = 0) -> int:
        """Get integer value from environment variable"""
        try:
            return int(os.getenv(key, str(default)))
        except ValueError:
            logger.warning(f"Invalid integer value for {key}, using default: {default}")
            return default
    
    def get_env_float(self, key: str, default: float = 0.0) -> float:
        """Get float value from environment variable"""
        try:
            return float(os.getenv(key, str(default)))
        except ValueError:
            logger.warning(f"Invalid float value for {key}, using default: {default}")
            return default
    
    def load_from_env(self) -> TMDBConfig:
        """Load configuration from environment variables"""
        self.load_env_file()
        
        # Network configuration
        network = NetworkConfig(
            enabled=self.get_env_bool('NETWORK_ENABLED'),
            type=os.getenv('NETWORK_TYPE', 'smb'),
            server=os.getenv('NETWORK_SERVER', ''),
            share=os.getenv('NETWORK_SHARE', ''),
            username=os.getenv('NETWORK_USERNAME', ''),
            password=os.getenv('NETWORK_PASSWORD', ''),
            domain=os.getenv('NETWORK_DOMAIN', 'WORKGROUP'),
            mount_point=os.getenv('NETWORK_MOUNT_POINT', '/mnt/jellyfin-movies'),
            auto_mount=self.get_env_bool('NETWORK_AUTO_MOUNT', True),
            nfs_version=os.getenv('NETWORK_NFS_VERSION'),
            ssh_key=os.getenv('NETWORK_SSH_KEY'),
            remote_path=os.getenv('NETWORK_REMOTE_PATH', '/movies')
        )
        
        # Download configuration
        download = DownloadConfig(
            quality=os.getenv('DOWNLOAD_QUALITY', 'best'),
            max_trailers_per_movie=self.get_env_int('MAX_TRAILERS_PER_MOVIE', 5),
            skip_existing=self.get_env_bool('SKIP_EXISTING', True),
            trailer_naming_pattern=os.getenv('TRAILER_NAMING_PATTERN', 'trailer_{index}'),
            overwrite_existing=self.get_env_bool('OVERWRITE_EXISTING', False),
            download_timeout=self.get_env_int('DOWNLOAD_TIMEOUT', 300),
            max_concurrent_downloads=self.get_env_int('MAX_CONCURRENT_DOWNLOADS', 3),
            retry_attempts=self.get_env_int('RETRY_ATTEMPTS', 3),
            retry_delay=self.get_env_int('RETRY_DELAY', 5)
        )
        
        # Scan configuration
        scan = ScanConfig(
            recursive=self.get_env_bool('SCAN_RECURSIVE', True),
            movie_folder_pattern=os.getenv('MOVIE_FOLDER_PATTERN', r"^(.+?)\s*\((\d{4})\).*$")
        )
        
        # Upcoming movies configuration
        upcoming = UpcomingConfig(
            enabled=self.get_env_bool('UPCOMING_ENABLED', False),
            months_ahead=self.get_env_int('UPCOMING_MONTHS_AHEAD', 6),
            min_popularity=self.get_env_float('UPCOMING_MIN_POPULARITY', 10.0),
            max_movies=self.get_env_int('UPCOMING_MAX_MOVIES', 50),
            cleanup_days=self.get_env_int('UPCOMING_CLEANUP_DAYS', 30)
        )
        
        # Log configuration
        log = LogConfig(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            file=os.getenv('LOG_FILE') or None
        )
        
        # Main configuration
        config = TMDBConfig(
            tmdb_api_key=os.getenv('TMDB_API_KEY', ''),
            jellyfin_movies_path=os.getenv('JELLYFIN_MOVIES_PATH', '/path/to/your/jellyfin/movies/library'),
            network=network,
            download=download,
            scan=scan,
            upcoming=upcoming,
            log=log
        )
        
        return config
    
    def load_from_json(self) -> Optional[TMDBConfig]:
        """Load configuration from JSON file (legacy support)"""
        if not self.json_file.exists():
            return None
        
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            
            # Convert JSON to config object
            config = TMDBConfig()
            config.tmdb_api_key = data.get('tmdb_api_key', '')
            config.jellyfin_movies_path = data.get('remote_share_path', '/path/to/your/jellyfin/movies/library')
            config.download.quality = data.get('quality', 'best')
            config.movies = data.get('movies', [])
            
            # Handle network config if present
            if 'network' in data:
                net_data = data['network']
                config.network = NetworkConfig(
                    enabled=net_data.get('enabled', False),
                    type=net_data.get('type', 'smb'),
                    server=net_data.get('server', ''),
                    share=net_data.get('share', ''),
                    username=net_data.get('username', ''),
                    password=net_data.get('password', ''),
                    domain=net_data.get('domain', 'WORKGROUP'),
                    mount_point=net_data.get('mount_point', '/mnt/jellyfin-movies'),
                    auto_mount=net_data.get('auto_mount', True)
                )
            
            logger.info(f"Loaded configuration from {self.json_file}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading JSON config: {e}")
            return None
    
    def load_config(self) -> TMDBConfig:
        """Load configuration from environment variables, falling back to JSON"""
        # Try environment variables first
        config = self.load_from_env()
        
        # If no API key in env, try JSON file
        if not config.tmdb_api_key:
            json_config = self.load_from_json()
            if json_config and json_config.tmdb_api_key:
                logger.info("Using API key from JSON config")
                config.tmdb_api_key = json_config.tmdb_api_key
                # Also merge movies list if not specified in env
                if not hasattr(config, 'movies') or not config.movies:
                    config.movies = json_config.movies
        
        return config
    
    def validate_config(self, config: TMDBConfig) -> list[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        if not config.tmdb_api_key:
            errors.append("TMDB API key is required (set TMDB_API_KEY)")
        
        if not config.jellyfin_movies_path or config.jellyfin_movies_path == "/path/to/your/jellyfin/movies/library":
            errors.append("Jellyfin movies path must be set (set JELLYFIN_MOVIES_PATH)")
        
        if config.network.enabled:
            if not config.network.server:
                errors.append("Network server is required when network is enabled")
            if not config.network.share and config.network.type in ['smb', 'nfs']:
                errors.append("Network share is required for SMB/NFS")
            if config.network.type in ['smb', 'sshfs'] and not config.network.username:
                errors.append("Username is required for SMB/SSHFS")
        
        return errors
    
    def save_env_template(self) -> None:
        """Save current configuration as .env template"""
        template_file = self.config_dir / ".env.example"
        if template_file.exists():
            logger.info(f"Environment template already exists: {template_file}")
        else:
            logger.info(f"Created environment template: {template_file}")

def setup_logging(log_config: LogConfig) -> None:
    """Setup logging based on configuration"""
    level = getattr(logging, log_config.level.upper(), logging.INFO)
    
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if log_config.file:
        logging.basicConfig(
            level=level,
            format=format_str,
            handlers=[
                logging.FileHandler(log_config.file),
                logging.StreamHandler()
            ]
        )
    else:
        logging.basicConfig(level=level, format=format_str)

if __name__ == "__main__":
    # Test the configuration system
    manager = ConfigManager()
    config = manager.load_config()
    
    print("TMDB Trailer Downloader Configuration Test")
    print("=" * 50)
    print(f"TMDB API Key: {'***' + config.tmdb_api_key[-4:] if config.tmdb_api_key else 'Not set'}")
    print(f"Movies Path: {config.jellyfin_movies_path}")
    print(f"Download Quality: {config.download.quality}")
    print(f"Network Enabled: {config.network.enabled}")
    if config.network.enabled:
        print(f"Network Type: {config.network.type}")
        print(f"Network Server: {config.network.server}")
        print(f"Network Share: {config.network.share}")
    print(f"Log Level: {config.log.level}")
    
    # Validate configuration
    errors = manager.validate_config(config)
    if errors:
        print("\nConfiguration Errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\nConfiguration is valid!")
    
    print(f"\nTo get started:")
    print(f"1. Copy .env.example to .env")
    print(f"2. Edit .env with your settings")
    print(f"3. Run the main script")
