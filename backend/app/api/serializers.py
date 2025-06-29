"""Serializers for API responses.

This module contains utility functions to convert internal data structures
into JSON-friendly dictionaries for API responses.
"""

import os

def player_status_schema(player_status):
    """
    Serialize player status object.
    
    Args:
        player_status: Dictionary containing player state information
        
    Returns:
        Dictionary with standardized player status fields
    """
    return {
        'state': player_status.get('state'),    # TODO: Could use enum to indicate state
        'current_track': track_schema(player_status.get('current_track')),
        'position': player_status.get('position', 0),
        'duration': player_status.get('duration', 0),
        'volume': player_status.get('volume', 100)
    }

def track_schema(track):
    """
    Serialize track object.
    
    Args:
        track: Track object or dictionary
        
    Returns:
        Dictionary with standardized track fields
    """
    if not track:
        return None

    # If a plain file path string is provided, return minimal info
    if isinstance(track, str):
        base = os.path.basename(track)
        return {
            'id': None,
            'path': track,
            'title': base,
            'artist': '',
            'album': '',
            'duration': 0,
            'track_num': 0,
            'genre': '',
            'album_art_path': None,
            'has_thumbnail': False
        }
        
    track_id = track.get('id') if isinstance(track, dict) else getattr(track, 'id', None)
    
    result = {
        'id': track_id,
        'path': track.get('path') if isinstance(track, dict) else getattr(track, 'path', ''),
        'title': track.get('title') if isinstance(track, dict) else getattr(track, 'title', ''),
        'artist': track.get('artist') if isinstance(track, dict) else getattr(track, 'artist', ''),
        'album': track.get('album') if isinstance(track, dict) else getattr(track, 'album', ''),
        'duration': track.get('duration') if isinstance(track, dict) else getattr(track, 'duration', 0),
        'track_num': track.get('track_num') if isinstance(track, dict) else getattr(track, 'track_num', 0),
        'genre': track.get('genre') if isinstance(track, dict) else getattr(track, 'genre', ''),
        'album_art_path': track.get('album_art_path') if isinstance(track, dict) else getattr(track, 'album_art_path', None),
        'has_thumbnail': track.get('has_thumbnail') if isinstance(track, dict) else getattr(track, 'has_thumbnail', False)
    }
    
    # Include thumbnail data if this is a Track object with the get_thumbnail_base64 method
    if not isinstance(track, dict) and hasattr(track, 'get_thumbnail_base64'):
        result['thumbnail'] = track.get_thumbnail_base64()
        
    return result

def playlist_schema(playlist):
    """
    Serialize playlist object.
    
    Args:
        playlist: Playlist object or dictionary
        
    Returns:
        Dictionary with standardized playlist fields
    """
    if not playlist:
        return None
    
    playlist_id = playlist.get('id') if isinstance(playlist, dict) else getattr(playlist, 'id', None)
    
    return {
        'id': playlist_id,
        'name': playlist.get('name') if isinstance(playlist, dict) else getattr(playlist, 'name', ''),
        'track_count': playlist.get('track_count') if isinstance(playlist, dict) else getattr(playlist, 'track_count', 0)
    }

def playlist_tracks_schema(tracks):
    """
    Serialize a list of tracks in a playlist.
    
    Args:
        tracks: List of track objects or dictionaries
        
    Returns:
        List of serialized tracks
    """
    return [track_schema(track) for track in tracks]

def library_tracks_schema(tracks):
    """
    Serialize a list of tracks in the library.
    
    Args:
        tracks: List of track objects or dictionaries
        
    Returns:
        List of serialized tracks
    """
    return [track_schema(track) for track in tracks]