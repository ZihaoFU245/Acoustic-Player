import sys
import os
#import pytest

#pytest.skip("manual player test", allow_module_level=True)

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.models.player import MusicPlayer


def test_music_player(file_path: str):
    player = MusicPlayer() # Increased blocksize
    player.load_music(file_path)
    print("Commands: play, pause, resume, stop, ff <sec>, rw <sec>, seek <sec>,set <1-100 volumn> duration, at, quit")
    while True:
        cmd = input("Enter command: ").strip().lower()
        if cmd == "play":
            player.start()
            print("Playing...")
        elif cmd == "pause":
            player.pause()
            print("Paused.")
        elif cmd == "resume":
            player.resume()
            print("Resumed.")
        elif cmd == "stop":
            player.stop()
            print("Stopped.")
        elif cmd.startswith("ff "):
            try:
                sec = float(cmd.split()[1])
                player.fast_forward(sec)
                print(f"Fast forwarded {sec} seconds.")
            except Exception as e:
                print(f"Invalid input: {e}")
        elif cmd.startswith("rw "):
            try:
                sec = float(cmd.split()[1])
                player.rewind(sec)
                print(f"Rewound {sec} seconds.")
            except Exception as e:
                print(f"Invalid input: {e}")
        elif cmd.startswith("seek "):
            try:
                sec = float(cmd.split()[1])
                player.to_point(sec)
                print(f"Seeked to {sec} seconds.")
            except Exception as e:
                print(f"Invalid input: {e}")
        elif cmd == "duration":
            duration = player.duration
            print(f"Duration: {str(duration)} seconds")
        elif cmd == "at":
            try:
                at = player.at
                print(f"Current position: {str(at)} seconds")
            except Exception as e:
                print(f"Invalid input: {e}")        
        elif cmd == "quit":
            player.stop()
            print("Exiting.")
            break
        elif cmd.startswith("set"):
            try:
                vol = float(cmd.split(sep=' ')[1])
                player.set_volume(vol)
                print(f"Set volumn as {vol}")
            except Exception as e:
                print(f"Invalid input: {e}")
        else:
            print("Unknown command.")

if __name__ == "__main__":
    file_path = r"E:\saves\Taylor Swift - THE TORTURED POETS DEPARTMENT\04. Down Bad [Explicit].flac"

    test_music_player(file_path)  # Replace with your audio file path