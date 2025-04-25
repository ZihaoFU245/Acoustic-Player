import os
import logging
import io
from PIL import Image
from mutagen import File
import base64
import mutagen.flac
from .. import utils

class MetadataManager:
    """Class to manage metadata of audio files."""
    _logger = logging.getLogger(__name__)

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
    def get_duration(file_path: str, is_formatted=False) -> str:
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