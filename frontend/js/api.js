/**
 * API Client for communicating with the backend
 * This module provides functions to interact with the Flask API
 */

// Base URL for the API
const API_BASE_URL = 'http://localhost:5000/api';

// Socket.IO instance for real-time updates
let socket = null;

/**
 * Initialize the API client and WebSocket connection
 */
export function initApi() {
  // Import Socket.IO client library
  const { io } = require('socket.io-client');
  
  // Connect to WebSocket server
  socket = io('http://localhost:5000', {
    transports: ['websocket'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionAttempts: 5
  });
  
  // Setup socket event listeners
  setupSocketListeners();
  
  return {
    socket,
    playerApi,
    libraryApi,
    playlistApi,
    lyricsApi
  };
}

/**
 * Set up event listeners for WebSocket events
 */
function setupSocketListeners() {
  if (!socket) return;
  
  socket.on('connect', () => {
    console.log('Connected to server');
  });
  
  socket.on('disconnect', () => {
    console.log('Disconnected from server');
  });
  
  socket.on('player_status_update', (status) => {
    // Update frontend state when player status changes
    window.dispatchEvent(new CustomEvent('player-status-update', { detail: status }));
  });
  
  socket.on('library_update', () => {
    console.log('Library updated');
    // Trigger library refresh
    window.dispatchEvent(new CustomEvent('library-update'));
  });
  
  socket.on('playlist_changed', (data) => {
    console.log('Playlist changed:', data);
    // Trigger playlist refresh
    window.dispatchEvent(new CustomEvent('playlist-changed', { detail: data }));
  });
}

/**
 * Player API functions
 */
export const playerApi = {
  /**
   * Get the current player status
   * @returns {Promise} Promise resolving to player status object
   */
  async getStatus() {
    try {
      const response = await fetch(`${API_BASE_URL}/player/status`);
      if (!response.ok) throw new Error('Failed to get player status');
      return await response.json();
    } catch (error) {
      console.error('Error getting player status:', error);
      throw error;
    }
  },
  
  /**
   * Play a track
   * @param {string} path - Path to the audio file
   * @returns {Promise} Promise resolving to player status object
   */
  async play(path) {
    try {
      const response = await fetch(`${API_BASE_URL}/player/play`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path })
      });
      if (!response.ok) throw new Error('Failed to play track');
      return await response.json();
    } catch (error) {
      console.error('Error playing track:', error);
      throw error;
    }
  },
  
  /**
   * Pause playback
   * @returns {Promise} Promise resolving to player status object
   */
  async pause() {
    try {
      const response = await fetch(`${API_BASE_URL}/player/pause`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error('Failed to pause playback');
      return await response.json();
    } catch (error) {
      console.error('Error pausing playback:', error);
      throw error;
    }
  },
  
  /**
   * Resume playback
   * @returns {Promise} Promise resolving to player status object
   */
  async resume() {
    try {
      const response = await fetch(`${API_BASE_URL}/player/resume`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error('Failed to resume playback');
      return await response.json();
    } catch (error) {
      console.error('Error resuming playback:', error);
      throw error;
    }
  },
  
  /**
   * Stop playback
   * @returns {Promise} Promise resolving to player status object
   */
  async stop() {
    try {
      const response = await fetch(`${API_BASE_URL}/player/stop`, {
        method: 'POST'
      });
      if (!response.ok) throw new Error('Failed to stop playback');
      return await response.json();
    } catch (error) {
      console.error('Error stopping playback:', error);
      throw error;
    }
  },
  
  /**
   * Seek to a position in the current track
   * @param {number} position - Position in milliseconds
   * @returns {Promise} Promise resolving to player status object
   */
  async seek(position) {
    try {
      const response = await fetch(`${API_BASE_URL}/player/seek`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ position })
      });
      if (!response.ok) throw new Error('Failed to seek');
      return await response.json();
    } catch (error) {
      console.error('Error seeking:', error);
      throw error;
    }
  },
  
  /**
   * Set the volume level
   * @param {number} level - Volume level (0-100)
   * @returns {Promise} Promise resolving to player status object
   */
  async setVolume(level) {
    try {
      const response = await fetch(`${API_BASE_URL}/player/volume`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level })
      });
      if (!response.ok) throw new Error('Failed to set volume');
      return await response.json();
    } catch (error) {
      console.error('Error setting volume:', error);
      throw error;
    }
  }
};

/**
 * Library API functions
 */
