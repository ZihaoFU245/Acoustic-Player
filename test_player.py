import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.player import MusicPlayer


def test_music_player(file_path: str):
    player = MusicPlayer()
    player.load_music(file_path)
    print("Commands: play, pause, resume, stop, ff <sec>, rw <sec>, seek <sec>, duration, at, quit")
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
        else:
            print("Unknown command.")

if __name__ == "__main__":
    file_path = r"D:\MyProject\Datasets\music\Taylor Swift - 1989 (Taylor's Version) (Deluxe) (2023) [24Bit-48kHz] FLAC [PMEDIA] ⭐️\09. Wildest Dreams (Taylor's Version).flac"  # Replace with your audio file path

    test_music_player(file_path)  # Replace with your audio file path
