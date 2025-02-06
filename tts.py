import os
from kokoro import KPipeline
import soundfile as sf
from datetime import datetime

# Initialize the TTS pipeline
pipeline = KPipeline(lang_code='a')  # American English

# Ensure audio directory exists
AUDIO_DIR = "static/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_audio(text: str) -> str:
    """
    Converts text into speech using Kokoro TTS
    Returns: filename of the generated audio
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file = f"summary_{timestamp}.wav"
    file_path = os.path.join(AUDIO_DIR, audio_file)

    generator = pipeline(text, voice='af_heart', speed=1)

    for _, _, audio in generator:
        sf.write(file_path, audio, 24000)
        break  # Only save the first generated audio

    return audio_file
