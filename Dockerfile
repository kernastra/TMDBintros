# TMDB Trailer Downloader - Docker Image
FROM python:3.11-slim

# Set build arguments
ARG BUILD_DATE
ARG VERSION="v3.0.0"

# Add metadata
LABEL maintainer="TMDB Trailer Downloader" \
      description="Automated trailer downloader for Jellyfin Cinema Mode v3.0.0" \
      version="${VERSION}" \
      build-date="${BUILD_DATE}"

# Install system dependencies for network mounting
RUN apt-get update && apt-get install -y \
    cifs-utils \
    nfs-common \
    sshfs \
    fuse \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create app user and group
RUN groupadd -r -g 1000 tmdb && \
    useradd -r -u 1000 -g tmdb -s /bin/bash -d /app tmdb

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=tmdb:tmdb . .

# Create necessary directories
RUN mkdir -p /app/logs /app/cache /app/downloads && \
    chown -R tmdb:tmdb /app

# Create mount points for network shares
RUN mkdir -p /mnt/movies /mnt/network && \
    chown tmdb:tmdb /mnt/movies /mnt/network

# Switch to non-root user
USER tmdb

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO \
    LOG_FILE=/app/logs/tmdb.log

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)" || exit 1

# Expose any ports if needed (not typically required for this app)
# EXPOSE 8080

# Default command (can be overridden in docker-compose.yml)
CMD ["python3", "enhanced_downloader.py", "--help"]
