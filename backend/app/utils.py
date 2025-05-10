"""
Utility functions for the music player app.
"""
import time
import os
import json
from typing import Dict, List, Union, Optional

def format_time(seconds: float) -> str:
    """
    Format seconds into a string of the form mm:ss.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def format_time_ms(milliseconds: float) -> str:
    """
    Format milliseconds into a string of the form mm:ss.
    
    Args:
        milliseconds: Time in milliseconds
        
    Returns:
        Formatted time string
    """
    return format_time(milliseconds / 1000)

def get_supported_formats() -> List[str]:
    """
    Get a list of supported audio formats.
    
    Returns:
        List of supported file extensions
    """
    return [
        "mp3",
        "wav",
        "ogg", 
        "flac",
        "aac",
        "m4a",
        # Remove wma for now, as it is not supported by mutagen
        "opus",
    ]

def is_supported_format(file_path: str) -> bool:
    """Check if the file format is supported."""
    ext = file_path.split('.')[-1].lower()
    return ext in get_supported_formats()

def scan_music_folder(path):
    """Scan the music folder for supported audio files."""
    supported_formats = set(get_supported_formats())
    music_files = []

    def _scan_dir(current_path):
        try:
            with os.scandir(current_path) as it:
                for entry in it:
                    if entry.is_file():
                        ext = entry.name.split('.' , 1)[-1].lower()
                        if ext in supported_formats:
                            music_files.append(entry.path)
                    # Leave this commented out for now, as we are not scanning subdirectories
                    #elif entry.is_dir():
                        #_scan_dir(entry.path)
        except PermissionError:
            pass

    _scan_dir(path)
    return music_files


def read_json(path):
    """Read a JSON file and return its content."""
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    return data

def write_json(path, data) -> bool: # bool indicate success or failure
    """Write data to a JSON file."""
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        return False

