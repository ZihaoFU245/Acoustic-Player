"""
Player API Endpoints
This module defines the API routes for player controls.
"""
# NOTE: This code is reviewed
from flask import Blueprint, request, jsonify
from ..models.player import MusicPlayer
from .serializers import player_status_schema
from ..ws.events import emit_player_status

# Create Blueprint
player_api = Blueprint('player_api', __name__)

# Initialize global player instance
player = MusicPlayer()

@player_api.route('/status', methods=['GET'])
def get_status():
    """Get current player status."""
    status = player.get_status()
    return jsonify(player_status_schema(status))

@player_api.route('/play', methods=['POST'])
def play_track():
    """Play a track from given path."""
    data = request.json
    if not data or 'path' not in data:
        return jsonify({'error': 'Path is required'}), 400
    
    try:
        player.play(data['path'])
        status = player.get_status()
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@player_api.route('/pause', methods=['POST'])
def pause_playback():
    """Pause current playback."""
    try:
        player.pause()
        status = player.get_status()
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@player_api.route('/resume', methods=['POST'])
def resume_playback():
    """Resume paused playback."""
    try:
        player.resume()
        status = player.get_status()
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@player_api.route('/stop', methods=['POST'])
def stop_playback():
    """Stop current playback."""
    try:
        player.stop()
        status = player.get_status()
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
        player.seek(data['position'])
        status = player.get_status()
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
        player.set_volume(data['level'])
        status = player.get_status()
        # Emit WebSocket event
        emit_player_status(status)
        return jsonify(player_status_schema(status))
    except Exception as e:
        return jsonify({'error': str(e)}), 500