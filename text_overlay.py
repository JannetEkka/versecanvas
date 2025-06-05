"""
Text Overlay Module
Adds poem text overlay to generated background images with customizable styling.
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from typing import Tuple, Optional, List, Union
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextOverlay:
    """Class for adding text overlays to images with various styling options."""
    
    def __init__(self):
        """Initialize with default font fallbacks."""
        self.default_fonts = self._get_default_fonts()
    
    def _get_default_fonts(self) -> List[str]:
        """Get list of available system fonts."""
        # Common font paths for different operating systems
        font_paths = [
            # Windows
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/times.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            # macOS
            "/System/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Times.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
            # Linux
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        ]
        
        available_fonts = []
        for font_path in font_paths:
            if os.path.exists(font_path):
                available_fonts.append(font_path)
        
        return available_fonts
    
    def add_text_overlay(
        self,
        image: Image.Image,
        text: str,
        font_size: int = 24,
        font_color: Tuple[int, int, int] = (255, 255, 255),
        position: str = "center",
        background_opacity: float = 0.7,
        background_color: Tuple[int, int, int] = (0, 0, 0),
        margin: int = 50,
        line_spacing: int = 10,
        font_style: str = "arial",
        text_alignment: str = "center",
        max_width_ratio: float = 0.8
    ) -> Image.Image:
        """
        Add text overlay to an image with customizable styling.
        
        Args:
            image: PIL Image to add text to
            text: Text content to overlay
            font_size: Size of the font
            font_color: RGB color tuple for text
            position: Position of text ("center", "top", "bottom", "left", "right")
            background_opacity: Opacity of text background (0.0-1.0)
            background_color: RGB color tuple for text background
            margin: Margin from edges in pixels
            line_spacing: Additional spacing between lines
            font_style: Font style preference
            text_alignment: Text alignment ("left", "center", "right")
            max_width_ratio: Maximum width of text as ratio of image width
            
        Returns:
            PIL Image with text overlay
        """
        try:
            # Create a copy of the original image
            result_image = image.copy()
            
            # Get font
            font = self._get_font(font_size, font_style)
            
            # Prepare text with word wrapping
            max_width = int(image.width * max_width_ratio)
            wrapped_text = self._wrap_text(text, font, max_width)
            
            # Calculate text dimensions
            text_width, text_height = self._calculate_text_size(wrapped_text, font, line_spacing)
            
            # Calculate position
            text_x, text_y = self._calculate_position(
                image.width, image.height, text_width, text_height, position, margin
            )
            
            # Create text background if opacity > 0
            if background_opacity > 0:
                self._add_text_background(
                    result_image, text_x, text_y, text_width, text_height,
                    background_color, background_opacity, margin // 2
                )
            
            # Add text
            self._draw_text(
                result_image, wrapped_text, text_x, text_y, font,
                font_color, line_spacing, text_alignment
            )
            
            return result_image
            
        except Exception as e:
            logger.error(f"Error adding text overlay: {str(e)}")
            return image
    
    def _get_font(self, size: int, style: str) -> Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]:
        """Get font object based on style preference."""
        try:
            # Try to load specific font based on style
            font_map = {
                "arial": ["arial.ttf", "Arial.ttf"],
                "times": ["times.ttf", "Times.ttc", "times new roman.ttf"],
                "helvetica": ["helvetica.ttf", "Helvetica.ttc"],
                "serif": ["times.ttf", "liberation-serif.ttf", "DejaVuSerif.ttf"],
                "sans-serif": ["arial.ttf", "liberation-sans.ttf", "DejaVuSans.ttf"]
            }
            
            # Try style-specific fonts first
            if style.lower() in font_map:
                for font_name in font_map[style.lower()]:
                    for base_path in ["/System/Library/Fonts/", "C:/Windows/Fonts/", "/usr/share/fonts/truetype/"]:
                        font_path = os.path.join(base_path, font_name)
                        if os.path.exists(font_path):
                            return ImageFont.truetype(font_path, size)
            
            # Fallback to any available font
            for font_path in self.default_fonts:
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
            
            # Ultimate fallback to default font
            return ImageFont.load_default()
            
        except Exception as e:
            logger.warning(f"Font loading failed, using default: {str(e)}")
            return ImageFont.load_default()
    
    def _wrap_text(self, text: str, font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont], max_width: int) -> List[str]:
        """Wrap text to fit within specified width."""
        lines = []
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append("")
                continue
                
            # Use textwrap as starting point
            wrapper = textwrap.TextWrapper(width=50)  # Start with character-based wrapping
            wrapped_lines = wrapper.wrap(paragraph)
            
            # Refine based on actual pixel width
            final_lines = []
            for line in wrapped_lines:
                if self._get_text_width(line, font) <= max_width:
                    final_lines.append(line)
                else:
                    # Further split if still too wide
                    words = line.split()
                    current_line = ""
                    for word in words:
                        test_line = current_line + " " + word if current_line else word
                        if self._get_text_width(test_line, font) <= max_width:
                            current_line = test_line
                        else:
                            if current_line:
                                final_lines.append(current_line)
                            current_line = word
                    if current_line:
                        final_lines.append(current_line)
            
            lines.extend(final_lines)
        
        return lines
    
    def _get_text_width(self, text: str, font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]) -> int:
        """Get pixel width of text."""
        # Create temporary image to measure text
        temp_img = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(temp_img)
        bbox = draw.textbbox((0, 0), text, font=font)
        return int(bbox[2] - bbox[0])
    
    def _calculate_text_size(self, lines: List[str], font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont], line_spacing: int) -> Tuple[int, int]:
        """Calculate total text dimensions."""
        if not lines:
            return 0, 0
        
        # Calculate width (maximum line width)
        max_width = 0
        for line in lines:
            width = self._get_text_width(line, font)
            max_width = max(max_width, width)
        
        # Calculate height
        temp_img = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(temp_img)
        bbox = draw.textbbox((0, 0), "Ag", font=font)  # Use text with ascenders and descenders
        line_height = bbox[3] - bbox[1]
        
        total_height = len(lines) * line_height + (len(lines) - 1) * line_spacing
        
        return max_width, int(total_height)
    
    def _calculate_position(
        self, img_width: int, img_height: int, text_width: int, text_height: int,
        position: str, margin: int
    ) -> Tuple[int, int]:
        """Calculate text position based on alignment preference."""
        if position == "center":
            x = (img_width - text_width) // 2
            y = (img_height - text_height) // 2
        elif position == "top":
            x = (img_width - text_width) // 2
            y = margin
        elif position == "bottom":
            x = (img_width - text_width) // 2
            y = img_height - text_height - margin
        elif position == "left":
            x = margin
            y = (img_height - text_height) // 2
        elif position == "right":
            x = img_width - text_width - margin
            y = (img_height - text_height) // 2
        else:  # Default to center
            x = (img_width - text_width) // 2
            y = (img_height - text_height) // 2
        
        return max(0, x), max(0, y)
    
    def _add_text_background(
        self, image: Image.Image, x: int, y: int, width: int, height: int,
        color: Tuple[int, int, int], opacity: float, padding: int
    ):
        """Add semi-transparent background behind text."""
        # Create overlay for background
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Draw rounded rectangle background
        bg_x1 = max(0, x - padding)
        bg_y1 = max(0, y - padding)
        bg_x2 = min(image.width, x + width + padding)
        bg_y2 = min(image.height, y + height + padding)
        
        # Create background color with opacity
        bg_color = color + (int(255 * opacity),)
        draw.rectangle([bg_x1, bg_y1, bg_x2, bg_y2], fill=bg_color)
        
        # Composite with original image
        image.paste(Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB'))
    
    def _draw_text(
        self, image: Image.Image, lines: List[str], x: int, y: int,
        font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont], color: Tuple[int, int, int], line_spacing: int,
        alignment: str
    ):
        """Draw text lines on image."""
        draw = ImageDraw.Draw(image)
        
        # Calculate line height
        bbox = draw.textbbox((0, 0), "Ag", font=font)
        line_height = bbox[3] - bbox[1]
        
        current_y = y
        for line in lines:
            if alignment == "center":
                line_width = self._get_text_width(line, font)
                line_x = x + (self._calculate_text_size(lines, font, line_spacing)[0] - line_width) // 2
            elif alignment == "right":
                line_width = self._get_text_width(line, font)
                line_x = x + (self._calculate_text_size(lines, font, line_spacing)[0] - line_width)
            else:  # left alignment
                line_x = x
            
            draw.text((line_x, current_y), line, font=font, fill=color)
            current_y += line_height + line_spacing

# Convenience function for the main app
def add_poem_to_image(
    image: Image.Image,
    poem_text: str,
    font_size: int = 24,
    font_color: Tuple[int, int, int] = (255, 255, 255),
    position: str = "center",
    background_opacity: float = 0.7,
    background_color: Tuple[int, int, int] = (0, 0, 0),
    font_style: str = "serif",
    text_alignment: str = "center"
) -> Image.Image:
    """
    Convenience function to add poem text to an image.
    
    Args:
        image: PIL Image to add text to
        poem_text: The poem text to overlay
        font_size: Size of the font
        font_color: RGB color tuple for text
        position: Position of text on image
        background_opacity: Opacity of text background
        background_color: RGB color tuple for text background
        font_style: Font style preference
        text_alignment: Text alignment
        
    Returns:
        PIL Image with poem text overlay
    """
    try:
        overlay = TextOverlay()
        return overlay.add_text_overlay(
            image=image,
            text=poem_text,
            font_size=font_size,
            font_color=font_color,
            position=position,
            background_opacity=background_opacity,
            background_color=background_color,
            font_style=font_style,
            text_alignment=text_alignment
        )
    except Exception as e:
        logger.error(f"Error in add_poem_to_image function: {str(e)}")
        return image