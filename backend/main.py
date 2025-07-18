"""
Acoustic Player Main Application
This module serves as the entry point for the Flask API server.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import settings
from app.api import player_api, library_api, playlist_api, lyrics_api
from app.ws import socketio
from app.models.database import init_db, close_db_session

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config.settings')
    
    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})  # NOTE: potential risk for *
    
    # Initialize database
    init_db()
    
    # Register API blueprints
    app.register_blueprint(player_api, url_prefix='/api/player')
    app.register_blueprint(library_api, url_prefix='/api/library')
    app.register_blueprint(playlist_api, url_prefix='/api/playlists')
    app.register_blueprint(lyrics_api, url_prefix='/api/lyrics')
    
    # Register teardown function to close database session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_db_session()
    
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

    # Run the app with Socket.IO using configured host and port
    socketio.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        debug=settings.DEBUG,
    )
