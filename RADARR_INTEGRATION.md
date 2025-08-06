# Radarr Integration for Upcoming Movies

## ✅ Implementation Status: COMPLETE

The Radarr integration has been fully implemented with three operational modes and comprehensive filtering options.

## How Radarr Integration Works

### Configuration
```bash
# Add to .env file
RADARR_ENABLED=true
RADARR_URL=http://localhost:7878
RADARR_API_KEY=your_radarr_api_key
RADARR_INTEGRATION_MODE=hybrid  # upcoming, radarr_only, or hybrid
```

### Modes

#### 1. `upcoming` (Current Mode)
- Download trailers for all popular upcoming movies
- Store in `_upcoming_trailers/` folder
- Manual copy when you add movies

#### 2. `radarr_only` (Radarr-Focused) ✅ IMPLEMENTED
- Only download trailers for movies in your Radarr monitored list
- Place trailers directly in Radarr movie folders when created
- Wait for Radarr to create folder structure first

#### 3. `hybrid` (Best of Both) ✅ IMPLEMENTED
- Download all popular upcoming trailers to `_upcoming_trailers/`
- **Prioritize** movies that are already in Radarr
- **Auto-move** trailers when Radarr creates the movie folder

### Workflow Examples

#### Radarr-Only Mode
```
1. You add "The Batman 2 (2025)" to Radarr
2. Radarr creates: /movies/The Batman 2 (2025)/
3. Upcoming movies service detects the Radarr movie
4. Downloads trailers directly to: /movies/The Batman 2 (2025)/trailers/
5. When movie file arrives, trailers are already there!
```

#### Hybrid Mode
```
1. Upcoming movies downloads trailers for popular movies to _upcoming_trailers/
2. You decide you want "The Batman 2" and add it to Radarr
3. Radarr creates: /movies/The Batman 2 (2025)/
4. Service detects the new Radarr folder
5. Auto-moves trailers from _upcoming_trailers/ to the Radarr folder
6. Cleans up the upcoming folder
```

### Implementation Considerations

#### Radarr API Integration
- Query Radarr for monitored movies list
- Check movie status (announced, in cinemas, available, etc.)
- Monitor for new folder creation
- Respect Radarr's naming conventions

#### Folder Monitoring
- Watch for new folders created by Radarr
- Match movie titles and years between TMDB and Radarr
- Handle different naming schemes gracefully

#### Benefits
- **No manual copying** of trailers
- **Radarr-first workflow** - only get trailers for movies you want
- **Automatic placement** in correct Radarr folders
- **Reduced storage** - no unused upcoming trailers

#### Challenges
- Radarr folder creation timing
- Movie name/year matching between systems
- Handling Radarr's custom naming schemes
- API rate limiting and connectivity
