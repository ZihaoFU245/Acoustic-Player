"""
Playlist API Endpoints
This module defines the API routes for playlist management.
"""
from flask import Blueprint, request, jsonify
from ..models.playlist import PlaylistManager
from .serializers import playlist_schema, playlist_tracks_schema
from ..ws.events import emit_playlist_changed

# Create Blueprint
playlist_api = Blueprint('playlist_api', __name__)

# Initialize playlist manager
playlist_manager = PlaylistManager()

@playlist_api.route('', methods=['GET'])
def get_playlists():
    """Get all playlists."""
    try:
        playlists = playlist_manager.list_playlists()
        return jsonify([playlist_schema(playlist) for playlist in playlists])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@playlist_api.route('', methods=['POST'])
def create_playlist():
    """Create a new playlist."""
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Playlist name is required'}), 400
    
    try:
        playlist = playlist_manager.create_playlist(data['name'])
        # Emit WebSocket event
        emit_playlist_changed(playlist.id, 'created', playlist_schema(playlist))
        return jsonify(playlist_schema(playlist))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@playlist_api.route('/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    """Delete a playlist."""
    try:
        result = playlist_manager.delete_playlist(playlist_id)
        if result:
            # Emit WebSocket event
            emit_playlist_changed(playlist_id, 'deleted')
            return jsonify({'message': f'Playlist {playlist_id} deleted successfully'})
        else:
            return jsonify({'error': 'Playlist not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@playlist_api.route('/<playlist_id>/tracks', methods=['GET'])
def get_playlist_tracks(playlist_id):
    """Get all tracks in a playlist."""
    try:
        tracks = playlist_manager.get_playlist_tracks(playlist_id)
        return jsonify(playlist_tracks_schema(tracks))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@playlist_api.route('/<playlist_id>/tracks', methods=['POST'])
def add_track_to_playlist(playlist_id):
    """Add a track to a playlist."""
    data = request.json
    if not data or 'track_id' not in data:
        return jsonify({'error': 'Track ID is required'}), 400
    
    try:
        result = playlist_manager.add_track(playlist_id, data['track_id'])
        if result:
            # Emit WebSocket event
            emit_playlist_changed(playlist_id, 'track_added', {'track_id': data['track_id']})
            return jsonify({'message': 'Track added to playlist successfully'})
        else:
            return jsonify({'error': 'Failed to add track to playlist'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@playlist_api.route('/<playlist_id>/tracks/<int:track_index>', methods=['DELETE'])
def remove_track_from_playlist(playlist_id, track_index):
    """Remove a track from a playlist."""
    try:
        result = playlist_manager.remove_track(playlist_id, track_index)
        if result:
            # Emit WebSocket event
            emit_playlist_changed(playlist_id, 'track_removed', {'track_index': track_index})
            return jsonify({'message': 'Track removed from playlist successfully'})
        else:
            return jsonify({'error': 'Failed to remove track from playlist'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500