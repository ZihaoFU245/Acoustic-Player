"""
Player API Endpoints
This module defines the API routes for player controls.
"""
# NOTE: This code is reviewed
from flask import Blueprint, request, jsonify
from ..services.audio_service import AudioService
from .serializers import player_status_schema
from ..ws.events import emit_player_status

# Create Blueprint
player_api = Blueprint('player_api', __name__)

# Initialize global audio service instance
audio_service = AudioService()

@player_api.route('/status', methods=['GET'])
def get_status():
    """Get current player status."""
    status = audio_service.status()
    return jsonify(player_status_schema(status))

@player_api.route('/play', methods=['POST'])
def play_track():
    """Play a track from given path."""
    data = request.json
    if not data or 'path' not in data:
        return jsonify({'error': 'Path is required'}), 400
    
    try:
        status = audio_service.play(data['path'])
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@player_api.route('/pause', methods=['POST'])
def pause_playback():
    """Pause current playback."""
    try:
        status = audio_service.pause()
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@player_api.route('/resume', methods=['POST'])
def resume_playback():
    """Resume paused playback."""
    try:
        status = audio_service.resume()
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@player_api.route('/stop', methods=['POST'])
def stop_playback():
    """Stop current playback."""
    try:
        status = audio_service.stop()
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@player_api.route('/seek', methods=['POST'])
def seek_position():
    """Seek to a position in the current track."""
    data = request.json
    if not data or 'position' not in data:
        return jsonify({'error': 'Position is required'}), 400
    
    try:
        status = audio_service.seek(data['position'])
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@player_api.route('/volume', methods=['POST'])
def set_volume():
    """Set the player volume."""
    data = request.json
    if not data or 'level' not in data:
        return jsonify({'error': 'Volume level is required'}), 400
    
    try:
        status = audio_service.set_volume(data['level'])
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500