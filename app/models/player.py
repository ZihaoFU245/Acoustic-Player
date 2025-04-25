import sounddevice as sd
import numpy as np
import soundfile as sf
import os


class MusicPlayer:
    """
    Handle music playback using sounddevice and soundfile.

    Note: 
        - This class is the playback engine for the music player.
        - Using sounddevice for playback and soundfile for reading audio files.
        - Need to support various audio formats like MP3, WAV, FLAC, etc.
        - It needs to fully perserve the audio quality of the original file.
        - The code should be efficient and fast.
        - Use Numba for performance optimization where applicable.
        - Error handling should be robust.
    """
    def __init__(self):
        self.stream = None
        self.file_path = None
        self.samplerate = None
        self.channels = None

    def load(self, file_path: str):
        """Load an audio file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        self.file_path = file_path
        data, self.samplerate = sf.read(file_path, dtype='float32')
        self.channels = data.shape[1] if len(data.shape) > 1 else 1