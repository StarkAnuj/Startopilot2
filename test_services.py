#!/usr/bin/env python3
"""
Test script for Gemini AI Assistant API
"""

import os
import sys
import asyncio
import tempfile
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from dotenv import load_dotenv

async def test_services():
    """Test all service components"""
    
    print("🧪 Testing Gemini AI Assistant Services")
    print("=" * 50)
    
    # Test Gemini Service
    print("\n1. Testing Gemini Service...")
    try:
        from api.services.gemini_service import GeminiService
        gemini_service = GeminiService()
        
        # Test text generation
        response = await gemini_service.generate_text("Hello, this is a test.")
        print(f"✅ Text generation: {response[:50]}...")
        
        # Test connection
        is_connected = await gemini_service.test_connection()
        print(f"✅ API Connection: {'Connected' if is_connected else 'Failed'}")
        
    except Exception as e:
        print(f"❌ Gemini Service error: {e}")
    
    # Test Vision Service
    print("\n2. Testing Vision Service...")
    try:
        from api.services.vision_service import VisionService
        vision_service = VisionService()
        print("✅ Vision Service initialized")
        
    except Exception as e:
        print(f"❌ Vision Service error: {e}")
    
    # Test Speech Service
    print("\n3. Testing Speech Service...")
    try:
        from api.services.speech_service import SpeechService
        speech_service = SpeechService()
        
        is_available = speech_service.is_available()
        print(f"✅ Speech Service: {'Available' if is_available else 'VOSK model needed'}")
        
        # Test TTS
        test_text = "Hello, this is a test of text to speech."
        audio_b64 = await speech_service.text_to_speech(test_text)
        print(f"✅ Text-to-Speech: Generated {len(audio_b64)} bytes")
        
    except Exception as e:
        print(f"❌ Speech Service error: {e}")
    
    # Test Utility Classes
    print("\n4. Testing Utility Classes...")
    try:
        from api.utils.audio_utils import AudioProcessor
        from api.utils.image_utils import ImageProcessor
        
        audio_processor = AudioProcessor()
        image_processor = ImageProcessor()
        
        print("✅ Audio Processor initialized")
        print("✅ Image Processor initialized")
        
    except Exception as e:
        print(f"❌ Utility Classes error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Service testing completed!")


async def test_api_endpoints():
    """Test API endpoints using httpx"""
    
    print("\n🌐 Testing API Endpoints")
    print("=" * 50)
    
    try:
        import httpx
        
        base_url = "http://localhost:8000"
        
        async with httpx.AsyncClient() as client:
            # Test health endpoint
            response = await client.get(f"{base_url}/")
            if response.status_code == 200:
                print("✅ Root endpoint accessible")
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
            
            # Test health check
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✅ Health check passed")
                data = response.json()
                print(f"   Status: {data.get('status')}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                
    except ImportError:
        print("⚠️  httpx not installed, skipping API endpoint tests")
        print("   Install with: pip install httpx")
    except Exception as e:
        print(f"❌ API endpoint test error: {e}")
        print("   Make sure the server is running on http://localhost:8000")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check environment
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in environment")
        print("   Please set up your .env file with your Gemini API key")
        sys.exit(1)
    
    asyncio.run(test_services())
    
    # Ask if user wants to test API endpoints
    test_api = input("\n🔄 Test API endpoints? (requires server running) [y/N]: ").lower().startswith('y')
    if test_api:
        asyncio.run(test_api_endpoints())
    
    print("\n✨ Testing complete!")