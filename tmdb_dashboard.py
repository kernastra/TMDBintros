#!/usr/bin/env python3
"""
TMDB Trailer Dashboard - Web interface for monitoring and management
This is a future enhancement concept showing what the dashboard could become.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from config_manager import ConfigManager

logger = logging.getLogger(__name__)

class TMDBDashboard:
    """Web dashboard for TMDB Trailer Downloader monitoring and management"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager.load_config()
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_routes(self):
        """Setup web routes"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page"""
            stats = self.get_system_stats()
            return render_template('dashboard.html', stats=stats)
        
        @self.app.route('/api/stats')
        def api_stats():
            """API endpoint for system statistics"""
            return jsonify(self.get_system_stats())
        
        @self.app.route('/api/logs')
        def api_logs():
            """API endpoint for recent logs"""
            return jsonify(self.get_recent_logs())
        
        @self.app.route('/api/movies')
        def api_movies():
            """API endpoint for movie status"""
            return jsonify(self.get_movie_status())
        
        @self.app.route('/api/services')
        def api_services():
            """API endpoint for service status"""
            return jsonify(self.get_service_status())
    
    def get_system_stats(self):
        """Get system statistics"""
        return {
            'total_movies': self.count_movies(),
            'movies_with_trailers': self.count_movies_with_trailers(),
            'total_trailers': self.count_trailers(),
            'upcoming_movies': self.count_upcoming_movies(),
            'upcoming_trailers': self.count_upcoming_trailers(),
            'disk_usage': self.get_disk_usage(),
            'last_scan': self.get_last_scan_time(),
            'services_running': self.get_running_services(),
            'api_status': self.check_tmdb_api(),
            'uptime': self.get_uptime()
        }
    
    def get_recent_logs(self, limit=100):
        """Get recent log entries"""
        logs = []
        log_files = Path('/app/logs').glob('*.log')
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()[-limit:]
                    for line in lines:
                        if line.strip():
                            logs.append({
                                'timestamp': self.parse_log_timestamp(line),
                                'level': self.parse_log_level(line),
                                'service': log_file.stem,
                                'message': line.strip()
                            })
            except Exception as e:
                logger.warning(f"Error reading log file {log_file}: {e}")
        
        return sorted(logs, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_movie_status(self):
        """Get status of all movies"""
        movies_path = Path(self.config.jellyfin_movies_path)
        movies = []
        
        if movies_path.exists():
            for movie_dir in movies_path.iterdir():
                if movie_dir.is_dir():
                    trailers_dir = movie_dir / 'trailers'
                    trailer_count = 0
                    
                    if trailers_dir.exists():
                        trailer_count = len([f for f in trailers_dir.iterdir() 
                                           if f.suffix.lower() in ['.mp4', '.mkv', '.avi']])
                    
                    movies.append({
                        'name': movie_dir.name,
                        'has_trailers': trailer_count > 0,
                        'trailer_count': trailer_count,
                        'size': self.get_directory_size(movie_dir),
                        'last_modified': movie_dir.stat().st_mtime
                    })
        
        return movies
    
    def get_service_status(self):
        """Get status of running services"""
        # This would check Docker containers or system processes
        return {
            'monitor': {'status': 'running', 'uptime': '2h 15m'},
            'scheduler': {'status': 'running', 'uptime': '2h 15m'},
            'scanner': {'status': 'idle', 'last_run': '1h ago'}
        }
    
    def count_movies(self):
        """Count total movies"""
        movies_path = Path(self.config.jellyfin_movies_path)
        if not movies_path.exists():
            return 0
        return len([d for d in movies_path.iterdir() if d.is_dir()])
    
    def count_movies_with_trailers(self):
        """Count movies that have trailers"""
        movies_path = Path(self.config.jellyfin_movies_path)
        count = 0
        
        if movies_path.exists():
            for movie_dir in movies_path.iterdir():
                if movie_dir.is_dir():
                    trailers_dir = movie_dir / 'trailers'
                    if trailers_dir.exists() and any(trailers_dir.iterdir()):
                        count += 1
        
        return count
    
    def count_trailers(self):
        """Count total trailers"""
        movies_path = Path(self.config.jellyfin_movies_path)
        count = 0
        
        if movies_path.exists():
            for movie_dir in movies_path.iterdir():
                if movie_dir.is_dir():
                    trailers_dir = movie_dir / 'trailers'
                    if trailers_dir.exists():
                        count += len([f for f in trailers_dir.iterdir() 
                                    if f.suffix.lower() in ['.mp4', '.mkv', '.avi']])
        
        return count
    
    def count_upcoming_movies(self):
        """Count upcoming movies with trailers"""
        movies_path = Path(self.config.jellyfin_movies_path)
        upcoming_path = movies_path / "_upcoming_trailers"
        
        if not upcoming_path.exists():
            return 0
        
        count = 0
        for movie_dir in upcoming_path.iterdir():
            if movie_dir.is_dir() and movie_dir.name != "README.md":
                trailers_dir = movie_dir / 'trailers'
                if trailers_dir.exists() and any(trailers_dir.iterdir()):
                    count += 1
        
        return count
    
    def count_upcoming_trailers(self):
        """Count total upcoming trailers"""
        movies_path = Path(self.config.jellyfin_movies_path)
        upcoming_path = movies_path / "_upcoming_trailers"
        
        if not upcoming_path.exists():
            return 0
        
        count = 0
        for movie_dir in upcoming_path.iterdir():
            if movie_dir.is_dir() and movie_dir.name != "README.md":
                trailers_dir = movie_dir / 'trailers'
                if trailers_dir.exists():
                    count += len([f for f in trailers_dir.iterdir() 
                                if f.suffix.lower() in ['.mp4', '.mkv', '.avi', '.webm']])
        
        return count
    
    def run(self, host='0.0.0.0', port=8080, debug=False):
        """Run the dashboard web server"""
        logger.info(f"Starting TMDB Dashboard on http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

def main():
    """Main entry point for the dashboard"""
    import argparse
    
    parser = argparse.ArgumentParser(description='TMDB Trailer Dashboard')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--config-dir', help='Configuration directory path')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Load configuration
        config_manager = ConfigManager(config_dir=args.config_dir)
        
        # Create and run dashboard
        dashboard = TMDBDashboard(config_manager)
        dashboard.run(host=args.host, port=args.port, debug=args.debug)
        
    except Exception as e:
        logger.error(f"Failed to start dashboard: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
