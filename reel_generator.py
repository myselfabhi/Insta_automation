"""
Optimized reel generator - creates video reels from profile picture and content
"""
import os
import subprocess
import logging
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip
from utils import logger, ensure_directory, cleanup_temp_files, validate_video_file
from config import Config

class ReelGenerator:
    """Generates Instagram reels from profile picture and content with optimizations"""
    
    # Instagram reel dimensions: 1080x1920 (9:16 aspect ratio)
    REEL_WIDTH = 1080
    REEL_HEIGHT = 1920
    
    def __init__(self, profile_pic_path: str, output_dir: str = 'output', use_logo: bool = False, logo_path: Optional[str] = None):
        self.profile_pic_path = profile_pic_path
        self.use_logo = use_logo
        self.logo_path = logo_path or Config.LOGO_PATH
        self.output_dir = ensure_directory(output_dir)
        self._fonts = self._load_fonts()
        self._ffmpeg_available = self._check_ffmpeg()
        
        # Determine which image to use
        if self.use_logo and os.path.exists(self.logo_path):
            self.image_path = self.logo_path
            logger.info(f"Using logo: {self.logo_path}")
        else:
            self.image_path = self.profile_pic_path
            logger.info(f"Using profile picture: {self.profile_pic_path}")
        
    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'], 
                capture_output=True, 
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    
    def _load_fonts(self) -> dict:
        """Load fonts with fallbacks"""
        fonts = {}
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "arial.ttf"
        ]
        
        # Try to load large font
        for path in font_paths:
            try:
                fonts['large'] = ImageFont.truetype(path, 60)
                break
            except:
                continue
        else:
            fonts['large'] = ImageFont.load_default()
        
        # Try to load medium font
        for path in font_paths:
            try:
                fonts['medium'] = ImageFont.truetype(path, 40)
                break
            except:
                continue
        else:
            fonts['medium'] = ImageFont.load_default()
        
        return fonts
    
    def download_image(self, url: str, save_path: str) -> bool:
        """Download image from URL with streaming"""
        try:
            import requests
            response = requests.get(url, timeout=15, stream=True)
            response.raise_for_status()
            
            save_path_obj = Path(save_path)
            save_path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.debug(f"Downloaded image: {save_path}")
            return True
        except Exception as e:
            logger.error(f"Error downloading image from {url}: {e}")
            return False
    
    def _create_circular_mask(self, size: int) -> Image.Image:
        """Create a circular mask for profile picture"""
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        return mask
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list:
        """Wrap text to fit within max_width efficiently"""
        words = text.split()
        if not words:
            return []
        
        lines = []
        current_line = []
        
        # Create a temporary image for text measurement (reuse)
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = temp_draw.textbbox((0, 0), test_line, font=font)
            test_width = bbox[2] - bbox[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _extract_background_from_logo(self, logo_path: str) -> Image.Image:
        """Extract and resize the cosmic background from the logo"""
        try:
            logo = Image.open(logo_path)
            logo = logo.convert('RGB')  # Convert to RGB to remove alpha if present
            
            # Resize logo background to fit reel dimensions (1080x1920)
            # Use high-quality resampling to maintain the cosmic effect
            background = logo.resize((self.REEL_WIDTH, self.REEL_HEIGHT), Image.Resampling.LANCZOS)
            logo.close()
            
            logger.debug(f"Extracted background from logo: {logo_path}")
            return background
        except Exception as e:
            logger.warning(f"Error extracting background from logo: {e}. Using default background.")
            # Fallback to dark space background
            return Image.new('RGB', (self.REEL_WIDTH, self.REEL_HEIGHT), color='#0a0a1a')
    
    def create_reel_frame(
        self, 
        profile_pic_path: str, 
        content_text: str, 
        content_image_path: Optional[str] = None
    ) -> Image.Image:
        """Create a single frame for the reel"""
        # Use logo background if logo is enabled, otherwise use black background
        if self.use_logo and os.path.exists(self.logo_path):
            frame = self._extract_background_from_logo(self.logo_path)
        else:
            # Create base frame with dark background
            frame = Image.new('RGB', (self.REEL_WIDTH, self.REEL_HEIGHT), color='#000000')
        
        draw = ImageDraw.Draw(frame)
        
        # Load and add profile picture or logo
        # When using logo background, we can optionally show a smaller logo watermark
        # or skip it since the background already has the cosmic theme
        if not self.use_logo:
            # Only show profile picture if not using logo background
            try:
                image = Image.open(profile_pic_path)
                image = image.convert('RGBA' if image.mode == 'RGBA' else 'RGB')
                image_size = 400
                
                # Resize image
                image = image.resize((image_size, image_size), Image.Resampling.LANCZOS)
                
                # Create and apply circular mask for profile pic
                mask = self._create_circular_mask(image_size)
                
                # Paste image at top center
                image_x = (self.REEL_WIDTH - image.width) // 2
                image_y = 200
                frame.paste(image, (image_x, image_y), mask)
                
                # Clean up
                image.close()
                
            except Exception as e:
                logger.warning(f"Error loading profile picture: {e}")
        else:
            # When using logo background, optionally add a small logo watermark at top
            # This is optional - comment out if you don't want the logo character on top
            try:
                logo_img = Image.open(self.logo_path)
                logo_img = logo_img.convert('RGBA' if logo_img.mode == 'RGBA' else 'RGB')
                
                # Make logo smaller as a watermark (optional)
                watermark_size = 150
                logo_img.thumbnail((watermark_size, watermark_size), Image.Resampling.LANCZOS)
                
                # Position at top right corner as watermark
                logo_x = self.REEL_WIDTH - logo_img.width - 30
                logo_y = 30
                
                if logo_img.mode == 'RGBA':
                    frame.paste(logo_img, (logo_x, logo_y), logo_img)
                else:
                    frame.paste(logo_img, (logo_x, logo_y))
                
                logo_img.close()
            except Exception as e:
                logger.debug(f"Optional logo watermark not added: {e}")
        
        # Add content image if available
        if content_image_path and os.path.exists(content_image_path):
            try:
                content_img = Image.open(content_image_path)
                content_img = content_img.convert('RGB')
                
                # Resize to fit in middle section while maintaining aspect ratio
                max_size = 600
                content_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                img_x = (self.REEL_WIDTH - content_img.width) // 2
                img_y = 700
                frame.paste(content_img, (img_x, img_y))
                
                # Clean up
                content_img.close()
                
            except Exception as e:
                logger.warning(f"Error loading content image: {e}")
        
        # Add text overlay
        text_y = 1300
        text_lines = self._wrap_text(content_text, self._fonts['medium'], self.REEL_WIDTH - 100)
        
        for i, line in enumerate(text_lines[:3]):  # Max 3 lines
            bbox = draw.textbbox((0, 0), line, font=self._fonts['medium'])
            text_width = bbox[2] - bbox[0]
            text_x = (self.REEL_WIDTH - text_width) // 2
            draw.text((text_x, text_y + i * 50), line, fill='white', font=self._fonts['medium'])
        
        return frame
    
    def _generate_video_moviepy(self, frame_path: str, output_path: str, duration: int) -> bool:
        """Generate video using moviepy"""
        try:
            clip = ImageClip(frame_path, duration=duration)
            clip.write_videofile(
                output_path,
                fps=Config.REEL_FPS,
                codec='libx264',
                audio=False,
                preset='medium',
                logger=None,
                verbose=False
            )
            clip.close()
            return True
        except Exception as e:
            logger.warning(f"MoviePy video generation failed: {e}")
            return False
    
    def _generate_video_ffmpeg(self, frame_path: str, output_path: str, duration: int) -> bool:
        """Generate video using ffmpeg directly (more efficient)"""
        if not self._ffmpeg_available:
            return False
        
        try:
            cmd = [
                'ffmpeg', '-y',  # Overwrite output file
                '-loop', '1',  # Loop the image
                '-i', frame_path,  # Input image
                '-t', str(duration),  # Duration
                '-vf', f'scale={self.REEL_WIDTH}:{self.REEL_HEIGHT}:force_original_aspect_ratio=decrease,pad={self.REEL_WIDTH}:{self.REEL_HEIGHT}:(ow-iw)/2:(oh-ih)/2',
                '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
                '-r', str(Config.REEL_FPS),  # Frame rate
                '-preset', 'medium',  # Encoding preset
                output_path
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            if result.returncode == 0:
                return True
            else:
                logger.error(f"ffmpeg error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("ffmpeg command timed out")
            return False
        except Exception as e:
            logger.error(f"ffmpeg execution error: {e}")
            return False
    
    def generate_reel(self, content_data: dict, duration: int = 15) -> str:
        """Generate a video reel with optimized methods"""
        # Download content image if available
        content_image_path = None
        if content_data.get('image_url'):
            content_image_path = self.output_dir / 'content_image.jpg'
            if not self.download_image(content_data['image_url'], str(content_image_path)):
                content_image_path = None
        
        # Create frame (use logo or profile pic based on config)
        image_path = self.image_path if hasattr(self, 'image_path') else self.profile_pic_path
        frame = self.create_reel_frame(
            image_path,
            content_data.get('text', 'Space Update'),
            str(content_image_path) if content_image_path else None
        )
        
        # Save frame
        frame_path = self.output_dir / 'reel_frame.jpg'
        frame.save(frame_path, quality=95, optimize=True)
        frame.close()  # Free memory
        
        # Create video from frame
        output_path = self.output_dir / 'reel.mp4'
        
        # Try ffmpeg first (faster and more efficient)
        if self._ffmpeg_available:
            logger.info("Generating video using ffmpeg...")
            if self._generate_video_ffmpeg(str(frame_path), str(output_path), duration):
                logger.info(f"Video created successfully: {output_path}")
                # Cleanup temp files
                cleanup_temp_files(str(self.output_dir), "*.jpg", keep_recent=2)
                return str(output_path)
        
        # Fallback to moviepy
        logger.info("Generating video using moviepy...")
        if self._generate_video_moviepy(str(frame_path), str(output_path), duration):
            logger.info(f"Video created successfully: {output_path}")
            cleanup_temp_files(str(self.output_dir), "*.jpg", keep_recent=2)
            return str(output_path)
        
        # If both fail, raise exception
        raise Exception("Could not create video file with any available method")
    
    def cleanup(self):
        """Cleanup temporary files"""
        cleanup_temp_files(str(self.output_dir), "*.jpg", keep_recent=2)
