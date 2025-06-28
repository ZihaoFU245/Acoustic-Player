"""
Module for managing metadata of audio files.

Use in the Acoustic Player Application:
- Read metadata in a provided/imported audio folder.
- Extract album art and duration from audio files.
- Save them in a JSON file as Cache.
"""
# NOTE: Reviewed
import os
import logging
import io
from PIL import Image
from mutagen import File
import base64
import mutagen.flac
from .. import utils

class MetadataManager:
    """
    Module for managing metadata of audio files.
    This module provides functionality to extract metadata, duration, and album art from audio files.
    It uses the mutagen library to handle various audio formats.

    Methods:
        - get_metadata(file_path: str) -> tuple: Extracts metadata, duration, and album art from the audio file.
        - get_duration(file_path: str, is_formatted=True) -> str: Returns the duration of the audio file.
        - get_album_art(file_path: str) -> PIL.Image.Image: Retrieves the album art from the audio file.
        - generate_thumbnail(image, max_size=150) -> bytes: Generates a thumbnail of the album art.
    """
    _logger = logging.getLogger(__name__)
    
    def __init__(self, album_art_dir=None):
        """
        Initialize the metadata manager.
        
        Args:
            album_art_dir: Directory to save extracted album art (default: None)
        """
        # If no album art directory is specified, use a default in the application data directory
        if album_art_dir is None:
            user_data_dir = os.path.expanduser("~/.acoustic_player")
            self.album_art_dir = os.path.join(user_data_dir, "album_art")
        else:
            self.album_art_dir = album_art_dir
        
        # Create the album art directory if it doesn't exist
        os.makedirs(self.album_art_dir, exist_ok=True)

    @staticmethod
    def get_metadata(file_path: str) -> tuple:
        """
        Get cleaned, normalized metadata from the audio file.
        Returns (info_dict, duration, album_art), where:
        - info_dict: all keys except useless ones, all values as strings
        - duration: float (seconds)
        - album_art: bytes (image data) or None
        """
        if not os.path.exists(file_path):
            MetadataManager._logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        audio = File(file_path)
        if audio is None:
            MetadataManager._logger.error(f"Unsupported or unrecognized file format: {file_path}")
            raise ValueError(f"Unsupported or unrecognized file format: {file_path}")

        useless_keys = {
            'copyright', 'encodersettings', 'credits', 'encoded-by', 'provider',
            'isrc', 'label', 'releasecountry', 'work', 'compilation', 'publisher'
        }

        info = {}
        album_art = None
        for key, value in audio.items():
            key_lower = key.lower()
            if key_lower in useless_keys:
                continue
            # Normalize value to string
            if hasattr(value, 'text'):
                v = value.text
            elif hasattr(value, 'value'):
                v = value.value
            else:
                v = value
            if isinstance(v, (list, tuple)):
                info[key] = ', '.join(map(str, v))
            else:
                info[key] = str(v)
        # Album art extraction for common formats
        try:
            if hasattr(audio, 'pictures') and audio.pictures:
                album_art = audio.pictures[0].data
        except Exception as e:
            MetadataManager._logger.warning(f"Error extracting album art from pictures: {e}")
            album_art = None
        # For MP3/ID3 and other formats
        if album_art is None:
            for key, value in audio.items():
                key_lower = key.lower()
                try:
                    if key_lower.startswith('apic') and hasattr(value, 'data'):
                        album_art = value.data
                        break
                    elif key_lower == 'metadata_block_picture':
                        pic = mutagen.flac.Picture(base64.b64decode(value[0]))
                        album_art = pic.data
                        break
                except Exception as e:
                    MetadataManager._logger.warning(f"Error extracting album art from tag {key}: {e}")
        if album_art is None and hasattr(audio, 'tags') and audio.tags:
            for tag in audio.tags.values():
                try:
                    if tag.__class__.__name__ == 'APIC' and hasattr(tag, 'data'):
                        album_art = tag.data
                        break
                except Exception as e:
                    MetadataManager._logger.warning(f"Error extracting album art from APIC tag: {e}")
        duration = float(getattr(audio.info, 'length', 0.0))
        return info, duration, album_art

    @staticmethod
    def get_duration(file_path: str, is_formatted=True) -> str:
        """
        Get the duration of the audio file.
        Args:
            file_path (str): Path to the audio file.
            is_formatted (bool): If True, return duration in mm:ss format.
        Returns:
            - Duration in seconds if is_formatted is False
            - Formatted duration (mm:ss) if is_formatted is True
        """
        audio = File(file_path)
        if audio is None or not hasattr(audio, 'info'):
            MetadataManager._logger.error(f"Unsupported or unrecognized file format: {file_path}")
            raise ValueError(f"Unsupported or unrecognized file format: {file_path}")
        length = getattr(audio.info, 'length', 0.0)
        if is_formatted:
            return utils.format_time(length)
        else:
            return str(length)

    @staticmethod
    def get_album_art(file_path):
        """
        Retrieve the album art from an audio file and return it as a PIL.Image instance.
        Args:
            file_path (str): Path to the audio file.
        Returns:
            PIL.Image.Image: The album art as a PIL image, or None if no album art is found.
        """
        audio = File(file_path)
        if audio is None:
            MetadataManager._logger.error(f"Unsupported or unrecognized file format: {file_path}")
            raise ValueError(f"Unsupported or unrecognized file format: {file_path}")
        try:
            if hasattr(audio, 'pictures') and audio.pictures:
                album_art = audio.pictures[0]
                image = Image.open(io.BytesIO(album_art.data))
                return image
        except Exception as e:
            MetadataManager._logger.warning(f"Error extracting album art as image: {e}")
        # Try fallback extraction for MP3/ID3
        if hasattr(audio, 'tags') and audio.tags:
            for tag in audio.tags.values():
                try:
                    if tag.__class__.__name__ == 'APIC' and hasattr(tag, 'data'):
                        image = Image.open(io.BytesIO(tag.data))
                        return image
                except Exception as e:
                    MetadataManager._logger.warning(f"Error extracting album art from APIC tag as image: {e}")
        return None

    def extract_embedded_art(self, file_path: str) -> tuple:
        """
        Extract album art from audio file, save it to disk, and generate a thumbnail.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Tuple of (path_to_saved_album_art, thumbnail_bytes_data) or (None, None) if not found
        """
        try:
            image = self.get_album_art(file_path)
            if not image:
                return None, None
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            art_filename = f"{base_name}_cover.jpg"
            art_path = os.path.join(self.album_art_dir, art_filename)
            # Save the full-size image as JPEG (convert to RGB if needed)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            image.save(art_path, "JPEG")

            thumbnail_data = self.generate_thumbnail(image)
            return art_path, thumbnail_data
        except Exception as e:
            self._logger.error(f"Error extracting album art: {str(e)}")
            return None, None

    def read_tags(self, file_path: str) -> dict:
        """
        Read tags from an audio file and return them as a dictionary.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary containing audio metadata
        """
        try:
            metadata, duration, _ = self.get_metadata(file_path)
            
            # Add duration to metadata
            metadata['duration'] = duration
            
            # Standardize common fields
            result = {
                'path': file_path,
                'title': metadata.get('title', os.path.basename(file_path)),
                'artist': metadata.get('artist', ''),
                'album': metadata.get('album', ''),
                'duration': duration,
                'track_num': int(metadata.get('tracknumber', '0').split('/')[0]) if metadata.get('tracknumber') else 0,
                'genre': metadata.get('genre', ''),
                'year': int(metadata.get('date', '0')[:4]) if metadata.get('date') else None,
                'lyrics': metadata.get('lyrics', '')
            }
            
            return result
        except Exception as e:
            self._logger.error(f"Error reading tags from {file_path}: {str(e)}")
            # Return basic metadata with file path and estimated duration
            return {
                'path': file_path,
                'title': os.path.basename(file_path),
                'artist': 'Unknown Artist',
                'album': 'Unknown Album',
                'duration': 0,
                'track_num': 0,
                'genre': '',
                'year': None,
                'lyrics': ''
            }

    @staticmethod
    def generate_thumbnail(image, max_size=150):
        """
        Generate a thumbnail of the album art with the specified maximum dimension.
        
        Args:
            image: PIL.Image.Image object
            max_size: Maximum size of the thumbnail in pixels (for the largest dimension)
            
        Returns:
            bytes: The thumbnail image data in JPEG format
        """
        if not image:
            return None
            
        # Create a copy to avoid modifying the original
        thumbnail = image.copy()
        
        # Calculate new dimensions while maintaining aspect ratio
        width, height = thumbnail.size
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
            
        # Resize image
        thumbnail = thumbnail.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to RGB if needed (for formats like PNG with transparency)
        if thumbnail.mode != 'RGB':
            thumbnail = thumbnail.convert('RGB')
            
        # Save to bytes buffer
        buffer = io.BytesIO()
        thumbnail.save(buffer, format="JPEG", quality=85)
        
        return buffer.getvalue()