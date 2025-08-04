#!/usr/bin/env python3
"""
Enhanced TMDB Trailer Downloader with Network Share Support
Supports automatic mounting of SMB/NFS shares with credentials
"""

import subprocess
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NetworkMounter:
    """Handle mounting and unmounting of network shares"""
    
    def __init__(self, network_config: Dict[str, Any]):
        self.config = network_config
        self.mount_point = Path(network_config.get('mount_point', '/mnt/jellyfin-movies'))
        
    def is_mounted(self) -> bool:
        """Check if the share is already mounted"""
        try:
            result = subprocess.run(['mountpoint', '-q', str(self.mount_point)], 
                                  capture_output=True)
            return result.returncode == 0
        except FileNotFoundError:
            # Fallback method if mountpoint command not available
            try:
                with open('/proc/mounts', 'r') as f:
                    return str(self.mount_point) in f.read()
            except:
                return False
    
    def mount_smb(self) -> bool:
        """Mount SMB/CIFS share"""
        try:
            # Create mount point if it doesn't exist
            self.mount_point.mkdir(parents=True, exist_ok=True)
            
            server = self.config['server']
            share = self.config['share']
            username = self.config.get('username', '')
            password = self.config.get('password', '')
            domain = self.config.get('domain', 'WORKGROUP')
            
            # Build mount command
            share_path = f"//{server}/{share}"
            mount_options = [
                f"username={username}",
                f"password={password}",
                f"domain={domain}",
                f"uid={os.getuid()}",
                f"gid={os.getgid()}",
                "iocharset=utf8"
            ]
            
            cmd = [
                'sudo', 'mount', '-t', 'cifs',
                share_path, str(self.mount_point),
                '-o', ','.join(mount_options)
            ]
            
            logger.info(f"Mounting SMB share: {share_path}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully mounted {share_path} to {self.mount_point}")
                return True
            else:
                logger.error(f"Failed to mount SMB share: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error mounting SMB share: {e}")
            return False
    
    def mount_nfs(self) -> bool:
        """Mount NFS share"""
        try:
            # Create mount point if it doesn't exist
            self.mount_point.mkdir(parents=True, exist_ok=True)
            
            server = self.config['server']
            share = self.config['share']
            share_path = f"{server}:/{share.lstrip('/')}"
            
            cmd = ['sudo', 'mount', '-t', 'nfs', share_path, str(self.mount_point)]
            
            # Add NFS version if specified
            nfs_version = self.config.get('nfs_version')
            if nfs_version:
                cmd.extend(['-o', f'nfsvers={nfs_version}'])
            
            logger.info(f"Mounting NFS share: {share_path}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully mounted {share_path} to {self.mount_point}")
                return True
            else:
                logger.error(f"Failed to mount NFS share: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error mounting NFS share: {e}")
            return False
    
    def mount_sshfs(self) -> bool:
        """Mount using SSHFS"""
        try:
            # Create mount point if it doesn't exist
            self.mount_point.mkdir(parents=True, exist_ok=True)
            
            server = self.config['server']
            username = self.config['username']
            remote_path = self.config.get('remote_path', '/movies')
            
            # Build sshfs command
            remote_location = f"{username}@{server}:{remote_path}"
            cmd = ['sshfs', remote_location, str(self.mount_point)]
            
            # Add SSH key if specified
            ssh_key = self.config.get('ssh_key')
            if ssh_key:
                cmd.extend(['-o', f'IdentityFile={ssh_key}'])
            
            logger.info(f"Mounting SSHFS: {remote_location}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully mounted {remote_location} to {self.mount_point}")
                return True
            else:
                logger.error(f"Failed to mount SSHFS: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error mounting SSHFS: {e}")
            return False
    
    def mount(self) -> bool:
        """Mount the network share based on type"""
        if self.is_mounted():
            logger.info(f"Share already mounted at {self.mount_point}")
            return True
        
        share_type = self.config.get('type', 'smb').lower()
        
        if share_type in ['smb', 'cifs']:
            return self.mount_smb()
        elif share_type == 'nfs':
            return self.mount_nfs()
        elif share_type in ['ssh', 'sshfs']:
            return self.mount_sshfs()
        else:
            logger.error(f"Unsupported share type: {share_type}")
            return False
    
    def unmount(self) -> bool:
        """Unmount the network share"""
        if not self.is_mounted():
            logger.info("Share not mounted")
            return True
        
        try:
            cmd = ['sudo', 'umount', str(self.mount_point)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully unmounted {self.mount_point}")
                return True
            else:
                logger.error(f"Failed to unmount: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error unmounting: {e}")
            return False

def load_config_with_network(config_path: str) -> tuple[Dict, Optional[NetworkMounter]]:
    """Load configuration and create network mounter if needed"""
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    network_config = config.get('network')
    mounter = None
    
    if network_config and network_config.get('auto_mount', False):
        mounter = NetworkMounter(network_config)
    
    return config, mounter

if __name__ == "__main__":
    print("Enhanced TMDB Trailer Downloader with Network Share Support")
    print("This is an example of how to extend the main script.")
    print("Key features:")
    print("- Automatic SMB/CIFS mounting with credentials")
    print("- NFS mounting support")
    print("- SSHFS mounting for SSH access")
    print("- Automatic mount/unmount handling")
    print()
    print("To use this, you would:")
    print("1. Update your config.json with network settings")
    print("2. Integrate these classes into the main script")
    print("3. Call mounter.mount() before running the downloader")
    print("4. Call mounter.unmount() when finished (optional)")
