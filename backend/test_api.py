"""
Test script for the Flask API.
Run this script to test the API endpoints.
"""
import requests
import json
import time

BASE_URL = 'http://localhost:5000/api'

def test_player_endpoints():
    """Test player API endpoints."""
    print("\n=== Testing Player Endpoints ===")
    
    # Get player status
    print("\nGetting player status...")
    response = requests.get(f"{BASE_URL}/player/status")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    
    # Add your music file path here
    SAMPLE_MUSIC_PATH = "path/to/your/music.mp3"
    
    # Play a track
    print("\nPlaying a track...")
    response = requests.post(
        f"{BASE_URL}/player/play", 
        json={"path": SAMPLE_MUSIC_PATH}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    
    # Wait a moment
    time.sleep(2)
    
    # Pause playback
    print("\nPausing playback...")
    response = requests.post(f"{BASE_URL}/player/pause")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    
    # Wait a moment
    time.sleep(1)
    
    # Resume playback
    print("\nResuming playback...")
    response = requests.post(f"{BASE_URL}/player/resume")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    
    # Wait a moment
    time.sleep(2)
    
    # Set volume
    print("\nSetting volume...")
    response = requests.post(
        f"{BASE_URL}/player/volume", 
        json={"level": 70}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    
    # Wait a moment
    time.sleep(1)
    
    # Stop playback
    print("\nStopping playback...")
    response = requests.post(f"{BASE_URL}/player/stop")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))

def test_library_endpoints():
    """Test library API endpoints."""
    print("\n=== Testing Library Endpoints ===")
    
    # Get tracks
    print("\nGetting tracks...")
    response = requests.get(f"{BASE_URL}/library/tracks")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        # Print only the first 2 tracks to avoid cluttering the output
        tracks = response.json()
        print(f"Found {len(tracks)} tracks.")
        if tracks:
            print("First two tracks:")
            print(json.dumps(tracks[:2], indent=2))
    
    # Scan directory
    MUSIC_DIR = "path/to/your/music"  # Replace with your music directory
    print(f"\nScanning directory: {MUSIC_DIR}...")
    response = requests.post(
        f"{BASE_URL}/library/scan", 
        json={"path": MUSIC_DIR}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    
    # Search for tracks
    SEARCH_QUERY = "your_search_query"  # Replace with your search query
    print(f"\nSearching for: {SEARCH_QUERY}...")
    response = requests.get(f"{BASE_URL}/library/search?query={SEARCH_QUERY}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        tracks = response.json()
        print(f"Found {len(tracks)} matching tracks.")
        if tracks:
            print("First matching track:")
            print(json.dumps(tracks[0], indent=2))

    # Get track thumbnail
    print("\nGetting track thumbnail...")
    # Get the first track ID
    track_id = None
    response = requests.get(f"{BASE_URL}/library/tracks")
    if response.status_code == 200:
        tracks = response.json()
        if tracks:
            track_id = tracks[0].get('id')
    
    if track_id:
        print(f"Testing thumbnail for track ID: {track_id}")
        response = requests.get(f"{BASE_URL}/library/tracks/{track_id}/thumbnail")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'thumbnail' in data:
                thumbnail_preview = data['thumbnail'][:50] + '...' if data['thumbnail'] else None
                print(f"Thumbnail received: {thumbnail_preview}")
            else:
                print("No thumbnail data in response")
        elif response.status_code == 404:
            print("No thumbnail available for this track")
    else:
        print("No tracks available to test thumbnail")

def test_playlist_endpoints():
    """Test playlist API endpoints."""
    print("\n=== Testing Playlist Endpoints ===")
    
    # Get playlists
    print("\nGetting playlists...")
    response = requests.get(f"{BASE_URL}/playlists")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        playlists = response.json()
        print(f"Found {len(playlists)} playlists.")
        if playlists:
            print("Playlists:")
            print(json.dumps(playlists, indent=2))
    
    # Create playlist
    PLAYLIST_NAME = "Test Playlist"
    print(f"\nCreating playlist: {PLAYLIST_NAME}...")
    response = requests.post(
        f"{BASE_URL}/playlists", 
        json={"name": PLAYLIST_NAME}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        playlist = response.json()
        print("Created playlist:")
        print(json.dumps(playlist, indent=2))
        
        # Save playlist ID for further operations
        playlist_id = playlist.get("id")
        if playlist_id:
            # Add track to playlist (you'd need a valid track ID)
            TRACK_ID = "your_track_id"  # Replace with a valid track ID
            print(f"\nAdding track {TRACK_ID} to playlist...")
            response = requests.post(
                f"{BASE_URL}/playlists/{playlist_id}/tracks", 
                json={"track_id": TRACK_ID}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=2))
            
            # Get playlist tracks
            print("\nGetting playlist tracks...")
            response = requests.get(f"{BASE_URL}/playlists/{playlist_id}/tracks")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                tracks = response.json()
                print(f"Found {len(tracks)} tracks in playlist.")
                if tracks:
                    print("Tracks in playlist:")
                    print(json.dumps(tracks, indent=2))
            
            # Delete playlist
            print(f"\nDeleting playlist {playlist_id}...")
            response = requests.delete(f"{BASE_URL}/playlists/{playlist_id}")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    try:
        test_player_endpoints()
        test_library_endpoints()
        test_playlist_endpoints()
        print("\nAll tests completed!")
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server. Make sure it's running at http://localhost:5000")
    except Exception as e:
        print(f"An error occurred: {e}")
