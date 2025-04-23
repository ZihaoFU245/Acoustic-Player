"""
Acoustic Player Application Package
This package contains the main modules for the music player app.
"""

from .main_window import MainWindow
from .player import MusicPlayer
from .playlist import PlaylistManager
from .metadata import MetadataManager
from .utils import *
# Optional modules
from .lyrics import LyricsManager
from .visualizer import AudioVisualizer
from .hotkeys import HotkeyManager
from .mini_test import MiniTest