"""
Image utilities for processing and handling images
"""

import io
import base64
from pathlib import Path
from typing import Tuple, Optional, Union

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np


class ImageProcessor:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.optimal_size = (800, 600)  # Optimal size for processing
    
    async def process_for_gemini(self, image_path: str) -> bytes:
        """Process image for optimal Gemini API analysis"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                
                # Auto-rotate based on EXIF data
                img = ImageOps.exif_transpose(img)
                
                # Resize if too large (Gemini has size limits)
                max_dimension = 1024
                if max(img.size) > max_dimension:
                    img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                
                # Enhance image quality
                img = self._enhance_for_analysis(img)
                
                # Convert to bytes
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='JPEG', quality=90, optimize=True)
                
                return img_bytes.getvalue()
                
        except Exception as e:
            raise Exception(f"Image processing for Gemini failed: {str(e)}")
    
    def _enhance_for_analysis(self, img: Image.Image) -> Image.Image:
        """Enhance image for better AI analysis"""
        try:
            # Slight sharpening for better text/detail recognition
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.1)
            
            # Improve contrast slightly
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.05)
            
            # Adjust brightness if too dark or too bright
            brightness = self._calculate_brightness(img)
            if brightness < 0.3:  # Too dark
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.2)
            elif brightness > 0.8:  # Too bright
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(0.9)
            
            return img
            
        except Exception:
            return img  # Return original if enhancement fails
    
    def _calculate_brightness(self, img: Image.Image) -> float:
        """Calculate average brightness of an image (0-1 scale)"""
        try:
            # Convert to grayscale
            grayscale = img.convert('L')
            
            # Calculate average pixel value
            pixels = np.array(grayscale)
            avg_brightness = np.mean(pixels) / 255.0
            
            return avg_brightness
            
        except Exception:
            return 0.5  # Return neutral brightness if calculation fails
    
    def validate_image(self, image_path: str) -> dict:
        """Validate image and return validation results"""
        try:
            path = Path(image_path)
            
            # Check if file exists
            if not path.exists():
                return {"valid": False, "error": "File does not exist"}
            
            # Check file extension
            if path.suffix.lower() not in self.supported_formats:
                return {"valid": False, "error": f"Unsupported format: {path.suffix}"}
            
            # Check file size
            file_size = path.stat().st_size
            if file_size > self.max_file_size:
                return {"valid": False, "error": f"File too large: {file_size / 1024 / 1024:.1f}MB"}
            
            # Try to open and validate image
            with Image.open(image_path) as img:
                img.verify()
                
                # Reopen for getting info (verify() closes the image)
                with Image.open(image_path) as img:
                    return {
                        "valid": True,
                        "format": img.format,
                        "mode": img.mode,
                        "size": img.size,
                        "file_size_mb": round(file_size / 1024 / 1024, 2)
                    }
            
        except Exception as e:
            return {"valid": False, "error": f"Invalid image: {str(e)}"}
    
    def resize_image(self, image_path: str, target_size: Tuple[int, int], 
                    maintain_aspect: bool = True) -> str:
        """Resize image to target size"""
        try:
            with Image.open(image_path) as img:
                if maintain_aspect:
                    img.thumbnail(target_size, Image.Resampling.LANCZOS)
                else:
                    img = img.resize(target_size, Image.Resampling.LANCZOS)
                
                # Save resized image
                output_path = Path(image_path).with_suffix('.resized.jpg')
                img.save(str(output_path), 'JPEG', quality=85, optimize=True)
                
                return str(output_path)
                
        except Exception as e:
            raise Exception(f"Image resize failed: {str(e)}")
    
    def convert_to_base64(self, image_path: str) -> str:
        """Convert image to base64 string"""
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                return base64.b64encode(img_data).decode('utf-8')
        except Exception as e:
            raise Exception(f"Base64 conversion failed: {str(e)}")
    
    def save_base64_image(self, base64_data: str, output_path: str) -> str:
        """Save base64 image data to file"""
        try:
            # Remove data URL prefix if present
            if ',' in base64_data:
                base64_data = base64_data.split(',')[1]
            
            img_data = base64.b64decode(base64_data)
            
            with open(output_path, 'wb') as f:
                f.write(img_data)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Base64 save failed: {str(e)}")
    
    def crop_smart(self, image_path: str, target_ratio: float = 16/9) -> str:
        """Smart crop image to target aspect ratio"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                current_ratio = width / height
                
                if abs(current_ratio - target_ratio) < 0.1:
                    # Already close to target ratio
                    return image_path
                
                if current_ratio > target_ratio:
                    # Too wide, crop horizontally
                    new_width = int(height * target_ratio)
                    left = (width - new_width) // 2
                    img = img.crop((left, 0, left + new_width, height))
                else:
                    # Too tall, crop vertically
                    new_height = int(width / target_ratio)
                    top = (height - new_height) // 2
                    img = img.crop((0, top, width, top + new_height))
                
                # Save cropped image
                output_path = Path(image_path).with_suffix('.cropped.jpg')
                img.save(str(output_path), 'JPEG', quality=85)
                
                return str(output_path)
                
        except Exception as e:
            raise Exception(f"Smart crop failed: {str(e)}")
    
    def enhance_image(self, image_path: str, enhancement_type: str = 'auto') -> str:
        """Enhance image with various options"""
        try:
            with Image.open(image_path) as img:
                
                if enhancement_type == 'auto':
                    img = self._auto_enhance(img)
                elif enhancement_type == 'sharpen':
                    img = img.filter(ImageFilter.SHARPEN)
                elif enhancement_type == 'denoise':
                    img = img.filter(ImageFilter.MedianFilter())
                elif enhancement_type == 'contrast':
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.3)
                elif enhancement_type == 'brightness':
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(1.2)
                elif enhancement_type == 'color':
                    enhancer = ImageEnhance.Color(img)
                    img = enhancer.enhance(1.1)
                
                # Save enhanced image
                output_path = Path(image_path).with_suffix(f'.{enhancement_type}.jpg')
                img.save(str(output_path), 'JPEG', quality=90)
                
                return str(output_path)
                
        except Exception as e:
            raise Exception(f"Image enhancement failed: {str(e)}")
    
    def _auto_enhance(self, img: Image.Image) -> Image.Image:
        """Apply automatic enhancement"""
        try:
            # Apply auto contrast
            img = ImageOps.autocontrast(img, cutoff=1)
            
            # Slight sharpening
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.05)
            
            # Color enhancement
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.02)
            
            return img
            
        except Exception:
            return img
    
    def get_dominant_colors(self, image_path: str, num_colors: int = 5) -> list:
        """Extract dominant colors from image"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB and resize for faster processing
                img = img.convert('RGB')
                img.thumbnail((150, 150))
                
                # Get pixels
                pixels = np.array(img).reshape(-1, 3)
                
                # Simple k-means clustering (simplified)
                # For a more robust solution, consider using sklearn.cluster.KMeans
                unique_colors = []
                pixel_counts = {}
                
                for pixel in pixels:
                    color_tuple = tuple(pixel)
                    pixel_counts[color_tuple] = pixel_counts.get(color_tuple, 0) + 1
                
                # Sort by frequency and get top colors
                sorted_colors = sorted(pixel_counts.items(), key=lambda x: x[1], reverse=True)
                
                dominant_colors = []
                for color, count in sorted_colors[:num_colors]:
                    dominant_colors.append({
                        'rgb': color,
                        'hex': '#{:02x}{:02x}{:02x}'.format(*color),
                        'percentage': round(count / len(pixels) * 100, 2)
                    })
                
                return dominant_colors
                
        except Exception as e:
            raise Exception(f"Color extraction failed: {str(e)}")
    
    def create_thumbnail(self, image_path: str, size: Tuple[int, int] = (150, 150)) -> str:
        """Create thumbnail of image"""
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Save thumbnail
                output_path = Path(image_path).with_suffix('.thumb.jpg')
                img.save(str(output_path), 'JPEG', quality=80)
                
                return str(output_path)
                
        except Exception as e:
            raise Exception(f"Thumbnail creation failed: {str(e)}")
    
    def detect_orientation(self, image_path: str) -> str:
        """Detect image orientation"""
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                if width > height:
                    return 'landscape'
                elif height > width:
                    return 'portrait'
                else:
                    return 'square'
                    
        except Exception as e:
            raise Exception(f"Orientation detection failed: {str(e)}")