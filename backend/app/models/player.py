"""
This is the core playback engine.
"""
# NOTE: This code has been reviewed by Zihao
import vlc
import os

class MusicPlayer:
    """Core playboack engine."""
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = None
        self.current_track = None   # A file path string
        self.events = self.player.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self._on_end)
        self.events.event_attach(vlc.EventType.MediaPlayerEncounteredError, self._on_error)

    def load_music(self, file_path: str):
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
        self.player.play()

    def pause(self):
        self.player.pause()

    def resume(self):
        # VLC toggles pause with pause() if already paused
        if self.player.get_state() == vlc.State.Paused:
            self.player.pause()

    def stop(self):
        self.player.stop()

    def fast_forward(self, seconds: float):
        self.seek(self.at * 1000 + seconds * 1000)

    def rewind(self, seconds: float):
        self.seek(self.at * 1000 - seconds * 1000)

    def to_point(self, seconds: float):
        self.seek(seconds * 1000)

    def seek(self, position_ms: float):
        duration_ms = self.duration * 1000
        if 0 <= position_ms <= duration_ms:
            self.player.set_time(int(position_ms))

    def set_volume(self, level: int):
        if not isinstance(level, (int, float)):
            raise ValueError(f"Data type {type(level)} not supported.")
        level = int(level)
        level = max(0, min(100, level))
        self.player.audio_set_volume(level)

    @property
    def duration(self):
        # Try twice since duration might not be available immediately
        dur = self.player.get_length()
        if dur <= 0:
            self.player.play()
            import time
            time.sleep(0.1)
            self.player.pause()
            dur = self.player.get_length()
        return dur / 1000 if dur > 0 else 0

    @property
    def at(self):
        return self.player.get_time() / 1000

    def get_status(self):
        return {
            "state": str(self.player.get_state()),  # get_state return: Opening / Playing, etc.
            "current_track": self.current_track,
            "position": self.at,
            "duration": self.duration,
            "volume": self.player.audio_get_volume(),
        }
    
    """
    TODO: Add callback support to handle tracks and error, when playlist implemented
    TODO: Connect to websocket
    TODO: Automatic next track
    TODO: Better error handling
    """
    def _on_end(self, event):
        print("Track finished.")

    def _on_error(self, event):
        print("Playback error occurred.")

    



