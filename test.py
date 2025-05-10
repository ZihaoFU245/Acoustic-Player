file_path = r"D:\MyProject\Datasets\music\Taylor Swift - 1989 (Taylor's Version) (Deluxe) (2023) [24Bit-48kHz] FLAC [PMEDIA] ⭐️\14. Wonderland (Taylor's Version).flac"

import vlc
import time

instance = vlc.Instance()
player = instance.media_player_new()

media = instance.media_new("Error path")

print(player.get_state())











