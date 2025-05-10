"""
Lyrics API Endpoints
This module defines the API routes for lyrics retrieval.
"""
from flask import Blueprint, jsonify
from ..lyrics import get_lyrics_for_track

# Create Blueprint
lyrics_api = Blueprint('lyrics_api', __name__)

@lyrics_api.route('/<track_id>', methods=['GET'])
def get_lyrics(track_id):
    """Get lyrics for a track."""
    try:
        lyrics_data = get_lyrics_for_track(track_id)
        if not lyrics_data:
            return jsonify({'error': 'No lyrics found for this track'}), 404
        
        return jsonify(lyrics_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500