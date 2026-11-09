
import sounddevice as sd
from scipy.io.wavfile import write
from pathlib import Path


def record_audio(duration: int = 5) -> Path:
    """Record audio from the microphone and save it as a WAV file."""

    sample_rate = 16000
    output_path = Path(__file__).parent / 'utils' / "recording.wav"

    input("Press Enter to start recording...")
    print("Recording...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
    )

    sd.wait()

    write(str(output_path), sample_rate, audio)

    print(f"Recording saved to {output_path}")

    return output_path
