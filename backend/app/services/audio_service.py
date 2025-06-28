"""Abstraction layer for audio playback."""

from ..models.player import MusicPlayer


class AudioService:
    """Simple wrapper around :class:`MusicPlayer` used by API handlers."""

    def __init__(self):
        self.player = MusicPlayer()

    # Expose a subset of player methods with some basic error handling
    def play(self, path: str):
        self.player.play(path)
        return self.player.get_status()

    def pause(self):
        self.player.pause()
        return self.player.get_status()

    def resume(self):
        self.player.resume()
        return self.player.get_status()

    def stop(self):
        self.player.stop()
        return self.player.get_status()

    def seek(self, position_ms: float):
        self.player.seek(position_ms)
        return self.player.get_status()

    def set_volume(self, level: int):
        self.player.set_volume(level)
        return self.player.get_status()

    def status(self):
        return self.player.get_status()
