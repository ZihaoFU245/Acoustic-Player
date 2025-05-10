"""
Library API Endpoints
This module defines the API routes for library management.
"""
from flask import Blueprint, request, jsonify, send_file
from ..models.library import LibraryManager
from .serializers import library_tracks_schema
from ..ws.events import emit_library_update
import os

# Create Blueprint
library_api = Blueprint('library_api', __name__)

# Initialize library manager
library_manager = LibraryManager()

@library_api.route('/tracks', methods=['GET'])
def get_tracks():
    """Get all tracks in the library with optional sorting/filtering."""
    # Get query parameters
    sort_by = request.args.get('sort_by', 'title')
    filter_term = request.args.get('filter', '')
    
    try:
        tracks = library_manager.get_tracks(sort_by=sort_by, filter=filter_term)
        return jsonify(library_tracks_schema(tracks))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@library_api.route('/scan', methods=['POST'])
def scan_directory():
    """Scan a directory for audio files."""
    data = request.json
    if not data or 'path' not in data:
        return jsonify({'error': 'Path is required'}), 400
    
    path = data['path']
    if not os.path.isdir(path):
        return jsonify({'error': 'Invalid directory path'}), 400
    
    try:
        result = library_manager.scan_directory(path)
        # Emit WebSocket event
        emit_library_update()
        return jsonify({
            'message': 'Library scan completed',
            'tracks_added': result.get('tracks_added', 0),
            'tracks_updated': result.get('tracks_updated', 0)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@library_api.route('/search', methods=['GET'])
def search_tracks():
    """Search for tracks in the library."""
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        tracks = library_manager.search_tracks(query)
        return jsonify(library_tracks_schema(tracks))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@library_api.route('/art/<track_id>', methods=['GET'])
def get_album_art(track_id):
    """Get album art for a track."""
    try:
        art_path = library_manager.get_album_art(track_id)
        if not art_path:
            return jsonify({'error': 'No album art available'}), 404
        
        return send_file(art_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@library_api.route('/tracks/<int:track_id>/thumbnail', methods=['GET'])
def get_track_thumbnail(track_id):
    """
    Get the album art thumbnail for a track.
    
    Returns the thumbnail as a base64-encoded data URL.
    If the track has no thumbnail, returns a 404 error.
    """
    try:
        track = library_manager.get_track_by_id(track_id)
        if not track:
            return jsonify({'error': 'Track not found'}), 404
        
        thumbnail = track.get_thumbnail_base64()
        if not thumbnail:
            return jsonify({'error': 'No thumbnail available for this track'}), 404
        
        return jsonify({'thumbnail': thumbnail})
    except Exception as e:
        return jsonify({'error': str(e)}), 500