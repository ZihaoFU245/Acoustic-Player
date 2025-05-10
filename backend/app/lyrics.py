

"""
Lyrics Management
This module handles finding and parsing lyrics for music tracks.
"""
import os
import json
from .models.metadata import MetadataManager

class LyricsManager:
    """
    A class to manage and display lyrics for the music player.

    Plannings:
    * Basics:
        - Display lyrics in sync with the music playback.
        - Read lyrics files: lrc, txt, srt, etc.
        - Use a library like `lyricsgenius` or `musixmatch` to fetch lyrics

    * Advanced:
        - Support for multiple languages and formats.
        - Display lyrics in a separate window or overlay. // TODO: Implement this in the UI layer.
        - Enable searching for lyrics using the song title and artist name, or use lyrics to search for the song.
        - Save fetched lyrics to a local file for offline access.
    
    * IDEAS:
        - Use OpenAI's Whisper API or OpenAI Whisper Library to transcribe lyrics from audio files.
        - Use a machine learning model to identify the song from the lyrics.
    """
    def __init__(self, lyrics_dir=None):
        """
        Initialize the lyrics manager.
        
        Args:
            lyrics_dir: Directory where lyrics files are stored
        """
        self.lyrics_dir = lyrics_dir
        self.metadata_manager = MetadataManager()
    
    def find_lrc_file(self, audio_path):
        """
        Find a LRC file for the given audio file.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Path to the LRC file if found, None otherwise
        """
        if not audio_path:
            return None
            
        # Try looking for a file with the same name but .lrc extension
        base_path = os.path.splitext(audio_path)[0]
        lrc_path = base_path + '.lrc'
        
        if os.path.exists(lrc_path):
            return lrc_path
            
        # If lyrics_dir is specified, look there using the audio filename
        if self.lyrics_dir:
            audio_filename = os.path.basename(base_path)
            potential_lrc = os.path.join(self.lyrics_dir, audio_filename + '.lrc')
            
            if os.path.exists(potential_lrc):
                return potential_lrc
                
        return None
    
    def parse_lrc(self, lrc_content):
        """
        Parse LRC file content into a structured format.
        
        Args:
            lrc_content: String content of an LRC file
            
        Returns:
            Dictionary with metadata and timed lyrics
        """
        if not lrc_content:
            return {'metadata': {}, 'lines': []}
            
        lines = lrc_content.strip().split('\n')
        result = {
            'metadata': {},
            'lines': []
        }
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Parse metadata tags (e.g., [ar:Artist])
            if line.startswith('[') and ':' in line and ']' in line:
                tag_end = line.find(']')
                tag = line[1:line.find(':')]
                value = line[line.find(':')+1:tag_end]
                
                if tag not in ['00', '01', '02'] and not tag.replace('.', '').isdigit():
                    result['metadata'][tag] = value
                    continue
            
            # Parse timed lyrics
            time_tags = []
            remaining_line = line
            
            while remaining_line.startswith('[') and ']' in remaining_line:
                tag_end = remaining_line.find(']')
                potential_time = remaining_line[1:tag_end]
                
                # Check if this tag looks like a timestamp
                if ':' in potential_time and potential_time.replace(':', '').replace('.', '').isdigit():
                    try:
                        # Parse time format [mm:ss.xx]
                        minutes, seconds = potential_time.split(':')
                        total_seconds = int(minutes) * 60 + float(seconds)
                        time_tags.append(total_seconds * 1000)  # Convert to milliseconds
                        
                        remaining_line = remaining_line[tag_end+1:]
                    except ValueError:
                        break
                else:
                    break
            
            # If we found timestamps and have text remaining, add as a lyric line
            if time_tags and remaining_line:
                for time_ms in time_tags:
                    result['lines'].append({
                        'time': time_ms,
                        'text': remaining_line.strip()
                    })
        
        # Sort lines by timestamp
        result['lines'].sort(key=lambda x: x['time'])
        
        return result
    def get_lyrics_for_track(self, track_id):
        """
        Get lyrics for a track.
        
        Args:
            track_id: Track ID or path
            
        Returns:
            Dictionary with lyrics data or None if not found
        """
        from .models.library import LibraryManager
        
        # Get track details from library
        library = LibraryManager()
        track = library.get_track_details(track_id)
        
        if not track:
            return None
            
        track_path = track.get('path') if isinstance(track, dict) else getattr(track, 'path', None)
        
        if not track_path:
            return None
            
        # First, check if the audio file has embedded lyrics
        try:
            embedded_lyrics = self.metadata_manager.read_tags(track_path).get('lyrics')
            if embedded_lyrics:
                return {
                    'type': 'plain',
                    'source': 'embedded',
                    'content': embedded_lyrics
                }
        except Exception as e:
            print(f"Error reading embedded lyrics: {e}")
            
        # Next, look for an LRC file
        lrc_path = self.find_lrc_file(track_path)
        if lrc_path:
            try:
                with open(lrc_path, 'r', encoding='utf-8') as f:
                    lrc_content = f.read()
                    
                parsed_lrc = self.parse_lrc(lrc_content)
                return {
                    'type': 'synchronized',
                    'source': 'lrc_file',
                    'content': parsed_lrc
                }
            except Exception as e:
                print(f"Error reading LRC file: {e}")
                
        # TODO: If no local lyrics found, could try fetching from an online service
                
        return None

# Create a singleton instance for the application
lyrics_manager = LyricsManager()

def get_lyrics_for_track(track_id):
    """
    Get lyrics for a track.
    
    Args:
        track_id: Track ID or path
    
    Returns:
        Dictionary with lyrics data or None if not found
    """
    return lyrics_manager.get_lyrics_for_track(track_id)