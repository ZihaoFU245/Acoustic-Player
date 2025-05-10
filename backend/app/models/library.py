"""
Library Manager module for managing audio track library.
"""
import os
import glob
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from config import settings
from .database import Track, get_db_session
from .metadata import MetadataManager

class LibraryManager:
    """
    Library manager class for scanning directories and managing tracks.
    """
    def __init__(self):
        self.db_session = get_db_session()
        self.metadata_manager = MetadataManager()
    
    def scan_directory(self, path: str) -> Dict[str, int]:
        """
        Scan a directory recursively for audio files and add them to the database.
        
        Args:
            path: Directory path to scan
            
        Returns:
            Dictionary with counts of tracks added and updated
        """
        if not os.path.isdir(path):
            raise ValueError(f"Invalid directory path: {path}")
        
        # Get list of supported audio file extensions
        extensions = settings.ALLOWED_EXTENSIONS
        
        # Track statistics
        stats = {
            "tracks_added": 0,
            "tracks_updated": 0
        }
        
        # Scan directory recursively for audio files
        for ext in extensions:
            for file_path in glob.glob(os.path.join(path, f"**/*.{ext}"), recursive=True):
                try:
                    # Check if file already exists in database
                    existing_track = self.db_session.query(Track).filter_by(path=file_path).first()
                    
                    # Read metadata from file
                    metadata = self.metadata_manager.read_tags(file_path)
                    
                    # Extract album art and thumbnail
                    album_art_path, thumbnail_data = self.metadata_manager.extract_embedded_art(file_path)
                    
                    if existing_track:
                        # Update existing track
                        existing_track.title = metadata.get('title', os.path.basename(file_path))
                        existing_track.artist = metadata.get('artist', 'Unknown Artist')
                        existing_track.album = metadata.get('album', 'Unknown Album')
                        existing_track.duration = metadata.get('duration', 0)
                        existing_track.track_num = metadata.get('track_num', 0)
                        existing_track.genre = metadata.get('genre', '')
                        existing_track.year = metadata.get('year', None)
                        
                        # Update album art if available
                        if album_art_path:
                            existing_track.album_art_path = album_art_path
                        if thumbnail_data:
                            existing_track.album_art_thumbnail = thumbnail_data
                            
                        stats["tracks_updated"] += 1
                    else:
                        # Create new track
                        track = Track(
                            path=file_path,
                            title=metadata.get('title', os.path.basename(file_path)),
                            artist=metadata.get('artist', 'Unknown Artist'),
                            album=metadata.get('album', 'Unknown Album'),
                            duration=metadata.get('duration', 0),
                            track_num=metadata.get('track_num', 0),
                            genre=metadata.get('genre', ''),
                            year=metadata.get('year', None),
                            album_art_path=album_art_path,
                            album_art_thumbnail=thumbnail_data
                        )
                        self.db_session.add(track)
                        stats["tracks_added"] += 1
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")
                    continue
        
        # Commit changes to database
        try:
            self.db_session.commit()
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")
        
        return stats
    
    def get_tracks(self, sort_by: str = 'title', filter: str = '') -> List[Track]:
        """
        Get tracks from the database with optional sorting and filtering.
        
        Args:
            sort_by: Field to sort by (title, artist, album, duration)
            filter: Optional filter string to search in title, artist, album
            
        Returns:
            List of Track objects
        """
        query = self.db_session.query(Track)
        
        # Apply filter if provided
        if filter:
            filter_query = f"%{filter}%"
            query = query.filter(
                (Track.title.ilike(filter_query)) |
                (Track.artist.ilike(filter_query)) |
                (Track.album.ilike(filter_query))
            )
        
        # Apply sorting
        if sort_by == 'title':
            query = query.order_by(Track.title)
        elif sort_by == 'artist':
            query = query.order_by(Track.artist)
        elif sort_by == 'album':
            query = query.order_by(Track.album)
        elif sort_by == 'duration':
            query = query.order_by(Track.duration)
        
        return query.all()
    
    def search_tracks(self, query: str) -> List[Track]:
        """
        Search for tracks by title, artist, or album.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching Track objects
        """
        if not query:
            return []
        
        search_query = f"%{query}%"
        results = self.db_session.query(Track).filter(
            (Track.title.ilike(search_query)) |
            (Track.artist.ilike(search_query)) |
            (Track.album.ilike(search_query))
        ).all()
        
        return results
    
    def get_album_art(self, track_id: int) -> Optional[str]:
        """
        Get album art file path for a track.
        
        Args:
            track_id: ID of the track
            
        Returns:
            Path to album art file or None if not found
        """
        track = self.db_session.query(Track).filter_by(id=track_id).first()
        
        if not track:
            return None
        
        # If we already have album art path stored, return it
        if track.album_art_path and os.path.exists(track.album_art_path):
            return track.album_art_path
        
        # Try to extract album art from the audio file
        try:
            art_path = self.metadata_manager.extract_embedded_art(track.path)
            if art_path:
                track.album_art_path = art_path
                self.db_session.commit()
                return art_path
        except Exception as e:
            print(f"Error extracting album art: {str(e)}")
        
        return None
    
    def get_track_details(self, track_id: int) -> Optional[Track]:
        """
        Get detailed information for a track.
        
        Args:
            track_id: ID of the track
            
        Returns:
            Track object or None if not found
        """
        return self.db_session.query(Track).filter_by(id=track_id).first()
    
    def add_track_to_db(self, track_metadata: Dict[str, Any]) -> Track:
        """
        Add a track to the database.
        
        Args:
            track_metadata: Dictionary containing track metadata
            
        Returns:
            Added Track object
        """
        # Check if the file already exists in the database
        existing_track = self.db_session.query(Track).filter_by(path=track_metadata['path']).first()
        
        if existing_track:
            return existing_track
        
        track = Track(
            path=track_metadata['path'],
            title=track_metadata.get('title', os.path.basename(track_metadata['path'])),
            artist=track_metadata.get('artist', 'Unknown Artist'),
            album=track_metadata.get('album', 'Unknown Album'),
            duration=track_metadata.get('duration', 0),
            track_num=track_metadata.get('track_num', 0),
            genre=track_metadata.get('genre', ''),
            year=track_metadata.get('year', None)
        )
        
        self.db_session.add(track)
        self.db_session.commit()
        
        return track

    def get_track_by_id(self, track_id: int) -> Optional[Track]:
        """
        Get a track by its ID.
        
        Args:
            track_id: ID of the track to retrieve
            
        Returns:
            Track object or None if not found
        """
        return self.db_session.query(Track).filter_by(id=track_id).first()