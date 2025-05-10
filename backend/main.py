"""
Acoustic Player Main Application
This module serves as the entry point for the Flask API server.
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os
from app.api import player_api, library_api, playlist_api, lyrics_api
from app.ws import socketio

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.settings')
    
    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})  # NOTE: potential risk for *
    
    # Register API blueprints
    app.register_blueprint(player_api, url_prefix='/api/player')
    app.register_blueprint(library_api, url_prefix='/api/library')
    app.register_blueprint(playlist_api, url_prefix='/api/playlists')
    app.register_blueprint(lyrics_api, url_prefix='/api/lyrics')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Initialize WebSocket
    socketio.init_app(app, cors_allowed_origins="*")
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app with Socket.IO
    socketio.run(app, host='0.0.0.0', port=port, debug=True)