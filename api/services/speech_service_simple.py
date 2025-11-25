"""
Simplified Speech Service Module for testing
Handles text-to-speech using gTTS (audio processing temporarily disabled)
"""

import os
import json
import base64
import tempfile
import asyncio
from typing import Optional
from pathlib import Path

from gtts import gTTS


class SpeechService:
    def __init__(self):
        self.model = None
        print("⚠️ Speech-to-text temporarily disabled due to audio dependency issues")
        print("   Text-to-speech is available")
    
    def is_available(self) -> bool:
        """Check if speech service is available (partial functionality)"""
        return True  # TTS is available
    
    async def transcribe_audio(self, audio_path: str) -> str:
        """
        Placeholder for audio transcription
        """
        return "Voice input received - transcription temporarily unavailable. Please use text input."
    
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


# Simplified download function
async def download_vosk_model():
    """Placeholder - VOSK model download temporarily disabled"""
    print("⚠️ VOSK model download temporarily disabled")
    print("   Voice transcription will return placeholder text")
    pass