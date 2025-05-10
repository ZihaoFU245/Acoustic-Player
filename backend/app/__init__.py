"""
Acoustic Player Application Package
This package contains the main modules for the music player app.
"""

# Export core classes for easier imports
from .models.player import MusicPlayer
from .models.playlist import PlaylistManager
from .models.metadata import MetadataManager
from .models.library import LibraryManager

# Make API endpoints available
from .api import player_api, library_api, playlist_api, lyrics_api

# Make WebSocket functionality available
from .ws import socketio, emit_player_status, emit_library_update, emit_playlist_changed

# Make lyrics functionality available
from .lyrics import get_lyrics_for_track, LyricsManager
