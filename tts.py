import os
from pathlib import Path
from kokoro import KPipeline
import soundfile as sf
import numpy as np
from typing import List, Union

def generate_audio(text: str, add_music: bool = False, music_path: Union[str, Path] = None, music_volume: float = 0.1) -> str:
    """
    Generate audio file from text using Kokoro Text-to-Speech
    
    Args:
        text: Text to convert to speech
        add_music: Whether to add background music
        music_path: Path to background music file (if add_music is True)
        music_volume: Volume level for background music (0.0 to 1.0)
    
    Returns:
        str: Filename of the generated audio
    """
    # Create static/audio directory if it doesn't exist
    output_dir = Path('static/audio')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize Kokoro pipeline
    pipeline = KPipeline(lang_code='a')  # 'a' for American English
    
    # Generate audio segments
    audio_segments = []
    pause = np.zeros(int(24000 * 0.3))  # 0.3 second pause
    
    generator = pipeline(
        text,
        voice='af_heart',  # Young female voice
        speed=1,
        split_pattern=r'[.!?]\s+'  # Split by sentences
    )
    
    # Process each segment
    temp_segments = []
    segments_dir = output_dir / "segments"
    segments_dir.mkdir(exist_ok=True)
    
    for i, (_, _, audio) in enumerate(generator):
        # Save individual segment (useful for debugging)
        segment_path = segments_dir / f'segment_{i:03d}.wav'
        sf.write(segment_path, audio, 24000)
        temp_segments.append(segment_path)
        
        # Add to audio segments
        audio_segments.append(audio)
        audio_segments.append(pause)
    
    # Remove the last pause and concatenate all segments
    final_audio = np.concatenate(audio_segments[:-1])
    
    # Base filename for voice only
    voice_filename = f"{output_dir}/voice_output.wav"
    
    # Save the voice audio
    sf.write(voice_filename, final_audio, 24000)
    
    # Add background music if requested
    if add_music and music_path:
        music_path = Path(music_path)
        if not music_path.exists():
            raise FileNotFoundError(f"Music file not found: {music_path}")
        
        # Read the voice and music files
        voice_audio, _ = sf.read(voice_filename)
        music_audio, music_sr = sf.read(music_path)
        
        # Loop music if it's shorter than voice
        if len(music_audio) < len(voice_audio):
            repeats = int(np.ceil(len(voice_audio) / len(music_audio)))
            music_audio = np.tile(music_audio, repeats)[:len(voice_audio)]
        else:
            music_audio = music_audio[:len(voice_audio)]
        
        # Mix voice and music
        mixed_audio = voice_audio + (music_audio * music_volume)
        
        # Normalize to prevent clipping
        mixed_audio = mixed_audio / np.max(np.abs(mixed_audio))
        
        # Final filename for mixed audio
        final_filename = f"{output_dir}/final_output.wav"
        sf.write(final_filename, mixed_audio, 24000)
        
        # Clean up temporary files
        for segment in temp_segments:
            segment.unlink()
        Path(voice_filename).unlink()
        
        return os.path.basename(final_filename)
    
    # Clean up temporary files
    for segment in temp_segments:
        segment.unlink()
    
    return os.path.basename(voice_filename)
