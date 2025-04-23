# -*- coding: utf-8 -*-
from . import utils
import os
from PIL import Image
import io
from mutagen import File

class MetadataManager:
    """Class to manage metadata of audio files."""

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
            raise FileNotFoundError(f"File not found: {file_path}")

        audio = File(file_path)
        if audio is None:
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
        # Try to extract using the same logic as get_album_art
        if hasattr(audio, 'pictures') and audio.pictures:
            try:
                album_art = audio.pictures[0].data
            except Exception:
                album_art = None
        # For MP3/ID3 and other formats
        if album_art is None:
            for key, value in audio.items():
                key_lower = key.lower()
                if key_lower.startswith('apic') and hasattr(value, 'data'):
                    album_art = value.data
                    break
                elif key_lower == 'metadata_block_picture':
                    import base64
                    import mutagen.flac
                    try:
                        pic = mutagen.flac.Picture(base64.b64decode(value[0]))
                        album_art = pic.data
                        break
                    except Exception:
                        pass
        if album_art is None and hasattr(audio, 'tags') and audio.tags:
            for tag in audio.tags.values():
                if tag.__class__.__name__ == 'APIC' and hasattr(tag, 'data'):
                    album_art = tag.data
                    break
        duration = float(getattr(audio.info, 'length', 0.0))
        return info, duration, album_art

    @staticmethod
    def get_duration(file_path: str) -> float:
        """Get the duration of the audio file."""
        audio = File(file_path)
        if audio is None or not hasattr(audio, 'info'):
            raise ValueError(f"Unsupported or unrecognized file format: {file_path}")

        return getattr(audio.info, 'length', 0.0)
    
    @staticmethod
    def get_album_art(file_path):
        """
        Retrieve the album art from a FLAC file and return it as a PIL.Image instance.

        Args:
            file_path (str): Path to the FLAC file.

        Returns:
            PIL.Image.Image: The album art as a PIL image, or None if no album art is found.
        """
        audio = File(file_path)
        if audio is None:
            raise ValueError(f"Unsupported or unrecognized file format: {file_path}")
        
        try:
            if not audio.pictures:
                return None
            
            album_art = audio.pictures[0]
            image = Image.open(io.BytesIO(album_art.data))
            return image
        
        except AttributeError:
            # If the file doesn't have pictures, return None
            return None
        
        except IOError:
            # If the image cannot be opened, return None
            return None
           
        except Exception as e:
            raise ValueError(f"Error retrieving album art: {e}")






