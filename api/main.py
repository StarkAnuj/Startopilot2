"""
Main FastAPI application for Gemini AI Assistant
Handles voice and vision interactions with Google Gemini Pro Vision API
"""

import os
import base64
import tempfile
import asyncio
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import aiofiles

from api.services.speech_service_simple import SpeechService
from api.services.vision_service import VisionService
from api.services.gemini_service import GeminiService
from api.utils.image_utils import ImageProcessor

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Gemini AI Assistant API",
    description="Voice and Vision AI Assistant powered by Google Gemini Pro Vision",
    version="1.0.0"
)

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
speech_service = SpeechService()
vision_service = VisionService()
gemini_service = GeminiService()
image_processor = ImageProcessor()

# Create temp directories
TEMP_AUDIO_DIR = Path("temp_audio")
TEMP_IMAGES_DIR = Path("temp_images")
TEMP_AUDIO_DIR.mkdir(exist_ok=True)
TEMP_IMAGES_DIR.mkdir(exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Gemini AI Assistant API",
        "status": "active",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Test services
        gemini_available = await gemini_service.test_connection()
        speech_available = speech_service.is_available()
        
        return {
            "status": "healthy",
            "services": {
                "gemini": gemini_available,
                "speech": speech_available,
                "vision": True
            },
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@app.post("/api/interact")
async def interact_with_ai(
    audio: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    text_prompt: Optional[str] = Form(None)
):
    """
    Main interaction endpoint
    Accepts audio, image, and optional text prompt
    Returns Gemini's response with audio output
    """
    try:
        # Validate input
        if not audio and not text_prompt:
            raise HTTPException(
                status_code=400, 
                detail="Either audio file or text prompt is required"
            )
        
        if not image:
            raise HTTPException(
                status_code=400, 
                detail="Image file is required for vision analysis"
            )
        
        # Process audio to text if provided
        transcribed_text = ""
        if audio:
            # Save uploaded audio temporarily
            audio_path = TEMP_AUDIO_DIR / f"temp_audio_{asyncio.get_event_loop().time()}.wav"
            async with aiofiles.open(audio_path, 'wb') as f:
                content = await audio.read()
                await f.write(content)
            
            # Convert audio to text
            try:
                transcribed_text = await speech_service.transcribe_audio(str(audio_path))
                # Clean up temp file
                audio_path.unlink(missing_ok=True)
            except Exception as e:
                audio_path.unlink(missing_ok=True)
                raise HTTPException(status_code=500, detail=f"Audio transcription failed: {str(e)}")
        
        # Use text prompt if provided, otherwise use transcribed text
        user_input = text_prompt if text_prompt else transcribed_text
        
        if not user_input.strip():
            raise HTTPException(status_code=400, detail="No valid input text found")
        
        # Process image
        image_content = await image.read()
        image_path = TEMP_IMAGES_DIR / f"temp_image_{asyncio.get_event_loop().time()}.jpg"
        
        async with aiofiles.open(image_path, 'wb') as f:
            await f.write(image_content)
        
        try:
            # Process image for Gemini
            processed_image = await image_processor.process_for_gemini(str(image_path))
            
            # Get response from Gemini
            gemini_response = await gemini_service.analyze_with_vision(
                text=user_input,
                image_data=processed_image
            )
            
            # Convert response to speech
            audio_base64 = await speech_service.text_to_speech(gemini_response)
            
            # Clean up temp image
            image_path.unlink(missing_ok=True)
            
            return JSONResponse(content={
                "success": True,
                "user_input": user_input,
                "transcribed_text": transcribed_text,
                "gemini_response": gemini_response,
                "audio_response": audio_base64,
                "metadata": {
                    "audio_provided": audio is not None,
                    "image_provided": True,
                    "text_prompt_provided": text_prompt is not None
                }
            })
            
        except Exception as e:
            # Clean up temp image on error
            image_path.unlink(missing_ok=True)
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/api/transcribe")
async def transcribe_audio_only(audio: UploadFile = File(...)):
    """Transcribe audio file to text"""
    try:
        # Save uploaded audio temporarily
        audio_path = TEMP_AUDIO_DIR / f"transcribe_{asyncio.get_event_loop().time()}.wav"
        async with aiofiles.open(audio_path, 'wb') as f:
            content = await audio.read()
            await f.write(content)
        
        # Transcribe
        try:
            text = await speech_service.transcribe_audio(str(audio_path))
            audio_path.unlink(missing_ok=True)
            
            return JSONResponse(content={
                "success": True,
                "transcribed_text": text
            })
        except Exception as e:
            audio_path.unlink(missing_ok=True)
            raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")


@app.post("/api/tts")
async def text_to_speech_endpoint(text: str = Form(...)):
    """Convert text to speech"""
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text is required")
        
        audio_base64 = await speech_service.text_to_speech(text)
        
        return JSONResponse(content={
            "success": True,
            "audio_response": audio_base64,
            "text": text
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )