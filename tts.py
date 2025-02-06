
from kokoro import KPipeline
import soundfile as sf

# Initialize the TTS pipeline
pipeline = KPipeline(lang_code='a')  # American English

def generate_audio(text: str):
    """Converts text into speech using Kokoro TTS"""
    generator = pipeline(text, voice='af_heart', speed=1)

    for i, (_, _, audio) in enumerate(generator):
        audio_file = f"output_{i}.wav"
        sf.write(audio_file, audio, 24000)  # Save audio file
        return audio_file
