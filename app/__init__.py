"""
Acoustic Player Application Package
This package contains the main modules for the music player app.
"""

from .models.player import MusicPlayer
from .models.playlist import PlaylistManager
from .models.metadata import MetadataManager
from .viewmodels.player_vm import PlayerViewModel
from .viewmodels.playlist_vm import PlaylistViewModel
from .viewmodels.metadata_vm import MetadataViewModel
from .views.main_window import MainWindow
# Optional modules
from .utils import *
from .lyrics import LyricsManager
from .visualizer import AudioVisualizer
from .hotkeys import HotkeyManager
from .mini_test import MiniTest