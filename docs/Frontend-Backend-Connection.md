# Connecting Frontend to Backend in Acoustic Player

This document explains how to connect the Electron.js frontend to the Flask backend in the Acoustic Player application.

## Architecture Overview

The Acoustic Player follows a client-server architecture:

1. **Backend (Server)**: A Flask application that provides REST APIs and WebSocket endpoints for player controls, library management, playlists, and lyrics.

2. **Frontend (Client)**: An Electron.js application that presents the user interface and communicates with the backend using HTTP requests and WebSockets.

## Setup Steps

### 1. Start the Backend Server

First, ensure the Flask backend server is running:

```bash
cd backend
python main.py
```

By default, the server runs on `http://localhost:5000`.

### 2. Connect from Frontend

In your Electron.js application, use the provided `api.js` module to communicate with the backend:

```javascript
// In your Electron renderer process
const { initApi } = require('./js/api.js');

// Initialize the API and get API handlers
const { playerApi, libraryApi, playlistApi, lyricsApi, socket } = initApi();

// Now you can use the API handlers to interact with the backend
async function exampleUsage() {
  try {
    // Get player status
    const status = await playerApi.getStatus();
    console.log('Player status:', status);
    
    // Play a track
    await playerApi.play('/path/to/track.mp3');
    
    // Get library tracks
    const tracks = await libraryApi.getTracks();
    console.log(`Found ${tracks.length} tracks in library`);
    
    // Create a playlist
    const playlist = await playlistApi.createPlaylist('My Playlist');
    console.log('Created playlist:', playlist);
    
    // Add a track to the playlist
    await playlistApi.addTrackToPlaylist(playlist.id, tracks[0].id);
    
    // Get lyrics for a track
    const lyrics = await lyricsApi.getLyrics(tracks[0].id);
    if (lyrics) {
      console.log('Found lyrics:', lyrics);
    } else {
      console.log('No lyrics found for this track');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### 3. Listen for Real-Time Updates

The API client automatically sets up WebSocket listeners. You can listen for these events in your frontend code:

```javascript
// Listen for player status updates
window.addEventListener('player-status-update', (event) => {
  const playerStatus = event.detail;
  console.log('Player status updated:', playerStatus);
  
  // Update UI based on player status
  updatePlayerUI(playerStatus);
});

// Listen for library updates
window.addEventListener('library-update', () => {
  console.log('Library updated');
  
  // Refresh library view
  refreshLibraryView();
});

// Listen for playlist changes
window.addEventListener('playlist-changed', (event) => {
  const playlistChange = event.detail;
  console.log('Playlist changed:', playlistChange);
  
  // Refresh playlist view
  refreshPlaylistView();
});
```

## Frontend Components that Interact with Backend

Here's how different frontend components interact with the backend:

### Player Controls (`ui/playerControls.js`)

```javascript
const { playerApi } = require('../api.js');

// Play button click handler
playButton.addEventListener('click', async () => {
  if (isPlaying) {
    await playerApi.pause();
  } else {
    await playerApi.resume();
  }
});

// Next button click handler
nextButton.addEventListener('click', async () => {
  // Logic to get next track
  const nextTrack = getNextTrack();
  await playerApi.play(nextTrack.path);
});

// Volume control change handler
volumeSlider.addEventListener('change', async (event) => {
  await playerApi.setVolume(event.target.value);
});
```

### Seek Bar (`ui/seekBar.js`)

```javascript
const { playerApi } = require('../api.js');

// Update seek bar based on player status
function updateSeekBar(playerStatus) {
  seekBar.value = playerStatus.position;
  seekBar.max = playerStatus.duration;
  currentTimeElement.textContent = formatTime(playerStatus.position);
  durationElement.textContent = formatTime(playerStatus.duration);
}

// Seek bar change handler
seekBar.addEventListener('change', async (event) => {
  await playerApi.seek(parseInt(event.target.value));
});

// Listen for player status updates
window.addEventListener('player-status-update', (event) => {
  updateSeekBar(event.detail);
});
```

### Library View (`ui/playlistView.js`)

```javascript
const { libraryApi, playerApi } = require('../api.js');

// Load library tracks
async function loadLibraryTracks() {
  try {
    const tracks = await libraryApi.getTracks();
    displayTracks(tracks);
  } catch (error) {
    console.error('Error loading library tracks:', error);
  }
}

// Track selection handler
function onTrackSelected(track) {
  playerApi.play(track.path);
}

// Scan button click handler
scanButton.addEventListener('click', async () => {
  try {
    const result = await libraryApi.scanDirectory(musicFolderInput.value);
    console.log('Scan result:', result);
  } catch (error) {
    console.error('Error scanning directory:', error);
  }
});
```

### Playlist Management

```javascript
const { playlistApi, playerApi } = require('../api.js');

// Load playlists
async function loadPlaylists() {
  try {
    const playlists = await playlistApi.getPlaylists();
    displayPlaylists(playlists);
  } catch (error) {
    console.error('Error loading playlists:', error);
  }
}

// Create playlist button click handler
createPlaylistButton.addEventListener('click', async () => {
  try {
    const playlist = await playlistApi.createPlaylist(playlistNameInput.value);
    console.log('Created playlist:', playlist);
  } catch (error) {
    console.error('Error creating playlist:', error);
  }
});
```

## Error Handling

It's important to handle errors gracefully in the frontend:

```javascript
async function performAction() {
  try {
    // API call
    const result = await playerApi.play(track.path);
    // Update UI based on result
    updateUI(result);
  } catch (error) {
    // Show error to user
    showErrorNotification('Failed to play track: ' + error.message);
    // Log detailed error
    console.error('Error playing track:', error);
  }
}
```

## Next Steps

1. Implement proper state management in the frontend (using a library like Redux or a simple state object)
2. Build UI components that update based on the backend state
3. Add error handling and loading states for async operations
4. Implement offline mode handling for situations when the backend is unreachable
