"""
Audio utilities for processing audio files
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from pydub import AudioSegment
import numpy as np
import soundfile as sf


class AudioProcessor:
    def __init__(self):
        self.supported_formats = {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.webm'}
        self.target_sample_rate = 16000  # Standard for speech recognition
        self.target_channels = 1  # Mono
    
    async def process_for_speech_recognition(self, audio_path: str) -> str:
        """Process audio file for optimal speech recognition"""
        try:
            audio = AudioSegment.from_file(audio_path)
            
            # Convert to mono
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Set sample rate to 16kHz (optimal for speech recognition)
            audio = audio.set_frame_rate(self.target_sample_rate)
            
            # Set sample width to 16-bit
            audio = audio.set_sample_width(2)
            
            # Normalize volume
            audio = self.normalize_audio(audio)
            
            # Remove silence from beginning and end
            audio = self.trim_silence(audio)
            
            # Save processed audio
            output_path = Path(audio_path).with_suffix('.processed.wav')
            audio.export(str(output_path), format="wav")
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"Audio processing failed: {str(e)}")
    
    def normalize_audio(self, audio: AudioSegment) -> AudioSegment:
        """Normalize audio volume"""
        try:
            # Calculate the maximum possible amplitude
            max_amplitude = audio.max
            
            if max_amplitude > 0:
                # Normalize to prevent clipping while maintaining good volume
                target_amplitude = min(max_amplitude * 1.2, 32767)  # 16-bit max
                change_in_db = 20 * np.log10(target_amplitude / max_amplitude)
                audio = audio + change_in_db
            
            return audio
        except Exception:
            return audio  # Return original if normalization fails
    
    def trim_silence(self, audio: AudioSegment, silence_threshold: int = -40) -> AudioSegment:
        """Remove silence from beginning and end of audio"""
        try:
            # Detect non-silent parts
            non_silent_ranges = self.detect_non_silent(audio, silence_threshold)
            
            if not non_silent_ranges:
                return audio  # Return original if no non-silent parts found
            
            # Get the range from first non-silent to last non-silent
            start = non_silent_ranges[0][0]
            end = non_silent_ranges[-1][1]
            
            return audio[start:end]
            
        except Exception:
            return audio  # Return original if trimming fails
    
    def detect_non_silent(self, audio: AudioSegment, silence_threshold: int = -40, 
                         min_silence_len: int = 100) -> list:
        """Detect non-silent parts of audio"""
        try:
            # Convert to numpy array for analysis
            samples = np.array(audio.get_array_of_samples())
            
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
                samples = samples.mean(axis=1)
            
            # Calculate RMS in chunks
            chunk_size = int(audio.frame_rate * min_silence_len / 1000)  # Convert ms to samples
            chunks = len(samples) // chunk_size
            
            non_silent_chunks = []
            
            for i in range(chunks):
                start_idx = i * chunk_size
                end_idx = (i + 1) * chunk_size
                chunk = samples[start_idx:end_idx]
                
                # Calculate RMS
                rms = np.sqrt(np.mean(chunk ** 2))
                db = 20 * np.log10(rms + 1e-10)  # Add small value to avoid log(0)
                
                if db > silence_threshold:
                    start_time = start_idx * 1000 // audio.frame_rate
                    end_time = end_idx * 1000 // audio.frame_rate
                    non_silent_chunks.append((start_time, end_time))
            
            return non_silent_chunks
            
        except Exception:
            return [(0, len(audio))]  # Return full duration if detection fails
    
    def convert_to_wav(self, input_path: str, output_path: Optional[str] = None) -> str:
        """Convert audio file to WAV format"""
        try:
            if output_path is None:
                output_path = Path(input_path).with_suffix('.wav')
            
            audio = AudioSegment.from_file(input_path)
            audio.export(str(output_path), format="wav")
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"WAV conversion failed: {str(e)}")
    
    def get_audio_info(self, audio_path: str) -> dict:
        """Get audio file information"""
        try:
            audio = AudioSegment.from_file(audio_path)
            
            return {
                'duration_ms': len(audio),
                'duration_seconds': len(audio) / 1000.0,
                'frame_rate': audio.frame_rate,
                'channels': audio.channels,
                'sample_width': audio.sample_width,
                'frame_count': audio.frame_count(),
                'max_amplitude': audio.max,
                'rms': audio.rms
            }
            
        except Exception as e:
            raise Exception(f"Failed to get audio info: {str(e)}")
    
    def split_audio_by_silence(self, audio_path: str, min_silence_len: int = 500, 
                              silence_threshold: int = -40) -> list:
        """Split audio by silence into chunks"""
        try:
            audio = AudioSegment.from_file(audio_path)
            
            chunks = audio.split_on_silence(
                min_silence_len=min_silence_len,
                silence_thresh=silence_threshold,
                keep_silence=100  # Keep some silence at the edges
            )
            
            # Save chunks to temporary files
            chunk_paths = []
            temp_dir = Path(tempfile.gettempdir()) / "audio_chunks"
            temp_dir.mkdir(exist_ok=True)
            
            for i, chunk in enumerate(chunks):
                chunk_path = temp_dir / f"chunk_{i}.wav"
                chunk.export(str(chunk_path), format="wav")
                chunk_paths.append(str(chunk_path))
            
            return chunk_paths
            
        except Exception as e:
            raise Exception(f"Audio splitting failed: {str(e)}")
    
    def validate_audio_file(self, audio_path: str) -> bool:
        """Validate if audio file is supported and readable"""
        try:
            path = Path(audio_path)
            
            # Check extension
            if path.suffix.lower() not in self.supported_formats:
                return False
            
            # Try to load the file
            audio = AudioSegment.from_file(str(path))
            
            # Basic validation
            return len(audio) > 0 and audio.frame_rate > 0
            
        except Exception:
            return False
    
    def enhance_speech_audio(self, audio_path: str) -> str:
        """Enhance audio specifically for speech recognition"""
        try:
            audio = AudioSegment.from_file(audio_path)
            
            # Apply high-pass filter to remove low-frequency noise
            # (This is a simple approximation using pydub)
            audio = audio.high_pass_filter(80)
            
            # Apply low-pass filter to remove high-frequency noise
            audio = audio.low_pass_filter(8000)
            
            # Normalize
            audio = self.normalize_audio(audio)
            
            # Compress dynamic range slightly
            audio = audio.compress_dynamic_range()
            
            # Save enhanced audio
            output_path = Path(audio_path).with_suffix('.enhanced.wav')
            audio.export(str(output_path), format="wav")
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"Audio enhancement failed: {str(e)}")