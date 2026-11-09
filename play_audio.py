import subprocess
from pathlib import Path


def play_audio(audio_path: Path) -> None:
    subprocess.run(["afplay", str(audio_path)], check=True)