export const libraryApi = {
  /**
   * Get all tracks in the library
   * @param {string} sortBy - Sort by field
   * @param {string} filter - Filter string
   * @returns {Promise} Promise resolving to array of tracks
   */
  async getTracks(sortBy = 'title', filter = '') {
    try {
      const url = new URL(`${API_BASE_URL}/library/tracks`);
      if (sortBy) url.searchParams.append('sort_by', sortBy);
      if (filter) url.searchParams.append('filter', filter);
      
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to get library tracks');
      return await response.json();
    } catch (error) {
      console.error('Error getting library tracks:', error);
      throw error;
    }
  },
  
  /**
   * Scan a directory for audio files
   * @param {string} path - Directory path to scan
   * @returns {Promise} Promise resolving to scan results
   */
  async scanDirectory(path) {
    try {
      const response = await fetch(`${API_BASE_URL}/library/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path })
      });
      if (!response.ok) throw new Error('Failed to scan directory');
      return await response.json();
    } catch (error) {
      console.error('Error scanning directory:', error);
      throw error;
    }
  },
  
  /**
   * Search for tracks in the library
   * @param {string} query - Search query
   * @returns {Promise} Promise resolving to array of matching tracks
   */
  async searchTracks(query) {
    try {
      const url = new URL(`${API_BASE_URL}/library/search`);
      url.searchParams.append('query', query);
      
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to search tracks');
      return await response.json();
    } catch (error) {
      console.error('Error searching tracks:', error);
      throw error;
    }
  },
  
  /**
   * Get the URL for album art
   * @param {string} trackId - Track ID
   * @returns {string} URL for album art
   */
  getAlbumArtUrl(trackId) {
    return `${API_BASE_URL}/library/art/${trackId}`;
  }
};

/**
 * Playlist API functions
 */
export const playlistApi = {
  /**
   * Get all playlists
   * @returns {Promise} Promise resolving to array of playlists
   */
  async getPlaylists() {
    try {
      const response = await fetch(`${API_BASE_URL}/playlists`);
      if (!response.ok) throw new Error('Failed to get playlists');
      return await response.json();
    } catch (error) {
      console.error('Error getting playlists:', error);
      throw error;
    }
  },
  
  /**
   * Create a new playlist
   * @param {string} name - Playlist name
   * @returns {Promise} Promise resolving to created playlist object
   */
  async createPlaylist(name) {
    try {
      const response = await fetch(`${API_BASE_URL}/playlists`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      });
      if (!response.ok) throw new Error('Failed to create playlist');
      return await response.json();
    } catch (error) {
      console.error('Error creating playlist:', error);
      throw error;
    }
  },
  
  /**
   * Delete a playlist
   * @param {string} playlistId - Playlist ID
   * @returns {Promise} Promise resolving to delete result
   */
  async deletePlaylist(playlistId) {
    try {
      const response = await fetch(`${API_BASE_URL}/playlists/${playlistId}`, {
        method: 'DELETE'
      });
      if (!response.ok) throw new Error('Failed to delete playlist');
      return await response.json();
    } catch (error) {
      console.error('Error deleting playlist:', error);
      throw error;
    }
  },
  
  /**
   * Get tracks in a playlist
   * @param {string} playlistId - Playlist ID
   * @returns {Promise} Promise resolving to array of tracks
   */
  async getPlaylistTracks(playlistId) {
    try {
      const response = await fetch(`${API_BASE_URL}/playlists/${playlistId}/tracks`);
      if (!response.ok) throw new Error('Failed to get playlist tracks');
      return await response.json();
    } catch (error) {
      console.error('Error getting playlist tracks:', error);
      throw error;
    }
  },
  
  /**
   * Add a track to a playlist
   * @param {string} playlistId - Playlist ID
   * @param {string} trackId - Track ID
   * @returns {Promise} Promise resolving to result
   */
  async addTrackToPlaylist(playlistId, trackId) {
    try {
      const response = await fetch(`${API_BASE_URL}/playlists/${playlistId}/tracks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ track_id: trackId })
      });
      if (!response.ok) throw new Error('Failed to add track to playlist');
      return await response.json();
    } catch (error) {
      console.error('Error adding track to playlist:', error);
      throw error;
    }
  },
  
  /**
   * Remove a track from a playlist
   * @param {string} playlistId - Playlist ID
   * @param {number} trackIndex - Track index in playlist
   * @returns {Promise} Promise resolving to result
   */
  async removeTrackFromPlaylist(playlistId, trackIndex) {
    try {
      const response = await fetch(`${API_BASE_URL}/playlists/${playlistId}/tracks/${trackIndex}`, {
        method: 'DELETE'
      });
      if (!response.ok) throw new Error('Failed to remove track from playlist');
      return await response.json();
    } catch (error) {
      console.error('Error removing track from playlist:', error);
      throw error;
    }
  }
};

/**
 * Lyrics API functions
 */
export const lyricsApi = {
  /**
   * Get lyrics for a track
   * @param {string} trackId - Track ID
   * @returns {Promise} Promise resolving to lyrics object
   */
  async getLyrics(trackId) {
    try {
      const response = await fetch(`${API_BASE_URL}/lyrics/${trackId}`);
      if (response.status === 404) return null; // No lyrics found
      if (!response.ok) throw new Error('Failed to get lyrics');
      return await response.json();
    } catch (error) {
      console.error('Error getting lyrics:', error);
      throw error;
    }
  }
};
