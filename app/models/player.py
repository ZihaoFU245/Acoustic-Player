import logging
import numpy as np
import sounddevice as sd
import soundfile as sf
from typing import Any
from ..utils import is_supported_format  


class MusicPlayer:
    """
    MusicPlayer is the core playback engine for the Acoustic Player application.

    This class handles loading, playing, pausing, resuming, seeking, and stopping audio playback using sounddevice and soundfile.
    It is designed to be integrated with a GUI (such as PySide6/PyQt) and is suitable for MVVM or MVC patterns.

    Key features for GUI binding:
    - Exposes playback state (is_playing, is_paused, current_time, duration) as properties for easy binding to ViewModels or UI.
    - Provides methods for playback control (start, stop, pause, resume, fast_forward, rewind, to_point).
    - Handles audio loading and stream management robustly, with error handling and logging.
    - Can be extended to emit signals or callbacks for UI updates (e.g., on track end, on error) if needed.

    Usage:
        player = MusicPlayer()
        player.load_music('path/to/file.mp3')
        player.start()
        Bind UI controls to player methods and properties.
    """

    def __init__(self, blocksize: int = 1024):
        self._audio_file_path: str | None = None
        self._audio_data: np.ndarray | None = None
        self._sample_rate: int | None = None
        self._dtype: np.dtype | None = None
        self.channels: int | None = None

        self._playback_pos: int = 0  # current sample index in the audio data
        self._stream: sd.OutputStream | None = None
        self._logger = logging.getLogger(__name__)
        if blocksize <= 0:
            self._logger.warning(f"Invalid blocksize {blocksize}, falling back to 1024")
            blocksize = 1024
        self._blocksize = blocksize

        self._is_playing: bool = False
        self._is_paused: bool = False

    @staticmethod
    def _choose_dtype(info_subtype: str) -> np.dtype:
        """
        Determine the appropriate NumPy data type based on the subtype of the audio file.

        Args:
            info_subtype (str): The subtype of the audio file (e.g., 'PCM_16', 'PCM_32', 'DOUBLE').

        Returns:
            np.dtype: The corresponding NumPy data type.
        """
        # Use float64 for DOUBLE and PCM_64, float32 for others
        if info_subtype in ('DOUBLE', 'PCM_64' , 'PCM_32'):
            return np.float64
        else:
            return np.float32

    def load_music(self, file_path: str) -> None:
        """
        Load the music file and prepare it for playback.

        Args:
            file_path (str): The path to the audio file to be loaded.

        Returns:
            None
        """
        if not is_supported_format(file_path):
            raise ValueError(f"Unsupported file format: {file_path}")

        self._audio_file_path = file_path
        self._audio_data = None
        self._sample_rate = None
        self._dtype = None
        self.channels = None
        self._playback_pos = 0
        self._is_playing = False
        self._is_paused = False

        if self._stream and self._stream.active:
            self.stop()

        try:
            self._dtype = self._choose_dtype(sf.info(self._audio_file_path).subtype)
            """
            This reads the entire file in memory, 
            we can update for streaming in future.
            """
            self._audio_data, self._sample_rate = sf.read(
                self._audio_file_path, always_2d=True, dtype=self._dtype
            )
            self.channels = self._audio_data.shape[1]

        except FileNotFoundError:
            self._audio_file_path = None
            raise FileNotFoundError(f"File not found: {file_path}")

        except Exception as e:
            self._audio_file_path = None
            raise RuntimeError(f"Error loading audio file: {e}")

    def _audio_callback(self, outdata: np.ndarray, frames: int, time: Any, status: Any) -> None:
        """
        Callback function for the audio stream. This function is called by sounddevice to fill the output buffer.

        Args:
            outdata (np.ndarray): The output buffer to be filled with audio data.
            frames (int): The number of frames to be written to the output buffer.
            time (sd.CallbackTime): The time information for the callback.
            status (sd.CallbackFlags): The status flags for the callback.

        Returns:
            None
        """
        if status:
            self._logger.warning(f"Sound device status: {status}")

        if self._audio_data is None or self._is_paused:
            outdata.fill(0)
            return

        remaining_samples = self._audio_data.shape[0] - self._playback_pos
        chunk_size = min(frames, remaining_samples)

        outdata[:chunk_size] = self._audio_data[self._playback_pos : self._playback_pos + chunk_size]
        if chunk_size < frames:
            outdata[chunk_size:] = 0
            # End of audio: stop playback
            self._is_playing = False
            try:
                if self._stream:
                    self._stream.stop()
            except Exception as e:
                self._logger.error(f"Error stopping stream: {e}")
        # advance position
        self._playback_pos += chunk_size

    def start(self):
        """
        Start the playback of the loaded audio file.

        Returns:
            None
        """
        if self._audio_file_path is None:
            raise ValueError("No audio file loaded. Please load a file before starting playback.")

        if self._stream and self._stream.active:
            if self._is_paused:
                self._is_paused = False
                self._is_playing = True
            return

        self._is_paused = False

        try:
            self._stream = sd.OutputStream(
                blocksize=self._blocksize,
                samplerate=self._sample_rate,
                channels=self.channels,
                dtype=self._dtype,
                callback=self._audio_callback,
            )
            self._stream.start()
            self._is_playing = True

        except Exception as e:
            self._stream = None
            self._is_playing = False
            raise RuntimeError(f"Error starting playback: {e}")


    def stop(self) -> None:
        """
        Stop the playback and release the audio stream.

        Returns:
            None
        """
        if self._stream and self._stream.active:
            self._stream.stop()
            self._stream.close()
            self._stream = None
            self._is_paused = False
            self._is_playing = False
        elif self._stream:
            self._stream.close()
            self._stream = None
            self._is_paused = False
            self._is_playing = False
        else:
            return

    def pause(self) -> None:
        """
        Pause the playback.

        Returns:
            None
        """
        if self._stream and self._stream.active and not self._is_paused:
            self._is_paused = True
            self._is_playing = False
        elif self._is_paused:
            return
        else:
            return

    def resume(self) -> None:
        """
        Resume the playback from the current position.

        Returns:
            None
        """
        if self._stream and self._stream.active and self._is_paused:
            self._is_paused = False
            self._is_playing = True
        elif not self._is_paused:
            return
        else:
            return

    def fast_forward(self, seconds: float) -> None:
        """
        Fast forward the playback by a specified number of seconds.

        Args:
            seconds (float): The number of seconds to fast forward.

        Returns:
            None
        """
        if self._audio_data is None or self._sample_rate is None:
            return

        new_pos = self._playback_pos + int(seconds * self._sample_rate)
        if new_pos >= self._audio_data.shape[0]:
            new_pos = self._audio_data.shape[0] - 1

        new_pos = max(0, min(new_pos, len(self._audio_data)))

        if new_pos != self._playback_pos:
            self._playback_pos = new_pos
        else:
            return

    def rewind(self, seconds: float) -> None:
        """
        Rewind the playback by a specified number of seconds.

        Args:
            seconds (float): The number of seconds to rewind.

        Returns:
            None
        """
        if self._audio_data is None or self._sample_rate is None:
            return

        new_pos = self._playback_pos - int(seconds * self._sample_rate)
        if new_pos < 0:
            new_pos = 0

        new_pos = max(0, min(new_pos, len(self._audio_data)))

        if new_pos != self._playback_pos:
            self._playback_pos = new_pos
        else:
            return

    def to_point(self, seconds: float) -> None:
        """
        Seek to a specific point in the audio file.

        Args:
            seconds (float): The time in seconds to seek to.

        Returns:
            None
        """
        if self._audio_data is None or self._sample_rate is None:
            return

        new_pos = int(seconds * self._sample_rate)
        if new_pos >= self._audio_data.shape[0]:
            new_pos = self._audio_data.shape[0] - 1

        new_pos = max(0, min(new_pos, len(self._audio_data)))

        if new_pos != self._playback_pos:
            self._playback_pos = new_pos
        else:
            return

    @property
    def at(self) -> float:
        """
        Get the current playback time in seconds, rounded to 2 significant figures.
        Returns:
            float: The current playback time in seconds.
        """
        if self._sample_rate is None or self._sample_rate == 0:
            return 0.0
        return round(self._playback_pos / self._sample_rate, 2)

    @property
    def duration(self) -> float:
        """
        Get the total duration of the loaded audio file in seconds, rounded to 2 significant figures.
        Returns:
            float: The total duration of the audio file in seconds.
        """
        if self._audio_data is None or self._sample_rate is None or self._sample_rate == 0:
            return 0.0
        return round(len(self._audio_data) / self._sample_rate, 2)

    @property
    def is_playing(self) -> bool:
        """
        Check if the audio is currently playing.

        Returns:
            bool: True if the audio is playing, False otherwise.
        """
        return self._stream is not None and self._stream.active and not self._is_paused

    @property
    def is_paused(self) -> bool:
        """
        Check if the audio is currently paused.

        Returns:
            bool: True if the audio is paused, False otherwise.
        """
        return self._is_paused




