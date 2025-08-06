# Testing Setup - No .env Required

This directory contains a standalone testing configuration that doesn't require a separate `.env` file. All environment variables are embedded directly in the docker-compose file.

## Quick Start

### Without Docker (Testing Mode)

1. **Get your TMDB API key** from https://www.themoviedb.org/settings/api

2. **Test the configuration:**
   ```bash
   python3 test_standalone.py YOUR_TMDB_API_KEY
   ```

3. **See the dashboard interface:**
   ```bash
   python3 dashboard_simulator.py
   ```
   Then visit http://localhost:8085

### With Docker (Full Mode)

1. **Validate the configuration** (optional):
   ```bash
   ./validate.sh YOUR_TMDB_API_KEY
   ```

2. **Run the test script:**
   ```bash
   ./test.sh YOUR_TMDB_API_KEY
   ```

3. **Access the dashboard** at http://localhost:8085

## Available Commands

### Testing Without Docker
```bash
# Test configuration and logic
python3 test_standalone.py YOUR_API_KEY

# Run dashboard simulator 
python3 dashboard_simulator.py
```

### Docker Commands
```bash
# Validate configuration (doesn't require Docker running)
./validate.sh YOUR_API_KEY

# Start all services
./test.sh YOUR_API_KEY up

# Start only the dashboard
./test.sh YOUR_API_KEY dashboard

# Run a one-time library scan
./test.sh YOUR_API_KEY scan

# Run upcoming movies scan
./test.sh YOUR_API_KEY upcoming

# View logs
./test.sh YOUR_API_KEY logs

# Stop all services
./test.sh YOUR_API_KEY down
```

## What's Pre-configured

The testing setup includes these default settings:

### Upcoming Movies
- **Enabled**: `true`
- **Days ahead**: 90 days
- **Max movies**: 20 (reduced for testing)
- **Max trailers per movie**: 3
- **Countries**: US, GB (English-speaking)
- **Languages**: English
- **Genres**: Action, Adventure, Sci-Fi, Thriller
- **Excluded**: Horror, Documentary
- **Studios**: Marvel, Warner Bros, Disney, Universal
- **Ratings**: PG, PG-13, R
- **Quality**: Min 6.0 rating, 100+ votes

### Dashboard
- **Port**: 8085 (avoids conflicts)
- **Debug mode**: Disabled

### Integrations
- **Radarr**: Disabled (for simple testing)
- **Network shares**: Disabled
- **Monitoring**: Disabled

## File Structure

During testing, the following directories will be created:
- `./movies/` - Downloaded trailers
- `./logs/` - Application logs

## Manual Docker Commands

If you prefer manual control:

```bash
# Replace YOUR_API_KEY with your actual key
sed 's/your_tmdb_api_key_here/YOUR_API_KEY/g' docker-compose.testing.yml > docker-compose.test.yml

# Start services
docker-compose -f docker-compose.test.yml up -d

# View logs
docker-compose -f docker-compose.test.yml logs -f

# Stop services
docker-compose -f docker-compose.test.yml down

# Cleanup
rm docker-compose.test.yml
```

## Testing Different Configurations

To test different settings, edit the environment variables in `docker-compose.testing.yml`:

### Test Different Genres
```yaml
UPCOMING_FILTER_GENRES: "35,18,10749"  # Comedy, Drama, Romance
```

### Test Different Countries
```yaml
UPCOMING_FILTER_COUNTRIES: "US,CA,AU,NZ"  # English-speaking countries
```

### Test More Movies
```yaml
UPCOMING_MAX_MOVIES: "50"
```

### Enable Radarr Integration
```yaml
RADARR_ENABLED: "true"
RADARR_URL: "http://your-radarr:7878"
RADARR_API_KEY: "your_radarr_api_key"
```

## Troubleshooting

### Docker not running
- **Error**: "Couldn't connect to Docker daemon"
- **Solution**: Start Docker service or Docker Desktop
- **Alternative**: Use `./validate.sh YOUR_API_KEY` to check configuration

### Dashboard not accessible
- Check port 8085 is not in use: `netstat -tulpn | grep 8085`
- View dashboard logs: `./test.sh YOUR_API_KEY logs`

### No trailers downloaded
- Check API key is valid
- Verify internet connection
- Check logs for TMDB API errors
- Ensure movie directories are writable

### Permission issues
- Ensure Docker has access to the current directory
- Check file permissions on `./movies/` and `./logs/`

## Security Notes

- This testing setup includes API keys in plaintext environment variables
- Use only for testing, not in production
- The `test.sh` script temporarily creates files with your API key
- Files are cleaned up automatically when the script exits

## Moving to Production

Once testing is complete, use the full production setup:
1. Copy `.env.example` to `.env`
2. Configure all settings in `.env`
3. Use `docker-compose.yml` for production deployment
4. Follow security best practices in `DOCKER.md`
