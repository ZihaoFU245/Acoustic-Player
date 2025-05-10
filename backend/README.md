# Acoustic Player Backend

This directory contains the backend code for the Acoustic Player application, which is built using Flask.

## Project Structure

- `main.py` - The main entry point for the Flask application
- `app/` - Core application logic
  - `models/` - Data & Business Logic (Model)
  - `api/` - API Endpoints (ViewModel)
  - `ws/` - WebSocket handling
  - `services/` - Business logic services
- `config/` - Configuration files
- `tests/` - Unit/Integration tests

## Setup and Installation

### Prerequisites

- Python 3.8+ installed
- pip (Python package manager)

### Installation Steps

1. Create and activate a virtual environment (recommended):

```
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```
pip install -r requirements.txt
```

## Running the Application

To run the application in development mode:

```
python main.py
```

This will start the Flask server on the configured host and port (default: http://localhost:5000).

## API Endpoints

### Player Controls

- `GET /api/player/status` - Get current player status
- `POST /api/player/play` - Play a track
- `POST /api/player/pause` - Pause current playback
- `POST /api/player/resume` - Resume paused playback
- `POST /api/player/stop` - Stop current playback
- `POST /api/player/seek` - Seek to a position in current track
- `POST /api/player/volume` - Set volume level

### Library Management

- `GET /api/library/tracks` - List all tracks in the library
- `POST /api/library/scan` - Scan a directory for audio files
- `GET /api/library/search` - Search for tracks
- `GET /api/library/tracks/{track_id}/thumbnail` - Get album art thumbnail as base64 data

### Playlist Management

- `GET /api/playlists` - List all playlists
- `POST /api/playlists` - Create a new playlist
- `DELETE /api/playlists/{playlist_id}` - Delete a playlist
- `GET /api/playlists/{playlist_id}/tracks` - List all tracks in a playlist
- `POST /api/playlists/{playlist_id}/tracks` - Add a track to a playlist
- `DELETE /api/playlists/{playlist_id}/tracks/{track_index}` - Remove a track from a playlist

### Lyrics

- `GET /api/lyrics/{track_id}` - Get lyrics for a track

## WebSocket Events

The application uses Socket.IO for real-time updates. The following events are emitted:

- `player_status_update` - Emitted when player status changes
- `library_update` - Emitted when library is updated
- `playlist_changed` - Emitted when a playlist is created, updated, or deleted

## Album Art Storage

The backend implements a hybrid approach for album art storage:

- Full-size album art is stored on the filesystem (in `~/.acoustic_player/album_art` by default)
- Thumbnail versions (150px) are stored directly in the database for efficient loading

This provides both performance benefits (fast loading of thumbnails) and optimal resource usage 
(large files kept out of database). See `docs/Album-Art-Strategy.md` for more details.

## Testing

To run the included API tests:

```
python test_api.py
```

To run the unit tests:

```
pytest
```
