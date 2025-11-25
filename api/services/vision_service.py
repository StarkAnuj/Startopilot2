"""
Vision Service Module
Handles image processing and vision-related utilities
"""

import io
import base64
from typing import Tuple, Optional
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np


class VisionService:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
        self.max_image_size = (1024, 1024)  # Max size for processing
    
    async def process_image(self, image_path: str) -> bytes:
        """Process and optimize image for analysis"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large
                if img.size[0] > self.max_image_size[0] or img.size[1] > self.max_image_size[1]:
                    img.thumbnail(self.max_image_size, Image.Resampling.LANCZOS)
                
                # Save to bytes
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='JPEG', quality=85, optimize=True)
                return img_bytes.getvalue()
                
        except Exception as e:
            raise Exception(f"Image processing failed: {str(e)}")
    
    def validate_image(self, image_path: str) -> bool:
        """Validate if image is supported format"""
        try:
            path = Path(image_path)
            if path.suffix.lower() not in self.supported_formats:
                return False
            
            # Try to open the image
            with Image.open(image_path) as img:
                img.verify()
            return True
            
        except Exception:
            return False
    
    async def enhance_image(self, image_data: bytes, enhance_type: str = 'auto') -> bytes:
        """Enhance image quality for better analysis"""
        try:
            img = Image.open(io.BytesIO(image_data))
            
            if enhance_type == 'auto':
                # Auto enhance brightness and contrast
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.1)
                
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.1)
                
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.05)
            
            elif enhance_type == 'sharpen':
                img = img.filter(ImageFilter.SHARPEN)
            
            elif enhance_type == 'brightness':
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.2)
            
            # Save enhanced image
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG', quality=90)
            return img_bytes.getvalue()
            
        except Exception as e:
            raise Exception(f"Image enhancement failed: {str(e)}")
    
    def get_image_info(self, image_data: bytes) -> dict:
        """Get image metadata and info"""
        try:
            img = Image.open(io.BytesIO(image_data))
            
            return {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
            }
            
        except Exception as e:
            raise Exception(f"Failed to get image info: {str(e)}")
    
    async def convert_to_base64(self, image_path: str) -> str:
        """Convert image to base64 string"""
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                return base64.b64encode(img_data).decode('utf-8')
        except Exception as e:
            raise Exception(f"Base64 conversion failed: {str(e)}")
    
    def resize_image(self, image_data: bytes, target_size: Tuple[int, int]) -> bytes:
        """Resize image to target dimensions"""
        try:
            img = Image.open(io.BytesIO(image_data))
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG', quality=85)
            return img_bytes.getvalue()
            
        except Exception as e:
            raise Exception(f"Image resize failed: {str(e)}")
    
    def crop_center(self, image_data: bytes, crop_size: Tuple[int, int]) -> bytes:
        """Crop image from center"""
        try:
            img = Image.open(io.BytesIO(image_data))
            width, height = img.size
            crop_width, crop_height = crop_size
            
            left = (width - crop_width) // 2
            top = (height - crop_height) // 2
            right = left + crop_width
            bottom = top + crop_height
            
            img = img.crop((left, top, right, bottom))
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG', quality=85)
            return img_bytes.getvalue()
            
        except Exception as e:
            raise Exception(f"Image crop failed: {str(e)}")
    
    async def prepare_for_gemini(self, image_data: bytes) -> bytes:
        """Prepare image specifically for Gemini API"""
        try:
            # Get image info
            img_info = self.get_image_info(image_data)
            
            # If image is too large, resize it
            max_dimension = 1024
            if img_info['width'] > max_dimension or img_info['height'] > max_dimension:
                # Calculate new size maintaining aspect ratio
                ratio = min(max_dimension / img_info['width'], max_dimension / img_info['height'])
                new_size = (int(img_info['width'] * ratio), int(img_info['height'] * ratio))
                image_data = self.resize_image(image_data, new_size)
            
            # Enhance for better analysis
            image_data = await self.enhance_image(image_data, 'auto')
            
            return image_data
            
        except Exception as e:
            raise Exception(f"Gemini preparation failed: {str(e)}")