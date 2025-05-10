"""
API Package
This package contains API endpoints for the music player app.
"""

from .player_endpoints import player_api
from .library_endpoints import library_api
from .playlist_endpoints import playlist_api
from .lyrics_endpoints import lyrics_api
from .serializers import (
    player_status_schema,
    track_schema,
    playlist_schema,
    playlist_tracks_schema,
    library_tracks_schema
)