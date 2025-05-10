"""
Database models and configuration for the Acoustic Player application.
This module sets up SQLAlchemy ORM models for tracks, playlists, and playlist tracks.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, create_engine, event, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
import os
from config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URI, connect_args={"check_same_thread": False})
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

# Define many-to-many relationship between playlists and tracks
playlist_tracks = Table(
    'playlist_tracks',
    Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id'), primary_key=True),
    Column('track_id', Integer, ForeignKey('tracks.id'), primary_key=True),
    Column('position', Integer, nullable=False)
)

class Track(Base):
    """Track model representing an audio file in the library."""
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    path = Column(String(255), unique=True, nullable=False)
    title = Column(String(255), nullable=True)
    artist = Column(String(255), nullable=True)
    album = Column(String(255), nullable=True)
    duration = Column(Float, nullable=True)  # Duration in seconds
    track_num = Column(Integer, nullable=True)
    genre = Column(String(255), nullable=True)
    year = Column(Integer, nullable=True)
    album_art_path = Column(String(255), nullable=True)  # Path to full-size album art file
    album_art_thumbnail = Column(LargeBinary, nullable=True)  # Small thumbnail stored directly in DB
    
    # Relationship: a track can be in multiple playlists
    playlists = relationship(
        "Playlist", 
        secondary=playlist_tracks,
        back_populates="tracks"
    )
    def to_dict(self):
        """Convert track to dictionary for serialization."""
        return {
            'id': self.id,
            'path': self.path,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'duration': self.duration,
            'track_num': self.track_num,
            'genre': self.genre,
            'year': self.year,
            'album_art_path': self.album_art_path,
            'has_thumbnail': self.album_art_thumbnail is not None
        }
        
    def get_thumbnail_base64(self):
        """
        Get the album art thumbnail as a base64-encoded string.
        
        Returns:
            String: Base64-encoded thumbnail data with image/jpeg mime type prefix,
                   or None if no thumbnail exists
        """
        if self.album_art_thumbnail:
            import base64
            b64_data = base64.b64encode(self.album_art_thumbnail).decode('utf-8')
            return f"data:image/jpeg;base64,{b64_data}"
        return None

class Playlist(Base):
    """Playlist model representing a collection of tracks."""
    __tablename__ = 'playlists'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    
    # Relationship: a playlist has multiple tracks
    tracks = relationship(
        "Track", 
        secondary=playlist_tracks,
        back_populates="playlists",
        order_by=playlist_tracks.c.position
    )
    
    @property
    def track_count(self):
        """Get number of tracks in the playlist."""
        return len(self.tracks)
    
    def to_dict(self):
        """Convert playlist to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'track_count': self.track_count
        }

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """Get a database session."""
    return db_session

def close_db_session():
    """Close the database session."""
    db_session.remove()

# Create database file directory if it doesn't exist
@event.listens_for(engine, "connect")
def _connect(dbapi_connection, connection_record):
    db_path = settings.DATABASE_URI.replace('sqlite:///', '')
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)