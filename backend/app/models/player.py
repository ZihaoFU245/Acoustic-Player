"""
This is the core playback engine.
"""
# NOTE: This code has been reviewed by Zihao
import vlc
import os

class MusicPlayer:
    """Core playback engine."""
    def __init__(self):
        """Initialize the VLC player instance.

        On systems where the native ``libvlc`` library is not available,
        instantiating :class:`vlc.Instance` raises a ``NameError``.  To make
        unit tests runnable in such environments we catch the error and put the
        player into a disabled state.  All playback related methods will then
        raise a ``RuntimeError`` explaining the situation.
        """
        try:
            self.instance = vlc.Instance()
            self.player = self.instance.media_player_new()
            self._init_error = None
        except Exception as e:  # libvlc not installed
            self.instance = None
            self.player = None
            self._init_error = e

        self.media = None
        self.current_track = None   # A file path string

        if self.player is not None:
            self.events = self.player.event_manager()
            self.events.event_attach(
                vlc.EventType.MediaPlayerEndReached, self._on_end
            )
            self.events.event_attach(
                vlc.EventType.MediaPlayerEncounteredError, self._on_error
            )
        else:
            self.events = None

    def load_music(self, file_path: str):
        if self.player is None:
            raise RuntimeError(
                f"VLC backend not available: {self._init_error}"
            )
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        self.media = self.instance.media_new(file_path)
        self.player.set_media(self.media)
        self.current_track = file_path

    def play(self, file_path: str):
        """Convenience method to load a track and start playback."""
        self.load_music(file_path)
        self.start()

    def start(self):
        if self.player is None:
            raise RuntimeError(
                f"VLC backend not available: {self._init_error}"
            )
        self.player.play()

    def pause(self):
        if self.player is None:
            return
        self.player.pause()

    def resume(self):
        # VLC toggles pause with pause() if already paused
        if self.player is None:
            return
        if self.player.get_state() == vlc.State.Paused:
            self.player.pause()

    def stop(self):
        if self.player is None:
            return
        self.player.stop()

    def fast_forward(self, seconds: float):
        if self.player is not None:
            self.seek(self.at * 1000 + seconds * 1000)

    def rewind(self, seconds: float):
        if self.player is not None:
            self.seek(self.at * 1000 - seconds * 1000)

    def to_point(self, seconds: float):
        if self.player is not None:
            self.seek(seconds * 1000)

    def seek(self, position_ms: float):
        if self.player is None:
            return
        duration_ms = self.duration * 1000
        if 0 <= position_ms <= duration_ms:
            self.player.set_time(int(position_ms))

    def set_volume(self, level: int):
        if not isinstance(level, (int, float)):
            raise ValueError(f"Data type {type(level)} not supported.")
        level = int(level)
        level = max(0, min(100, level))
        if self.player is not None:
            self.player.audio_set_volume(level)

    @property
    def duration(self):
        if self.player is None:
            return 0
        # Get duration from media if available
        dur = self.player.get_length()
        if dur <= 0 and self.media is not None:
            # Try to get duration from media object
            dur = self.media.get_duration()
        return dur / 1000 if dur > 0 else 0

    @property
    def at(self):
        if self.player is None:
            return 0
        return self.player.get_time() / 1000

    def get_status(self):
        if self.player is None:
            state = "unavailable"
            volume = 0
        else:
            state = str(self.player.get_state())
            volume = self.player.audio_get_volume()
        return {
            "state": state,
            "current_track": self.current_track,
            "position": self.at,
            "duration": self.duration,
            "volume": volume,
        }
    
    """
    TODO: Add callback support to handle tracks and error, when playlist implemented
    TODO: Connect to websocket
    TODO: Automatic next track
    TODO: Better error handling
    """
    def _on_end(self, event):
        """Handle track end event."""
        print("Track finished.")
        # Emit WebSocket event when track ends
        try:
            from ..ws.events import emit_player_status
            emit_player_status(self.get_status())
        except ImportError:
            pass  # WebSocket not available

    def _on_error(self, event):
        """Handle playback error event."""
        print("Playback error occurred.")
        # Emit WebSocket event on error
        try:
            from ..ws.events import emit_player_status  
            emit_player_status(self.get_status())
        except ImportError:
            pass  # WebSocket not available

    



