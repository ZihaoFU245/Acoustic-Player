"""
WebSocket Events
This module handles real-time updates via Socket.IO.
"""
from flask_socketio import SocketIO, emit
from ..api.serializers import player_status_schema, track_schema, playlist_schema

# Initialize Socket.IO
socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    # This could log connections or initialize client-specific state
    print("Client connected")
    
@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print("Client disconnected")

def emit_player_status(status):
    """
    Emit player status update to all connected clients.
    
    Args:
        status: Player status dictionary
    """
    socketio.emit('player_status_update', player_status_schema(status))

def emit_library_update():
    """Emit library update notification to all connected clients."""
    socketio.emit('library_update')

def emit_playlist_changed(playlist_id, action, data=None):
    """
    Emit playlist change notification to all connected clients.
    
    Args:
        playlist_id: ID of the changed playlist
        action: The action performed (created, updated, deleted, track_added, track_removed)
        data: Optional additional data (depends on action)
    """
    event_data = {
        'playlist_id': playlist_id,
        'action': action
    }
    
    if data:
        event_data['data'] = data
        
    socketio.emit('playlist_changed', event_data)