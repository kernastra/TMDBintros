#!/usr/bin/env python3
"""
Version information for TMDB Trailer Downloader
"""

__version__ = "3.0.0"
__version_info__ = (3, 0, 0)
__release_date__ = "2025-08-04"
__release_name__ = "Enterprise Container Edition"

# Version components
MAJOR = 3
MINOR = 0
PATCH = 0

# Build information
BUILD_DATE = "2025-08-04"
GIT_BRANCH = "main"
DOCKER_TAG = f"v{__version__}"

# Feature flags for this version
FEATURES = {
    "docker_support": True,
    "web_dashboard": True,
    "real_time_monitoring": True,
    "scheduled_scanning": True,
    "network_shares": True,
    "environment_config": True,
    "enterprise_deployment": True,
    "json_config": True,  # Legacy support
}

# Compatibility information
COMPATIBILITY = {
    "jellyfin_cinema_mode": "1.x",
    "python_min": "3.7",
    "docker_compose_min": "1.27.0",
    "docker_min": "20.10.0",
}

def get_version():
    """Get the current version string"""
    return __version__

def get_version_info():
    """Get detailed version information"""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "release_date": __release_date__,
        "release_name": __release_name__,
        "build_date": BUILD_DATE,
        "docker_tag": DOCKER_TAG,
        "features": FEATURES,
        "compatibility": COMPATIBILITY,
    }

def print_version():
    """Print version information to console"""
    print(f"TMDB Trailer Downloader v{__version__}")
    print(f"Release: {__release_name__}")
    print(f"Build Date: {BUILD_DATE}")
    print(f"Docker Tag: {DOCKER_TAG}")
    
    print("\nFeatures:")
    for feature, enabled in FEATURES.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {feature.replace('_', ' ').title()}")
    
    print(f"\nCompatibility:")
    for component, version in COMPATIBILITY.items():
        print(f"  {component.replace('_', ' ').title()}: {version}")

if __name__ == "__main__":
    print_version()
