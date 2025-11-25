"""
Speech Service Module
Handles speech-to-text using VOSK and text-to-speech using gTTS
"""

import os
import json
import base64
import tempfile
import asyncio
from typing import Optional
from pathlib import Path

import wave
import vosk
from gtts import gTTS
from pydub import AudioSegment
import soundfile as sf


class SpeechService:
    def __init__(self):
        self.model = None
        self.model_path = None
        self.setup_vosk_model()
    
    def setup_vosk_model(self):
        """Download and setup VOSK model if not available"""
        try:
            # Check for existing model
            model_dir = Path("vosk-model")
            if not model_dir.exists():
                print("VOSK model not found. Please download a model manually.")
                print("Visit: https://alphacephei.com/vosk/models")
                print("Download vosk-model-en-us-0.22 and extract to 'vosk-model' directory")
                self.model = None
                return
            
            self.model = vosk.Model(str(model_dir))
            print("VOSK model loaded successfully")
        except Exception as e:
            print(f"Failed to load VOSK model: {e}")
            self.model = None
    
    def is_available(self) -> bool:
        """Check if speech service is available"""
        return self.model is not None
    
    async def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribe audio file to text using VOSK
        """
        if not self.model:
            raise Exception("VOSK model not available. Please setup the model first.")
        
        try:
            # Convert audio to WAV format if needed
            wav_path = await self._convert_to_wav(audio_path)
            
            # Read WAV file
            wf = wave.open(wav_path, "rb")
            
            # Check if audio is in correct format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
                raise Exception("Audio file must be WAV format mono PCM")
            
            # Create recognizer
            rec = vosk.KaldiRecognizer(self.model, wf.getframerate())
            rec.SetMaxAlternatives(0)
            rec.SetWords(True)
            
            results = []
            
            # Process audio in chunks
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if result.get('text'):
                        results.append(result['text'])
            
            # Get final result
            final_result = json.loads(rec.FinalResult())
            if final_result.get('text'):
                results.append(final_result['text'])
            
            wf.close()
            
            # Clean up temporary WAV file if created
            if wav_path != audio_path:
                Path(wav_path).unlink(missing_ok=True)
            
            transcription = ' '.join(results).strip()
            
            if not transcription:
                return "I couldn't understand the audio. Please try again."
            
            return transcription
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    async def _convert_to_wav(self, audio_path: str) -> str:
        """Convert audio file to WAV format suitable for VOSK"""
        try:
            audio_path = Path(audio_path)
            
            # If already WAV, check if it needs conversion
            if audio_path.suffix.lower() == '.wav':
                return str(audio_path)
            
            # Convert using pydub
            audio = AudioSegment.from_file(str(audio_path))
            
            # Convert to mono, 16kHz, 16-bit
            audio = audio.set_channels(1)
            audio = audio.set_frame_rate(16000)
            audio = audio.set_sample_width(2)
            
            # Save as WAV
            wav_path = audio_path.with_suffix('.wav')
            audio.export(str(wav_path), format="wav")
            
            return str(wav_path)
            
        except Exception as e:
            raise Exception(f"Audio conversion failed: {str(e)}")
    
    async def text_to_speech(self, text: str, lang: str = 'en') -> str:
        """
        Convert text to speech using gTTS and return base64 encoded audio
        """
        try:
            if not text.strip():
                raise Exception("Text is empty")
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_path = temp_file.name
            
            # Generate speech
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_path)
            
            # Convert to base64
            with open(temp_path, 'rb') as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # Clean up
            Path(temp_path).unlink(missing_ok=True)
            
            return audio_base64
            
        except Exception as e:
            raise Exception(f"Text-to-speech failed: {str(e)}")
    
    async def process_audio_chunk(self, audio_data: bytes) -> str:
        """Process real-time audio chunk"""
        # This would be used for real-time streaming in future versions
        pass


# Utility function to download VOSK model
async def download_vosk_model():
    """Download VOSK model if not present"""
    import urllib.request
    import zipfile
    
    model_url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
    model_dir = Path("vosk-model")
    zip_path = Path("vosk-model.zip")
    
    if model_dir.exists():
        print("VOSK model already exists")
        return
    
    try:
        print("Downloading VOSK model...")
        urllib.request.urlretrieve(model_url, zip_path)
        
        print("Extracting model...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('.')
        
        # Rename extracted folder
        extracted_dir = Path("vosk-model-en-us-0.22")
        if extracted_dir.exists():
            extracted_dir.rename(model_dir)
        
        # Clean up
        zip_path.unlink(missing_ok=True)
        
        print("VOSK model downloaded and setup successfully")
        
    except Exception as e:
        print(f"Failed to download VOSK model: {e}")
        # Clean up on failure
        zip_path.unlink(missing_ok=True)
        if model_dir.exists():
            import shutil
            shutil.rmtree(model_dir)