#!/usr/bin/env python3
"""
TMDB Trailer Downloader - Local Runner
Run the application locally with SMB/network share support
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LocalRunner:
    def __init__(self, env_file=".env.local"):
        self.env_file = env_file
        self.load_environment()
        
    def load_environment(self):
        """Load environment variables from local config"""
        if not os.path.exists(self.env_file):
            logger.error(f"Environment file {self.env_file} not found!")
            logger.info("Copy .env.local.example to .env.local and configure your settings")
            sys.exit(1)
            
        load_dotenv(self.env_file)
        logger.info(f"Loaded configuration from {self.env_file}")
        
        # Validate required settings
        required_vars = ["TMDB_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var) or os.getenv(var) == "your_tmdb_api_key_here"]
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            logger.info(f"Please configure these in {self.env_file}")
            sys.exit(1)
    
    def setup_smb_mount(self):
        """Setup SMB mount if network is enabled"""
        if os.getenv("NETWORK_ENABLED", "false").lower() != "true":
            logger.info("Network mounting disabled")
            return True
            
        network_type = os.getenv("NETWORK_TYPE", "smb")
        if network_type != "smb":
            logger.info(f"Network type {network_type} - skipping SMB setup")
            return True
            
        server = os.getenv("NETWORK_SERVER")
        share = os.getenv("NETWORK_SHARE")
        username = os.getenv("NETWORK_USERNAME")
        password = os.getenv("NETWORK_PASSWORD")
        domain = os.getenv("NETWORK_DOMAIN", "WORKGROUP")
        mount_point = os.getenv("NETWORK_MOUNT_POINT", "/mnt/jellyfin-movies")
        
        if not all([server, share, username, password]):
            logger.error("SMB configuration incomplete. Required: SERVER, SHARE, USERNAME, PASSWORD")
            return False
            
        logger.info(f"Setting up SMB mount: //{server}/{share} -> {mount_point}")
        
        # Create mount point
        mount_path = Path(mount_point)
        try:
            mount_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created mount point: {mount_point}")
        except Exception as e:
            logger.error(f"Failed to create mount point: {e}")
            return False
            
        # Check if already mounted
        try:
            result = subprocess.run(["mount"], capture_output=True, text=True)
            if mount_point in result.stdout:
                logger.info(f"SMB share already mounted at {mount_point}")
                return True
        except Exception as e:
            logger.warning(f"Could not check mount status: {e}")
            
        # Mount SMB share
        mount_cmd = [
            "sudo", "mount", "-t", "cifs",
            f"//{server}/{share}",
            mount_point,
            "-o", f"username={username},password={password},domain={domain},uid={os.getuid()},gid={os.getgid()},iocharset=utf8"
        ]
        
        try:
            logger.info("Mounting SMB share (you may be prompted for sudo password)...")
            result = subprocess.run(mount_cmd, check=True, capture_output=True, text=True)
            logger.info(f"SMB share mounted successfully at {mount_point}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to mount SMB share: {e}")
            logger.error(f"Error output: {e.stderr}")
            logger.info("Try mounting manually or check SMB credentials")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        logger.info("Installing Python dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True)
            logger.info("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def run_library_scan(self):
        """Run library scan for existing movies"""
        logger.info("Running library scan for existing movies...")
        try:
            from tmdb_trailer_downloader import main as tmdb_main
            tmdb_main()
            return True
        except Exception as e:
            logger.error(f"Library scan failed: {e}")
            return False
    
    def run_upcoming_scan(self):
        """Run upcoming movies scan"""
        logger.info("Running upcoming movies scan...")
        try:
            from tmdb_upcoming import main as upcoming_main
            upcoming_main()
            return True
        except Exception as e:
            logger.error(f"Upcoming scan failed: {e}")
            return False
    
    def run_dashboard(self):
        """Run web dashboard"""
        dashboard_enabled = os.getenv("DASHBOARD_ENABLED", "false").lower() == "true"
        if not dashboard_enabled:
            logger.info("Dashboard disabled in configuration")
            return True
            
        logger.info("Starting web dashboard...")
        try:
            from tmdb_dashboard import app
            port = int(os.getenv("DASHBOARD_PORT", 8085))
            host = os.getenv("DASHBOARD_HOST", "127.0.0.1")
            debug = os.getenv("DASHBOARD_DEBUG", "false").lower() == "true"
            
            logger.info(f"Dashboard starting at http://{host}:{port}")
            app.run(host=host, port=port, debug=debug)
            return True
        except Exception as e:
            logger.error(f"Dashboard failed to start: {e}")
            return False
    
    def run_monitor(self):
        """Run file system monitor"""
        logger.info("Starting file system monitor...")
        try:
            from tmdb_monitor import main as monitor_main
            monitor_main()
            return True
        except Exception as e:
            logger.error(f"Monitor failed: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="TMDB Trailer Downloader - Local Runner")
    parser.add_argument("--env", default=".env.local", help="Environment file to use")
    parser.add_argument("--no-mount", action="store_true", help="Skip SMB mounting")
    parser.add_argument("--no-deps", action="store_true", help="Skip dependency installation")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Commands
    subparsers.add_parser("scan", help="Scan existing movie library")
    subparsers.add_parser("upcoming", help="Scan for upcoming movies")
    subparsers.add_parser("dashboard", help="Start web dashboard")
    subparsers.add_parser("monitor", help="Start file system monitor")
    subparsers.add_parser("setup", help="Setup environment only")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize runner
    runner = LocalRunner(args.env)
    
    # Install dependencies
    if not args.no_deps:
        if not runner.install_dependencies():
            return 1
    
    # Setup SMB mount
    if not args.no_mount:
        if not runner.setup_smb_mount():
            logger.warning("SMB mount failed, but continuing...")
    
    # Execute command
    success = False
    if args.command == "scan":
        success = runner.run_library_scan()
    elif args.command == "upcoming":
        success = runner.run_upcoming_scan()
    elif args.command == "dashboard":
        success = runner.run_dashboard()
    elif args.command == "monitor":
        success = runner.run_monitor()
    elif args.command == "setup":
        logger.info("Environment setup complete")
        success = True
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
