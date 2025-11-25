#!/usr/bin/env python3
"""
Setup script for Gemini AI Assistant
Downloads VOSK model and tests API configuration
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from api.services.speech_service import download_vosk_model
from api.services.gemini_service import GeminiService


async def main():
    print("🚀 Setting up Gemini AI Assistant...")
    print()

    # Check environment variables
    print("1. Checking environment configuration...")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("   Please add your Gemini API key to the .env file")
        return False
    else:
        print("✅ GEMINI_API_KEY found")

    # Test Gemini connection
    print("\n2. Testing Gemini API connection...")
    try:
        gemini_service = GeminiService()
        is_available = await gemini_service.test_connection()
        if is_available:
            print("✅ Gemini API connection successful")
        else:
            print("❌ Gemini API connection failed")
            return False
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        return False

    # Download VOSK model
    print("\n3. Setting up speech recognition...")
    model_dir = Path("vosk-model")
    if model_dir.exists():
        print("✅ VOSK model already exists")
    else:
        print("📥 Downloading VOSK model (this may take a while)...")
        try:
            await download_vosk_model()
            print("✅ VOSK model downloaded successfully")
        except Exception as e:
            print(f"❌ VOSK model download failed: {e}")
            print("   You can download it manually from: https://alphacephei.com/vosk/models")
            print("   Extract 'vosk-model-en-us-0.22' and rename to 'vosk-model'")

    # Create necessary directories
    print("\n4. Creating directories...")
    directories = ["temp_audio", "temp_images", "uploads"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created {directory}/ directory")

    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the backend: python -m uvicorn api.main:app --reload --port 8000")
    print("2. Start the frontend: cd frontend && npm run dev")
    print("3. Open http://localhost:3000 in your browser")
    
    return True


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    success = asyncio.run(main())
    sys.exit(0 if success else 1)