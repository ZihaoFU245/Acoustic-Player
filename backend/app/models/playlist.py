"""
Playlist model for managing playlists in the application.

- Create and manage playlists.
- Add, remove, and reorder tracks in playlists.
- Use the MetadataManager to extract metadata and album art for tracks.
- Use the MusicPlayer to play tracks from the playlist.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func
from .database import Playlist, Track, playlist_tracks, get_db_session

class PlaylistManager:
    """
    Manager class for creating and managing playlists.
    """
    def __init__(self):
        self.db_session = get_db_session()
    
    def create_playlist(self, name: str) -> Playlist:
        """
        Create a new playlist.
        
        Args:
            name: Name of the playlist
            
        Returns:
            Created Playlist object
        """
        playlist = Playlist(name=name)
        
        try:
            self.db_session.add(playlist)
            self.db_session.commit()
            return playlist
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Error creating playlist: {str(e)}")
    
    def delete_playlist(self, playlist_id: int) -> bool:
        """
        Delete a playlist.
        
        Args:
            playlist_id: ID of the playlist to delete
            
        Returns:
            True if playlist was deleted, False otherwise
        """
        playlist = self.db_session.query(Playlist).filter_by(id=playlist_id).first()
        
        if not playlist:
            return False
        
        try:
            self.db_session.delete(playlist)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Error deleting playlist: {str(e)}")
    
    def add_track(self, playlist_id: int, track_id: int) -> bool:
        """
        Add a track to a playlist.
        
        Args:
            playlist_id: ID of the playlist
            track_id: ID of the track to add
            
        Returns:
            True if track was added, False otherwise
        """
        playlist = self.db_session.query(Playlist).filter_by(id=playlist_id).first()
        track = self.db_session.query(Track).filter_by(id=track_id).first()
        
        if not playlist or not track:
            return False
        
        # Check if track is already in the playlist
        existing = self.db_session.query(playlist_tracks).filter(
            and_(
                playlist_tracks.c.playlist_id == playlist_id,
                playlist_tracks.c.track_id == track_id
            )
        ).first()
        
        if existing:
            return False
        
        # Get the next position in the playlist
        max_pos_result = self.db_session.query(func.max(playlist_tracks.c.position)).filter(
            playlist_tracks.c.playlist_id == playlist_id
        ).scalar()
        
        next_position = 1 if max_pos_result is None else max_pos_result + 1
        
        try:
            # Insert into playlist_tracks with the next position
            stmt = playlist_tracks.insert().values(
                playlist_id=playlist_id,
                track_id=track_id,
                position=next_position
            )
            self.db_session.execute(stmt)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Error adding track to playlist: {str(e)}")
    
    def remove_track(self, playlist_id: int, track_index: int) -> bool:
        """
        Remove a track from a playlist by its position.
        
        Args:
            playlist_id: ID of the playlist
            track_index: Position of the track in the playlist (0-based)
            
        Returns:
            True if track was removed, False otherwise
        """
        # Adjust track_index to be 1-based (database positions start at 1)
        db_position = track_index + 1
        
        playlist = self.db_session.query(Playlist).filter_by(id=playlist_id).first()
        
        if not playlist:
            return False
        
        try:
            # Find the track at the given position
            track_entry = self.db_session.query(playlist_tracks).filter(
                and_(
                    playlist_tracks.c.playlist_id == playlist_id,
                    playlist_tracks.c.position == db_position
                )
            ).first()
            
            if not track_entry:
                return False
            
            # Delete the track from the playlist
            stmt = playlist_tracks.delete().where(
                and_(
                    playlist_tracks.c.playlist_id == playlist_id,
                    playlist_tracks.c.position == db_position
                )
            )
            self.db_session.execute(stmt)
            
            # Update positions for tracks after the deleted one
            tracks_to_update = self.db_session.query(playlist_tracks).filter(
                and_(
                    playlist_tracks.c.playlist_id == playlist_id,
                    playlist_tracks.c.position > db_position
                )
            ).all()
            
            for track in tracks_to_update:
                update_stmt = playlist_tracks.update().where(
                    and_(
                        playlist_tracks.c.playlist_id == playlist_id,
                        playlist_tracks.c.track_id == track.track_id,
                        playlist_tracks.c.position == track.position
                    )
                ).values(position=track.position - 1)
                self.db_session.execute(update_stmt)
            
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise RuntimeError(f"Error removing track from playlist: {str(e)}")
    
    def get_playlist_tracks(self, playlist_id: int) -> List[Track]:
        """
        Get all tracks in a playlist.
        
        Args:
            playlist_id: ID of the playlist
            
        Returns:
            List of Track objects in the playlist
        """
        playlist = self.db_session.query(Playlist).filter_by(id=playlist_id).first()
        
        if not playlist:
            return []
        
        return playlist.tracks
    
    def list_playlists(self) -> List[Playlist]:
        """
        List all playlists.
        
        Returns:
            List of Playlist objects
        """
        return self.db_session.query(Playlist).all()