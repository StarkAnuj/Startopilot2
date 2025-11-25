"""
Gemini Service Module
Handles interactions with Google Gemini Pro Vision API
"""

import os
import base64
import asyncio
from typing import Optional, Dict, Any

import google.generativeai as genai
from PIL import Image
import io


class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        self.vision_model = None
        self.setup_gemini()
    
    def setup_gemini(self):
        """Initialize Gemini API with optimized config for speed"""
        if not self.api_key:
            raise Exception("GEMINI_API_KEY not found in environment variables")
        
        try:
            # Configure the API
            genai.configure(api_key=self.api_key)
            
            # Initialize models - using the latest working Gemini 2.5 Flash model
            # This model supports both text and vision capabilities
            self.model = genai.GenerativeModel('models/gemini-2.5-flash')
            self.vision_model = genai.GenerativeModel('models/gemini-2.5-flash')
            
            print("Gemini API configured with speed optimizations")
            
        except Exception as e:
            # Fallback to other working models
            try:
                print(f"Warning: gemini-2.5-flash not available, trying gemini-2.0-flash: {str(e)}")
                self.model = genai.GenerativeModel('models/gemini-2.0-flash')
                self.vision_model = genai.GenerativeModel('models/gemini-2.0-flash')
                print("Gemini API configured with gemini-2.0-flash (optimized)")
            except Exception as e2:
                raise Exception(f"Failed to setup Gemini API: {str(e2)}")
    
    async def test_connection(self) -> bool:
        """Test if Gemini API is accessible"""
        try:
            # Simple test with text model
            response = await self.generate_text("Hello")
            return bool(response)
        except Exception:
            return False
    
    async def generate_text(self, prompt: str) -> str:
        """Generate text using Gemini Pro with speed optimization"""
        try:
            # Add concise instruction prefix
            optimized_prompt = f"Give a brief, direct answer (max 2 sentences): {prompt}"
            response = self.model.generate_content(optimized_prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Text generation failed: {str(e)}")
    
    async def analyze_with_vision(self, text: str, image_data: bytes) -> str:
        """
        Analyze image and text using Gemini Pro Vision
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Create enhanced prompt for better responses
            enhanced_prompt = self._create_enhanced_prompt(text)
            
            # Generate response
            response = self.vision_model.generate_content([enhanced_prompt, image])
            
            if not response.text:
                return "I couldn't analyze the image properly. Please try again."
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Vision analysis failed: {str(e)}")
    
    def _create_enhanced_prompt(self, user_text: str) -> str:
        """Create an optimized prompt for fast, concise responses"""
        
        # Streamlined prompt for quick responses
        base_prompt = """Be a helpful AI assistant. Give SHORT, direct answers (1-2 sentences max). 
        For images: describe key elements briefly. Answer the user's question directly.
        
        User: """
        
        return f"{base_prompt}{user_text}"
    
    async def analyze_image_only(self, image_data: bytes, prompt: Optional[str] = None) -> str:
        """Analyze image without specific user text"""
        default_prompt = "What do you see in this image? Describe it in detail."
        analysis_prompt = prompt if prompt else default_prompt
        
        return await self.analyze_with_vision(analysis_prompt, image_data)
    
    async def get_image_description(self, image_data: bytes) -> Dict[str, Any]:
        """Get detailed image analysis with structured output"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            structured_prompt = """
            Analyze this image and provide a detailed description including:
            1. Main objects or subjects
            2. Setting or environment
            3. Colors and lighting
            4. Any text visible
            5. Activities or actions happening
            6. Overall mood or atmosphere
            
            Be descriptive but concise.
            """
            
            response = self.vision_model.generate_content([structured_prompt, image])
            
            return {
                "description": response.text,
                "analysis_type": "detailed_description",
                "image_dimensions": image.size
            }
            
        except Exception as e:
            raise Exception(f"Image description failed: {str(e)}")
    
    async def answer_about_image(self, question: str, image_data: bytes) -> str:
        """Answer specific questions about an image"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            contextual_prompt = f"""
            Please look at this image and answer the following question accurately:
            
            Question: {question}
            
            Base your answer only on what you can actually see in the image. 
            If the question cannot be answered from the image, say so politely.
            """
            
            response = self.vision_model.generate_content([contextual_prompt, image])
            return response.text
            
        except Exception as e:
            raise Exception(f"Question answering failed: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Gemini service is properly configured"""
        return self.api_key is not None and self.vision_model is not None


class GeminiError(Exception):
    """Custom exception for Gemini service errors"""
    pass